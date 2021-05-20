import time
from bs4 import BeautifulSoup
import urllib.request
import re
import asyncio
from outputs import *
import requests
import json

API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

compsci_staff_directory = "https://www.dur.ac.uk/research/directory/view/?mode=department&id=4"


# ###################################################################################################################################################

# 1. Durham -> ORCID

async def fetch_durham(member):
    url = "https://www.dur.ac.uk/research/directory/staff/?mode=staff&id=" + member['id']
    print(f"fetching the page for {url}")
    x = urllib.request.urlopen(url)
    return x.read()


async def scrape_staff_profile():
    with open("./compsci_staff_directory.html") as infile:
        soup = BeautifulSoup(infile, 'html.parser')
    infile.close()

    staff = []
    for link in soup.find_all('a'):
        # We want to obtain any a's that have links towards the durham uni staff directory.
        # the A's are in the format <a href="/research/directory/staff/?mode=staff&amp;id=18378">Dr Donald Sturgeon</a>
        # So we extract the name of the staff member and the id that corresponds to their individual page; where we can find links to their orcid profile.
        if link.get('href').startswith("/research/directory/staff/"):
            n = link.text
            # Remove any newlines
            n.replace("\n", "")
            # Remove any double spaces
            while len(n.split("  ")) > 1:
                n = n.replace("  ", " ")
            # Create a profile for this staff member
            staff.append(
                {"name": n, "id": link.get('href').split('=')[-1], 'type': link.parent.parent.previous.previous})

    # Result: staff = [{'name': 'Miss Helene Rusby', 'id': '1620'},{'name': 'Mr Ahmed Alamri', 'id': '17805'},...]
    # Now for each staff member we want to go to their durham university page and obtain the URL to their orcid profile
    # That is if they have one in the first place. Otherwise we will try to find any research they made seperately.
    for loop in range(len(staff)):
        member = staff[loop]
        response = await fetch_durham(member)
        soup = BeautifulSoup(response, "html.parser")
        r = soup.body.find(text=re.compile('^ORCID*'))

        try:
            staff[loop]['ORCID_url'] = r.parent.get('href')[2:]
        except AttributeError:
            continue

    lis4 = []
    lis3 = []

    for x in staff:
        if len(x) == 3:
            lis3.append(x)
        else:
            lis4.append(x)
    print("[")
    for x in lis4:
        print(str(x) + ",")
    for x in lis3:
        print(str(x) + ",")
    print("]")

    return 1

# If you want to achieve all the compsci staff, their orcid id's, their names, faculty type, and their durham id; then uncomment the next line.
# To see the output look at output_scrape_staff_profile() in the outputs.py
# asyncio.run(scrape_staff_profile())

# ###################################################################################################################################################

# 2. ORCID -> SCOPUS (People who linked their SCOPUS to their ORCID)

# \/  This code uses the orcid id's that are known; and finds the assosiated scopus ID if the accounts have been linked.  \/
# The result can be seen in output_from_scrape_Author_Search_API() in the outputs.py

async def fetch_EID_from_orcid(member):
    orcid = member['ORCID_url'][-19:]
    resp = requests.get(
        ("https://api.elsevier.com/content/author/orcid/" + orcid),
        headers={'Accept': 'application/json'}
    )
    resp = resp.json()
    try:
        return resp['author-retrieval-response']['coredata']['eid']
    except KeyError:
        return ""


async def scrape_Author_Search_API():
    staff = output_scrape_staff_profile()

    for loop in range(len(staff)):
        if 'ORCID_url' in staff[loop]:
            t = await fetch_EID_from_orcid(staff[loop])
            if t != "":
                staff[loop]['EID'] = t

    for x in staff:
        print(x)
    return staff


# Uncomment to run.
# asyncio.run(scrape_Author_Search_API())


# ###################################################################################################################################################
# 3. ORCID -> SCOPUS (the rest of who havent linked their 2 profiles)
# Find the remaining SCOPUS ID's by searching their name

def scrape_Author_id_from_name():
    staff = output_from_scrape_Author_Search_API()
    for loop in range(len(staff)):
        if not ('AuthorID' in staff[loop]):
            if not ('EID' in staff[loop]):
                names = staff[loop]['name'].split(" ")
                if names[0] in ['Mr.', "Mr", "Miss", "Miss.", "Ms", "Ms.", "Mrs", "Mrs.", ""]:
                    q = f"AUTHFIRST({names[1]}) AND AUTHLASTNAME({names[-1]})"
                else:
                    q = f"AUTHFIRST({names[0]}) AND AUTHLASTNAME({names[-1]})"
                print(f"'{q}',")
#             I produced some search query's and had to gather the data using a JS console script due to permission issues with the API
#             This is has been highlighted in the email I sent you.
#             The output can be seen in output_from_scrape_Using_names() in outputs.py

# scrape_Author_id_from_name()
# ###################################################################################################################################################
# 2. Durham -> SCOPUS (if anyone has publications on SCOPUS and do not have an ORCID at all)
# Find the remaining SCOPUS ID's by using one of the publications on their Durham pages

# ###################################################################################################################################################

# '{"access_token":"76c1c797-83ec-4b7b-881f-3c861a1a911b","token_type":"bearer","refresh_token":"00feacd8-8335-48b5-8b89-552e2c4c8520","expires_in":631138518,"scope":"/read-public","orcid":null}'


async def fetch_profile(member,DATA):
    profile = requests.post(f"https://pub.orcid.org/{member['orcid']}/record", headers={'Accept': 'application/json'},data=DATA)
    profile = json.loads(profile.text)
    return profile

async def fetch_works(work,DATA):
    G = requests.post(('https://pub.orcid.org' + work['path']), headers={'Accept': 'application/json'}, data=DATA)
    G = json.loads(G.text)
    return G

async def scrape_orcid_api():
    DATA = {'access_token': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 'token_type': 'bearer'}
    staff = []
    with open("./staff.json",'r') as infile:
        while True:
            temp = infile.readline()
            if temp:
                staff.append(json.loads(temp))
            else:
                break
    infile.close()
    citations = {}
    just_titles = {}
    loop = 0
    for member in staff:
        if "orcid" in member and loop >= 50:
            print(f"Examining member: {member['name']}")
            profile = await fetch_profile(member,DATA)
            try:
                for work in profile['activities-summary']['works']['group']:
                    G = await fetch_works(work['work-summary'][0],DATA)
                    if G['citation']:
                        if 'citation-value' in G['citation']:
                            if not member['AuthorID'] in citations:
                                citations[member['AuthorID']] = []
                            citations[member['AuthorID']].append(G['citation']['citation-value'])
                        else:
                            if not member['AuthorID'] in just_titles:
                                just_titles[member['AuthorID']] = []
                            just_titles[member['AuthorID']].append(G)
                    else:
                        if not member['AuthorID'] in just_titles:
                            just_titles[member['AuthorID']] = []
                        just_titles[member['AuthorID']].append(G)

            except KeyError:
                print(f"Something went wrong with {member['name']}")
                continue
        loop += 1

    print("Done")

asyncio.run(scrape_orcid_api())

# ###################################################################################################################################################


import bibtexparser


def prepare_citations(citations):
    errors = []
    output = {}
    for person in citations:
        if not person in output:
            output[person] = []

        for cite in citations[person]:
            try:
                temp = bibtexparser.loads(cite)
                temp = temp.entries[0]
                if len(temp['author'].split(" and ")) > 1:
                    output[person].append({'title':temp['title'],'authors':temp['author'].split(" and ")})
            except (KeyError, IndexError) as e:
                errors.append(cite)
                pass


    print(output)


prepare_citations(citations())


# ###################################################################################################################################################
# Now search scopus for any articles where we dont have any co-authors; just making sure that it isn't the orcid user's fault for not adding a co-author or bibliography,
# but there are other co-authors e.g. rob powell didnt list anyone else, but he DID co-author
# Cant be done, if it has not been gathered already,
# We cant use titles
# bibtex has yielded a whole bunch of initials that are basically useless because we hardly know the potential affiliation.
