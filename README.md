# A collaborative social network based off of Co-authorship at Durham University

## Overview
The complexity of this task comes in the form of creating this dataset with the use of the semantic web and web ontology languages. And also in drawing conclusions and creating data visualisation of the network. For this I opted for Gephi for it's ability to compute various graph metrics, and a Geographic Information Systems (GIS) application to draw on international relations in co-authorship.


Without prevalent web ontology frameworks being implemented for public deployement; to a certain extent, it is possible to web scraping with website specific knowledge to gather publically available information to then use several API's to develop a corpus of publication metadata which can then be used for any number of analyses. 

The specific methodology employed was:
- Gather the names of researchers listed as being members of a department at a given university
- Gather their ORCID Identifiers where publicly listed (e.g. staff profile pages).
- Use their ORCID identifiers or name (if for any reason ORCID identifiers are unknown), to gather authorship attribution identifier for this researcher from SCOPUS.
- Use SCOPUS's attribution identifier to enumerate all the works of a researcher.
- Infer the SCOPUS authorship identifiers of all their co-authors.
- Infer all the co-authors' ORCID Identifiers.
- Gather individual co-author metadata through all available means (ORCID and SCOPUS), chiefly the most recent institution, the country of this institution and researcher's fields of interest.
- Dataset is prepared


I then use the data gathered to generate a graph $G(V,E)$, where every node $n \in N$ is represented by a researcher in the dataset, and each edge $e \in E$ is exists between a pair of nodes when they have co-authored a paper, a pair of nodes can have several edges if they have collaborated more than once.
## Important note:
The datasets cannot be made public to respect the privacy of the real researchers about whom this data was gathered. and unfortunately annonymisation is also not an option as this is also not allowed under the terms of the Scopus and ORCID API's.

# ... Now to the written project:

# Analysing trends in the co-authorship activity of Durham Computer science researchers using collaborative social networks

### A summative Assignment for Computational Modelling in the Humanities and social sciences


## Introduction

The chosen modelling task is to examine co-authorship in the department
of computer Science at Durham university. The chosen implementation was
a social network which consists of nodes which represent researchers,
and a single edge between two nodes represents a co-authorship
collaboration on a single publication. Social Network analysis (SNA) is
the use of networks within the context of graph theory, to model some
real-world behaviour; by modelling co-authorship as a social network, it
is possible to correlate the structure of the network to some constraint
in the environment. SNA's key applications are in the Humanities and
social sciences from examining culture spreading to information
circulation. SNA has proven to provide meaningful insight in evaluating
research networks \[1\]. It has also been shown in studies that use
bibliometric data that co-authored papers achieve more exposure and
impact \[2\],

Since there is no publicly available dataset one had to be created
first; the data was gathered in 3 steps. The first step involved
scraping the names and ORCID details of each researcher in the
department using the Durham university website; most researchers from
the Computer Science department's website. ORCID is a 16-digit number in
the format xxxx-xxxx-xxxx-xxxx, which uniquely identifies a certain
researcher but requires them to create an account first.

This was an issue since many did not; additionally, ORCID only displays
publications the researcher wishes to make public; in order to gain
access to the corpus of all of their works a different database would be
required. SCOPUS is one such corpus with unique author attribution for
all of the researcher's works that are publicly available. Scopus uses a
rich underlying metadata architecture to index its corpus of
publications and their authorship information to make searching
unstructured meta data feasible \[3\].

The SCOPUS API has several layers of security, access can only be made
through institutional IP addresses, and an API key must be registered
with a cap of 7,500 queries. The API contains all the data required
however was not built with this specific use case; and so the process of
obtaining the dataset used was quite convoluted. The dataset comprises
of 2,400 researchers collaborating on 2,300 publications, forming a
co-authorship social network.

Authorship data can be found using ORCID numbers or even just their name
and a Durham university affiliation. All scopus author IDs were gathered
for our staff members, in step 2 The SCOPUS database was queried with
these IDs, and Scopus's authorship attribution fetched all of the
researcher's publications, along with the co-author information. Step 3
is gathering affiliation data for each co-author, their names,
university affiliation and country where they are currently active.

The two csv files in this project comprises the built dataset.
Articles.csv consists of pairwise undirected edges of two researcher's
unique IDs which represent collaboration on a single publication, if
they collaborate in multiple papers, they will have more edges.
Researchers.csv consists of researcher's affiliation information as well
as their names to validate the uniqueness of the author IDs taken from
scopus.

The nodes and edges were imported into Gephi as two csv files and were
formatted using the Force Atlas and Yifan Hu layouts, the toolkit also
produced all the metrics seen in this paper. The visualisations shown in
this paper include the manipulation of feature data for each node, in
order to produce a word cloud that gives context to the clusters. The
names in these visualisations are not anonymised since this data is
publicly available, however some ethical considerations should have been
made to anonymise the data collected.

## Evaluation and Conclusions from the Social network

![Timeline Description automatically generated with medium
confidence](./images/media/image1.png)

**Figure 1.0** The co-authorship social network of Durham researchers
with red edges showing collaboration within the department.

Examining (Figure 1.0), the data suggests the specific areas of interest
that have little intra-department collaboration, are Virtual/Augmented
reality, graph theory, NLP, high performance computing and cryptography.
This is done by observing the clustering of certain modularity classes,
and the Durham researchers within the clique and confirming they
encompass the whole department's contribution to this topic, it is also
clear these modularity classes are weakly connected components, and such
it is possible to draw this conclusion from (Figure 1.0). It is typical
in social networks for the tendency to form communities through triadic
closure, however it is seen that weakly connected and disjoint
components reflect the nicheness of the researcher's topic of interest
in not collaborating often within the department.

![A picture containing text, smoke, dark Description automatically
generated](./images/media/image2.png)

**Figure 2.0** The co-authorship social network coloured by modularity
class with labelled for Durham researchers and scaled in size by the
author's publication count.

The network depicted above was coloured using the modularity classes
created by using Blondel's algorithm to depict the different clusters in
the graph. The size of each label shows the degree centrality of that
node. Modularity is the deviation from the expected random proportion of
edges within communities, and the assignment is made iteratively
converging on some reasonable objective function.

Intuitively the model appears to show that some staff members
particularly recent additions have their own neighbourhood of
researchers with whom they form a clique which other researchers in the
department do not interact with. And a main cluster of long-standing
staff members who collaborate more often and collaborate with each
other's co-collaborators. It is also clear that there is a sizeable
cluster of PhD students who co-author a paper with certain professors
and rarely contribute to any works outside of the university.

Certain researchers do not have many publications with internal
co-authoring, this is most likely due to the length of their career and
being less research oriented within the department as it stands with
David Budgen and software engineering being a specific example from the
graph above. One limitation of the data gathered toward this model is
that it does not consider the publications made only in the researcher's
tenure at Durham, and so the graph is populated with historical
connections that are likely not ongoing co-authorships, and this is
particularly evident from the clusters in each corner of (Figure 1.2 ).

Fields such as computer vision and specific AI applications lead to some
clear clustering around certain researchers, this is likely due to
co-authorship in PhD research, one such example is the blue clustering
in the centre of the Figure X-1.0. One other observation is the green
cluster directly above.



### Demographics of International Collaboration

![A picture containing background pattern Description automatically
generated](./images/media/image3.png)

**Figure 1.2** The co-authorship social network coloured by country
where the author was last affiliated with, and labels for Durham
researchers which are scaled in size by the author's publication count.

When trying to understand a pattern in international collaboration, the
model does not present a coherent message. This is as a result of
insufficient data mining which is down to how the Scopus API was
created, an author does not have to explicitly create a profile for one
to exist; and so, for some co-authors where they have not declared a
country of activity the default location is the country where their last
publication was made publicly available. It is typically either the
United States or Switzerland.

Additionally, a researcher's location may have changed since the
publication was made and the affiliation attribution was set, which
further invalidates any conclusions without further verifying the
integrity of the dataset. It is possible however to report the
demographic data as collected, with the assumption that researchers
typically remain working in the same country.

One missed opportunity for this implementation is the potential use of
TEI data, this is because scopus only made university's addresses
available on the API the week prior to this assignment's due date;
however, had this been available it would have been possible to view
international collaborations without using a forced based layout seen in
this paper's visualisations. TEI gives a much more intuitive
visualisation of node's specific interactions with the rest of the
world.

The heatmap shown in (Figure 3.0) shows a large majority of Europe, the
Americas and most of Asia being countries whose researchers have
collaborated with Durham researchers, but also shows few are
disproportionately higher than others. This may be down to the nature of
research in the developed world, and the clustering of technology
researchers in the parts highlighted. However the conclusion drawn from
this model is that since other countries could have a higher degree of
centrality in a global co-author social network and display more world
wide collaboration; that Durham Computer Science represents a small
footprint in such a network.

![Table Description automatically
generated](./images/media/image4.png)

**Table 1.0** showing the demographics of co-authors in this social
network.

![Map Description automatically
generated](./images/media/image5.png)

**Figure 3.0** A heatmap of co-author citations with Durham
publications.

![Chart, pie chart Description automatically
generated](./images/media/image6.png)

**Figure X-2.6** A further breakdown of the heatmap in Figure X-2.5.

### Measures of centrality

![Diagram Description automatically
generated](./images/media/image7.png)

**Figure 4.0** The co-authorship social network where the size of a node
is determined by it's betweenness centrality

Betweenness centrality measures how central individuals are within the

social network by measuring the path lengths that would flow through
this one node compared to all others. This can be seen for the network
in (Figure 4.0). There are 2,400 nodes with 2,300 Articles that form
44,850 edges in the network. In calculating the betweenness centrality
for this network we find the average path length is of 6. The nodes with
highest centrality can be explained, researchers in certain disciplines
such as Image processing, are likely to be co-authoring papers with game
developers, computer vision and AI researchers; it is evident such
disciplines exist when you view these node's topics of interest. And by
inspecting the individuals with high centrality we examine their role in
facilitating conversation. Nodes with high amount of centrality play a
large role in facilitating communication in this case across key topic
interests \[4\].

Degree centrality is a ranking of nodes by their degree. The topology of
the graph leads to a cycle starting with one author and passes through
each co-author representing a single publication. And so, the degree
centrality only highlighted certain Durham researchers who have had long
careers and provided no further insight into group dynamics.

![Table Description automatically
generated](./images/media/image8.png){width="2.86587489063867in"
height="1.9069772528433946in"}![Chart, scatter chart Description
automatically
generated](./images/media/image9.png){width="2.935416666666667in"
height="1.953251312335958in"}\
![Chart Description automatically
generated](./images/media/image10.png){width="2.86587489063867in"
height="1.9069772528433946in"}![Graphical user interface, application,
table Description automatically
generated](./images/media/image11.png){width="2.9357731846019246in"
height="1.9534886264216973in"}

![Chart, application, table Description automatically
generated](./images/media/image12.png){width="2.918297244094488in"
height="1.9418602362204724in"}

**Figure 5.0** The graphs produced by blondel's and Louvain algorithms
\[5\] \[6\] in calculating Betweenness centrality and mean clustering
coefficient.

The clustering coefficient explains the triangulation within a network
by averaging the clustering coefficients of all its nodes. It is used in
the analysis of social networks to measure the degree to which nodes in
a graph tend to cluster together \[7\]. The clustering coefficient of
0.881 suggests the department's researchers have a high tendency to
cluster together on related tasks. The local cluster efficient (Watz,
Strogaatz) \[8\] is a measure of to what degree is a node's
neighbourhood fully connected, and the global value in an undirected
graph such as this is the average local coefficient across all nodes.
The number of communities that maximises modularity is 35, with a score
of 0.67. And as discussed in the lectures it is apparent that such a
large number of clusters despite maximising modularity should be
constrained in order to identify fewer key topics in computer science,
in order to gather some more data.

One unique observation is the Average path length of 5.9 coinciding with
the small world phenomenon \[9\] of every person's 6 degrees of
separation. This would suggest this social network is no more well
connected than one of the world's computer science researchers. The
small world phenomenon is typically a small average path length and a
large global clustering coefficient.

One final limitation of the model is the assumption that all
collaborations can be shown through widely available publications such
as articles; and fails to capture works such as books or software, this
could be strengthened by including more data sources.

Bibliography

| [1] | V. S. Malbas, &quot;Mapping the collaboration networks of biomedical research in Southeast Asia,&quot; 2015. |
| --- | --- |
| [2] | G. &amp;. D. C. Abramo, &quot;(2015). The relationship between the number of authors of a publication...,&quot; _Journal of Informetrics.,_ 2015. |
| [3] | [Online]. Available: https://www.elsevier.com/solutions/scopus/how-scopus-works#. |
| [4] | M. G. |. A. Mauro, &quot;(Reviewing Editor) (2016) A social network analysis of Twitter: Mapping the digital humanities community,,&quot; _Cogent Arts &amp; Humanities, ,_ vol. 3:1, no. DOI: 10.1080, 2016. |
| [5] | J.-C. D. M. B. R. Lambiotte, &quot;Laplacian Dynamics and Multiscale Modular Structure in Networks,&quot; 2009. |
| [6] | J.-L. G. R. L. E. L. Vincent D Blondel, &quot; Fast unfolding of communities in large networks,,&quot; in _in Journal of Statistical Mechanics: Theory and Experiment_ , 2008. |
| [7] | M. E. J. Newman, &quot;Networks: An Introduction,&quot; in _Oxford University Press_, New York, 2010. |
| [8] | D. J. W. &amp;. S. H. Strogatz, &quot;Collective dynamics of &#39;small-world&#39; networks,&quot; _Department of Theoretical and Applied Mechanics, Kimball Hall, Cornell University, Ithaca, New York 14853, USA,_ 1998. |
| [9] | S. Milgram, &quot;The Small World Problem,&quot; in _Psychology Today. Ziff-Davis Publishing Company_, 1967. |
