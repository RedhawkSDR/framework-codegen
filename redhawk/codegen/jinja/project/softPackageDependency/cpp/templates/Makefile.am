#{#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#}
#
AM_CXXFLAGS = 
lib{{component.name}}{{generator.variant}}_la_LIBADD = {{generator.linkLibraries}}

lib_LTLIBRARIES = lib{{component.name}}{{generator.variant}}.la
libdir = $(prefix)/{{component.sdrpath}}/{{component.name}}{{generator.variant}}/{{component.impl.id}}/lib

pkgconfigdir = $(prefix)/{{component.sdrpath}}/{{component.name}}{{generator.variant}}/{{component.impl.id}}/lib/pkgconfig
pkgconfig_DATA = {{component.name}}{{generator.variant}}.pc

xmldir = $(prefix)/{{component.sdrpath}}/{{component.name}}{{generator.variant}}/
dist_xml_DATA = ../{{component.name}}{{generator.variant}}.spd.xml

datadir = $(prefix)/{{component.sdrpath}}/{{component.name}}{{generator.variant}}/{{component.impl.id}}/lib/


lib{{component.name}}{{generator.variant}}_la_SOURCES = $(source)

incdir = $(prefix)/{{component.sdrpath}}/{{component.name}}{{generator.variant}}/{{component.impl.id}}/include
dist_inc_DATA = $(headers)

#list source files here in decending order of importance. Use the convention
#source = \
#foo1.cpp \
#foo2.cpp \
source = \



#list header files here in decending order of importance. Use the convention 
#headers = \
#foo1.h \
#foo2.h \
headers = \


distclean-local:
	rm -f config.*
	rm -rf autom4te.cache
	rm -f acinclude.m4
	rm -f aclocal.m4
	rm -f configure
	rm -f depcomp
	rm -f install-sh
	rm -f ltmain.sh
	rm -f Makefile.in
	rm -f missing
	rm -rf .deps
