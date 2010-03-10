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
        
    out = 'test.fp'
    

    foot = footprint('pies');
    current_pin=0

    
    for i in range(10):
        pn = pin()
        pn.simple( mm(20), mm(10*(i+1)),mm(0.2*(i+1)),str(i+1))
        foot.add(pn)


    print foot.generate()
