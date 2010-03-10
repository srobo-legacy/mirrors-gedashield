#!/usr/bin/env python
#     This file is part of Gedashield.
#
#     Gedashield is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Gedashield is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Gedashield.  If not, see <http://www.gnu.org/licenses/>.

#     Copyright 2009 Tom Bennellick gedashield (at) bennellick.com


from  padgen import *

def dimm(val):
    if dim=='mm':
        return mm(val)
    elif dim=='mil':
        return mil(val)
    elif dim =='cmil':
        return val
    else:
        raise ArithmeticError, 'valid dim args are mm mil cmil'

if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 13:
        print 'Usage: '+sys.argv[0] + """ name xs ys xn yn ph pw pp xd yd dim out

Where:
name = package or footprint name
xs = distance between rows of pin centers in x
ys = distance between rows of pin centers in y
xn = number of pins up sides
yn = number of pins allong top and bottom 
ph = pad height
pw = pad width
pp = pad pitch
xd = package width
yd = package height
dim = {mm,mil,cmil}
out = output file

 
"""
        sys.exit()
    
    dim=sys.argv[11]
    name = sys.argv[1]
    xs = dimm(float(sys.argv[2]))
    ys = dimm(float(sys.argv[3]))
    xn = int(sys.argv[4])
    yn = int(sys.argv[5])
    ph = dimm(float(sys.argv[6]))
    pw = dimm(float(sys.argv[7]))
    pp = dimm(float(sys.argv[8]))
    xd = dimm(float(sys.argv[9]))
    yd = dimm(float(sys.argv[10]))
    
    out = sys.argv[12]


    foot = footprint(name);
    current_pin=0

    x = -xs/2
    y = -pp*(xn-1)/2
    
    for i in range(0,xn):
        p = pad()
        p.len_wid(x,y+(i*pp),ph,pw ,90,i+1)
        p.addattr('square')
        foot.add(p)


    x = - pp*(yn-1)/2 
    y = ys/2

    for i in range(0,yn):
        p = pad()
        p.len_wid(x+(i*pp),y,ph,pw ,0,i+1+xn)
        p.addattr('square')
        foot.add(p)

 
    x = xs/2
    y = pp*(xn-1)/2

    for i in range(0,xn):
        p = pad()
        p.len_wid(x,y-(i*pp),ph,pw ,90,i+1+yn+xn)
        p.addattr('square')
        foot.add(p)

    x = pp*(yn-1)/2 
    y = -ys/2

    for i in range(0,yn):
        p = pad()
        p.len_wid(x-(i*pp),y,ph,pw ,0,i+1+xn+yn+xn)
        p.addattr('square')
        foot.add(p)

    a= xd/2
    b= yd/2

    poly =[[-a,-b],[-a,b],[a,b],[a,-b]]
    for i in range(0,len(poly)):
        foot.add(line(poly[i][0],poly[i][1],poly[i-1][0],poly[i-1][1],1000))

    ind = arc()
    ind.circ(-a*0.9,-b*0.9,a*0.05,1000)
    foot.add(ind)

    foot.elements[0].setattr('')#make pin 1 round
    
    f = open(out,'w')
    f.write(foot.generate())
