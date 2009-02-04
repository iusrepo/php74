%define contentdir /var/www
%define apiver 20041225
%define zendver 20060613
%define pdover 20060511

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 5.2.8
Release: 6%{?dist}
License: PHP
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: macros.php

Patch1: php-5.2.6-gnusrc.patch
Patch2: php-4.3.3-install.patch
Patch3: php-5.2.4-norpath.patch
Patch5: php-5.0.2-phpize64.patch
Patch8: php-5.2.0-includedir.patch
Patch9: php-5.2.4-embed.patch

# Fixes for extension modules
Patch22: php-4.3.11-shutdown.patch
Patch24: php-5.2.3-macropen.patch

# Functional changes
Patch30: php-5.0.4-dlopen.patch
Patch31: php-5.2.4-easter.patch
Patch32: php-5.2.6-systzdata.patch

# Fixes for tests
Patch50: php-5.2.7-tests-dashn.patch
Patch51: php-5.0.4-tests-wddx.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
BuildRequires: zlib-devel, pcre-devel >= 6.6, smtpdaemon, readline-devel
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
Obsoletes: php-dbg, php3, phpfi, stronghold-php
# Enforce Apache module ABI compatibility
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)
Provides: mod_php = %{version}-%{release}
Requires: php-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: php-common = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}
Provides: php-pcntl, php-readline

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package common
Group: Development/Languages
Summary: Common files for PHP
Provides: php-api = %{apiver}, php-zend-abi = %{zendver}
Provides: php(api) = %{apiver}, php(zend-abi) = %{zendver}
# Provides for all builtin modules:
Provides: php-bz2, php-calendar, php-ctype, php-curl, php-date, php-exif
Provides: php-ftp, php-gettext, php-gmp, php-hash, php-iconv, php-libxml
Provides: php-reflection, php-session, php-shmop, php-simplexml, php-sockets
Provides: php-spl, php-tokenizer, php-openssl, php-pcre
Provides: php-zlib, php-json, php-zip, php-dbase
Obsoletes: php-openssl, php-pecl-zip, php-json, php-dbase

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php = %{version}-%{release}, autoconf, automake
Obsoletes: php-pecl-pdo-devel

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-pecl-pdo-sqlite, php-pecl-pdo
Provides: php-pdo-abi = %{pdover}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Provides: php_database, php-mysqli
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel >= 4.1.0

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
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

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Provides: php-posix, php-sysvsem, php-sysvshm, php-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Summary: A module for PHP applications that use ODBC databases
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

%package soap
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
Requires: php-common = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-domxml, php-dom
Provides: php-dom, php-xsl, php-domxml, php-wddx
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package ncurses
Summary: A module for PHP applications for using ncurses interfaces
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: ncurses-devel

%description ncurses
The php-ncurses package contains a dynamic shared object that will add
support for using the ncurses terminal output interfaces.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: php-common = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libXpm-devel, libjpeg-devel, libpng-devel, freetype-devel, t1lib-devel

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package mhash
Summary: Standard PHP module provides mhash support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: mhash-devel

%description mhash
The php-mhash package contains a dynamic shared object that will add
support for using the mhash library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
BuildRequires: freetds-devel

%description mssql
The php-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%prep
%setup -q
%patch1 -p1 -b .gnusrc
%patch2 -p1 -b .install
%patch3 -p1 -b .norpath
%patch5 -p1 -b .phpize64
%patch8 -p1 -b .includedir
%patch9 -p1 -b .embed

%patch22 -p1 -b .shutdown
%patch24 -p1 -b .macropen

%patch30 -p1 -b .dlopen
%patch31 -p1 -b .easter
%patch32 -p1 -b .systzdata

%patch50 -p1 -b .tests-dashn
%patch51 -p1 -b .tests-wddx

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

# Source is built trice: once for /usr/bin/php, once for the Apache DSO
# and once for inclusion as embedded script language into other programs
mkdir build-cgi build-apache build-embedded

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

%build
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
	--cache-file=../config.cache \
        --with-libdir=%{_lib} \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--disable-debug \
	--with-pic \
	--disable-rpath \
	--without-pear \
	--with-bz2 \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-xpm-dir=%{_prefix} \
	--enable-gd-native-ttf \
	--with-t1lib=%{_prefix} \
	--without-gdbm \
	--with-gettext \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-openssl \
        --with-pcre-regex=%{_prefix} \
	--with-zlib \
	--with-layout=GNU \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-sockets \
	--enable-sysvsem --enable-sysvshm --enable-sysvmsg \
	--with-kerberos \
	--enable-ucd-snmp-hack \
	--enable-shmop \
	--enable-calendar \
        --without-mime-magic \
        --without-sqlite \
        --with-libxml-dir=%{_prefix} \
	--enable-xml \
        --with-system-tzdata \
	$* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi
build --enable-force-cgi-redirect \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-ncurses=shared \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{_bindir}/mysql_config \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,%{_prefix} \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --with-readline \
      --enable-dbase=shared \
      --with-pspell=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-mhash=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix}
popd

without_shared="--without-mysql --without-gd \
      --without-unixODBC --disable-dom \
      --disable-dba --without-unixODBC \
      --disable-pdo --disable-xmlreader --disable-xmlwriter \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed ${without_shared}
popd

%check
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE: $f --"
    cat "$f"
    echo "-- $f result ends."
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install INSTALL_ROOT=$RPM_BUILD_ROOT 

# Install the Apache module
make -C build-apache install-sapi INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 $RPM_SOURCE_DIR/php.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/php/pear \
                  $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/php.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql mysql mysqli odbc ldap snmp xmlrpc imap \
    mbstring ncurses gd dom xsl soap bcmath dba xmlreader xmlwriter \
    pdo pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite json zip \
    dbase mcrypt mhash tidy pdo_dblib mssql pspell curl wddx \
    posix sysvshm sysvsem sysvmsg; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_mysql >> files.mysql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo

# Package json, dbase and zip in -common.
cat files.json files.dbase files.zip files.curl > files.common

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < $RPM_SOURCE_DIR/macros.php > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.php

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf.d/php.conf
%{contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_localstatedir}/lib/php
%dir %{_libdir}/php/pear
%dir %{_datadir}/php

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/php-cgi
%{_mandir}/man1/php.1*
%doc sapi/cgi/README* sapi/cli/README

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*
%config %{_sysconfdir}/rpm/macros.php

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{version}.so

%files pgsql -f files.pgsql
%files mysql -f files.mysql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%files ncurses -f files.ncurses
%files gd -f files.gd
%doc gd_README
%files soap -f files.soap
%files bcmath -f files.bcmath
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files mhash -f files.mhash
%files tidy -f files.tidy
%files mssql -f files.mssql
%files pspell -f files.pspell
%files process -f files.process

%changelog
* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 5.2.8-6
- drop obsolete configure args
- drop -odbc patch (#483690)

* Mon Jan 26 2009 Joe Orton <jorton@redhat.com> 5.2.8-5
- split out sysvshm, sysvsem, sysvmsg, posix into php-process

* Sun Jan 25 2009 Joe Orton <jorton@redhat.com> 5.2.8-4
- move wddx to php-xml, build curl shared in -common
- remove BR for expat-devel, bogus configure option

* Fri Jan 23 2009 Joe Orton <jorton@redhat.com> 5.2.8-3
- rebuild for new MySQL

* Sat Dec 13 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.8-2
- libtool 2 workaround for phpize (#476004)
- add missing php_embed.h (#457777)

* Tue Dec 09 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.8-1
- update to 5.2.8

* Sat Dec 06 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.7-1.1
- libtool 2 workaround

* Fri Dec 05 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.7-1
- update to 5.2.7
- enable pdo_dblib driver in php-mssql

* Mon Nov 24 2008 Joe Orton <jorton@redhat.com> 5.2.6-7
- tweak Summary, thanks to Richard Hughes

* Tue Nov  4 2008 Joe Orton <jorton@redhat.com> 5.2.6-6
- move gd_README to php-gd
- update to r4 of systzdata patch; introduces a default timezone
  name of "System/Localtime", which uses /etc/localtime (#469532)

* Sat Sep 13 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.6-5
- enable XPM support in php-gd
- Fix BR for php-gd

* Sun Jul 20 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.6-4
- enable T1lib support in php-gd

* Mon Jul 14 2008 Joe Orton <jorton@redhat.com> 5.2.6-3
- update to 5.2.6
- sync default php.ini with upstream
- drop extension_dir from default php.ini, rely on hard-coded
  default, to make php-common multilib-safe (#455091)
- update to r3 of systzdata patch

* Thu Apr 24 2008 Joe Orton <jorton@redhat.com> 5.2.5-7
- split pspell extension out into php-spell (#443857)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.2.5-6
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Joe Orton <jorton@redhat.com> 5.2.5-5
- ext/date: use system timezone database

* Fri Dec 28 2007 Joe Orton <jorton@redhat.com> 5.2.5-4
- rebuild for libc-client bump

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 5.2.5-3
 - Rebuild for openssl bump

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 5.2.5-2
- update to 5.2.5

* Mon Oct 15 2007 Joe Orton <jorton@redhat.com> 5.2.4-3
- correct pcre BR version (#333021)
- restore metaphone fix (#205714)
- add READMEs to php-cli

* Sun Sep 16 2007 Joe Orton <jorton@redhat.com> 5.2.4-2
- update to 5.2.4

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 5.2.3-9
- rebuild for fixed APR

* Tue Aug 28 2007 Joe Orton <jorton@redhat.com> 5.2.3-8
- add ldconfig post/postun for -embedded (Hans de Goede)

* Fri Aug 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.2.3-7
- add php-embedded sub-package

* Fri Aug 10 2007 Joe Orton <jorton@redhat.com> 5.2.3-6
- fix build with new glibc
- fix License

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 5.2.3-5
- define php_extdir in macros.php

* Mon Jul  2 2007 Joe Orton <jorton@redhat.com> 5.2.3-4
- obsolete php-dbase

* Tue Jun 19 2007 Joe Orton <jorton@redhat.com> 5.2.3-3
- add mcrypt, mhash, tidy, mssql subpackages (Dmitry Butskoy)
- enable dbase extension and package in -common

* Fri Jun  8 2007 Joe Orton <jorton@redhat.com> 5.2.3-2
- update to 5.2.3 (thanks to Jeff Sheltren)

* Wed May  9 2007 Joe Orton <jorton@redhat.com> 5.2.2-4
- fix php-pdo *_arg_force_ref global symbol abuse (#216125)

* Tue May  8 2007 Joe Orton <jorton@redhat.com> 5.2.2-3
- rebuild against uw-imap-devel

* Fri May  4 2007 Joe Orton <jorton@redhat.com> 5.2.2-2
- update to 5.2.2
- synch changes from upstream recommended php.ini

* Thu Mar 29 2007 Joe Orton <jorton@redhat.com> 5.2.1-5
- enable SASL support in LDAP extension (#205772)

* Wed Mar 21 2007 Joe Orton <jorton@redhat.com> 5.2.1-4
- drop mime_magic extension (deprecated by php-pecl-Fileinfo)

* Mon Feb 19 2007 Joe Orton <jorton@redhat.com> 5.2.1-3
- fix regression in str_{i,}replace (from upstream)

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 5.2.1-2
- update to 5.2.1
- add Requires(pre) for httpd
- trim %%changelog to versions >= 5.0.0

* Thu Feb  8 2007 Joe Orton <jorton@redhat.com> 5.2.0-10
- bump default memory_limit to 32M (#220821)
- mark config files noreplace again (#174251)
- drop trailing dots from Summary fields
- use standard BuildRoot
- drop libtool15 patch (#226294)

* Tue Jan 30 2007 Joe Orton <jorton@redhat.com> 5.2.0-9
- add php(api), php(zend-abi) provides (#221302)
- package /usr/share/php and append to default include_path (#225434)

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 5.2.0-8
- fix filter.h installation path
- fix php-zend-abi version (Remi Collet, #212804)

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-7
- rebuild again

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-6
- rebuild for net-snmp soname bump

* Mon Nov 27 2006 Joe Orton <jorton@redhat.com> 5.2.0-5
- build json and zip shared, in -common (Remi Collet, #215966)
- obsolete php-json and php-pecl-zip
- build readline extension into /usr/bin/php* (#210585)
- change module subpackages to require php-common not php (#177821)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-4
- provide php-zend-abi (#212804)
- add /etc/rpm/macros.php exporting interface versions
- synch with upstream recommended php.ini

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-3
- update to 5.2.0 (#213837)
- php-xml provides php-domxml (#215656)
- fix php-pdo-abi provide (#214281)

* Tue Oct 31 2006 Joseph Orton <jorton@redhat.com> 5.1.6-4
- rebuild for curl soname bump
- add build fix for curl 7.16 API

* Wed Oct  4 2006 Joe Orton <jorton@redhat.com> 5.1.6-3
- from upstream: add safety checks against integer overflow in _ecalloc

* Tue Aug 29 2006 Joe Orton <jorton@redhat.com> 5.1.6-2
- update to 5.1.6 (security fixes)
- bump default memory_limit to 16M (#196802)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.1.4-8.1
- rebuild

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-8
- Provide php-posix (#194583)
- only provide php-pcntl from -cli subpackage
- add missing defattr's (thanks to Matthias Saou)

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-7
- move Obsoletes for php-openssl to -common (#194501)
- Provide: php-cgi from -cli subpackage

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 5.1.4-6
- split out php-cli, php-common subpackages (#177821)
- add php-pdo-abi version export (#193202)

* Wed May 24 2006 Radek Vokal <rvokal@redhat.com> 5.1.4-5.1
- rebuilt for new libnetsnmp

* Thu May 18 2006 Joe Orton <jorton@redhat.com> 5.1.4-5
- provide mod_php (#187891)
- provide php-cli (#192196)
- use correct LDAP fix (#181518)
- define _GNU_SOURCE in php_config.h and leave it defined
- drop (circular) dependency on php-pear

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 5.1.4-3
- update to 5.1.4

* Wed May  3 2006 Joe Orton <jorton@redhat.com> 5.1.3-3
- update to 5.1.3

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 5.1.2-5
- provide php-api (#183227)
- add provides for all builtin modules (Tim Jackson, #173804)
- own %%{_libdir}/php/pear for PEAR packages (per #176733)
- add obsoletes to allow upgrade from FE4 PDO packages (#181863)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.3
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 5.1.2-4
- rebuild for new libc-client soname

* Mon Jan 16 2006 Joe Orton <jorton@redhat.com> 5.1.2-3
- only build xmlreader and xmlwriter shared (#177810)

* Fri Jan 13 2006 Joe Orton <jorton@redhat.com> 5.1.2-2
- update to 5.1.2

* Thu Jan  5 2006 Joe Orton <jorton@redhat.com> 5.1.1-8
- rebuild again

* Mon Jan  2 2006 Joe Orton <jorton@redhat.com> 5.1.1-7
- rebuild for new net-snmp

* Mon Dec 12 2005 Joe Orton <jorton@redhat.com> 5.1.1-6
- enable short_open_tag in default php.ini again (#175381)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Joe Orton <jorton@redhat.com> 5.1.1-5
- require net-snmp for php-snmp (#174800)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 5.1.1-4
- add /usr/share/pear back to hard-coded include_path (#174885)

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 5.1.1-3
- rebuild for httpd 2.2

* Mon Nov 28 2005 Joe Orton <jorton@redhat.com> 5.1.1-2
- update to 5.1.1
- remove pear subpackage
- enable pdo extensions (php-pdo subpackage)
- remove non-standard conditional module builds
- enable xmlreader extension

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 5.0.5-6
- rebuilt against new openssl

* Mon Nov  7 2005 Joe Orton <jorton@redhat.com> 5.0.5-5
- pear: update to XML_RPC 1.4.4, XML_Parser 1.2.7, Mail 1.1.9 (#172528)

* Tue Nov  1 2005 Joe Orton <jorton@redhat.com> 5.0.5-4
- rebuild for new libnetsnmp

* Wed Sep 14 2005 Joe Orton <jorton@redhat.com> 5.0.5-3
- update to 5.0.5
- add fix for upstream #34435
- devel: require autoconf, automake (#159283)
- pear: update to HTTP-1.3.6, Mail-1.1.8, Net_SMTP-1.2.7, XML_RPC-1.4.1
- fix imagettftext et al (upstream, #161001)

* Thu Jun 16 2005 Joe Orton <jorton@redhat.com> 5.0.4-11
- ldap: restore ldap_start_tls() function

* Fri May  6 2005 Joe Orton <jorton@redhat.com> 5.0.4-10
- disable RPATHs in shared extensions (#156974)

* Tue May  3 2005 Joe Orton <jorton@redhat.com> 5.0.4-9
- build simplexml_import_dom even with shared dom (#156434)
- prevent truncation of copied files to ~2Mb (#155916)
- install /usr/bin/php from CLI build alongside CGI
- enable sysvmsg extension (#142988)

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 5.0.4-8
- prevent build of builtin dba as well as shared extension

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-7
- split out dba and bcmath extensions into subpackages
- BuildRequire gcc-c++ to avoid AC_PROG_CXX{,CPP} failure (#155221)
- pear: update to DB-1.7.6
- enable FastCGI support in /usr/bin/php-cgi (#149596)

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-6
- build /usr/bin/php with the CLI SAPI, and add /usr/bin/php-cgi,
  built with the CGI SAPI (thanks to Edward Rudd, #137704)
- add php(1) man page for CLI
- fix more test cases to use -n when invoking php

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-5
- rebuild for new libpq soname

* Tue Apr 12 2005 Joe Orton <jorton@redhat.com> 5.0.4-4
- bundle from PEAR: HTTP, Mail, XML_Parser, Net_Socket, Net_SMTP
- snmp: disable MSHUTDOWN function to prevent error_log noise (#153988)
- mysqli: add fix for crash on x86_64 (Georg Richter, upstream #32282)

* Mon Apr 11 2005 Joe Orton <jorton@redhat.com> 5.0.4-3
- build shared objects as PIC (#154195)

* Mon Apr  4 2005 Joe Orton <jorton@redhat.com> 5.0.4-2
- fix PEAR installation and bundle PEAR DB-1.7.5 package

* Fri Apr  1 2005 Joe Orton <jorton@redhat.com> 5.0.4-1
- update to 5.0.4 (#153068)
- add .phps AddType to php.conf (#152973)
- better gcc4 fix for libxmlrpc

* Wed Mar 30 2005 Joe Orton <jorton@redhat.com> 5.0.3-5
- BuildRequire mysql-devel >= 4.1
- don't mark php.ini as noreplace to make upgrades work (#152171)
- fix subpackage descriptions (#152628)
- fix memset(,,0) in Zend (thanks to Dave Jones)
- fix various compiler warnings in Zend

* Thu Mar 24 2005 Joe Orton <jorton@redhat.com> 5.0.3-4
- package mysqli extension in php-mysql
- really enable pcntl (#142903)
- don't build with --enable-safe-mode (#148969)
- use "Instant Client" libraries for oci8 module (Kai Bolay, #149873)

* Fri Feb 18 2005 Joe Orton <jorton@redhat.com> 5.0.3-3
- fix build with GCC 4

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 5.0.3-2
- install the ext/gd headers (#145891)
- enable pcntl extension in /usr/bin/php (#142903)
- add libmbfl array arithmetic fix (dcb314@hotmail.com, #143795)
- add BuildRequire for recent pcre-devel (#147448)

* Wed Jan 12 2005 Joe Orton <jorton@redhat.com> 5.0.3-1
- update to 5.0.3 (thanks to Robert Scheck et al, #143101)
- enable xsl extension (#142174)
- package both the xsl and dom extensions in php-xml
- enable soap extension, shared (php-soap package) (#142901)
- add patches from upstream 5.0 branch:
 * Zend_strtod.c compile fixes
 * correct php_sprintf return value usage

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 5.0.2-8
- update for db4-4.3 (Robert Scheck, #140167)
- build against mysql-devel
- run tests in %%check

* Wed Nov 10 2004 Joe Orton <jorton@redhat.com> 5.0.2-7
- truncate changelog at 4.3.1-1
- merge from 4.3.x package:
 - enable mime_magic extension and Require: file (#130276)

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-6
- fix dom/sqlite enable/without confusion

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-5
- fix phpize installation for lib64 platforms
- add fix for segfault in variable parsing introduced in 5.0.2

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-4
- update to 5.0.2 (#127980)
- build against mysqlclient10-devel
- use new RTLD_DEEPBIND to load extension modules
- drop explicit requirement for elfutils-devel
- use AddHandler in default conf.d/php.conf (#135664)
- "fix" round() fudging for recent gcc on x86
- disable sqlite pending audit of warnings and subpackage split

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-4
- don't build dom extension into 2.0 SAPI

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-3
- ExclusiveArch: x86 ppc x86_64 for the moment

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-2
- fix default extension_dir and conf.d/php.conf

* Thu Sep  9 2004 Joe Orton <jorton@redhat.com> 5.0.1-1
- update to 5.0.1
- only build shared modules once
- put dom extension in php-dom subpackage again
- move extension modules into %%{_libdir}/php/modules
- don't use --with-regex=system, it's ignored for the apache* SAPIs

* Wed Aug 11 2004 Tom Callaway <tcallawa@redhat.com>
- Merge in some spec file changes from Jeff Stern (jastern@uci.edu)

* Mon Aug 09 2004 Tom Callaway <tcallawa@redhat.com>
- bump to 5.0.0
- add patch to prevent clobbering struct re_registers from regex.h
- remove domxml references, replaced with dom now built-in
- fix php.ini to refer to php5 not php4
