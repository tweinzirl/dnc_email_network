Project contents:

dnc-downloader.sh - Email downloader script

dnc-email-graph.graphml (the graph)

Email metadata files:
dnc_to-out.tab - sender per email
dnc_from-out.tab - recipients per email
dnc_cc-out.tab - carbon copies per email
dnc_subject-out.tab - subject per email

headerdata.py - construct the metadata files
mkGraph.py - construct the graph from the metadata files, do community detection
analysis.py - simple graph analysis

dnc_network/ - R Shiny web application

Running the R Shiny app:
>>> library(shiny)
>>> runApp('dnc_network')]
