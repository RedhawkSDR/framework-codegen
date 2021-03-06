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
#% set outputdir = generator.getOutputDir()
#% set componentdir = component.name.replace('.','/')
#% set executable = component.impl.entrypoint|relpath(outputdir)
#% set target = automake.canonicalName(executable)
#{% block license %}
#{# Allow child templates to include license #}
#{% endblock %}
#{% block binInfo %}
ossieName = {{component.name}}
bindir = $(prefix)/{{component.sdrpath}}/{{componentdir}}/{{outputdir}}/
bin_PROGRAMS = {{executable}}
#{% endblock %}

#{% block xmlInfo %}
xmldir = $(prefix)/{{component.sdrpath}}/{{componentdir}}/
dist_xml_DATA = {{component.profile.values()|relpath(outputdir)|join(' ')}}
#{% endblock %}
ACLOCAL_AMFLAGS = -I m4 -I${OSSIEHOME}/share/aclocal/ossie
AUTOMAKE_OPTIONS = subdir-objects


#{% if component.mFunction != None %}
mdir = $(prefix)/{{component.sdrpath}}/{{componentdir}}/{{outputdir}}/
dist_m_DATA = *.m
#{% endif %}

#{% block distClean %}
distclean-local:
	rm -rf m4
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
#{% endblock %}

#{% block extensions %}
#{# Allow child templates to add extensions #}
#{% endblock %}

#{% block compileFlags %}
# Sources, libraries and library directories are auto-included from a file
# generated by the REDHAWK IDE. You can remove/modify the following lines if
# you wish to manually control these options.
include $(srcdir)/Makefile.am.ide
{{target}}_SOURCES = $(redhawk_SOURCES_auto)
{{target}}_LDADD = $(SOFTPKG_LIBS) $(PROJECTDEPS_LIBS) $(BOOST_LDFLAGS) $(BOOST_THREAD_LIB) $(BOOST_REGEX_LIB) $(BOOST_SYSTEM_LIB) $(INTERFACEDEPS_LIBS) $(redhawk_LDADD_auto)
{{target}}_CXXFLAGS = -Wall $(SOFTPKG_CFLAGS) $(PROJECTDEPS_CFLAGS) $(BOOST_CPPFLAGS) $(INTERFACEDEPS_CFLAGS) $(redhawk_INCLUDES_auto)
{{target}}_LDFLAGS = -Wall $(redhawk_LDFLAGS_auto)
#{% if component.mFunction %}
{{target}}_CXXFLAGS += $(M_FUNCTION_INTERPRETER_INCLUDE)
{{target}}_LDFLAGS += $(M_FUNCTION_INTERPRETER_LOAD)
#{% endif %}
#{% endblock %}
