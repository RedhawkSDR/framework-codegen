AC_INIT({{component.name}}, {{component.version}})
AM_INIT_AUTOMAKE(nostdinc)

AC_PROG_INSTALL

AC_CORBA_ORB
OSSIE_CHECK_OSSIE
OSSIE_SDRROOT_AS_PREFIX
AM_PATH_PYTHON([2.4])

PKG_CHECK_MODULES([OSSIE], [ossie >= 1.9])
AC_CHECK_PYMODULE(ossie, [], [AC_MSG_ERROR([the python ossie module is required])])
PKG_CHECK_MODULES([OMNIORB], [omniORB4 >= 4.1.0])
AC_CHECK_PYMODULE(omniORB, [], [AC_MSG_ERROR([the python omniORB module is required])])

#{% for interface in component.interfacedeps %}
PKG_CHECK_MODULES({{interface.name}}, {{interface.name}}{{interface.version}}) 
AC_CHECK_PYMODULE({{interface.module}}, [], [AC_MSG_ERROR([the python {{interface.module}} module is required])])
#{% endfor %}

AC_CONFIG_FILES(Makefile)

AC_OUTPUT
