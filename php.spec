%define contentdir /var/www
%define manual_langs en
# pt_BR cs nl fr de hu it ja kr es

%{!?oracle:%define oracle 0}

Summary: The PHP HTML-embedded scripting language.
Name: php
Version: 4.0.6
Release: 9
Group: Development/Languages
URL: http://www.php.net/
Source0: http://www.php.net/distributions/php-%{version}.tar.gz
# Manuals from http://www.php.net/distributions/manual/
Source1: php-manual-en.tar.gz
#Source2: php-manual-pt_BR.tar.gz
#Source3: php-manual-cs.tar.gz
#Source4: php-manual-nl.tar.gz
#Source5: php-manual-fr.tar.gz
#Source6: php-manual-de.tar.gz
#Source7: php-manual-hu.tar.gz
#Source8: php-manual-it.tar.gz
#Source9: php-manual-ja.tar.gz
#Source10: php-manual-kr.tar.gz
#Source11: php-manual-es.tar.gz
Source12: php-get-manuals
#Icon: php3.gif
Patch0: php-4.0.6-redhat.patch
Patch1: php-4.0.3-required.patch
Patch2: php-4.0.4pl1-linkage.patch
Patch3: php-4.0.6-libtool.patch
Patch4: php-4.0.5-db.patch
Patch5: php-4.0.5-ext.patch
Patch6: php-4.0.6-ZVAL.patch
License: PHP
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: mod_php, php3, phpfi
BuildPrereq: apache-devel, db2-devel, db3-devel, gdbm-devel, imap-devel >= 2000-9
BuildPrereq: krb5-devel, mysql-devel, openssl-devel, postgresql-devel, pam-devel
BuildPrereq: freetype-devel, gd-devel, libjpeg-devel, libpng-devel, zlib-devel
BuildPrereq: unixODBC-devel, libxml2-devel, pspell-devel, curl-devel >= 7.8
BuildPrereq: bzip2-devel >= 1.0.0, mm-devel

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. The
mod_php module enables the Apache Web server to understand and process
the embedded PHP language in Web pages.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions.

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Requires: krb5-libs, pam
Obsoletes: mod_php3-imap
Summary: An Apache module for PHP applications that use IMAP.
BuildPrereq: imap-devel, krb5-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Obsoletes: mod_php3-ldap
Summary: A module for PHP applications that use LDAP.
BuildPrereq: openldap-devel
Requires: openldap

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package manual
Obsoletes: mod_php3-manual
Group: Documentation
Summary: The PHP manual, in HTML format.
Prereq: php = %{version}-%{release}

%description manual
The php-manual package provides comprehensive documentation for the
PHP HTML-embedded scripting language, in HTML format. PHP is an
HTML-embedded scripting language.

%package mysql
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Summary: A module for PHP applications that use MySQL databases.
Provides: php_database
Obsoletes: mod_php3-mysql
BuildPrereq: mysql-devel
Requires: mysql

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php or mod_php package.

%package pgsql
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Summary: A PostgreSQL database module for PHP.
Provides: php_database
Obsoletes: mod_php3-pgsql
BuildPrereq: postgresql-devel
Requires: postgresql

%description pgsql
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package odbc
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Summary: A module for PHP applications that use ODBC databases.
Provides: php_database
BuildPrereq: unixODBC-devel
Requires: unixODBC

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%if %{oracle}
%package oci8
%description oci8
%endif
%prep
%setup -q -c
pushd %{name}-%{version}
%patch0 -p1 -b .redhat
%patch1 -p1 -b .required
%patch2 -p1 -b .linkage
%patch3 -p1 -b .libtool
%patch4 -p1 -b .db
%patch5 -p1 -b .ext
%patch6 -p1 -b .ZVAL

cp Zend/LICENSE Zend/ZEND_LICENSE

# Set things up for IMAP.  The library's named c-client.a, not libc-client.a,
# otherwise this mightn't be necessary.
ln -s %{_includedir} ext/imap/
mkdir ext/imap/lib
cp -fv %{_libdir}/c-client.a ext/imap/lib/libc-client.a

# Rebuild configure and friends.
./buildconf

popd

# Create another source tree like this one.
cp -a %{name}-%{version} %{name}-%{version}-cgi

%build
krb5libs="-L/usr/kerberos/lib -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err"
ssllibs="-lssl -lcrypto"
sasllibs="-lsasl $krb5libs $ssllibs"

CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
LIBS="-lttf -lfreetype -lpng -ljpeg -lz -lnsl"; export LIBS
REDO_ALL=yes; export REDO_ALL
EXTENSION_DIR=%{_libdir}/php4; export EXTENSION_DIR

compile() {
%configure \
	--prefix=%{_prefix} \
	--with-config-file-path=%{_sysconfdir} \
	--disable-debug \
	--enable-pic \
	--disable-rpath \
	--enable-inline-optimization \
	$* \
	--with-bz2 \
	--with-curl \
	--with-db3 \
	--with-dom \
	--with-exec-dir=%{_bindir} \
	--with-gd \
	--with-gdbm \
	--with-gettext \
	--with-jpeg-dir=%{_prefix} \
	--with-mm \
	--with-openssl \
	--with-png \
	--with-regex=system \
	--with-ttf \
	--with-zlib \
	--with-layout=GNU \
	--enable-debugger \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-safe-mode \
	--enable-sockets \
	--enable-sysvsem \
	--enable-sysvshm \
	--enable-track-vars \
	--enable-yp \
	--enable-wddx \
	--without-mysql \
	--without-unixODBC \
	--without-oracle \
	--without-oci8 \
	--with-pspell \
	--with-xml
make
}

# Build a standalone binary.
pushd %{name}-%{version}-cgi
compile --enable-force-cgi-redirect
popd

# Build a module.
pushd %{name}-%{version}
compile --with-apxs=%{_sbindir}/apxs

# Build individual PHP modules.
build_ext() {
./libtool --mode=link \
%{__cc} -fPIC -shared $RPM_OPT_FLAGS \
	-DCOMPILE_DL_`echo $1 | tr '[a-z]' '[A-Z]'` \
	-DHAVE_`echo $1 | tr '[a-z]' '[A-Z]'` \
	-I. -I./TSRM -I./main -I`%{_sbindir}/apxs -q INCLUDEDIR` -I./Zend \
	-I/usr/include/freetype -I/usr/include/$1 \
	-I./ext/$1 -I./ext/$1/lib$1 \
	-I./ext/xml/expat/xmltok -I./ext/xml/expat/xmlparse \
	`grep ^CPPFLAGS Zend/Makefile | cut -f2- -d=` \
	$4 $2 -o $1.so -L.libs $3 -lc
}
build_ext imap ext/imap/php_imap.c "%{_libdir}/c-client.a $krb5libs $ssllibs -lpam" "-DHAVE_IMAP2000 -DHAVE_IMAP_SSL"
build_ext ldap ext/ldap/ldap.c "-lldap -llber"
build_ext pgsql ext/pgsql/pgsql.c "-lpq" -DHAVE_PQCMDTUPLES
build_ext mysql ext/mysql/php_mysql.c "-L/usr/lib/mysql -lmysqlclient" "-DHAVE_MYSQL_MYSQL_H -DHAVE_MYSQL_REAL_CONNECT"
build_ext odbc ext/odbc/php_odbc.c "-lodbc" "-DHAVE_UNIXODBC -DHAVE_UODBC"
%if %{oracle}
build_ext oci8 ext/oci8/oci8.c "-I${ORACLE_HOME}/rdbms/public -I${ORACLE_HOME}/rdbms/demo -L${ORACLE_HOME}/lib -lclntsh"
%endif

popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
pushd %{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/{apache,php4}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd
mkdir -p $RPM_BUILD_ROOT%{contentdir}/icons

./libtool install -m755 libphp4.la $RPM_BUILD_ROOT%{_libdir}/apache/

pushd ../%{name}-%{version}-cgi
./libtool install -m755 php $RPM_BUILD_ROOT%{_bindir}/php
popd

install -m 755 pgsql.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 imap.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 ldap.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 mysql.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 odbc.so $RPM_BUILD_ROOT%{_libdir}/php4/
%if %{oracle}
install -m 755 oci8.so $RPM_BUILD_ROOT%{_libdir}/php4/
%endif
install -m 644 php.ini-dist $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 644 *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# manual
for lang in %{manual_langs} ; do
if test x${lang} = xen ; then
	# put english where the old single manual package used to be
	mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/
	gzip -dc $RPM_SOURCE_DIR/php-manual-${lang}.tar.gz | tar -x -C $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/ -f -
elif test x${lang} = xkr ; then
	# put english where the old single manual package used to be
	mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/ko/
	gzip -dc $RPM_SOURCE_DIR/php-manual-${lang}.tar.gz | tar -x -C $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/ko/ -f -
else
	mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/${lang}/
	gzip -dc $RPM_SOURCE_DIR/php-manual-${lang}.tar.gz | tar -x -C $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/${lang} -f -
fi
done

# pear and development files
%{makeinstall} -C pear peardir=$RPM_BUILD_ROOT%{_datadir}/php
for file in php-config phpextdist phpize ; do
	perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_bindir}/${file}
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%triggerpostun -- php < 4.0.0
perl -pi -e 's|^#LoadModule php3_module|LoadModule php3_module|g' \
	/etc/httpd/conf/httpd.conf
perl -pi -e 's|^#AddModule mod_php3.c|AddModule mod_php3.c|g' \
	/etc/httpd/conf/httpd.conf

%files
%defattr(-,root,root)
%doc %{name}-%{version}/{CODING_STANDARDS,CREDITS,EXTENSIONS,INSTALL}
%doc %{name}-%{version}/{LICENSE,NEWS,README.*,Zend/ZEND_*}
%config(noreplace) %{_sysconfdir}/php.ini
%{_bindir}/php
%{_datadir}/php
%{_libdir}/apache/libphp4.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%{_bindir}/pear
%{_bindir}/php-config
%{_bindir}/phpize
%{_bindir}/phpextdist
%{_includedir}/php
%{_libdir}/php/build

%files pgsql
%defattr(-,root,root)
%{_libdir}/php4/pgsql.so

%post pgsql
%{__perl} -pi -e "s|^;extension=pgsql.so|extension=pgsql.so|" %{_sysconfdir}/php.ini

%preun pgsql
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=pgsql.so|;extension=pgsql.so|" %{_sysconfdir}/php.ini
fi

%files mysql
%defattr(-,root,root)
%{_libdir}/php4/mysql.so

%post mysql
%{__perl} -pi -e "s|^;extension=mysql.so|extension=mysql.so|" %{_sysconfdir}/php.ini

%preun mysql
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=mysql.so|;extension=mysql.so|" %{_sysconfdir}/php.ini
fi

%files odbc
%defattr(-,root,root)
%{_libdir}/php4/odbc.so

%post odbc
%{__perl} -pi -e "s|^;extension=odbc.so|extension=odbc.so|" %{_sysconfdir}/php.ini

%preun odbc
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=odbc.so|;extension=odbc.so|" %{_sysconfdir}/php.ini
fi

%if %{oracle}
%files oci8
%defattr(-,root,root)
%{_libdir}/php4/oci8.so

%post oci8
%{__perl} -pi -e "s|^;extension=oci8.so|extension=oci8.so|" %{_sysconfdir}/php.ini

%preun oci8
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=oci8.so|;extension=oci8.so|" %{_sysconfdir}/php.ini
fi
%endif

%files imap
%defattr(-,root,root)
%{_libdir}/php4/imap.so

%post imap
%{__perl} -pi -e "s|^;extension=imap.so|extension=imap.so|" %{_sysconfdir}/php.ini

%preun imap
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=imap.so|;extension=imap.so|" %{_sysconfdir}/php.ini
fi

%files ldap
%defattr(-,root,root)
%{_libdir}/php4/ldap.so

%post ldap
%{__perl} -pi -e "s|^;extension=ldap.so|extension=ldap.so|" %{_sysconfdir}/php.ini

%preun ldap
if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
  %{__perl} -pi -e "s|^extension=ldap.so|;extension=ldap.so|" %{_sysconfdir}/php.ini
fi

%files manual
%defattr(-,root,root)
%{contentdir}/icons/*
%dir %{contentdir}/html/manual/mod/mod_php4/
%{contentdir}/html/manual/mod/mod_php4/*.html
#%lang(cs) %{contentdir}/html/manual/mod/mod_php4/cs
#%lang(de) %{contentdir}/html/manual/mod/mod_php4/de
#%lang(es) %{contentdir}/html/manual/mod/mod_php4/es
#%lang(fr) %{contentdir}/html/manual/mod/mod_php4/fr
#%lang(hu) %{contentdir}/html/manual/mod/mod_php4/hu
#%lang(it) %{contentdir}/html/manual/mod/mod_php4/it
#%lang(ja) %{contentdir}/html/manual/mod/mod_php4/ja
#%lang(ko) %{contentdir}/html/manual/mod/mod_php4/ko
#%lang(nl) %{contentdir}/html/manual/mod/mod_php4/nl
#%lang(pt) %{contentdir}/html/manual/mod/mod_php4/pt_BR

%changelog
* Mon Sep 17 2001 Tim Powers <timp@redhat.com>
- rebuilt against newer posgresql libs

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Mon Aug 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch from pzb at scyld.com to fix the ZVAL_TRUE and ZVAL_FALSE macros
  (#52501)

* Fri Aug 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable bzip2 extension
- enable curl extension
- enable use of mm
- clean up use of libtool (#51958)

* Fri Aug 10 2001 Tim Powers <timp@redhat.com>
- only english in php-manuals, space constraints

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- include %{_libdir}/%{name}/build instead of %{_libdir}/%{name}4/build (#51141)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add build deps on pam-devel, pspell-devel, gdbm-devel (#49878)
- add some conditional logic if %%{oracle} is defined (from Antony Nguyen)

* Mon Jul  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't obsolete subpackages we ended up not merging

* Mon Jul  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- cleanups
- add manuals in multiple languages (using ko instead of kr for Korean)
- merge all of the manuals into a single -manual subpackage
- use libtool to install binary files which libtool builds
- don't strip any binaries; let the buildroot policies take care of it

* Thu Jun 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.6 (preliminary)

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable ttf in the build because the gd support needs it
- add -lfreetype to the LIBS for the same reason

* Wed Jun  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Wed May 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually use two source trees to build things
- add %%post and %%postun scriptlets to run ldconfig

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- quote part of the AC_ADD_LIBRARY macro to make newer autoconf happy

* Mon May 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix error in %%install
- depend on the imap-devel which supplies linkage.c
- modify trigger to disable php versions less than 4.0.0 instead of 3.0.15
- enable DOM support via libxml2 (suggested by Sylvain Bergé)
- build the OpenSSL extension again

* Mon May  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable pspell extensions
- update to 4.0.5

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- build the ODBC extension

* Mon Apr 30 2001 Bill Nottingham <notting@redhat.com>
- build on ia64

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Feb 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- obsolete the old phpfi (PHP 2.x) package

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a commented-out curl extension to the config file (part of #24933)
- fix the PEAR-installation-directory-not-being-eval'ed problem (#24938)
- find the right starting point for multipart form data (#24933)

* Tue Jan 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- aaarrgh, the fix breaks something else, aaarrgh; revert it (#24933)
- terminate variable names at the right place (#24933)

* Sat Jan 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the fix some more

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- extract stas's fix for quoting problems from CVS for testing
- tweak the fix, ask the PHP folks about the tweak
- tweak the fix some more

* Wed Jan 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge mod_php into the main php package (#22906)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- try to fix a quoting problem

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.4 to get a raft of bug fixes
- enable sockets
- enable wddx

* Fri Nov  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in updated environment

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- add more commented-out modules to the default config file (#19276)

* Wed Nov  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix not-using-gd problem (#20137)

* Tue Oct 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.3pl1 to get some bug fixes

* Sat Oct 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- build for errata

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.3 to get security fixes integrated
- patch around problems configuring without Oracle support
- add TSRM to include path when building individual modules

* Fri Sep  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment
- enable OpenSSL support

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.2, and move the peardir settings to configure (#17171)
- require %%{version}-%%{release} for subpackages
- add db2-devel and db3-devel prereqs (#17168)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (new imap-devel)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summary and descriptions to match the specspo package

* Wed Aug  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- hard-code the path to apxs in build_ext() (#15799)

* Tue Aug  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add "." to the include path again, which is the default

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable PEAR and add it to the include path
- add the beginnings of a -devel subpackage

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweaks to post and postun from Bill Peck

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- fixes from Nils for building the MySQL client
- change back to requiring %{version} instead of %{version}-%{release}

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.1pl2
- enable MySQL client
- move the php.ini file to %{_sysconfdir}

* Fri Jun 30 2000 Nils Philippsen <nils@redhat.de>
- build_ext defines HAVE_PGSQL so pgsql.so in fact contains symbols
- post/un scripts tweak php.ini correctly now

* Thu Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.1
- refresh manual

* Tue Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new krb5 package

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new db3 package

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix syntax error in post and preun scripts.
- Disable IMAP, LDAP, PgSql in the standalone version because it picks up
  the extensions.

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- Unexclude the Sparc arch.
- Exclude the ia64 arch until we get a working Postgres build.
- Stop stripping extensions as aggressively.
- Start linking the IMAP module to libpam again.
- Work around extension loading problems.
- Reintroduce file-editing post and preun scripts for the mod_php extensions
  until we come up with a better way to do it.

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- ExcludeArch: sparc for now

* Sun Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Obsoletes: phpfi, because their content handler names are the same
- add standalone binary, rename module packages to mod_php
- FHS fixes

* Tue May 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- change license from "GPL" to "PHP"
- add URL: tag
- disable mysql support by default (license not specified)

* Mon May 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to PHP 4.0.0
- nuke the -mysql subpackage (php comes with a bundled mysql client lib now)

* Tue May 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- link IMAP module against GSS-API and PAM to get dependencies right
- change most of the Requires to Prereqs, because the post edits config files
- move the PHP *Apache* module back to the right directory
- fix broken postun trigger that broke the post
- change most of the postuns to preuns in case php gets removed before subpkgs

* Thu May 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuilt against new postgres libraries

* Tue May 09 2000 Preston Brown <pbrown@redhat.com>
- php3 .so modules moved to /usr/lib/php3 from /usr/lib/apache (was incorrect)

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- make subpackages require php = %{version} (bug #10671)

* Thu Apr 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0.16

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- fixed the post script to work when upgrading a package
- add triggere to fix the older packages

* Tue Feb 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0.15
- add build-time dependency for openldap-devel
- enable db,ftp,shm,sem support to fix bug #9648

* Fri Feb 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- add dependency for imap subpackage
- rebuild against Apache 1.3.12

* Thu Feb 24 2000 Preston Brown <pbrown@redhat.com>
- don't include old, outdated manual.  package one from the php distribution.

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependency problem

* Fri Jan 14 2000 Preston Brown <pbrown@redhat.com>
- added commented out mysql module, thanks to Jason Duerstock 
  (jason@sdi.cluephone.com). Uncomment to build if you have mysql installed.

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- rely on imap-devel, don't include imap in src.rpm (#5099).
- xml enabled (#5393)

* Tue Nov 02 1999 Preston Brown <pborwn@redhat.com>
- added post/postun sections to modify httpd.conf (#5259)
- removed old obsolete faq and gif (#5260)
- updated manual.tar.gz package (#5261)

* Thu Oct 07 1999 Matt Wilson <msw@redhat.com>
- rebuilt for sparc glibc brokenness

* Fri Sep 24 1999 Preston Brown <pbrown@redhat.com>
- --with-apxs --> --with-apxs=/usr/sbin/apxs (# 5094)
- ldap support (# 5097)

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- fix cmdtuples for postgresql, I had it slightly wrong

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- subpackages must obsolete old stuff...

* Sun Aug 29 1999 Preston Brown <pbrown@redhat.com>
- added -DHAVE_PGCMDTUPLES for postgresql module (bug # 4767)

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- name change to php to follow real name of package
- fix up references to php3 to refer to php
- upgrade to 3.0.12
- fixed typo in pgsql postun script (bug # 4686)

* Mon Jun 14 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.9
- fixed postgresql module and made separate package
- separated manual into separate documentation package

* Mon May 24 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.8, which fixes problems with glibc 2.1.
- took some ideas grom Gomez's RPM.

* Tue May 04 1999 Preston Brown <pbrown@redhat.com>
- hacked in imap support in an ugly way until imap gets an official
  shared library implementation

* Fri Apr 16 1999 Preston Brown <pbrown@redhat.com>
- pick up php3.ini

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- build against apache 1.3.6

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.7.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to php 3.0.6, built against apache 1.3.4

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- rebuild for apache 1.3.3

* Thu Oct 08 1998 Preston Brown <pbrown@redhat.com>
- updated to 3.0.5, fixes nasty bugs in 3.0.4.

* Sun Sep 27 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.0.4 and recompiled for apache 1.3.2

* Thu Sep 03 1998 Preston Brown <pbrown@redhat.com>
- improvements; builds with apache-devel package installed.

* Tue Sep 01 1998 Preston Brown <pbrown@redhat.com>
- Made initial cut for PHP3.
