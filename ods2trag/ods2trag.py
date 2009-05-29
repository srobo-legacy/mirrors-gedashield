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



import sys, string, os
import zipfile
from xml.sax import saxutils, handler, make_parser, InputSource, parseString

DELIMITER = '\x09'

def strclean(stin,row):
    stout =''
    for c in stin:
        if ord(c) > 128:
            print "Error: Input file has character not in ascii charset, on row",row,"skipping this character"
            #sys.exit()
        else:
            stout +=c

    return stout


class ContentGenerator(handler.ContentHandler):
    def __init__(self,outfile):
        handler.ContentHandler.__init__(self)
        self.sheet=[]
        self.row=0
        self.col=0
        self.outfile = outfile
        self.tabnames = []


    def endDocument(self):
        wstr=''
        count=0
        outcontent=''
        for t in self.sheet:
            pos = self.outfile.rfind('.') #find last full stop
            if pos >0: # -1 if no file extension
                name = self.outfile[:pos]+ self.tabnames[count] + self.outfile[pos:]
            else:
                name = self.outfile + self.tabnames[count]


            outf = open(name,'w')
            outcontent=''
            for r in t:
                wstr = ''
                for c in r:
                    wstr += c
                    wstr += DELIMITER
                    pass
                outcontent += wstr[:-1]#skip last tab on row
                outcontent += '\n'
            outf.write(outcontent)
            outf.close()
            count +=1
                

    def startElement(self, name, attrs):
       # print '>>>',name
        if name=='office:spreadsheet':
            self.ss_handle(name,attrs)
        elif name=='table:table':
            self.tb_handle(name,attrs)
        elif name=='table-column':
            self.tcol_handle(name,attrs)
        elif name=='table:table-row':
            self.trow_handle(name,attrs)
        elif name=='table:table-cell':
            self.tcell_handle(name,attrs)
        else:
            #print "tag",name,"unrecognised"
            pass




    # tag handler functions
    def characters(self, content):
        self.sheet[-1][-1][-1] += strclean(saxutils.escape(content),self.row)

    def ss_handle(self,name,attrs):
        pass

    def tb_handle(self,name,attrs):
        self.sheet.append([]) # add a table to the sheet
        self.tabnames.append(attrs.getValue('table:name')) # add tabe name to list so that output files can be appropriately named


    def tcol_handle(self,name,attrs):
        pass
    def trow_handle(self,name,attrs):
        self.sheet[-1].append([]) # add a row to the last table made
        self.row += 1
      
    def tcell_handle(self,name,attrs):
        self.sheet[-1][-1].append('') # add empty string last row created
      

#     def endElement(self, name):
#         pass
#     def startDocument(self):
#         pass
#     def ignorableWhitespace(self, content):
#         print "whitespace"
#     def processingInstruction(self, target, data):
#         print "processing instruction"

def run(inods,outcsv):
    zip= zipfile.ZipFile(inods, "r")
    xml = zip.read("content.xml")
    zip.close()
    parseString(xml,ContentGenerator(outcsv))

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print 'Usage: '+ os.path.basename(sys.argv[0]) + """ <input.ods> <output csv>"""
        sys.exit()

    run(sys.argv[1],sys.argv[2])


