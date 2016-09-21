#!/usr/bin/env python2.7

import numpy
from string import join
import os
from igraph import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pylab

frmFile = 'dnc_from-out.tab'
toFile = 'dnc_to-out.tab'
ccFile = 'dnc_cc-out.tab'

FROM = []
TO = []
arrTO = numpy.array([])
NODE = []

#Capture from address and node
fin = open(frmFile)
for line in fin.readlines()[:]:
    toks = line.split('.eml')
    eml = toks[0]
    tmp = toks[1].strip() #get e.g., linkedin security <security-noreply@linkedin.com>
    #isolate actual email address
    try:
        i1,i2 = tmp.index('<'), tmp.index('>')
        addr = tmp[i1+1:i2]
    except ValueError:
        #print eml, tmp
        if tmp=='None': 
            addr='None'
            #print 'None', tmp, addr
        else:
            try:
                i1 = tmp.index('(') #look for '(no email address available)'
                tmp=tmp[:i1]
                addr= join(tmp.split(' '), '_')
                if addr=='': addr='None'
                #print 'try uhoh', tmp, addr
            except ValueError:
                addr= join(tmp.split(' '),'_')
                #print 'except uhoh', tmp, addr
    #record node
    FROM.append(addr)
    NODE.append(os.path.basename(eml))
fin.close()


print 'From stats: shape=%s  nunique=%d'%(numpy.shape(FROM),len(numpy.unique(FROM)))
#for ui in numpy.unique(FROM): print ui

fin = open(toFile)
for line in fin.readlines()[:]:
    toks = line.split('.eml')
    tmp = toks[1].strip() #get e.g., linkedin security <security-noreply@linkedin.com>>, blah <blah.org>
    #isolate actual email addresses
    addrs = []
    try:
        for _ in tmp.split('>,'):
            i1,i2 = _.index('<'), _.index('>')
            addrs.append(_[i1+1:i2])
    except ValueError:
        if tmp=='None': 
            addrs.append(tmp)
            #print 'to none', tmp
        elif 'undisclosed' in tmp: 
            addrs.append('undisclosed')
            #print 'to undisclosed'
    TO.append(addrs)
    arrTO = numpy.append(arrTO,addrs)
    #print tmp, addrs
fin.close()

print 'To stats: shape=%s  nunique=%d'%(numpy.shape(arrTO),len(numpy.unique(arrTO)))

setFROM = set(FROM)
setTO = set(arrTO)
setALL = setFROM.union(setTO)

print 'union stats: num = %d'%(len(setALL))

#make mapping MAPPING = {key:index} where key = email address and val = row/col in D
MAPPING ={}
#make reverse mapping revMAPPING = {key:index} where key = ow/col in D and val = email address
revMAPPING ={}
count=0
for item in setALL: 
    MAPPING[item]=count
    revMAPPING[count]=item
    count+=1

print 'first 10 items', MAPPING.items()[:10]

#storage for Graph D[i,j]=val  means `val' emails were sent from i to j
D = numpy.zeros([len(setALL),len(setALL)])

for i in range(len(FROM))[:]:
    #to = TO[i]
    to = numpy.unique(TO[i]) #correct for the same people showing up in email recipient list more than once
    #print NODE[i], FROM[i], to, MAPPING[FROM[i]]
    for j in range(len(to)): D[ MAPPING[FROM[i]], MAPPING[to[j]] ]+=1

#seems correct on Sep 5

########### now construct the graph ###########
g=Graph()
g.add_vertices(len(setALL))
g.vs['name'] = [item for item in setALL]

#cycle through D to determine edges, 'magnitude' of connection, and 'direction'
num_edges = 0
for i in range(len(setALL)):
    for j in range(i+1): #this allows loops to be counted, which contribute 2 to the vertex degree count
        mag = D[i,j] + D[j,i]

        #only add edge if mag>0
        if mag > 0:
            if D[i,j]>0 and D[j,i]>0: direction=2 #two-way communication
            else: direction=1 #one-way communication

            g.add_edge(i,j)
            g.es[num_edges]['dir']=direction
            g.es[num_edges]['mag']=mag
            num_edges+=1

#snip None and undisclosed vertices and related edges
for name in ['None','undisclosed']:
    count = 0
    index = g.vs.find(name=name).index
    edgeseq = g.es.select(_to=index)
    count += len(edgeseq)
    g.delete_edges(edgeseq)
    edgeseq = g.es.select(_from=index)
    count += len(edgeseq)
    g.delete_edges(edgeseq)
    g.delete_vertices([index])
    print 'deleted vertex %s and %d edges'%(name,count)

#remove all vertices with 0 degree, 23/24 of which come from removing None and undisclosed vertices
vertseq = g.vs.select(_degree=0)
g.delete_vertices(vertseq)

#visual style
color_dict = {1: "gray", 2: "orange"}

visual_style={}
#visual_style["vertex_label"] = g.vs.indices
visual_style["vertex_frame_color"] = ['maroon' for _ in g.vs.indices]
visual_style["vertex_color"] = ['white' for _ in g.vs.indices]
visual_style["vertex_size"] = [4 for _ in g.vs.indices]
visual_style['edge_color'] = [color_dict[direct] for direct in g.es['dir']]
visual_style["bbox"] = (1000, 1000)

#'''
#update vertex frame color for the top 5 communities
cname = ['comers@dnc.org','mirandal@dnc.org','kaplanj@dnc.org','allenz@dnc.org','parrishd@dnc.org']
color = ['red','green','black','blue','magenta']
for i in range(len(cname)):
    idx = g.vs.find(name=cname[i]).index
    visual_style["vertex_frame_color"][idx] = color[i]
    visual_style["vertex_color"][idx] = color[i]
    visual_style["vertex_size"][idx] = 8
#'''
layout_str='fr' #layout_fruchterman_reingold()
layout = g.layout(layout_str) 
plot(g, 'dnc-%s-test.png'%layout_str, layout = layout, **visual_style)

### community analysis
community = g.community_multilevel()

membership = pylab.array(community.membership) #all vertices
sizes = pylab.array(community.sizes()) #cluster sizes, n_clusters
indices = pylab.array(g.vs.indices)
d=g.degree()
threshold=3 #require communities to have >= 3 members
good_cluster_index = pylab.where(sizes>threshold)[0]
print '%d clusters above threshold'%len(good_cluster_index)

#set appealing colors for visualization
#carray = ['blue','sea green','red','orange','aqua','aquamarine','cornflower','magenta','firebrick','lawn green','thistle','Goldenrod']
carray = ['blue','#2E8B57','red','orange','aqua','yellow','#6495ED','magenta','#B22222','#7CFC00','#D8BFD8','Goldenrod'] #

###assign vertex color based on community membership
colors = [] 
vsize = [6 for v in indices]
for m in membership:
    if m in good_cluster_index:
        i=pylab.where(m==good_cluster_index)[0][0]
        colors.append(carray[i])
    else:
        colors.append("rgb(0,0,0)")  #black

#find highest degree vertex in each cluster with >theshold members
for gci in good_cluster_index:
    idx = pylab.where(membership==gci)[0]
    vs = indices[idx]
    cldegree = []
    for v in vs: cldegree.append(d[v])
    print 'size of cluster: %d  max degree: %d   node of highest degree: %s (degree = %d)'%(len(idx), max(cldegree), g.vs['name'][vs[pylab.argmax(cldegree)]], d[vs[pylab.argmax(cldegree)]]), (pylab.array(colors)[idx])[0]
    vsize[vs[pylab.argmax(cldegree)]]=14

#redraw graph with updated coloring for community membership
plot(g, "graph-clusters-Fig4.png", layout=layout, vertex_color=colors, edge_color='gray',vertex_size=vsize, bbox=(1000,1000))

##### sanity checks
#write remaining vertex names to file
fout=open('dnc_vertex_names.txt','w')
for name in g.vs['name']: fout.write('%s\n'%name)
fout.close()

############# export data for use with R, other packages ########
g.write_graphml('dnc-email-graph.graphml') #read with g = Graph.Read_GraphML('dnc-email-graph.graphml')
