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
from polypin import *

def dimm(val):#unit choise mechanism, conversion funcs from padgen
    if dim=='mm':
        return mm(val)
    elif dim=='mil':
        return mil(val)
    elif dim =='cmil':
        return val
    else:
        raise ArithmeticError, 'valid dim args are mm mil cmil'



def dilic(name, xs, pp, pc, dr, xd, yd):
    foot = footprint(name);

    #left row
    x = -xs/2
    y =  -((pc/2)-1)*pp/2
    
    for i in range(0,pc/2):
        pinbits = extpin(x,y+(i*pp),dr,2,str(i+1))
        for parts in pinbits:
            foot.add(parts)

    #right row
    y = ((pc/2)-1)*pp/2
    x = xs/2
    
    for i in range(0,pc/2):
        pinbits = extpin(x,y-(i*pp),dr,2,str(i+1+(pc/2)))
        for parts in pinbits:
            foot.add(parts)



    if xd ==0 or yd==0:
        print 'outline skipped due to yd or xd =0'
    else:
        a= xd/2
        b= yd/2

        poly =[[-a,-b],[-a,b],[a,b],[a,-b]]
        for i in range(0,len(poly)):
            foot.add(line(poly[i][0],poly[i][1],poly[i-1][0],poly[i-1][1],1000))

        ind = arc()
        ind.circ(-a*0.9,-b*0.9,a*0.05,1000)
        foot.add(ind)
    return foot



if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 10:
        print 'Usage: '+sys.argv[0] + """ name xs pp pc dr xd yd dim out

Where:
name = package or footprint name
xs = distance between rows of pin centers in x
pp = pin pitch
pc = total pin count
dr = drill size
xd = package width
yd = package height
dim = {mm,mil,cmil}
out = output file

 
"""
        sys.exit()
    
    dim=sys.argv[8]
    name = sys.argv[1]
    xs = dimm(float(sys.argv[2]))
    pp = dimm(float(sys.argv[3]))
    pc = int(sys.argv[4])
    dr = dimm(float(sys.argv[5]))
    xd = dimm(float(sys.argv[6]))
    yd = dimm(float(sys.argv[7]))
    out = sys.argv[9]

    foot = dilic(name, xs, pp, pc, dr, xd, yd)
    
    f = open(out,'w')
    f.write(foot.generate())
