AC_INIT({{component.name}}, {{component.version}})
AM_INIT_AUTOMAKE(nostdinc)

AC_CORBA_ORB
OSSIE_CHECK_OSSIE
OSSIE_SDRROOT_AS_PREFIX

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig"
PKG_CHECK_MODULES([OSSIE], [ossie >= 1.9])

AC_CHECK_PROG([JAVAC], [javac], [javac], [AC_MSG_ERROR([cannot find Java compiler])])
AC_CHECK_PROG([JAR], [jar], [jar], [AC_MSG_ERROR([cannot find jar program])])
#{% if component.interfacedeps %}

PKG_CHECK_MODULES([INTERFACEDEPS], [{{component.interfacedeps|join(', ')}}])
#{% endif %}

AC_CONFIG_FILES(Makefile)
AC_OUTPUT
