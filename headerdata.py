#!/usr/bin/env python2.7

from email.parser import HeaderParser
import glob
from string import join
import numpy

def preprocess(val): #preprocess text string for whitespace
    if val is not None:
        val = val.replace('\r\n\t',' ')
        val = val.replace('\r\n',' ')
        val = val.replace('>,','>>,') #hack for splitting emails
        val = val.replace('"','') #hack for splitting emails
        val = val.lower()
    return val

psr = HeaderParser() #parser object
FILES = glob.glob('email/*.eml') #files

#storage for recipients
FROM = []
TO = []
CC = []

to_out = open('dnc_to-out.tab','w')
cc_out = open('dnc_cc-out.tab','w')
from_out = open('dnc_from-out.tab','w')
sender_out = open('dnc_sender-out.tab','w')
sub_out = open('dnc_subject-out.tab','w')

for i in range(len(FILES))[:]:
    #print '\n\n ########## %d %s #########'%(i,FILES[i])
    fin = open(FILES[i])
    msg = psr.parse(fin)
    sub,frm,to,cc,sender = msg.get('subject'), msg.get('from'), msg.get('to'), msg.get('cc'), msg.get('sender')

    #replace white space, handle '>' symbols conveniently
    sub = preprocess(sub)
    frm = preprocess(frm)
    sender = preprocess(sender)
    to = preprocess(to)
    cc = preprocess(cc)

    FROM.append(frm)
    if cc is not None: CC.extend(cc.split('>,'))
    if to is not None: TO.extend(to.split('>,'))

    #write out per each email
    sub_out.write('%s %s\n'%(FILES[i],sub))
    from_out.write('%s %s\n'%(FILES[i],frm))
    sender_out.write('%s %s\n'%(FILES[i],sender))
    to_out.write('%s %s\n'%(FILES[i],to))
    cc_out.write('%s %s\n'%(FILES[i],cc))

print 'number from', len(FROM)
print 'number to', len(TO)
print 'number cc', len(CC)

print '\n\n######### unique from (%d) #######', len(numpy.unique(FROM))
for u in numpy.unique(FROM): print u
print '\n\n######### unique to (%d) #######', len(numpy.unique(TO))
for u in numpy.unique(TO): print u
print '\n\n######### unique cc (%d) #######', len(numpy.unique(CC))
for u in numpy.unique(CC): print u

to_out.close()
cc_out.close()
from_out.close()
sender_out.close()
sub_out.close()
