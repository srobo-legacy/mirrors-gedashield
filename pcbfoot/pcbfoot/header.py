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

def header(name, xn, yn,pp=100,dim='mil',d=50):
    foot = footprint(name);

    # Token stupidity check
    if xn ==0 or yn==0:
        print 'youve got to have at least 1 row and 1 column!'
        sys.exit()
    # draw pins
    for i in range(0,xn):
        for j in range(0,yn):
            pinbits = extpin(i*mil(pp),j*mil(pp),mil(d),1,str((i+1)*(j*1)))
            for bit in pinbits:
                foot.add(bit)
            print i , j

    #draw outline
    x = y = -mil(pp)*0.6 # Top and Left
    a= (xn-0.4)*mil(pp) # right side
    b= (yn-0.4)*mil(pp) # Bottom side

    poly =[[x,y],[x,b],[a,b],[a,y]]
    for i in range(0,len(poly)):
        foot.add(line(poly[i][0],poly[i][1],poly[i-1][0],poly[i-1][1],1000))

    ind = arc()
    ind.circ(0,-(mil(pp)),a*0.05,1000)
    foot.add(ind)
    
    return foot



if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 4:
        print 'Usage: '+sys.argv[0] + """ name xn yn

Where:
name = package or footprint name

 
"""
        sys.exit()
    dim = 'mil'
    sname = sys.argv[1]
    sxn = int(sys.argv[2])
    syn = int(sys.argv[3])
#     print sname
#     print sxn
#     print syn
    foot = header(sname, sxn, syn)
    f = open(sname+'.fp','w')
    f.write(foot.generate())
    f.close()
