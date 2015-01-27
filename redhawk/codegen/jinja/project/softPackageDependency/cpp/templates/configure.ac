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
OSSIE_SDRROOT_AS_PREFIX

AC_PREFIX_DEFAULT(${SDRROOT})
AC_SUBST([spkg_dir],['${prefix}'/dom/deps/{{component.name}}{{generator.variant}}])
AC_SUBST([spkg_impl],[{{component.impl.id}}])
AC_SUBST([spkg_variant],[{{generator.variant}}])
AC_SUBST([spkg_impldir],['${spkg_dir}/${spkg_impl}'])
AC_SUBST([spkg_libdir],['${spkg_dir}/${spkg_impl}/lib'])
AC_SUBST([spkg_pkgconfig_dir],['${spkg_libdir}/pkgconfig'])
AC_SUBST([spkg_includedir],['${spkg_dir}/${spkg_impl}/include'])

AC_CONFIG_FILES([{{component.name}}${spkg_variant}.pc:package.pc])
AC_CONFIG_FILES([../{{component.name}}${spkg_variant}.spd.xml:../{{component.name}}.spd.xml])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
