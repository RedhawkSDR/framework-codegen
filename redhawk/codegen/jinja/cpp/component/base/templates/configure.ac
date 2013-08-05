AC_INIT({{component.name}}, {{component.version}})
AM_INIT_AUTOMAKE(nostdinc)

AC_PROG_CC
AC_PROG_CXX
AC_PROG_INSTALL

AC_CORBA_ORB
OSSIE_CHECK_OSSIE
OSSIE_SDRROOT_AS_PREFIX

# Dependencies
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig"
PKG_CHECK_MODULES([PROJECTDEPS], [ossie >= 1.9 omniORB4 >= 4.1.0])
#{% if component.interfacedeps %}
PKG_CHECK_MODULES([INTERFACEDEPS], [{{component.interfacedeps|join(', ')}}])
#{% endif %}
OSSIE_ENABLE_LOG4CXX
AX_BOOST_BASE([1.41])
AX_BOOST_THREAD
#{% block dependencies %}
#{% endblock %}

AC_CONFIG_FILES([
#%- filter trim|lines|join(' \\\n')|indent(17)
Makefile
#%- block files
#% endblock
#% endfilter
])
AC_OUTPUT
