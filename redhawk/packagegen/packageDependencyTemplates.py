
Makefile='# vim: noet: softtabstop=0\n\
\n\
xmldir = $(prefix)/dom/sharedPkgs/__LIBRARY_NAME__Pkg/\n\
dist_xml_DATA = __LIBRARY_NAME__Pkg.spd.xml\n\
domdir = $(prefix)/dom/sharedPkgs/__LIBRARY_NAME__Pkg/\n\
\n\
nobase_dist_dom_SCRIPTS = __LIBRARY_NAME__/*'

spd='<?xml version="1.0" encoding="UTF-8"?>\n\
<!-- \n\
This file is protected by Copyright. Please refer to the COPYRIGHT file distributed with this \n\
source distribution.\n\
\n\
This file is part of REDHAWK Basic Components.\n\
\n\
REDHAWK Basic Components is free software: you can redistribute it and/or modify it under the terms of \n\
the GNU Lesser General Public License as published by the Free Software Foundation, either \n\
version 3 of the License, or (at your option) any later version.\n\
\n\
REDHAWK Basic Components is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; \n\
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR \n\
PURPOSE.  See the GNU Lesser General Public License for more details.\n\
\n\
You should have received a copy of the GNU Lesser General Public License along with this \n\
program.  If not, see http://www.gnu.org/licenses/.\n\
-->\n\
<!DOCTYPE softpkg PUBLIC "-//JTRS//DTD SCA V2.2.2 SPD//EN" "softpkg.dtd">\n\
<softpkg id="__LIBRARY_NAME__Pkg" name="__LIBRARY_NAME__Pkg" type="sca_compliant">\n\
  <title></title>\n\
  <author>\n\
    <name></name>\n\
  </author>\n\
  <implementation id="default_impl">\n\
    <description></description>\n\
    <code type="SharedLibrary">\n\
      <localfile name="__LIBRARY_NAME__"/>\n\
    </code>\n\
    <compiler name="/usr/bin/gcc" version="4.1.2"/>\n\
    <programminglanguage name="Octave"/>\n\
    <humanlanguage name="EN"/>\n\
    <os name="Linux"/>\n\
    <processor name="x86"/>\n\
    <processor name="x86_64"/>\n\
  </implementation>\n\
</softpkg>'

reconf='#!/bin/sh\n\
\n\
rm -f config.cache\n\
\n\
# Setup the libtool stuff\n\
if [ -e /usr/local/share/aclocal/libtool.m4 ]; then\n\
    /bin/cp /usr/local/share/aclocal/libtool.m4 aclocal.d/acinclude.m4\n\
elif [ -e /usr/share/aclocal/libtool.m4 ]; then\n\
    /bin/cp /usr/share/aclocal/libtool.m4 acinclude.m4\n\
fi\n\
libtoolize --force --automake\n\
\n\
# Search in expected locations for the OSSIE acincludes\n\
if [ -n ${OSSIEHOME} ] && [ -d ${OSSIEHOME}/share/aclocal/ossie ]; then\n\
        OSSIE_AC_INCLUDE=${OSSIEHOME}/share/aclocal/ossie\n\
else\n\
    echo "Error: Cannot find the OSSIE aclocal files. This is not expected!"\n\
fi\n\
\n\
if [ -n ${OSSIE_AC_INCLUDE} ]; then\n\
        aclocal -I ${OSSIE_AC_INCLUDE}\n\
else\n\
        aclocal\n\
fi\n\
\n\
autoconf\n\
automake --foreign --add-missing'


configureAc='AC_INIT(python, 1.0.0)\n\
AM_INIT_AUTOMAKE(nostdinc)\n\
\n\
AC_PROG_INSTALL\n\
\n\
AC_CORBA_ORB\n\
OSSIE_CHECK_OSSIE\n\
OSSIE_SDRROOT_AS_PREFIX\n\
AM_PATH_PYTHON([2.3])\n\
\n\
PKG_CHECK_MODULES([OSSIE], [ossie >= 1.8])\n\
AC_CHECK_PYMODULE(ossie, [], [AC_MSG_ERROR([the python ossie module is required])])\n\
\n\
AC_CONFIG_FILES(Makefile)\n\
\n\
AC_OUTPUT'
