Summary: The PHP scripting language.
Name: php
Version: 4.0.1pl2
Release: 9
Group: Development/Languages
URL: http://www.php.net/
Source0: http://www.php.net/distributions/php-%{version}.tar.gz
Source1: http://www.php.net/distributions/manual.tar.gz
#Icon: php3.gif
Patch1: php-4.0.1pl2-redhat.patch
Patch2: php-4.0.0-extensions.patch
Patch3: php-4.0.1pl2-pear.patch
Copyright: PHP
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: php3
BuildPrereq: apache-devel
ExcludeArch: ia64

%define contentdir /var/www

%description
PHP is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

%package -n mod_php
Summary: The PHP HTML-embedded scripting language for use with Apache.
Group: System Environment/Daemons
URL: http://www.php.net/
Prereq: webserver
Obsoletes: php3, phpfi
BuildPrereq: apache-devel
Requires: php = %{version}

%description -n mod_php
PHP is an HTML-embedded scripting language.  PHP attempts to make it
easy for developers to write dynamically generated web pages.  PHP
also offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple.  The most common
use of PHP coding is probably as a replacement for CGI scripts.  The
mod_php module enables the Apache web server to understand and process
the embedded PHP language in web pages.

This package contains PHP version 4.0.  You'll also need to install the
Apache web server.

%if 0
%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions.

%description devel
The php-devel package contains the files needed when building PHP
extensions.  If you need to compile your own PHP extensions, you will
need to install this package.
%endif

%package imap
Group: Development/Languages
Prereq: php = %{version}, perl
Requires: krb5-libs, pam
Obsoletes: mod_php3-imap
Summary: A module for PHP applications that use IMAP.
BuildPrereq: imap-devel, krb5-devel

%description imap
The php-imap package contains a dynamic shared object that will add IMAP
(Internet Message Access Protocol) support to PHP. IMAP is a protocol
for retrieving, uploading, and manipulating e-mail messages on mail servers.
PHP is an HTML-embeddable scripting language.  If you need IMAP support
for PHP applications, you will need to install this package and the php or
mod_php package.

%package ldap
Group: Development/Languages
Prereq: php = %{version}, perl
Obsoletes: mod_php3-ldap
Summary: A module for PHP applications that use LDAP.
BuildPrereq: openldap-devel
Requires: openldap

%description ldap
The php-ldap package contains a dynamic shared object that will add LDAP
(Lightweight Directory Access Protocol) support to PHP. LDAP is a set
of protocols for accessing directory services over the Internet.
PHP is an HTML-embeddable scripting language.  If you need LDAP support
for PHP applications, you will need to install this package and the php or
mod_php package.

%package manual
Obsoletes: mod_php3-manual
Group: Documentation
Summary: The PHP manual, in HTML format.
Prereq: mod_php = %{version}

%description manual
The php-manual package provides comprehensive documentation for the
PHP HTML-embedded scripting language, in HTML format.

%package mysql
Group: Development/Languages
Prereq: php = %{version}, perl
Summary: A module for PHP applications that use MySQL databases.
Provides: php_database
Obsoletes: mod_php3-mysql
BuildPrereq: mysql-devel
Requires: mysql

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP.  MySQL is an object-relational database
management system.  PHP is an HTML-embeddable scripting language.  If
you need MySQL support for PHP applications, you will need to install
this package and the php or mod_php package.

%package pgsql
Group: Development/Languages
Prereq: php = %{version}, perl
Summary: A module for PHP applications that use PostgreSQL databases.
Provides: php_database
Obsoletes: mod_php3-pgsql
BuildPrereq: postgresql-devel
Requires: postgresql

%description pgsql
The php-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to PHP.  PostgreSQL is an object-relational
database management system that supports almost all SQL constructs.
PHP is an HTML-embeddable scripting language.  If you need PostgreSQL
support for PHP applications, you will need to install this package and
the php or mod_php package.

%prep
%setup -q
%patch1 -p1 -b .redhat
%patch2 -p1 -b .extensions
%patch3 -p1 -b .pear

mkdir manual
gzip -dc %{SOURCE1} | tar -xf - -C manual

cp Zend/LICENSE Zend/ZEND_LICENSE

# Set things up for IMAP.  The library's named c-cliant.a, not libc-client.a,
# otherwise this wouldn't be necessary.
ln -s %{_includedir} ext/imap/
mkdir ext/imap/lib
cp -fv %{_libdir}/c-client.a ext/imap/lib/libc-client.a

autoconf

%build
%{!?nokerberos:krb5libs="-L/usr/kerberos/lib -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err"}

CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS

compile() {
./configure \
	--target=%{_target_platform} \
	--prefix=%{_prefix} \
	--with-config-file-path=%{_sysconfdir} \
	--disable-debug \
	--enable-pic \
	--enable-inline-optimization \
	$* \
	--with-exec-dir=%{_bindir} \
	--with-regex=system \
	--with-gettext \
	--with-gd \
	--with-jpeg-dir=%{_prefix} \
	--with-png \
	--with-zlib \
	--with-db2 \
	--with-db3 \
	--with-gdbm \
	--enable-debugger \
	--enable-magic-quotes \
	--enable-safe-mode \
	--enable-sysvsem \
	--enable-sysvshm \
	--enable-track-vars \
	--enable-yp \
	--enable-ftp \
	--without-mysql \
	--with-xml
make
}

# Build a standalone binary.
compile --enable-force-cgi-redirect
cp php php_standalone
make distclean

# Build a module.
compile --with-apxs=%{_sbindir}/apxs --disable-static

# Build PHP modules.
build_ext() {
%{__cc} -fPIC -shared $RPM_OPT_FLAGS -DHAVE_CONFIG_H \
	-DCOMPILE_DL_`echo $1 | tr '[a-z]' '[A-Z]'` \
	-DHAVE_`echo $1 | tr '[a-z]' '[A-Z]'` \
	-I. -I./main -I`%{_sbindir}/apxs -q INCLUDEDIR` -I./Zend \
	-I/usr/include/freetype -I/usr/include/$1 \
	-I./ext/$1 -I./ext/$1/lib$1 \
	-I./ext/xml/expat/xmltok -I./ext/xml/expat/xmlparse \
	`grep ^CPPFLAGS Zend/Makefile | cut -f2- -d=` \
	$4 $2 -o $1.so -L.libs $3 -lc
}
build_ext imap ext/imap/php_imap.c "%{_libdir}/c-client.a $krb5libs -lpam -ldl"
build_ext ldap ext/ldap/ldap.c "-lldap -llber"
build_ext pgsql ext/pgsql/pgsql.c "-lpq" -DHAVE_PQCMDTUPLES
build_ext mysql ext/mysql/php_mysql.c "-L/usr/lib/mysql -lmysqlclient" "-DHAVE_MYSQL_MYSQL_H -DHAVE_MYSQL_REAL_CONNECT"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/{apache,php4}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd
mkdir -p $RPM_BUILD_ROOT%{contentdir}/icons
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 php_standalone $RPM_BUILD_ROOT%{_bindir}/php
install -m 755 .libs/libphp4.so $RPM_BUILD_ROOT%{_libdir}/apache/
strip -g $RPM_BUILD_ROOT%{_libdir}/apache/*
install -m 755 pgsql.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 imap.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 ldap.so $RPM_BUILD_ROOT%{_libdir}/php4/
install -m 755 mysql.so $RPM_BUILD_ROOT%{_libdir}/php4/
strip -g $RPM_BUILD_ROOT%{_libdir}/php4/*
install -m 644 php.ini-dist $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 644 *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# manual
mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4
cp manual/*.html $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4
ln -s manual.html $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/index.html

# pear and development files
%{makeinstall} -C pear peardir=$RPM_BUILD_ROOT%{_datadir}/php
for file in php-config phpextdist phpize ; do
	perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_bindir}/${file}
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%triggerpostun -- php <= 3.0.15-1
perl -pi -e 's|^#LoadModule php3_module|LoadModule php3_module|g' \
	/etc/httpd/conf/httpd.conf
perl -pi -e 's|^#AddModule mod_php3.c|AddModule mod_php3.c|g' \
	/etc/httpd/conf/httpd.conf

%files -n mod_php
%defattr(-,root,root)
%{contentdir}/icons/*
%{_libdir}/apache/libphp4.so

%files
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS FUNCTION_LIST.txt INSTALL LICENSE MAINTAINERS
%doc MODULES_STATUS NEWS README.* Zend/ZEND_*
%config %{_sysconfdir}/php.ini
%{_bindir}/php
%{_datadir}/php


%files pgsql
%defattr(-,root,root)
%{_libdir}/php4/pgsql.so

%if 0
%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_bindir}/phpextdist
%{_includedir}/php
%{_libdir}/php4/build
%endif

%post pgsql
%{__perl} -pi -e "s|^;extension=pgsql.so|extension=pgsql.so|" %{_sysconfdir}/php.ini

%preun pgsql
if [ $1 = 0 ] ; then
  %{__perl} -pi -e "s|^extension=pgsql.so|;extension=pgsql.so|" %{_sysconfdir}/php.ini
fi

%files mysql
%defattr(-,root,root)
%{_libdir}/php4/mysql.so

%post mysql
%{__perl} -pi -e "s|^;extension=mysql.so|extension=mysql.so|" %{_sysconfdir}/php.ini

%preun mysql
if [ $1 = 0 ] ; then
  %{__perl} -pi -e "s|^extension=mysql.so|;extension=mysql.so|" %{_sysconfdir}/php.ini
fi

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
%{contentdir}/html/manual/mod/mod_php4

%changelog
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
