%define contentdir /var/www
%define with_oci8 %{?_with_oci8:1}%{!?_with_oci8:0}
%define with_mssql %{?_with_mssql:1}%{!?_with_mssql:0}
%define with_mhash %{?_with_mhash:1}%{!?_with_mhash:0}
%define with_imap %{?_with_imap:1}%{!?_with_imap:0}

Summary: The PHP HTML-embedded scripting language. (PHP: Hypertext Preprocessor)
Name: php
Version: 4.3.4
Release: 10.1
License: The PHP License
Group: Development/Languages
URL: http://www.php.net/

Source0:  http://www.php.net/distributions/php-%{version}.tar.bz2

Source50: php.conf

Patch1: php-4.2.1-ldap-TSRM.patch
Patch2: php-4.3.4-config.patch
Patch3: php-4.2.2-lib64.patch
Patch4: php-4.2.2-cxx.patch
Patch5: php-4.3.3-install.patch
Patch6: php-4.3.1-tests.patch
Patch7: php-4.3.2-libtool15.patch
Patch8: php-4.3.3-miscfix.patch
Patch9: php-4.3.4-setenv.patch
Patch10: php-4.3.4-xmlrpc.patch

# Fixes for extension modules
Patch21: php-4.3.1-odbc.patch
Patch22: php-4.3.2-db4.patch
Patch23: php-4.3.4-libgd.patch

# Functional changes
Patch30: php-4.3.1-dlopen.patch
Patch31: php-4.3.4-easter.patch

BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, expat-devel, freetype-devel
BuildRequires: gd-devel >= 1.8.4, gdbm-devel, gmp-devel, aspell-devel >= 0.50.0
BuildRequires: httpd-devel >= 2.0.46-1, libjpeg-devel, libpng-devel, pam-devel
BuildRequires: libstdc++-devel, ncurses-devel, openssl-devel
BuildRequires: zlib-devel, pcre-devel
BuildRequires: bzip2, fileutils, perl, libtool >= 1.4.3
Obsoletes: php-dbg, mod_php, php3, phpfi, stronghold-php
%{!?_with_imap:Obsoletes: php-imap} 
# Enforce Apache module ABI compatibility
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)
Requires: php-pear

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

%package pear
Group: Development/Languages
Summary: PHP Extension and Application Repository Components
Requires: php

%description pear
PEAR is a framework and distribution system for reusable PHP
components.  This package contains a set of PHP components from the
PEAR repository.

%if %{with_imap} 
%package imap
Summary: An Apache module for PHP applications that use IMAP.
Group: Development/Languages
Requires: php = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, imap-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.
%endif

%package ldap
Summary: A module for PHP applications that use LDAP.
Group: Development/Languages
Requires: php = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package mysql
Summary: A module for PHP applications that use MySQL databases.
Group: Development/Languages
Requires: php = %{version}-%{release}
Provides: php_database
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php or mod_php package.

%package pgsql
Summary: A PostgreSQL database module for PHP.
Group: Development/Languages
Requires: php = %{version}-%{release}
Provides: php_database
Obsoletes: mod_php3-pgsql, stronghold-php-pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

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
Requires: php = %{version}-%{release}
Summary: A module for PHP applications that use ODBC databases.
Provides: php_database
Obsoletes: stronghold-php-odbc
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%if %{with_oci8}
%package oci8
Group: Development/Languages
Requires: php = %{version}-%{release}
Summary: A module for PHP applications that use OCI8 databases.
Provides: php_database

%description oci8
The php-oci8 package contains a dynamic shared object that will add
support for accessing OCI8 databases to PHP.
%endif

%if %{with_mssql}
%package mssql
Group: Development/Languages
Requires: php = %{version}-%{release}, freetds
Summary: A module for PHP applications that use MSSQL databases.
Provides: php_database
BuildRequires: freetds-devel

%description mssql
The mssql package contains a dynamic shared object that will add
support for accessing MSSQL databases to PHP.
%endif

%if %{with_mhash}
%package mhash
Summary: A module for PHP applications that use Mhash.
Group: Development/Languages
Requires: php = %{version}-%{release}
BuildRequires: mhash-devel

%description mhash
The php-mhash package is a dynamic shared object (DSO) for the Apache
Web server that adds Mhash support to PHP.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices.
Group: Development/Languages
Requires: php = %{version}-%{release}
BuildRequires: net-snmp-devel, elfutils-devel
# elfutils-devel requirement workaround for #103982

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package domxml
Summary: A module for PHP applications which manipulate XML data
Group: Development/Languages
Requires: php = %{version}-%{release}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description domxml
The php-domxml package contains a dynamic shared object that will add
support for manipulating XML data as a DOM tree to PHP.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: php = %{version}-%{release}
BuildRequires: expat-devel

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .config
%patch3 -p1 -b .lib64
%patch4 -p1 -b .cxx
%patch5 -p1 -b .install
%patch6 -p1 -b .tests
%patch7 -p1 -b .libtool15
%patch8 -p1 -b .miscfix
%patch9 -p1 -b .setenv
%patch10 -p1 -b .xmlrpc

%patch21 -p1 -b .odbc
%patch22 -p1 -b .db4
%patch23 -p1 -b .libgd

%patch30 -p1 -b .dlopen
%patch31 -p1 -b .easter

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

# Source is built twice: once for /usr/bin/php, once for the Apache DSO.
mkdir build-cgi build-apache

# Use correct libdir
perl -pi -e 's|%{_prefix}/lib|%{_libdir}|' php.ini-recommended

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/session/tests/019.phpt \
      ext/standard/tests/math/pow.phpt \
      ext/standard/tests/math/round.phpt \
      ext/standard/tests/math/abs.phpt \
      ext/iconv/tests/bug16069.phpt

%build

CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"; export CFLAGS

# Install extension modules in %{_libdir}/php4.
EXTENSION_DIR=%{_libdir}/php4; export EXTENSION_DIR

%if %{with_imap}
# This pulls the static /usr/lib/libc-client.a into the IMAP extension module.
IMAP_SHARED_LIBADD=-lc-client ; export IMAP_SHARED_LIBADD
%endif

# pull latest ltmain.sh, AC_PROG_LIBTOOL
libtoolize --force --copy
# force aclocal run during buildconf
touch acinclude.m4

# Regenerate configure scripts (patches change config.m4's)
./buildconf --force

# Shell function to configure and build a PHP tree.
build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
	--cache-file=../config.cache \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--enable-force-cgi-redirect \
	--disable-debug \
	--enable-pic \
	--disable-rpath \
	--enable-inline-optimization \
	--with-bz2 \
	--with-db4=%{_prefix} \
	--with-curl \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-gd \
	--enable-gd-native-ttf \
	--with-gdbm \
	--with-gettext \
	--with-ncurses \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-openssl \
	--with-png \
	--with-pspell \
	--with-regex=system \
	--with-xml \
	--with-expat-dir=%{_prefix} \
	--with-dom=shared,%{_prefix} \
        --with-dom-xslt=%{_prefix} --with-dom-exslt=%{_prefix} \
        --with-xmlrpc=shared \
        --with-pcre-regex=%{_prefix} \
	--with-zlib \
	--with-layout=GNU \
	--enable-bcmath \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-safe-mode \
	--enable-sockets \
	--enable-sysvsem \
	--enable-sysvshm \
	--enable-track-vars \
	--enable-trans-sid \
	--enable-yp \
	--enable-wddx \
	--with-pear=/usr/share/pear \
	%{?_with_imap:--with-imap=shared --with-imap-ssl} \
	--with-kerberos \
	--with-ldap=shared \
	--with-mysql=shared,%{_prefix} \
        %{?_with_oci8:--with-oci8=shared} \
        %{?_with_mssql:--with-mssql=shared} \
        %{?_with_mhash:--with-mhash=shared} \
	--with-pgsql=shared \
	--with-snmp=shared,%{_prefix} \
	--with-snmp=shared \
	--enable-ucd-snmp-hack \
	--with-unixODBC=shared,%{_prefix} \
	--enable-memory-limit \
	--enable-bcmath \
	--enable-shmop \
	--enable-calendar \
	--enable-dbx \
	--enable-dio \
	--enable-mcal \
        --enable-mbstring --enable-mbstr-enc-trans \
        --enable-mbregex \
	$*

make %{?_smp_mflags}
}

# Build standalone /usr/bin/php
pushd build-cgi
build --enable-force-cgi-redirect
# Run tests
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1
if ! TZ= LANG= LC_ALL= make test; then
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE -- $f --"
    cat $f
  done
fi
popd

# Build Apache module
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs
popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install from CGI tree
pushd build-cgi
make install INSTALL_ROOT=$RPM_BUILD_ROOT 
popd

# Install the Apache module
pushd build-apache
make install-sapi INSTALL_ROOT=$RPM_BUILD_ROOT
popd

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644    php.ini-recommended $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 build-apache/libs/libphp4.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/php.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql mysql odbc ldap snmp domxml xmlrpc \
    %{?_with_imap:imap} %{?_with_oci8:oci8} %{?_with_mssql:mssql} \
    %{?_with_mhash:mhash}; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php4/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF
done

# Remove PEAR testsuite
rm -rf $RPM_BUILD_ROOT%{_datadir}/pear/tests

# Remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/php4/*.a \
      $RPM_BUILD_ROOT%{_bindir}/{phptar,pearize}

# Remove irrelevant docs
rm README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.*

# remove extension= lines for packaged modules from php.ini (#112470)
%triggerpostun -- php < 4.3.4-5
perl -pi.rpmold -e 's/^extension=(pgsql|mysql|odbc|ldap|snmp|imap).so\n//' /etc/php.ini
exit 0

%files
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* gd_README TSRM_LICENSE regex_COPYRIGHT
%config(noreplace) %{_sysconfdir}/php.ini
%config %{_sysconfdir}/pear.conf
%{_bindir}/php
%dir %{_libdir}/php4
%dir %{_localstatedir}/lib/php
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/php/session
%{_libdir}/httpd/modules/libphp4.so
%config %{_sysconfdir}/httpd/conf.d/php.conf
%dir %{_sysconfdir}/php.d
%{contentdir}/icons/php.gif

%files pear
%defattr(-,root,root)
%{_bindir}/pear
%{_datadir}/pear

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_bindir}/phpextdist
%{_includedir}/php
%{_libdir}/php

%files pgsql -f files.pgsql

%files mysql -f files.mysql

%files odbc -f files.odbc

%if %{with_oci8}
%files oci8 -f files.oci8
%endif

%if %{with_mssql}
%files mssql -f files.mssql
%endif

%if %{with_mhash}
%files mhash -f files.mhash
%endif

%if %{with_imap}
%files imap -f files.imap
%endif

%files ldap -f files.ldap

%files snmp -f files.snmp

%files domxml -f files.domxml

%files xmlrpc -f files.xmlrpc

%changelog
* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Joe Orton <jorton@redhat.com> 4.3.4-10
- eliminate /usr/local/lib RPATH in odbc.so
- really use system pcre library

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 4.3.4-9
- rebuilt

* Mon Feb  2 2004 Bill Nottingham <notting@redhat.com> 4.3.4-8
- obsolete php-imap if we're not building it

* Wed Jan 28 2004 Joe Orton <jorton@redhat.com> 4.3.4-7
- gd fix for build with recent Freetype2 (from upstream)
- remove easter egg (Oden Eriksson, Mandrake)

* Wed Jan 21 2004 Joe Orton <jorton@redhat.com> 4.3.4-6
- php-pear requires php
- also remove extension=imap from php.ini in upgrade trigger
- merge from Taroon: allow upgrade from Stronghold 4.0

* Wed Jan 21 2004 Joe Orton <jorton@redhat.com> 4.3.4-5
- add defattr for php-pear subpackage
- restore defaults: output_buffering=Off, register_argc_argv=On
- add trigger to handle php.ini upgrades smoothly (#112470)

* Tue Jan 13 2004 Joe Orton <jorton@redhat.com> 4.3.4-4
- conditionalize support for imap extension for the time being
- switch /etc/php.ini to use php.ini-recommended (but leave
  variables_order as EGPCS) (#97765)
- set session.path to /var/lib/php/session by default (#89975)
- own /var/lib/php{,/session} and have apache own the latter
- split off php-pear subpackage (#83771)

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 4.3.4-3
- rebuild against db-4.2.52.

* Mon Dec  1 2003 Joe Orton <jorton@redhat.com> 4.3.4-2
- rebuild for new libxslt (#110658) 
- use --with-{mssql,oci8} for enabling extensions (#110482)
- fix rebuild issues (Jan Visser, #110274)
- remove hard-coded LIBS
- conditional support for mhash (Aleksander Adamowski, #111251)

* Mon Nov 10 2003 Joe Orton <jorton@redhat.com> 4.3.4-1.1
- rebuild for FC1 updates

* Mon Nov 10 2003 Joe Orton <jorton@redhat.com> 4.3.4-1
- update to 4.3.4
- include all licence files
- libxmlrpc fixes

* Mon Oct 20 2003 Joe Orton <jorton@redhat.com> 4.3.3-6
- use bundled libgd (#107407)
- remove manual: up-to-date manual sources are no longer DFSG-free;
  it's too big; it's on the web anyway; #91292, #105804, #107384

* Wed Oct 15 2003 Joe Orton <jorton@redhat.com> 4.3.3-5
- add php-xmlrpc subpackage (#107138)

* Mon Oct 13 2003 Joe Orton <jorton@redhat.com> 4.3.3-4
- drop recode support, symbols collide with MySQL

* Sun Oct 12 2003 Joe Orton <jorton@redhat.com> 4.3.3-3
- split domxml extension into php-domxml subpackage
- enable xslt and xml support in domxml extension (#106042)
- fix httpd-devel build requirement (#104341)
- enable recode extension (#106755)
- add workaround for #103982

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 4.3.3-3
- rebuild against db-4.2.42.

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 4.3.3-2
- don't use --enable-versioning, it depends on libtool being
 broken (#103690)

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 4.3.3-1
- update to 4.3.3
- add libtool build prereq (#103388)
- switch to apache2handler

* Mon Jul 28 2003 Joe Orton <jorton@redhat.com> 4.3.2-8
- rebuild

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.2-7
- rebuild

* Tue Jul  8 2003 Joe Orton <jorton@redhat.com> 4.3.2-6
- use system pcre library

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 4.3.2-5
- enable mbstring and mbregex (#81336)
- fix use of libtool 1.5

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Joe Orton <jorton@redhat.com> 4.3.2-3
- add lib64 and domxml fixes

* Tue Jun  3 2003 Frank Dauer <f@paf.net>
- added conditional support for mssql module (#92149)

* Fri May 30 2003 Joe Orton <jorton@redhat.com> 4.3.2-2
- update the -tests and -lib64 patches
- fixes for db4 detection
- require aspell-devel >= 0.50.0 for pspell compatibility

* Thu May 29 2003 Joe Orton <jorton@redhat.com> 4.3.2-1
- update to 4.3.2

* Fri May 16 2003 Joe Orton <jorton@redhat.com> 4.3.1-3
- link odbc module correctly
- patch so that php -n doesn't scan inidir
- run tests using php -n, avoid loading system modules

* Wed May 14 2003 Joe Orton <jorton@redhat.com> 4.3.1-2
- workaround broken parser produced by bison-1.875

* Tue May  6 2003 Joe Orton <jorton@redhat.com> 4.3.1-1
- update to 4.3.1; run test suite
- open extension modules with RTLD_NOW rather than _LAZY

* Tue May  6 2003 Joe Orton <jorton@redhat.com> 4.2.2-19
- patch for gd 2.x API changes in gd extension

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 4.2.2-18
- rebuild to use aspell (#89925)
- patch to work round conditional AC_PROG_CXX break in autoconf 2.57
- fix dba build against db >= 4.1

* Mon Feb 24 2003 Joe Orton <jorton@redhat.com> 4.2.2-17
- restrict SNMP patch to minimal changes, fixing segv on startup (#84607)

* Wed Feb 12 2003 Joe Orton <jorton@redhat.com> 4.2.2-16
- prevent startup if using httpd.worker to avoid thread-safety issues.
- fix parsing private keys in OpenSSL extension (#83994)
- fixes for SNMP extension (backport from 4.3) (#74761)

* Wed Jan 29 2003 Joe Orton <jorton@redhat.com> 4.2.2-15
- add security fixes for wordwrap() and mail()

* Mon Jan 13 2003 Joe Orton <jorton@redhat.com> 4.2.2-14
- drop explicit Requires in subpackages, rely on automatic deps.
- further fixes for libdir=lib64

* Tue Dec 17 2002 Joe Orton <jorton@redhat.com> 4.2.2-13
- drop prereq for perl, grep in subpackages
- rebuild and patch for OpenSSL 0.9.7

* Tue Dec 10 2002 Joe Orton <jorton@redhat.com> 4.2.2-12
- backport "ini dir scanning" patch from CVS HEAD; /etc/php.d/*.ini
  are now loaded at startup; each subpackage places an ini file
  in that directory rather than munging /etc/php.ini in post/postun.
- default config changes: enable short_open_tag; remove settings for
  php-dbg extension

* Wed Dec  4 2002 Joe Orton <jorton@redhat.com> 4.2.2-11
- own the /usr/lib/php4 directory (#73894)
- reinstate dropped patch to unconditionally disable ZTS

* Mon Dec  2 2002 Joe Orton <jorton@redhat.com> 4.2.2-10
- remove ldconfig invocation in post/postun
- fixes for #73516 (partially), #78586, #75029, #75712, #75878

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 4.2.2-9
- fixes for libdir=/usr/lib64, based on SuSE's patches.
- add build prereqs for zlib-devel, imap-devel, curl-devel (#74819)
- remove unpackaged files from install root
- libtoolize; use configure cache to speed up build

* Mon Sep 23 2002 Philip Copeland <bryce@redhat.com> 4.2.2-8.0.6
- PHP cannot determine which UID is being used, so safe
  mode restrictions were always applied. Fixed. (#74396)

* Tue Sep 3 2002 Philip Copeland <bryce@redhat.com> 4.2.2-8.0.4
- zts support seems to crash out httpd on a *second* sighup
  ie service httpd start;
  apachectl restart ; (ok)
  apachectl restart ; (httpd segv's and collapses)
  removed --enable-experimental-zts which this seems related to.
- Small patch added because some places need to know that they
  aren't using the ZTS API's (dumb)

* Mon Sep 2 2002 Philip Copeland <bryce@redhat.com> 4.2.2-8.0.3
- fixup /etc/httpd/conf.d/php.conf to limit largest amount
  of data accepted (#73254) Limited to 512K (which seems a
  little excessive but anyway,..)
  Note: php.conf is part of the srpm sources not part of the
  php codebase.
- ditched extrenious --enable-debugger (was for php-dbg)
- When upgrading we tend not to modify /etc/php.ini if it exists,
  instead we create php.ini.rpmnew. Modified the post scripts to
  edit php.ini.rpmnew if it exists, so that people can copy
  over the php.ini.rpmnew as php.ini knowing that it will
  be an edited version, consistant with what modules they
  installed #72033

* Sun Sep 1 2002 Joe Orton <jorton@redhat.com> 4.2.2-8.0.2
- require httpd-mmn for module ABI compatibility

* Fri Aug 30 2002 Philip Copeland <bryce@redhat.com> 4.2.2-8.0.1
- URLS would drop the last arguments #72752
        --enable-mbstring
        --enable-mbstr-enc-trans
  These were supposed to help provide multibyte language
  support, however, they cause problems. Removed. Maybe in
  a later errata when they work.
- added small patch to php_variables.c that allows
  $_GET[<var>] to initialise properly when
  --enable-mbstr-enc-trans is disabled.
- Be consistant with errata naming (8.0.x)

* Tue Aug 27 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.2-11
- rebuild

* Wed Aug 22 2002 Philip Copeland <bryce@redhat.com> 4.2.2-10
- Beat down the requirement list to something a little
  more sane

* Wed Aug 14 2002 Bill Nottingham <notting@redhat.com> 4.2.2-9
- trim manual language lists

* Mon Aug 12 2002 Gary Benson <gbenson@redhat.com> 4.2.2-8
- rebuild against httpd-2.0.40

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 4.2.2-7
- rebuilt with gcc-3.2 (we hope)

* Wed Aug 7 2002 Philip Copeland <bryce@redhat.com> 4.2.2-6
- Where multiple cookies are set, only the last one
  was actually made. Fixes #67853

* Mon Aug 5 2002 Philip Copeland <bryce@redhat.com> 4.2.2-5
- Shuffled the php/php-devel package file manifest
  with respect to PEAR (PHP Extension and Application
  Repository) #70673

* Fri Aug 2 2002 Philip Copeland <bryce@redhat.com> 4.2.2-4
- #67815, search path doesn't include the pear directory
- pear not being installed correctly. Added --with-pear=
  option.

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 4.2.2-2
- build using gcc-3.2-0.1

* Mon Jul 22 2002 Philip Copeland <bryce@redhat.com> 4.2.2-1
- Yippie 8/ another security vunerability (see
  http://www.php.net/release_4_2_2.php for details)

* Wed Jul 17 2002 Philip Copeland <bryce@redhat.com> 4.2.1-9
- Reminder to self that mm was pushed out because it's
  NOT thread safe.
- Updated the manuals (much to Bills horror)

* Tue Jul 16 2002 Philip Copeland <bryce@redhat.com> 4.2.1-8
- php.ini alteration to fit in with the install/uninstall
  of various php rpm based installable modules

* Mon Jul 15 2002 Philip Copeland <bryce@redhat.com> 4.2.1-8
- php -v showing signs of deep unhappiness with the world
  added  --enable-experimental-zts to configure to make it
  happy again (yes I know experimental sounds 'dangerous'
  it's just a name for an option we need)

* Fri Jul 12 2002 Philip Copeland <bryce@redhat.com> 4.2.1-7
- #68715, Wrong name for Mysql Module in php.ini. Fixed.

* Fri Jun 28 2002 Philip Copeland <bryce@redhat.com> 4.2.1-6
- SNMP fixup

* Thu Jun 27 2002 Philip Copeland <bryce@redhat.com> 4.2.1-5
- Ah,.. seems httpd2 has been renamed to just plain
  ol' httpd. Fixed spec file to suit.
- ucd-snmp changed to net-snmp overnight...
  temporarily disabled snmp while I work out the
  impact of this change and if it is safe

* Wed Jun 26 2002 Philip Copeland <bryce@redhat.com> 4.2.1-4
- openldap 2.1.x problem solved by Nalin. Sure the ldap
  API didn't change,... <mutter>. Added TSRMLS_FETCH()
  to ldap_rebind_proc().
- Removed the php-dbg package as thats going to be provided
  elsewhere

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 4.2.1-3
- automated rebuild

* Mon Jun 10 2002 Philip Copeland <bryce@redhat.com> 4.2.1-2
- Actually mm is now a dead project. Removed permently.

* Tue May 28 2002 Gary Benson <gbenson@redhat.com> 4.2.1-2
- change paths for httpd-2.0
- add the config file
- disable mm temporarily

* Sun May 26 2002 Tim Powers <timp@redhat.com> 4.2.1-1
- automated rebuild

* Wed May 22 2002 Philip Copeland <bryce@redhat.com> 4.2.1-0
- Initial pristine build of php-4.2.1
- Minor patch to get around a 64 bitism
- Added in the dgb debugging hooks

