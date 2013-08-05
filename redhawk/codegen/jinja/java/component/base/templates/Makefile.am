#% set target = automake.canonicalName(component.jarfile)
#% set classpath = ['CFInterfaces.jar', 'log4j-1.2.15.jar', 'ossie.jar'] + component.interfacejars
{{component.jarfile}}: $({{target}}_SOURCES)
	mkdir -p bin
	$(JAVAC) -cp {{classpath|prepend('$(OSSIE_HOME)/lib/')|join(':')}} -d bin $({{target}}_SOURCES)
	$(JAR) cf ./{{component.jarfile}} -C bin .

clean-local:
	rm -rf bin

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

#{% set outputdir = generator.getOutputDir() %}
ossieName = {{component.name}}
bindir = $(prefix)/{{component.sdrpath}}/{{component.name}}/{{outputdir}}/
bin_PROGRAMS = {{component.jarfile}}
{{target}}_SOURCES := $(shell find ./src -name "*.java")

xmldir = $(prefix)/{{component.sdrpath}}/{{component.name}}/
dist_xml_DATA = {{component.profile.values()|relpath(outputdir)|join(' ')}}

#{% set sdrbranch = component.sdrpath.split('/')[0] %}
{{sdrbranch}}dir = $(prefix)/{{component.sdrpath}}/{{component.name}}/{{outputdir}}/
dist_{{sdrbranch}}_SCRIPTS = {{component.impl.entrypoint|relpath(outputdir)}}
