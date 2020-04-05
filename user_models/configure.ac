dnl -*-m4-*-
dnl Process this file with autoconf to produce a configure script.
dnl --------------------------------------------------------------
dnl configure.in for Worldsens network simulator
dnl --------------------------------------------------------------
AC_INIT([wsnet],[0.7cvs])
AC_CANONICAL_TARGET
AM_INIT_AUTOMAKE
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

dnl --------------------------------------------------------------
dnl WSNet directory
dnl --------------------------------------------------------------
AC_PREFIX_DEFAULT(/usr/local/wsnet-2.0)
AC_ARG_VAR(WSNET_DIR, [WSNet distribution directory])
AC_ARG_WITH([wsnet-dir],
	    AS_HELP_STRING([--with-wsnet-dir=DIR],[WSNet distribution directory (default is "/usr/local/wsnet-2.0")]),
	    [WSNET_DIR=$withval],[WSNET_DIR="/usr/local/wsnet-2.0"])
CFLAGS="-I${WSNET_DIR} $CFLAGS"

AC_ARG_ENABLE([debug], AS_HELP_STRING([--enable-debug],[Set debug compilation options]), CFLAGS="-g -pg $CFLAGS",CFLAGS="-O2 $CFLAGS")


dnl --------------------------------------------------------------
dnl Checks for programs.
dnl --------------------------------------------------------------
AC_PROG_INSTALL
AC_LIBTOOL_DLOPEN
AC_PROG_LIBTOOL
AC_PROG_CC
AM_PROG_CC_C_O

dnl --------------------------------------------------------------
dnl Checks for pkg-config path.
dnl --------------------------------------------------------------
AC_ARG_VAR(PKG_CONFIG_DIR, [pkg-config directory])
AC_ARG_WITH([pkg-config-dir],
	    AS_HELP_STRING([--with-pkg-config-dir=DIR],[pkg-config directory]),
	    [PKG_CONFIG_DIR=$withval],
	    [PKG_CONFIG_DIR=""])

dnl --------------------------------------------------------------
dnl Checks for pkg-config.
dnl --------------------------------------------------------------
AC_PATH_PROG([PKG_CONFIG], [pkg-config], , [$PATH:$PKG_CONFIG_DIR])
AC_ARG_VAR(GLIB_LIBS, [glib libraries])
AC_ARG_VAR(GLIB_FLAGS, [glib flags])
if test "${GLIB_LIBS}" = ""; then
	[GLIB_LIBS]=`$PKG_CONFIG --libs gmodule-2.0`
	echo $GLIB_LIBS
else
	echo $GLIB_LIBS
fi

if test "${GLIB_FLAGS}" = ""; then
	[GLIB_FLAGS]=`$PKG_CONFIG --cflags gmodule-2.0`
	echo $GLIB_FLAGS
else
	echo $GLIB_FLAGS
fi

dnl --------------------------------------------------------------
dnl Output
dnl --------------------------------------------------------------
AC_CONFIG_FILES(
Makefile
)
AC_OUTPUT
