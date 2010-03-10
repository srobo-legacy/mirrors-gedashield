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


from pcbfoot.padgen import *


if __name__ == "__main__":
    foot = footprint()
    x = -10.4
    y = -8.75 
    for i in range(0,35):
        p = pad()
        p.len_wid(mm(x),mm(y+i*0.5),mm(1),mm(0.25),90,i+1)
        p.addattr('square')
        foot.add(p)

    x = -8.75
    y = 10.4 
    for i in range(0,35):
        p = pad()
        p.len_wid(mm(x+i*0.5),mm(y),mm(1),mm(0.25),0,i+37)
        p.addattr('square')
        foot.add(p)

    x = 10.4
    y = 8.75 
    for i in range(0,35):
        p = pad()
        p.len_wid(mm(x),mm(y-i*0.5),mm(1),mm(0.25),90,i+73)
        p.addattr('square')
        foot.add(p)

    x = 8.75
    y = -10.4 
    for i in range(0,35):
        p = pad()
        p.len_wid(mm(x-i*0.5),mm(y),mm(1),mm(0.25),0,i+109)
        p.addattr('square')
        foot.add(p)


    poly =[[-10,-10],[-10,10],[10,10],[10,-10]]
    for i in range(0,len(poly)):
        foot.add(line(mm(poly[i][0]),mm(poly[i][1]),mm(poly[i-1][0]),mm(poly[i-1][1]),1000))

    
    foot.elements[0].setattr('')

    print foot.generate()
