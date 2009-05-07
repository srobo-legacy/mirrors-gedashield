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



NAME=CY7C68014A-128AXC
SMD = ../pcbfoot/smd-ic.py
ODSTOOL= ./ods2trag.py
all: footprint symbol

footprint:
	$(SMD) $(NAME) 21.4 13.4 38 26 0.7 0.3 0.5 22 14 mm $(NAME).fp

symbol:
	$(ODSTOOL) $(NAME).ods $(NAME).src
	for i in $$(ls *.src); do  tragesym $$i $${i%.src}.sym ;done
 
clean:
	#beware of other files in the same dir!
	-rm -f *.sym *.src *.fp