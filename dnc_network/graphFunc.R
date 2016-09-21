library(igraph)

subgrph_ge_degree = function(g, d) {
    idx = which(degree(g)>=d)
    g2=induced_subgraph(g, idx, impl = c("create_from_scratch"))
    edgeColors = 1:length(E(g2))
    edgeColors[E(g2)$dir==1]='black'
    edgeColors[E(g2)$dir==2]='red'
    list(g2, edgeColors)
}

subgrph_le_degree = function(g, d) {
    idx = which((1<=degree(g)) & (degree(g)<=d))
    g2=induced_subgraph(g, idx, impl = c("create_from_scratch"))
    #g2=induced_subgraph(g, idx, impl = c("copy_and_delete"))
    edgeColors = 1:length(E(g2))
    edgeColors[E(g2)$dir==1]='black'
    edgeColors[E(g2)$dir==2]='red'
    list(g2, edgeColors)
}

subgrph_name= function(g, names) {
    idx = match(names, V(g)$name) #vertex of interest
    g2=subgraph.edges(g, E(g)[from(idx)], delete.vertices = TRUE)
    edgeColors = 1:length(E(g2))
    edgeColors[E(g2)$dir==1]='black'
    edgeColors[E(g2)$dir==2]='red'
    list(g2, edgeColors)
}
