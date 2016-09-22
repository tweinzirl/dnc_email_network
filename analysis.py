#!/usr/bin/env python2.7

import numpy
from string import join
import os
from igraph import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pylab

pylab.rc('axes',labelsize=16)
pylab.rc('xtick',labelsize=14)
pylab.rc('ytick',labelsize=14)
pylab.rc('legend',fontsize=9)

g = Graph.Read_GraphML('dnc-email-graph.graphml')

NE = float(len(g.es))
## edge properties
print 'number edges: ', NE
print 'number one-way edges', len(g.es.select(dir_eq=1)), len(g.es.select(dir_eq=1))/NE
print 'number two-way edges', len(g.es.select(dir_eq=2)), len(g.es.select(dir_eq=2))/NE

#visual style
color_dict = {1: "black", 2: "red"}

visual_style={}
visual_style["vertex_frame_color"] = 'blue'
visual_style["vertex_color"] = 'white'
visual_style["vertex_size"] = 5
visual_style['edge_color'] = [color_dict[direct] for direct in g.es['dir']]
visual_style["bbox"] = (1000, 1000)

maxdegree = g.maxdegree(loops=1)

'''
###vertex degree
pylab.figure(figsize=(8,6))

sums,bins,crap = pylab.hist(g.degree(loops=1),bins=pylab.arange(0,520,5),cumulative=1)
pylab.cla()
pylab.plot(bins[:-1], sums/float(len(g.vs)), 'b-', drawstyle='steps-mid')
pylab.xlabel('Vertex degree')
pylab.ylabel(r'Fraction ($\leq$ degree)')
pylab.xlim(0,480)

pylab.savefig('vertexDegree.png')
'''

###edge mag
pylab.figure(figsize=(8,6))

sums,bins,crap = pylab.hist(g.es['mag'],bins=pylab.arange(0,215,5),cumulative=1)
pylab.cla()
pylab.plot(bins[:-1], sums/float(len(g.es)), 'b-', drawstyle='steps-mid')
pylab.xlabel('Number of emails exchanged per edge')
pylab.ylabel(r'Cumulative fraction of emails')
pylab.annotate('Maximum emails exchanged per edge: %d'%max(g.es['mag']),(0.5,0.15),xycoords='axes fraction',ha='center',size=13)
pylab.xlim(0,200)

pylab.savefig('cumEmails-Fig3.png')

###community analysis plot
pylab.figure(figsize=(8,6))

d=g.degree()
srtd = pylab.sort(d)[::-1][:5] #top five 'steps'

maxedges = float(len(g.es.select(_within=g.vs)))
X,Y = [],[]

for i in range(maxdegree+1)[:]:
    vertices = g.vs.select(_degree_le=i)
    edges = g.es.select(_within=vertices)
    X.append(i)
    Y.append(len(edges)/maxedges)

pylab.plot(X,Y,label='_no_legend')
pylab.xlabel('Vertex degree')
pylab.ylabel(r'Cumulative fraction of confined edges')
pylab.annotate('Maximum vertex degree: %d'%maxdegree,(0.25,0.95),xycoords='axes fraction',ha='center',size=13)

color=['#FF0000','#00FF00','k','#0000FF','#FF00FF']
for i in range(len(srtd)): 
    pylab.axvline(x=srtd[i],ls=':',c=color[i],ymax=0.9,label='%s (degree = %d)'%(g.vs.find(_degree=srtd[i])['name'],srtd[i]),lw=3)

pylab.legend(numpoints=1,loc='best')
pylab.savefig('stepPlot-Fig4.png')
