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







#all units are 1/100 mil - this is imperial (10^-5 Inch)
MILS=39.3700787#mils in 1mm - source google

def mm(mmin):
    '''hundreds of mills equivalent to input mm'''
    centimils=MILS*100 # in mm not the other way round!
    return mmin * centimils

def mil(milin):
    '''returns hundereds of mills for mil input'''
    return milin * 100

def rstr(dec):
    return str(int(round(dec)))
        
class footprint():
    def __init__(self,nm):
        self.elements = []
        
        self.SFlags=''
        self.Desc = ''
        self.Name = nm 
        self.Value = ''
        self.MX = 0
        self.MY = 0
        self.TX = 0
        self.TY = 0
        self.TDir = 0
        self.TScale = 100
        self.TSFlags = ''

    def add(self,part):
        self.elements.append(part)

    def generate(self):
        s = ''
        s += 'Element["'+self.SFlags+ '" "'+self.Desc+'" "'+self.Name+'" "'+self.Value+'" '+str(self.MX)+' '+str(self.MY)+' '+str(self.TX)+' '+str(self.TY)+' '+str(self.TDir)+' '+str(self.TScale)+' "'+self.TSFlags+'"] \n'
        s += "(\n"
        for unit in self.elements:
            s += unit.getstring()

        s += ')\n'

        return s


# Element["" "TO-18" "" "" 65000 287500 -6000 3500 0 100 ""]
# (
#         Pin[-10000 10000 6000 2000 6600 2800 "" "C" "edge2"]
#         ElementLine [7500 3000 11500 3000 600]
#         ElementLine [11500 3000 11500 7000 600]
#         ElementLine [11500 7000 7500 7000 600]
#         ElementArc [-5000 5000 10500 10500 270 90 600]
#         ElementArc [-5000 5000 12500 12500 90 90 600]
#         ElementArc [-5001 5001 12499 12499 0 90 600]
# )

class pin():
    def __init__(self):
        self.rX=0
        self.rY=0 
        self.Thickness=0 
        self.Clearance=mm(0.35)
        self.Mask=0 
        self.Drill=0 
        self.Name=''
        self.Number=''
        self.SFlags=''
        
    def getattr(self):
        return self.SFlags
    def setattr(self,attr):
        self.SFlags = attr
    def addattr(self,attr):
        if self.SFlags=='':
            self.SFlags=attr
        else:
            self.SFlags +=','+attr



    def prim(self,X, Y, thick, clear, mask, drl,name, number, sf):
        self.rX=X
        self.rY=Y 
        self.Thickness=thick
        self.Clearance=clear
        self.Mask=mask
        self.Drill=drl
        self.Name=name
        self.Number=number
        self.SFlags=sf


    def simple(self,x,y,d,num):
        self.rX=x
        self.rY=y 
        self.Drill=d

        if d <= 4000: # this appears to be the algorythum other popular cad tools use....
            self.Thickness= d + 1000
        elif d > 12000:
            self.Thickness= d + 2000
        else:
            self.Thickness=  d+(d/2)

        self.Mask = self.Thickness + 400
        self.Name=num
        self.Number=num


#Pin [rX rY Thickness Clearance Mask Drill "Name" "Number" SFlags]
    def getstring(self):
        s = ''
        s += '\t'#tab in
        s += 'Pin['
        s += rstr(self.rX) + ' '
        s += rstr(self.rY) + ' '
        s += rstr(self.Thickness) + ' '
        s += rstr(self.Clearance) + ' '
        s += rstr(self.Mask) + ' '
        s += rstr(self.Drill) + ' '
        s += '"' + self.Name+'"' + ' '
        s += '"' + self.Number+'"' + ' '
        s += '"' + self.SFlags+'"' + ' '
        s += ']\n'
        return s





class pad():
    def __init__(self):
        self.posx=0
        self.posy=0
        self.name =''
        self.number=''
        self.SFlags=''
        
        self.thick=0
        self.x1=0
        self.x2=0
        self.y1=0
        self.y2=0
        self.mask =0
        self.clearance = mm(0.35)

        #temp vars
        self.linelen=0


    def getattr(self):
        return self.SFlags
    def setattr(self,attr):
        self.SFlags = attr
    def addattr(self,attr):
        if self.SFlags=='':
            self.SFlags=attr
        else:
            self.SFlags +=','+attr



    def len_wid(self,cen_x,cen_y,len,wid,rot,pin):
        if (wid > len): # where 
            raise AttributeError, 'It is assumed that pads are taller than wide, use rotate for other cases'
        
        self.thick = wid
        self.linelen = (len-wid)/2 # its div 2 because the center point is in the middle
        if ( rot == 0) or (rot == 180):
            self.x1 = cen_x
            self.y1 = cen_y - self.linelen
            self.x2 = cen_x
            self.y2 = cen_y + self.linelen
        elif (rot == 90) or (rot==270):
            self.x1 = cen_x - self.linelen
            self.y1 = cen_y
            self.x2 = cen_x  + self.linelen
            self.y2 = cen_y 
        else:
            raise AttributeError, ' sorry dont support arbitrary rot yet, 0,90,180,270 only'
        
        
        self.number = str(pin)
        self.name = str(pin)

       
            
    def getstring(self):
        s = ''
        s += '\t'#tab in
        s += 'Pad['
        s += rstr(self.x1) + ' '
        s += rstr(self.y1) + ' '
        s += rstr(self.x2) + ' '
        s += rstr(self.y2) + ' '
        s += rstr(self.thick) + ' '
        s += rstr(self.clearance) + ' '
        s += rstr(self.mask) + ' '
        s += '"' + self.name+'"' + ' '
        s += '"' + self.number+'"' + ' '
        s += '"' + self.SFlags+'"' + ' '
        s += ']\n'
        return s
        

#Pad [rX1 rY1 rX2 rY2 Thickness Clearance Mask "Name" "Number" SFlags]
# i predict this reference is wring - the flags should have "" also ?


class line():
    def __init__(self,ix1,iy1,ix2,iy2,iwid):
        self.thick=iwid
        self.x1=ix1
        self.x2=ix2
        self.y1=iy1
        self.y2=iy2

    def getstring(self):
        s = ''
        s += '\t'#tab in
        s += 'ElementLine['
        s += rstr(self.x1) + ' '
        s += rstr(self.y1) + ' '
        s += rstr(self.x2) + ' '
        s += rstr(self.y2) + ' '
        s += rstr(self.thick) 
        s += ']\n'
        return s
        
#ElementLine[rX1 rY1 rX2 rY2 Thickness]

class arc():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.sa = 0
        self.sd = 0
        self.thick = 0

    def prim(self,rX, rY, width, height,sangle,dangle, thickness):
        self.x = rX
        self.y = rY
        self.w = width
        self.h = height
        self.sa =sangle
        self.sd =dangle
        self.thick = thickness
        
    def circ(self,rX,rY,rad,thickness=1000):
        #print rX,rY,rad,thickness
        self.x = rX
        self.y = rY
        self.w = rad
        self.h = rad
        self.sa =0
        self.sd =360
        self.thick = thickness

    def getstring(self):
        s = ''
        s += '\t'#tab in
        s += 'ElementArc['
        s += rstr(self.x) + ' '
        s += rstr(self.y) + ' '
        s += rstr(self.w) + ' '
        s += rstr(self.h) + ' '
        s += rstr(self.sa) + ' '
        s += rstr(self.sd) + ' '
        s += rstr(self.thick) 
        s += ']\n'
        return s

#ElementArc [rX rY Width Height StartAngle DeltaAngle Thickness]


if __name__ == "__main__":
#     import sys
#     if not len(sys.argv) == 3:
#         print 

    foot = footprint();
    for i in range(10):
        p = pad()
        p.len_wid((i+1)*15,40,8,3,90,i+1)
        p.addattr('square')
        foot.add(p)

    print foot.generate()
