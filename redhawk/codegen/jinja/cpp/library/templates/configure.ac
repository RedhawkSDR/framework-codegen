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
AC_INIT({{component.name}}, {{component.version}})
AM_INIT_AUTOMAKE(nostdinc)

AC_PROG_CC
AC_PROG_CXX
AC_PROG_INSTALL
AC_PROG_LIBTOOL

AC_CORBA_ORB
OSSIE_CHECK_OSSIE
# TODO: Make this an installed macro
OSSIE_SDRROOT_AS_PREFIX
prefix="${prefix}dom/deps/{{component.name}}"
# Overrule "lib64" suffix
libdir='${prefix}/lib'

m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

# Dependencies
PKG_CHECK_MODULES([REDHAWK], [ossie >= {{versions.redhawk}}])
OSSIE_ENABLE_LOG4CXX
AX_BOOST_BASE([{{versions.boost}}])
AX_BOOST_SYSTEM
AX_BOOST_THREAD
AX_BOOST_REGEX

AC_CONFIG_FILES([Makefile {{component.pcfile}}])
AC_OUTPUT
