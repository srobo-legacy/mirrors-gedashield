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


# def ovlpin(x,y,d,ratio,name,other=True):
#     return results


def extpin(x,y,d,ratio,name,shape_choose='sq',other=True):
    if ratio < 1:
        raise ArithmeticError, 'ratio must be >=1'
    if shape_choose == 'sq':
        shape = 'square'
    else:#add octagon case later
        shape = ''
        

    results = []
    pn = pin()
    pn.simple(x,y,d,name)
    results.append(pn)
    p = pad()
    p.len_wid(x,y,pn.Thickness*ratio,pn.Thickness,90,name)
    p.addattr(shape)
    results.append(p)

    if other:#put pad on both sides
        p2 = pad()
        p2.len_wid(x,y,pn.Thickness*ratio,pn.Thickness,90,name)
        p2.addattr(shape)
        p2.addattr('onsolder')
        results.append(p2)

    return results


    
if __name__ == "__main__":

    foot = footprint('test');

    oct = extpin(mm(3),mm(4),mm(0.6),1.1,'op1')

    for i in range(len(oct)):
        foot.add(oct[i])

    print foot.generate()

