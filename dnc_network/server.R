#server.R

library(igraph)
library(qgraph)
source('graphFunc.R')

shinyServer(
  function(input, output) {
  
      g=read_graph('dnc-email-graph.graphml',format='graphml')

      output$lePlot = renderPlot({
          print(as.integer(input$leDegree[1]))
          result = subgrph_le_degree(g,as.integer(input$leDegree[1]))
          g2=result[[1]]
          edgeColors=result[[2]]
          community = cluster_louvain(g2)
          mod = modularity(community)
          qgraph(as_edgelist(g2),layout="spring",directed=FALSE,edge.color=edgeColors,border.color='blue',edge.width=0.5,node.width=0.5,labels=FALSE, title= sprintf('Graph A    Vertices: %d/%d, Edges: %d/%d, Modularity: %.2f', length(which(degree(g2)>0)), length(V(g)), length(E(g2)), length(E(g)), mod) )
      })

      output$gePlot = renderPlot({
          result = subgrph_ge_degree(g,as.integer(input$geDegree))
          print(as.numeric(input$geDegree))
          g2=result[[1]]
          edgeColors=result[[2]]
          community = cluster_louvain(g2)
          mod = modularity(community)
          qgraph(as_edgelist(g2),layout="spring",directed=FALSE,edge.color=edgeColors,border.color='blue',edge.width=0.5,node.width=0.5,labels=FALSE,width=5,height=5,title= sprintf('Graph B    Vertices: %d/%d, Edges: %d/%d, Modularity: %.2f', length(degree(g2)>0), length(V(g)), length(E(g2)), length(E(g)), mod) )
      })

      output$namePlot = renderPlot({
          result = subgrph_name(g,input$nameGroup)
          g2=result[[1]]
          edgeColors=result[[2]]
          community = cluster_louvain(g2)
          mod = modularity(community)
          qgraph(as_edgelist(g2),layout="spring",directed=FALSE,edge.color=edgeColors,border.color='blue',edge.width=0.5,node.width=0.5,labels=FALSE,width=5,height=5,title= sprintf('Graph C    Vertices: %d/%d, Edges: %d/%d, Modularity: %.2f', length(degree(g2)>0), length(V(g)), length(E(g2)), length(E(g)), mod) )
      })

  }
)
