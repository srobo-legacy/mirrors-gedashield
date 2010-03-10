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



import sys
from pcbfoot import dil_ic, padgen
from pcbfoot.padgen import mm # could be mil/cmil if needs must

#make basic pinlayout with no silkscreen
pins = dil_ic.dilic('xbee', mm(22), mm(2), 20, mm(0.8), 0, 0) # like command line args

#xbee details
#long faces
base = 24.52 
side = 22
#square sides of corner triangles
corner_base = 7.59
corner_height = 6.53

a= base/2
b= side/2

#define the outline as a list of points
poly =[[-a,-b],[-a,b],[a,b],[a,-b],[a-corner_base,-b-corner_height],[-a+corner_base,-b-corner_height]]

#join up the dots
for i in range(0,len(poly)):
    pins.add(padgen.line(mm(poly[i][0]),mm(poly[i][1]),mm(poly[i-1][0]),mm(poly[i-1][1]),1000))
 
#write description string to file
f = open(sys.argv[1],'w')
f.write(pins.generate())
