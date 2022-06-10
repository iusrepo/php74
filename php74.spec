# IUS spec file for php74, forked from
#
# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

# API/ABI check
%global apiver      20190902
%global zendver     20190902
%global pdover      20170320

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 7.4

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Regression tests take a long time, you can skip 'em with this
#global runselftest 0
%{!?runselftest: %global runselftest 1}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

# needed at srpm build time, when httpd-devel not yet installed
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

# subpackages
%global with_firebird 1
%global with_imap     1
%global with_freetds  1
%global with_sodium   1
%global with_pspell   1
%global with_tidy     1

%if 0%{?fedora}
%global with_zts      1
%global with_lmdb     1
%global with_libgd    1
%global with_libpcre  1
%else
%global with_zts      0
%global with_lmdb     0
%global with_libgd    0
%global with_libpcre  0
%endif

Summary: PHP scripting language for creating dynamic web sites
Name: php74
Version: 7.4.30
Release: 1%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
URL: http://www.php.net/

Source0: https://www.php.net/distributions/php-%{version}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source9: php.modconf
Source10: php.ztsmodconf
Source13: nginx-fpm.conf
Source14: nginx-php.conf
Source15: httpd-fpm.conf
# See https://secure.php.net/gpg-keys.php
Source20: https://www.php.net/distributions/php-keyring.gpg
Source21: https://www.php.net/distributions/php-%{version}.tar.xz.asc
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist
Source53: 20-ffi.ini

# Build fixes
Patch1: php-7.4.0-httpd.patch
Patch5: php-7.2.0-includedir.patch
Patch6: php-7.4.0-embed.patch
Patch8: php-7.2.0-libdb.patch

# Functional changes
Patch42: php-7.3.3-systzdata-v18.patch
# See http://bugs.php.net/53436
Patch43: php-7.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-7.4.0-ldap_r.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch
Patch49: php-7.4.0-curltls.patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-5.6.3-datetests.patch


BuildRequires: gnupg2
BuildRequires: bzip2-devel
BuildRequires: pkgconfig(libcurl)  >= 7.15.5
BuildRequires: pam-devel
BuildRequires: libstdc++-devel
# no pkgconfig to avoid compat-openssl10
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: pkgconfig(sqlite3) >= 3.7.4
BuildRequires: pkgconfig(zlib) >= 1.2.0.4
BuildRequires: smtpdaemon
BuildRequires: pkgconfig(libedit)
%if %{with_libpcre}
BuildRequires: pkgconfig(libpcre2-8) >= 10.30
%else
Provides:      bundled(pcre2) = 10.32
%endif
BuildRequires: bzip2
BuildRequires: perl-interpreter
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: systemtap-sdt-devel
# used for tests
BuildRequires: %{_bindir}/ps

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

%package -n mod_%{name}
Summary: PHP module for the Apache HTTP Server
# ensure we build with stock httpd, not httpd24u
BuildRequires: httpd-devel < 2.4.10
Requires: httpd-mmn = %{_httpd_mmn}
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_zts}
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif
# php engine for Apache httpd webserver
Provides: php(httpd)
# safe replacement
Provides:  php = %{version}-%{release}
Provides:  php%{?_isa} = %{version}-%{release}
Conflicts: php < %{version}-%{release}
Provides:  mod_php = %{version}-%{release}
Provides:  mod_php%{?_isa} = %{version}-%{release}
Conflicts: mod_php < %{version}-%{release}

%description -n mod_%{name}
The mod_%{name} package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}
# safe replacement
Provides:  php-cli = %{version}-%{release}
Provides:  php-cli%{?_isa} = %{version}-%{release}
Conflicts: php-cli < %{version}-%{release}

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Summary: The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-dbg = %{version}-%{release}
Provides:  php-dbg%{?_isa} = %{version}-%{release}
Conflicts: php-dbg < %{version}-%{release}

%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Summary: PHP FastCGI Process Manager
BuildRequires: libacl-devel
BuildRequires: pkgconfig(libsystemd) >= 209
Requires: php-common%{?_isa} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
%{?systemd_requires}
# php engine for Apache httpd webserver
Provides: php(httpd)
# safe replacement
Provides:  php-fpm = %{version}-%{release}
Provides:  php-fpm%{?_isa} = %{version}-%{release}
Conflicts: php-fpm < %{version}-%{release}

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%package fpm-nginx
Summary: Nginx configuration for PHP-FPM
BuildArch: noarch
Requires: %{name}-fpm = %{version}-%{release}
Requires: nginx
# safe replacement
Provides:  php-fpm-nginx = %{version}-%{release}
Conflicts: php-fpm-nginx < %{version}-%{release}

%description fpm-nginx
Nginx configuration files for the PHP FastCGI Process Manager.

%package fpm-httpd
Summary: Apache HTTP Server configuration for PHP-FPM
BuildArch: noarch
Requires: %{name}-fpm = %{version}-%{release}
Requires: httpd >= 2.4
# safe replacement
Provides:  php-fpm-httpd = %{version}-%{release}
Conflicts: php-fpm-httpd < %{version}-%{release}

%description fpm-httpd
Apache HTTP Server configuration file for the PHP FastCGI Process Manager.

%package common
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP and BSD
# ABI/API check - Arch specific
Provides: php(api) = %{apiver}-%{__isa_bits}
Provides: php(zend-abi) = %{zendver}-%{__isa_bits}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: bundled(timelib)
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: bundled(libmagic) = 5.29
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
Provides: php-zlib, php-zlib%{?_isa}
# safe replacement
Provides:  php-common = %{version}-%{release}
Provides:  php-common%{?_isa} = %{version}-%{release}
Conflicts: php-common < %{version}-%{release}
Conflicts: php56u-common, php70u-common, php71u-common, php72u-common, php73-common

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}
# always needed to build extension
Requires: autoconf
Requires: automake
Requires: gcc
Requires: gcc-c++
Requires: libtool
# see "php-config --libs"
Requires: krb5-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: openssl-devel%{?_isa} >= 1.0.1
%if %{with_libpcre}
Requires: pcre2-devel%{?_isa}
%endif
Requires: zlib-devel%{?_isa}
%if %{with_zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif
# safe replacement
Provides:  php-devel = %{version}-%{release}
Provides:  php-devel%{?_isa} = %{version}-%{release}
Conflicts: php-devel < %{version}-%{release}

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}
# safe replacement
Provides:  php-opcache = %{version}-%{release}
Provides:  php-opcache%{?_isa} = %{version}-%{release}
Conflicts: php-opcache < %{version}-%{release}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%if %{with_imap}
%package imap
Summary: A module for PHP applications that use IMAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(krb5)
BuildRequires: pkgconfig(krb5-gssapi)
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: libc-client-devel
# safe replacement
Provides:  php-imap = %{version}-%{release}
Provides:  php-imap%{?_isa} = %{version}-%{release}
Conflicts: php-imap < %{version}-%{release}

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif

%package ldap
Summary: A module for PHP applications that use LDAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libsasl2)
BuildRequires: openldap-devel
BuildRequires: openssl-devel >= 1.0.1
# safe replacement
Provides:  php-ldap = %{version}-%{release}
Provides:  php-ldap%{?_isa} = %{version}-%{release}
Conflicts: php-ldap < %{version}-%{release}

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}-%{__isa_bits}
Provides: php(pdo-abi) = %{pdover}-%{__isa_bits}
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}
# safe replacement
Provides:  php-pdo = %{version}-%{release}
Provides:  php-pdo%{?_isa} = %{version}-%{release}
Conflicts: php-pdo < %{version}-%{release}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
# safe replacement
Provides:  php-mysqlnd = %{version}-%{release}
Provides:  php-mysqlnd%{?_isa} = %{version}-%{release}
Conflicts: php-mysqlnd < %{version}-%{release}
Conflicts: php-mysql < %{version}-%{release}

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: postgresql-devel
# safe replacement
Provides:  php-pgsql = %{version}-%{release}
Provides:  php-pgsql%{?_isa} = %{version}-%{release}
Conflicts: php-pgsql < %{version}-%{release}

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}
# safe replacement
Provides:  php-process = %{version}-%{release}
Provides:  php-process%{?_isa} = %{version}-%{release}
Conflicts: php-process < %{version}-%{release}

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel
# safe replacement
Provides:  php-odbc = %{version}-%{release}
Provides:  php-odbc%{?_isa} = %{version}-%{release}
Conflicts: php-odbc < %{version}-%{release}

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libxml-2.0)
# safe replacement
Provides:  php-soap = %{version}-%{release}
Provides:  php-soap%{?_isa} = %{version}-%{release}
Conflicts: php-soap < %{version}-%{release}

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_firebird}
%package pdo-firebird
Summary: PDO driver for Interbase/Firebird databases
# All files licensed under PHP version 3.01
License: PHP
# for fb_config command
BuildRequires:  firebird-devel
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}
# safe replacement
Provides:  php-pdo-firebird = %{version}-%{release}
Provides:  php-pdo-firebird%{?_isa} = %{version}-%{release}
Conflicts: php-pdo-firebird < %{version}-%{release}

%description pdo-firebird
The php-pdo-firebird package contains the PDO driver for
Interbase/Firebird databases.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel
# safe replacement
Provides:  php-snmp = %{version}-%{release}
Provides:  php-snmp%{?_isa} = %{version}-%{release}
Conflicts: php-snmp < %{version}-%{release}

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: pkgconfig(libxslt)  >= 1.1
BuildRequires: pkgconfig(libexslt)
BuildRequires: pkgconfig(libxml-2.0)  >= 2.7.6
# safe replacement
Provides:  php-xml = %{version}-%{release}
Provides:  php-xml%{?_isa} = %{version}-%{release}
Conflicts: php-xml < %{version}-%{release}

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: php-xml%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-xmlrpc = %{version}-%{release}
Provides:  php-xmlrpc%{?_isa} = %{version}-%{release}
Conflicts: php-xmlrpc < %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and OpenLDAP
BuildRequires: pkgconfig(oniguruma) >= 6.8
Provides: bundled(libmbfl) = 1.3.2
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-mbstring = %{version}-%{release}
Provides:  php-mbstring%{?_isa} = %{version}-%{release}
Conflicts: php-mbstring < %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
# All files licensed under PHP version 3.01
%if %{with_libgd}
License: PHP
%else
# bundled libgd is licensed under BSD
License: PHP and BSD
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_libgd}
BuildRequires: pkgconfig(gdlib) >= 2.1.1
%else
# Required to build the bundled GD library
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libwebp-devel
Provides: bundled(gd) = 2.0.35
%endif
# safe replacement
Provides:  php-gd = %{version}-%{release}
Provides:  php-gd%{?_isa} = %{version}-%{release}
Conflicts: php-gd < %{version}-%{release}

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-bcmath = %{version}-%{release}
Provides:  php-bcmath%{?_isa} = %{version}-%{release}
Conflicts: php-bcmath < %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-gmp = %{version}-%{release}
Provides:  php-gmp%{?_isa} = %{version}-%{release}
Conflicts: php-gmp < %{version}-%{release}

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: libdb-devel
BuildRequires: tokyocabinet-devel
%if %{with_lmdb}
BuildRequires: lmdb-devel
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-dba = %{version}-%{release}
Provides:  php-dba%{?_isa} = %{version}-%{release}
Conflicts: php-dba < %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%if %{with_tidy}
%package tidy
Summary: Standard PHP module provides tidy library support
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel
# safe replacement
Provides:  php-tidy = %{version}-%{release}
Provides:  php-tidy%{?_isa} = %{version}-%{release}
Conflicts: php-tidy < %{version}-%{release}

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.
%endif

%if %{with_freetds}
%package pdo-dblib
Summary: PDO driver for Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}
# safe replacement
Provides:  php-pdo-dblib = %{version}-%{release}
Provides:  php-pdo-dblib%{?_isa} = %{version}-%{release}
Conflicts: php-pdo-dblib < %{version}-%{release}

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS library.
%endif

%package embedded
Summary: PHP library for embedding in applications
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-embedded = %{version}-%{release}
Provides:  php-embedded%{?_isa} = %{version}-%{release}
Conflicts: php-embedded < %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%if %{with_pspell}
%package pspell
Summary: A module for PHP applications for using pspell interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0
# safe replacement
Provides:  php-pspell = %{version}-%{release}
Provides:  php-pspell%{?_isa} = %{version}-%{release}
Conflicts: php-pspell < %{version}-%{release}

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.
%endif

%package intl
Summary: Internationalization extension for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(icu-i18n) >= 50.1
BuildRequires: pkgconfig(icu-io)   >= 50.1
BuildRequires: pkgconfig(icu-uc)   >= 50.1
# safe replacement
Provides:  php-intl = %{version}-%{release}
Provides:  php-intl%{?_isa} = %{version}-%{release}
Conflicts: php-intl < %{version}-%{release}

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(enchant)
# safe replacement
Provides:  php-enchant = %{version}-%{release}
Provides:  php-enchant%{?_isa} = %{version}-%{release}
Conflicts: php-enchant < %{version}-%{release}

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides:  php-pecl(json)         = %{version}
Provides:  php-pecl(json)%{?_isa} = %{version}
Provides:  php-pecl-json          = %{version}
Provides:  php-pecl-json%{?_isa}  = %{version}
# safe replacement
Provides:  php-json = %{version}-%{release}
Provides:  php-json%{?_isa} = %{version}-%{release}
Conflicts: php-json < %{version}-%{release}

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.

%if %{with_sodium}
%package sodium
Summary: Wrapper for the Sodium cryptographic library
# All files licensed under PHP version 3.0.1
License: PHP
BuildRequires:  pkgconfig(libsodium) >= 1.0.9

Requires: php-common%{?_isa} = %{version}-%{release}
Provides:  php-pecl(libsodium)         = %{version}
Provides:  php-pecl(libsodium)%{?_isa} = %{version}
# safe replacement
Provides:  php-sodium = %{version}-%{release}
Provides:  php-sodium%{?_isa} = %{version}-%{release}
Conflicts: php-sodium < %{version}-%{release}

%description sodium
The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.
%endif


%package ffi
Summary: Foreign Function Interface
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
BuildRequires:  pkgconfig(libffi)
Requires: php-common%{?_isa} = %{version}-%{release}
# safe replacement
Provides:  php-ffi = %{version}-%{release}
Provides:  php-ffi%{?_isa} = %{version}-%{release}
Conflicts: php-ffi < %{version}-%{release}

%description ffi
FFI is one of the features that made Python and LuaJIT very useful for fast
prototyping. It allows calling C functions and using C data types from pure
scripting language and therefore develop “system code” more productively.

For PHP, FFI opens a way to write PHP extensions and bindings to C libraries
in pure PHP.


%prep
%{?gpgverify:%{gpgverify} --keyring='%{SOURCE20}' --signature='%{SOURCE21}' --data='%{SOURCE0}'}

%setup -q -n php-%{version}

%patch1 -p1 -b .mpmcheck
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch8 -p1 -b .libdb

%patch42 -p1 -b .systzdata
%patch43 -p1 -b .headers
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch47 -p1 -b .phpinfo
%if 0%{?rhel}
%patch49 -p1 -b .curltls
%endif

# upstream patches

# security patches

# Fixes for tests
%patch300 -p1 -b .datetests


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/bcmath/libbcmath/LICENSE libbcmath_LICENSE
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt
# tar issue
rm ext/zlib/tests/004-mb.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

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

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# Some extensions have their own configuration file
cp %{SOURCE50} %{SOURCE51} %{SOURCE53} .


%build
# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)
# Override default uname detection.
export PHP_UNAME=$(uname)

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.ac
./buildconf --force

CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign | sed 's/-mstackrealign//')
export CFLAGS

# Install extension modules in %%{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

# Always static:
# date, ereg, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --enable-rtld-now \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --without-gdbm \
    --with-openssl \
    --with-system-ciphers \
%if %{with_libpcre}
    --with-external-pcre \
%endif
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --without-pcre-jit \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml \
    --with-system-tzdata \
    --with-mhash \
    --without-password-argon2 \
    --enable-dtrace \
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-opcache \
      --enable-phpdbg \
%if %{with_imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with_libgd}
      --with-external-gd \
%else
      --with-freetype \
      --with-webp \
      --with-jpeg \
      --with-xpm \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
%if %{with_lmdb}
                          --with-lmdb=%{_prefix} \
%endif
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with_firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
%if %{with_freetds}
      --with-pdo-dblib=shared,%{_prefix} \
%endif
      --with-sqlite3=shared \
      --enable-json=shared \
      --without-readline \
      --with-libedit \
%if %{with_pspell}
      --with-pspell=shared \
%endif
      --enable-phar=shared \
%if %{with_tidy}
      --with-tidy=shared,%{_prefix} \
%endif
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-ffi=shared \
%if %{with_sodium}
      --with-sodium=shared \
%else
      --without-sodium \
%endif
      --enable-intl=shared \
      --with-enchant=shared
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-phpdbg \
      --disable-json \
      --without-ffi \
      --disable-xmlreader --disable-xmlwriter \
      --without-sodium \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --with-fpm-acl \
      --with-fpm-systemd \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp7.so
pushd build-embedded
build --enable-embed \
      --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
%if %{with_imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with_libgd}
      --with-external-gd \
%else
      --with-freetype \
      --with-webp \
      --with-jpeg \
      --with-xpm \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
%if %{with_lmdb}
                          --with-lmdb=%{_prefix} \
%endif
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
%if %{with_firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
%if %{with_freetds}
      --with-pdo-dblib=shared,%{_prefix} \
%endif
      --with-sqlite3=shared \
      --enable-json=shared \
      --without-readline \
      --with-libedit \
%if %{with_pspell}
      --with-pspell=shared \
%endif
      --enable-phar=shared \
%if %{with_tidy}
      --with-tidy=shared,%{_prefix} \
%endif
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-ffi=shared \
%if %{with_sodium}
      --with-sodium=shared \
%else
      --without-sodium \
%endif
      --enable-intl=shared \
      --with-enchant=shared
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
%if %runselftest
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
export SKIP_IO_CAPTURE_TESTS=1
unset TZ LANG LC_ALL
if ! make test TESTS=-j4; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Use php-config from embed SAPI to reduce used libs
install -m 755 build-embedded/scripts/php-config $RPM_BUILD_ROOT%{_bindir}/php-config

# Install the default configuration file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php/preload

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7-zts.so
%endif

# Apache config fragment
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/peclxml
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/mod_php
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/mod_php/session
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/mod_php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/mod_php/opcache

install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl

# PHP-FPM stuff
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/fpm
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/fpm/session
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/fpm/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/fpm/opcache
# Log
install -m 750 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -Dm 644 %{SOURCE6}  $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf
# Apache httpd configuration
install -D -m 644 %{SOURCE15} $RPM_BUILD_ROOT%{_httpd_confdir}/php-fpm.conf

TESTCMD="$RPM_BUILD_ROOT%{_bindir}/php --no-php-ini"
# Ensure all provided extensions are really there
for mod in core date filter hash libxml openssl pcntl pcre readline reflection session spl standard zlib
do
     $TESTCMD --modules | grep -qi $mod
done

TESTCMD="$TESTCMD --define extension_dir=$RPM_BUILD_ROOT%{_libdir}/php/modules"

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp \
%if %{with_imap}
    imap \
%endif
    json \
    mysqlnd mysqli \
    mbstring gd dom xsl soap bcmath dba \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    sqlite3 \
    enchant phar fileinfo intl \
    ffi \
%if %{with_tidy}
    tidy \
%endif
%if %{with_pspell}
    pspell \
%endif
    curl \
%if %{with_sodium}
    sodium \
%endif
    posix shmop sysvshm sysvsem sysvmsg xml \
    pdo pdo_mysql pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with_firebird}
    pdo_firebird \
%endif
%if %{with_freetds}
    pdo_dblib \
%endif
    xmlrpc xmlreader xmlwriter
do
    case $mod in
      opcache)
        # Zend extensions
        TESTCMD="$TESTCMD --define zend_extension=$mod"
        ini=10-${mod}.ini;;
      pdo_*|mysqli|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=20-${mod}.ini;;
    esac

    $TESTCMD --modules | grep -qi $mod

    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
%if %{with_zts}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
%endif
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini
%endif

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}-%{__isa_bits}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}-%{__isa_bits}/" \
    -e "s/@PHP_PDOVER@/%{pdover}-%{__isa_bits}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{_rpmmacrodir}/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
%if %{with_zts}
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
%endif
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.a \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%pre fpm
getent group php-fpm >/dev/null || groupadd -r php-fpm
getent passwd php-fpm >/dev/null || \
    useradd -r -g php-fpm -d %{_sharedstatedir}/php/fpm \
    -s /sbin/nologin -c "php-fpm" php-fpm
exit 0

%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

%postun fpm
%systemd_postun_with_restart php-fpm.service

%post   embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig


%files -n mod_%{name}
%{_httpd_moddir}/libphp7.so
%if %{with_zts}
%{_httpd_moddir}/libphp7-zts.so
%endif
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/mod_php
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/mod_php/session
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/mod_php/wsdlcache
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/mod_php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_httpd_modconfdir}/15-php.conf

%files common -f files.common
%doc EXTENSIONS NEWS UPGRADING* README.REDIST.BINS *md docs
%license LICENSE TSRM_LICENSE
%license libmagic_LICENSE
%license timelib_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_sharedstatedir}/php
%dir %{_sharedstatedir}/php/peclxml
%dir %{_datadir}/php
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl

%files cli
%{_bindir}/php
%if %{with_zts}
%{_bindir}/zts-php
%{_mandir}/man1/zts-php.1*
%endif
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*

%files dbg
%doc sapi/phpdbg/{README.md,CREDITS}
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with_zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif

%files fpm
%doc php-fpm.conf.default www.conf.default
%license fpm_LICENSE
%attr(0770,root,php-fpm) %dir %{_sharedstatedir}/php/fpm
%attr(0770,root,php-fpm) %dir %{_sharedstatedir}/php/fpm/session
%attr(0770,root,php-fpm) %dir %{_sharedstatedir}/php/fpm/wsdlcache
%attr(0770,root,php-fpm) %dir %{_sharedstatedir}/php/fpm/opcache
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%{_unitdir}/php-fpm.service
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %{_sysconfdir}/php-fpm.d
%attr(750,php-fpm,php-fpm) %dir %{_localstatedir}/log/php-fpm
%dir %ghost /run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%files fpm-nginx
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf

%files fpm-httpd
%config(noreplace) %{_httpd_confdir}/php-fpm.conf

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_bindir}/zts-phpize
%{_includedir}/php-zts
%{_libdir}/php-zts/build
%{_mandir}/man1/zts-php-config.1*
%{_mandir}/man1/zts-phpize.1*
%endif
%{_mandir}/man1/php-config.1*
%{_rpmmacrodir}/macros.php

%files embedded
%{_libdir}/libphp7.so
%{_libdir}/libphp7-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%if %{with_imap}
%files imap -f files.imap
%endif
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%files gd -f files.gd
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_LICENSE
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%if %{with_tidy}
%files tidy -f files.tidy
%endif
%if %{with_freetds}
%files pdo-dblib -f files.pdo_dblib
%endif
%if %{with_pspell}
%files pspell -f files.pspell
%endif
%files intl -f files.intl
%files process -f files.process
%if %{with_firebird}
%files pdo-firebird -f files.pdo_firebird
%endif
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
%files json -f files.json
%if %{with_sodium}
%files sodium -f files.sodium
%endif
%files ffi -f files.ffi
%dir %{_datadir}/php/preload


%changelog
* Fri Jun 10 2022 Peter Zelina <pzelina@qualityunit.com> - 7.4.30-1
- Latest upstream

* Thu Apr 14 2022 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.29-1
- Latest upstream

* Mon Feb 21 2022 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.28-1
- Latest upstream

* Fri Jan 14 2022 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.27-1
- Latest upstream

* Thu Nov 18 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.26-1
- Latest upstream

* Sun Oct 24 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.25-1
- Latest upstream

* Fri Sep 24 2021 Chris Barnett <chris.barnett@lexisnexisrisk.com> - 7.4.24-1
- Latest upstream

* Thu Sep 17 2021 James Watson <james.watson1@lexisnexisrisk.com> - 7.4.23-1
- Latest upstream

* Thu Jul 29 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.22-1
- Latest upstream

* Fri Jul  2 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.21-1
- Latest upstream

* Mon Jun  7 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.20-1
- Latest upstream

* Thu May  6 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.19-1
- Latest upstream

* Fri Apr 30 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.18-1
- Latest upstream

* Fri Mar  5 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.16-1
- Latest upstream

* Thu Feb  4 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.15-1
- Latest upstream

* Thu Jan  7 2021 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.14-1
- Latest upstream

* Tue Dec  1 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.13-1
- Latest upstream

* Thu Oct 29 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.12-1
- Latest upstream

* Thu Oct  1 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.11-1
- Latest upstream

* Thu Sep  3 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.10-1
- Latest upstream

* Thu Aug  6 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.9-1
- Latest upstream

* Thu Jul  9 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.8-1
- Latest upstream
- Drop configure.ac uname patch

* Wed Jul  1 2020 Jeff Sheltren <jeff@tag1consulting.com> - 7.4.7-1
- Latest upstream

* Thu Jun 04 2020 Remi Collet <remi@remirepo.net> - 7.4.6-3
- use php-config from embed SAPI to reduce used libs

* Mon May 18 2020 David Alger <davidmalger@gmail.com> - 7.4.6-2
- Reintroduce freetype, jpeg and xpm support in GD

* Mon May 18 2020 David Alger <davidmalger@gmail.com> - 7.4.6-1
- Latest upstream

* Sun Apr 26 2020 David Alger <davidmalger@gmail.com> - 7.4.5-1
- Latest upstream

* Thu Jan 23 2020 Matt Linscott <matt.linscott@gmail.com> - 7.4.2-1
- Latest upstream

* Fri Jan 03 2020 Matt Linscott <matt.linscott@gmail.com> - 7.4.1-1
- Latest upstream

* Mon Dec 23 2019 Matt Linscott <matt.linscott@gmail.com> - 7.4.0-4
- Fix curltls patch name since it was updated for 7.4.0

* Thu Dec 12 2019 Matt Linscott <matt.linscott@gmail.com> - 7.4.0-3
- Fix pdo-firebird and remove references to interbase

* Wed Dec 11 2019 Matt Linscott <matt.linscott@gmail.com> - 7.4.0-2
- Initial port from Fedora to IUS
- Use bundled pcre and gd
- Move httpd module to mod_php subpackage
- Add fpm-nginx and fpm-httpd subpackages
- Add patch49 to enable TLS 1.1/1.2 support
- Enable subpackages pdo-firebird, imap, pdo-dblib, sodium, pspell

* Wed Nov 27 2019 Remi Collet <remi@remirepo.net> - 7.4.0-1
- update to 7.4.0 GA

* Mon Nov 11 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC6-1
- update to 7.4.0RC6

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 7.4.0~RC5-2
- Rebuild for ICU 65

* Tue Oct 29 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC5-1
- update to 7.4.0RC5
- set opcache.enable_cli in provided default configuration
- add /usr/share/php/preload as default ffi.preload configuration

* Tue Oct 15 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-1
- update to 7.4.0RC4

* Mon Oct  7 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-2
- ensure all shared extensions can be loaded
- add patch from https://github.com/php/php-src/pull/4794
  to ensure opcache is always linked with librt

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-1
- update to 7.4.0RC3
- bump API version to 20190902
- drop wddx, recode and interbase extensions
- add ffi extension
- drop dependency on libargon2, use libsodium implementation
- run test suite using 4 concurrent workers
- cleanup unused conditional
- add upstream patch to fix aarch64 build

* Tue Sep 24 2019 Remi Collet <remi@remirepo.net> - 7.3.10-1
- Update to 7.3.10 - http://www.php.net/releases/7_3_10.php

* Wed Sep 11 2019 Remi Collet <remi@remirepo.net> - 7.3.10~RC1-2
- update to 7.3.10RC1 (new tag)

* Tue Sep 10 2019 Remi Collet <remi@remirepo.net> - 7.3.10~RC1-1
- update to 7.3.10RC1

* Wed Aug 28 2019 Remi Collet <remi@remirepo.net> - 7.3.9-1
- Update to 7.3.9 - http://www.php.net/releases/7_3_9.php
- add tarball signature check

* Tue Aug 20 2019 Petr Pisar <ppisar@redhat.com> - 7.3.9~RC1-2
- Rebuild against recode-3.7.2 (bug #1379055)

* Mon Aug 19 2019 Remi Collet <remi@remirepo.net> - 7.3.9~RC1-1
- update to 7.3.9RC1

* Tue Jul 30 2019 Remi Collet <remi@remirepo.net> - 7.3.8-1
- Update to 7.3.8 - http://www.php.net/releases/7_3_8.php

* Tue Jul 16 2019 Remi Collet <remi@remirepo.net> - 7.3.8~RC1-1
- update to 7.3.8RC1
- add upstream patch for #78297
- main package now recommends commonly used extensions
  (json, mbstring, opcache, pdo, xml)

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 7.3.7-2
- Update to 7.3.7 - http://www.php.net/releases/7_3_7.php
- disable opcache.huge_code_pages in default configuration

* Thu Jun 20 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC3-1
- update to 7.3.7RC3

* Tue Jun 18 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC2-1
- update to 7.3.7RC2

* Tue Jun 11 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC1-1
- update to 7.3.7RC1

* Tue May 28 2019 Remi Collet <remi@remirepo.net> - 7.3.6-1
- Update to 7.3.6 - http://www.php.net/releases/7_3_6.php

* Wed May 15 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-2
- update to 7.3.6RC1 (new tag)

* Tue May 14 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-1
- update to 7.3.6RC1

* Wed May  1 2019 Remi Collet <remi@remirepo.net> - 7.3.5-1
- Update to 7.3.5 - http://www.php.net/releases/7_3_5.php

* Tue Apr 16 2019 Remi Collet <remi@remirepo.net> - 7.3.5~RC1-1
- update to 7.3.5RC1

* Tue Apr  2 2019 Remi Collet <remi@remirepo.net> - 7.3.4-1
- Update to 7.3.4 - http://www.php.net/releases/7_3_4.php

* Thu Mar 21 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-3
- update to 7.3.4RC1 new tag
- add upstream patches for failed tests
- add build dependency on ps command

* Wed Mar 20 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-2
- revert upstream change for extension test suite

* Tue Mar 19 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-1
- update to 7.3.4RC1

* Mon Mar 18 2019 Remi Collet <remi@fedoraproject.org> - 7.3.3-2
- rebuild for libargon2 new soname

* Wed Mar  6 2019 Remi Collet <remi@remirepo.net> - 7.3.3-1
- Update to 7.3.3 - http://www.php.net/releases/7_3_3.php
- add upstream patch for OpenSSL 1.1.1b

* Tue Feb 19 2019 Remi Collet <remi@remirepo.net> - 7.3.3~RC1-1
- update to 7.3.3RC1
- adapt systzdata patch (v18)

* Wed Feb  6 2019 Remi Collet <remi@remirepo.net> - 7.3.2-1
- Update to 7.3.2 - http://www.php.net/releases/7_3_2.php

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2~RC1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 7.3.2~RC1-2
- Rebuild for ICU 63

* Tue Jan 22 2019 Remi Collet <remi@remirepo.net> - 7.3.2~RC1-1
- update to 7.3.2RC1
- update system tzdata patch for timelib 2018.01

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 7.3.1-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Jan  8 2019 Remi Collet <remi@remirepo.net> - 7.3.1-1
- Update to 7.3.1 - http://www.php.net/releases/7_3_1.php

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 7.3.1-0.1.RC1
- update to 7.3.1RC1

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 7.3.0-1
- update to 7.3.0 GA
- update FPM configuration from upstream

* Tue Nov 20 2018 Remi Collet <remi@remirepo.net> - 7.3.0~0.3.RC5
- update to 7.3.0RC6

* Tue Nov  6 2018 Remi Collet <remi@remirepo.net> - 7.3.0~0.2.RC5
- update to 7.3.0RC5

* Fri Nov  2 2018 Remi Collet <remi@remirepo.net> - 7.3.0-0.1.RC4
- rebuild

* Tue Oct 23 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc4-1
- update to 7.3.0RC4

* Tue Oct  9 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc3-1
- update to 7.3.0RC3

* Thu Oct  4 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc2-1
- update to 7.3.0RC2
- bump API numbers
- switch from libpcre to libpcre2
- temporarily disable pcre jit on s390x see https://bugzilla.redhat.com/1636032

* Wed Sep 26 2018 Remi Collet <remi@remirepo.net> - 7.2.11~RC1-1
- update to 7.2.11RC1

* Tue Sep 11 2018 Remi Collet <remi@remirepo.net> - 7.2.10-1
- Update to 7.2.10 - http://www.php.net/releases/7_2_10.php

* Tue Aug 28 2018 Remi Collet <remi@remirepo.net> - 7.2.10~RC1-1
- update to 7.2.10RC1

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 7.2.9-1
- Update to 7.2.9 - http://www.php.net/releases/7_2_9.php

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 7.2.8-2
- Rebuild for new net-snmp

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 7.2.8-1
- Update to 7.2.8 - http://www.php.net/releases/7_2_8.php

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.8~RC1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 7.2.8~RC1-3
- Rebuild for ICU 62

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-2
- FPM: add getallheaders, backported from 7.3

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-1
- update to 7.2.8RC1

* Wed Jun 20 2018 Remi Collet <remi@remirepo.net> - 7.2.7-1
- Update to 7.2.7 - http://www.php.net/releases/7_2_7.php
- drop -mstackrealign option, workaround to #1593144

* Wed Jun  6 2018 Remi Collet <remi@remirepo.net> - 7.2.7~RC1-1
- update to 7.2.7RC1

* Wed May 23 2018 Remi Collet <remi@remirepo.net> - 7.2.6-1
- Update to 7.2.6 - http://www.php.net/releases/7_2_6.php

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 7.2.6~RC1-1
- update to 7.2.6RC1

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 7.2.5-2
- Rebuild for ICU 61.1

* Tue Apr 24 2018 Remi Collet <remi@remirepo.net> - 7.2.5-1
- Update to 7.2.5 - http://www.php.net/releases/7_2_5.php

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 7.2.5~RC1-1
- update to 7.2.5RC1

* Tue Apr  3 2018 Remi Collet <remi@remirepo.net> - 7.2.4-2
- add upstream patch for oniguruma 6.8.1, FTBFS #1562583

* Sun Apr 01 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.2.4-2
- Rebuild against oniguruma 6.8.1

* Tue Mar 27 2018 Remi Collet <remi@remirepo.net> - 7.2.4-1
- Update to 7.2.4 - http://www.php.net/releases/7_2_4.php
- FPM: update default pool configuration for process.dumpable

* Wed Mar 21 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-3
- use systemd RuntimeDirectory instead of /etc/tmpfiles.d

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-2
- add file trigger to restart the php-fpm service
  when new pool or new extension installed #1556762

* Tue Mar 13 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-1
- update to 7.2.4RC1

* Wed Feb 28 2018 Remi Collet <remi@remirepo.net> - 7.2.3-1
- Update to 7.2.3 - http://www.php.net/releases/7_2_3.php
- FPM: revert pid file removal

* Wed Feb 21 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-4
- disable ZTS on RHEL

* Fri Feb 16 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-3
- disable pspell extension on RHEL
- improve devel dependencies

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-2
- rebuild for new tag and drop patch merged upstream
- drop ldconfig scriptlets

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-1
- update to 7.2.3RC1
- adapt systzdata, fixheader and ldap_r patches
- apply upstream patch for date ext

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Remi Collet <remi@remirepo.net> - 7.2.2-1
- Update to 7.2.2 - http://www.php.net/releases/7_2_2.php

* Mon Jan 29 2018 Remi Collet <rcollet@redhat.com> - 7.2.2~RC1-3
- disable interbase, imap, pdo_dblib and sodium on rhel

* Thu Jan 25 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-3
- undefine _strict_symbol_defs_build

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 7.2.2~RC1-2
- Rebuilt for switch to libxcrypt

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-1
- update to 7.2.2RC1
- define SOURCE_DATE_EPOCH for reproducible build

* Wed Jan  3 2018 Remi Collet <remi@remirepo.net> - 7.2.1-1
- Update to 7.2.1 - http://www.php.net/releases/7_2_1.php

* Wed Dec 13 2017 Remi Collet <remi@remirepo.net> - 7.2.1~RC1-1
- update to 7.2.1RC1

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 7.2.0-3
- Rebuild for ICU 60.1

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-2
- refresh patch for https://bugs.php.net/75514

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-1
- update to 7.2.0 GA
- add upstream patch for https://bugs.php.net/75514

* Tue Nov  7 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC6-1
- Update to 7.2.0RC6

* Wed Oct 25 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC5-1
- Update to 7.2.0RC5
- make php-fpm a weak dependency

* Wed Oct 18 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC4-2
- enable argon2 password hash

* Tue Oct 10 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC4-1
- Update to 7.2.0RC4

* Fri Sep 29 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC3-1
- Update to 7.2.0RC3
- drop mcrypt extension
- add sodium extension
- use system oniguruma
- drop .so suffix from ini files
- refresh configuration files from upstream

* Wed Sep 27 2017 Remi Collet <remi@fedoraproject.org> - 7.1.10-1
- Update to 7.1.10 - http://www.php.net/releases/7_1_10.php

* Mon Sep 25 2017 Remi Collet <remi@fedoraproject.org> - 7.1.10~RC1-2
- php now requires php-fpm and start it with httpd / nginx

* Wed Sep 13 2017 Remi Collet <remi@fedoraproject.org> - 7.1.10~RC1-1
- Update to 7.1.10RC1

* Wed Sep  6 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9-2
- Automatically load OpenSSL configuration file, from PHP 7.2

* Wed Aug 30 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9-1
- Update to 7.1.9 - http://www.php.net/releases/7_1_9.php

* Wed Aug 16 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9~RC1-1
- Update to 7.1.9RC1
- php-fpm: drop unneeded "pid" from default configuration

* Wed Aug  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8-1
- Update to 7.1.8 - http://www.php.net/releases/7_1_8.php

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.8~RC1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8~RC1-1
- Update to 7.1.8RC1

* Tue Jul 18 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7-2
- disable httpd MPM check

* Thu Jul  6 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7-1
- Update to 7.1.7 - http://www.php.net/releases/7_1_7.php

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7~RC1-1
- Update to 7.1.7RC1

* Wed Jun  7 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6-1
- Update to 7.1.6 - http://www.php.net/releases/7_1_6.php
- add upstream security patches for oniguruma

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6~RC1-1
- Update to 7.1.6RC1

* Tue May  9 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-1
- Update to 7.1.5 - http://www.php.net/releases/7_1_5.php

* Sat May  6 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-0.3.RC1
- enable PHP execution of .phar files, see #1117140

* Thu Apr 27 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-0.2.RC1
- new sources from new tag

* Tue Apr 25 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-0.1.RC1
- Update to 7.1.5RC1

* Tue Apr 11 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-1
- Update to 7.1.4 - http://www.php.net/releases/7_1_4.php

* Wed Mar 29 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-0.1.RC1
- Update to 7.1.4RC1

* Wed Mar 22 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-3
- timelib is MIT license

* Wed Mar 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-2
- remove %%attr, see #1432372

* Wed Mar 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-1
- Update to 7.1.3 - http://www.php.net/releases/7_1_3.php

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> 7.1.3-0.1.RC1
- Update to 7.1.3RC1

* Wed Feb 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-1
- Update to 7.1.2 - http://www.php.net/releases/7_1_2.php

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.2-0.2.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-0.2.RC1
- Update to 7.1.2RC1 (new sources)

* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> 7.1.2-0.1.RC1
- Update to 7.1.2RC1

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-1
- Update to 7.1.1 - http://www.php.net/releases/7_1_1.php

* Fri Jan  6 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-0.1.RC1
- Update to 7.1.1RC1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-1
- Update to 7.1.0 - http://www.php.net/releases/7_1_0.php

* Fri Nov 25 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.3.RC6
- disable pcre.jit everywhere as it raise AVC #1398474
- sync provided configuration with upstream production defaults

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.2.RC6
- re-enable interbase sub package
  see http://bugzilla.redhat.com/1394750 sub package inconsistency
- add patch to fix firebird include path (using fb_config)

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.1.RC6
- Update to 7.1.0RC6
- update tzdata patch to v14, improve check for valid tz file
- disable interbase sub package (interbase and pdo_firebird)

* Tue Oct 11 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.1.RC3
- Update to 7.1.0RC3

* Wed Sep 28 2016 Remi Collet <remi@fedoraproject.org> 7.0.12-0.1.RC1
- Update to 7.0.12RC1

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> 7.0.11-1
- Update to 7.0.11 - http://www.php.net/releases/7_0_11.php

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> 7.0.11-0.1.RC1
- Update to 7.0.11RC1

* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> 7.0.10-1
- Update to 7.0.10 - http://www.php.net/releases/7_0_10.php

* Wed Aug  3 2016 Remi Collet <remi@fedoraproject.org> 7.0.10-0.1.RC1
- Update to 7.0.10RC1

* Wed Jul 20 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-1
- Update to 7.0.9 - http://www.php.net/releases/7_0_9.php
- wddx: add upstream patch for https://bugs.php.net/72564

* Wed Jul  6 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-0.1.RC1
- Update to 7.0.9RC1

* Thu Jun 30 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-2
- own tests/doc directories for pecl packages #1351345

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-1
- Update to 7.0.8 - http://www.php.net/releases/7_0_8.php
- https://fedoraproject.org/wiki/Changes/php70
- drop ereg, mysql, mssql extensions
- add json extension

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> 5.6.23-1
- Update to 5.6.23 - http://www.php.net/releases/5_6_23.php

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> 5.6.23-0.1.RC1
- update to 5.6.23RC1

* Fri May 27 2016 Remi Collet <remi@fedoraproject.org> 5.6.22-2
- drop unneeded option --with-vpx-dir, fix FTBFS, thanks Koschei

* Thu May 26 2016 Remi Collet <remi@fedoraproject.org> 5.6.22-1
- Update to 5.6.22 - http://www.php.net/releases/5_6_22.php

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> 5.6.22-0.1.RC1
- update to 5.6.22RC1

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> 5.6.21-1
- Update to 5.6.21
  http://www.php.net/releases/5_6_21.php

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> 5.6.21-0.2.RC1
- rebuild for ICU 57.1

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> 5.6.21-0.1.RC1
- update to 5.6.21RC1

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 5.6.20-1.1
- rebuild for ICU 57.1

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> 5.6.20-1
- Update to 5.6.20
  http://www.php.net/releases/5_6_20.php

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> 5.6.20-0.1.RC1
- update to 5.6.20RC1

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> 5.6.19-1
- Update to 5.6.19
  http://www.php.net/releases/5_6_19.php

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> 5.6.19-0.1.RC1
- update to 5.6.19RC1

* Tue Feb  9 2016 Remi Collet <remi@fedoraproject.org> 5.6.18-2
- define %%pecl_xmldir and own it (/var/lib/php/peclxml)

* Wed Feb  3 2016 Remi Collet <remi@fedoraproject.org> 5.6.18-1
- Update to 5.6.18
  http://www.php.net/releases/5_6_18.php

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> 5.6.18-0.1.RC1
- update to 5.6.18RC1

* Thu Jan  7 2016 Remi Collet <remi@fedoraproject.org> 5.6.17-1
- Update to 5.6.17
  http://www.php.net/releases/5_6_17.php

* Thu Dec 10 2015 Remi Collet <remi@fedoraproject.org> 5.6.17-0.1.RC1
- update to 5.6.17RC1

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> 5.6.16-2
- rebuild for libvpx 1.5.0

* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> 5.6.16-1
- Update to 5.6.16
  http://www.php.net/releases/5_6_16.php

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.16-0.2.RC2
- rebuild (tidy)

* Thu Nov 12 2015 Remi Collet <remi@fedoraproject.org> 5.6.16-0.1.RC1
- update to 5.6.16RC1

* Thu Oct 29 2015 Remi Collet <remi@fedoraproject.org> 5.6.15-1
- Update to 5.6.15
  http://www.php.net/releases/5_6_15.php
- php-config: reports all built sapis

* Thu Oct 15 2015 Remi Collet <remi@fedoraproject.org> 5.6.15-0.1.RC1
- update to 5.6.15RC1

* Wed Sep 30 2015 Remi Collet <remi@fedoraproject.org> 5.6.14-1
- Update to 5.6.14
  http://www.php.net/releases/5_6_14.php
- php-fpm: enable http authorization headers

* Thu Sep 17 2015 Remi Collet <remi@fedoraproject.org> 5.6.14-0.1.RC1
- update to 5.6.14RC1

* Thu Sep  3 2015 Remi Collet <remi@fedoraproject.org> 5.6.13-1
- Update to 5.6.13
  http://www.php.net/releases/5_6_13.php

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> 5.6.12-1
- Update to 5.6.12
  http://www.php.net/releases/5_6_12.php

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> 5.6.12-0.1.RC1
- update to 5.6.12RC1

* Fri Jul 17 2015 Remi Collet <remi@fedoraproject.org> 5.6.11-2
- fix typo in php.conf #1244104

* Sun Jul 12 2015 Remi Collet <remi@fedoraproject.org> 5.6.11-1
- Update to 5.6.11
  http://www.php.net/releases/5_6_11.php

* Thu Jun 25 2015 Remi Collet <remi@fedoraproject.org> 5.6.11-0.1.RC1
- update to 5.6.11RC1
- the phar link is now correctly created

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.10-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-1
- Update to 5.6.10
  http://www.php.net/releases/5_6_10.php
- add explicit spec license (implicit by FPCA)

* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-0.1.RC1
- update to 5.6.10RC1
- opcache is now 7.0.6-dev

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> 5.6.9-1
- Update to 5.6.9
  http://www.php.net/releases/5_6_9.php

* Thu Apr 30 2015 Remi Collet <remi@fedoraproject.org> 5.6.9-0.1.RC1
- update to 5.6.9RC1
- adapt systzdata patch for upstream changes for new zic

* Thu Apr 16 2015 Remi Collet <remi@fedoraproject.org> 5.6.8-1
- Update to 5.6.8
  http://www.php.net/releases/5_6_8.php

* Fri Apr 10 2015 Remi Collet <remi@fedoraproject.org> 5.6.8-0.3.RC1
- add upstream patch to drop SSLv3 tests

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 5.6.8-0.2.RC1
- rebuild for libvpx 1.4.0

* Wed Apr  1 2015 Remi Collet <remi@fedoraproject.org> 5.6.8-0.1.RC1
- update to 5.6.8RC1

* Fri Mar 20 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-2
- Update to 5.6.7
  http://www.php.net/releases/5_6_7.php

* Sun Mar  8 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-1
- update to 5.6.7RC1

* Thu Feb 19 2015 Remi Collet <remi@fedoraproject.org> 5.6.6-1
- Update to 5.6.6
  http://www.php.net/releases/5_6_6.php

* Thu Feb  5 2015 Remi Collet <rcollet@redhat.com> 5.6.6-0.1.RC1
- php 5.6.6RC1 for Koschei

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.6.5-2
- rebuild for ICU 54.1

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-1
- Update to 5.6.5
  http://www.php.net/releases/5_6_5.php
- drop deprecated php-fpm EnvironmentFile

* Fri Jan  9 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-0.1.RC1
- update to 5.6.5RC1
- FPM: enable ACL support for Unix Domain Socket
- FPM: switch default configuration to use UDS

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-2
- Update to 5.6.4 (real)
  http://www.php.net/releases/5_6_4.php
- php-xmlrpc requires php-xml

* Wed Dec 10 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-1
- Update to 5.6.4
  http://www.php.net/releases/5_6_4.php

* Fri Nov 28 2014 Remi Collet <rcollet@redhat.com> 5.6.4-0.1.RC1
- php 5.6.4RC1

* Mon Nov 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-4
- FPM: add upstream patch for https://bugs.php.net/68428
  listen.allowed_clients is IPv4 only

* Mon Nov 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-3
- sync php-fpm configuration with upstream
- refresh upstream patch for 68421

* Sun Nov 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-2
- FPM: add upstream patch for https://bugs.php.net/68421
  access.format=R doesn't log ipv6 address
- FPM: add upstream patch for https://bugs.php.net/68420
  listen=9000 listens to ipv6 localhost instead of all addresses
- FPM: add upstream patch for https://bugs.php.net/68423
  will no longer load all pools

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-1
- Update to PHP 5.6.3
  http://php.net/releases/5_6_3.php

* Fri Oct 31 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.2.RC1
- php 5.6.3RC1 (refreshed, phpdbg changes reverted)
- new version of systzdata patch, fix case sensitivity
- ignore Factory in date tests

* Wed Oct 29 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.1.RC1
- php 5.6.3RC1
- disable opcache.fast_shutdown in default config
- enable phpdbg_webhelper new extension (in php-dbg)

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.2
  http://php.net/releases/5_6_2.php

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.1
  http://php.net/releases/5_6_1.php
- use default system cipher list by Fedora policy
  http://fedoraproject.org/wiki/Changes/CryptoPolicy

* Wed Sep 24 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.2.RC1
- provides nginx configuration (see #1142298)

* Sat Sep 13 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.1.RC1
- php 5.6.1RC1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1
- PHP 5.6.0 is GA
  http://php.net/releases/5_6_0.php
- fix ZTS man pages, upstream patch for 67878
- provides php(httpd)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.0-0.7.RC4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.6.RC4
- php 5.6.0RC4

* Thu Jul 31 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.5.RC3
- fpm requires httpd >= 2.4.10 for proxy support in SetHandler

* Thu Jul 31 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.4.RC3
- php 5.6.0RC3
- cleanup with_libmysql
- fix licenses handling
- fix zts-php-config --php-binary output #1124605
- provide php.conf with php-fpm, allow apache + fpm
  to work with default configuration, without mod_php

* Mon Jul  7 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.3.RC2
- php 5.6.0RC2

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.2.RC1
- fix phpdbg with libedit https://bugs.php.net/67499
- add workaround for unserialize/mock issue from 5.4/5.5

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.1.RC1
- php 5.6.0RC1
  https://fedoraproject.org/wiki/Changes/Php56
- add php-dbg subpackage
- update php.ini and opcache.ini from upstream production template
- move zts-php to php-cli

* Thu Jun  5 2014 Remi Collet <rcollet@redhat.com> 5.5.13-3
- fix regression introduce in fix for #67118

* Tue Jun  3 2014 Remi Collet <remi@fedoraproject.org> 5.5.13-2
- fileinfo: fix insufficient boundary check
- workaround regression introduce in fix for 67072 in
  serialize/unzerialize functions

* Fri May 30 2014 Remi Collet <rcollet@redhat.com> 5.5.13-1
- Update to 5.5.13
  http://www.php.net/releases/5_5_13.php
- sync php.ini with upstream php.ini-production

* Sat May  3 2014 Remi Collet <rcollet@redhat.com> 5.5.12-1
- Update to 5.5.12
  http://www.php.net/releases/5_5_12.php
- php-fpm: change default unix socket permission CVE-2014-0185

* Wed Apr 23 2014 Remi Collet <rcollet@redhat.com> 5.5.11-2
- add numerical prefix to extension configuration files
- prevent .user.ini files from being viewed by Web clients
- load php directives only when mod_php is active

* Thu Apr  3 2014 Remi Collet <rcollet@redhat.com> 5.5.11-1
- Update to 5.5.11
  http://www.php.net/ChangeLog-5.php#5.5.11

* Thu Mar  6 2014 Remi Collet <rcollet@redhat.com> 5.5.10-1
- Update to 5.5.10
  http://www.php.net/ChangeLog-5.php#5.5.10
- php-fpm should own /var/lib/php/session and wsdlcache
- fix pcre test results with libpcre < 8.34

* Tue Feb 18 2014 Remi Collet <rcollet@redhat.com> 5.5.9-2
- upstream patch for https://bugs.php.net/66731

* Thu Feb 13 2014 Remi Collet <remi@fedoraproject.org> 5.5.9-1.1
- rebuild

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> 5.5.9-1
- Update to 5.5.9
  http://www.php.net/ChangeLog-5.php#5.5.9
- Install macros to /usr/lib/rpm/macros.d

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 5.5.8-2
- fix _httpd_mmn expansion in absence of httpd-devel

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-1
- update to 5.5.8
- drop conflicts with other opcode caches as both can
  be used only for user data cache

* Wed Dec 11 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1
- update to 5.5.7, fix for CVE-2013-6420
- fix zend_register_functions breaks reflection, php bug 66218
- fix Heap buffer over-read in DateInterval, php bug 66060
- fix fix overflow handling bug in non-x86

* Wed Nov 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-1
- update to 5.5.6

* Thu Oct 17 2013 Remi Collet <rcollet@redhat.com> - 5.5.5-1
- update to 5.5.5
- sync php.ini with upstream

* Thu Sep 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-1
- update to 5.5.4
- improve security, use specific soap.wsdl_cache_dir
  use /var/lib/php/wsdlcache for mod_php and php-fpm
- sync short_tag comments in php.ini with upstream

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-1
- update to 5.5.3
- fix typo and add missing entries in php.ini
- drop zip extension

* Mon Aug 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.2-1
- update to 5.5.2, fixes for CVE-2011-4718 + CVE-2013-4248

* Thu Aug 08 2013 Remi Collet <rcollet@redhat.com> - 5.5.1-3
- improve system libzip patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Remi Collet <rcollet@redhat.com> - 5.5.1-1
- update to 5.5.1
- add Provides: php(pdo-abi), for consistency with php(api)
  and php(zend-abi)
- improved description for mod_php
- fix opcache ZTS configuration (blacklists in /etc/php-zts.d)
- add missing man pages (phar, php-cgi)

* Fri Jul 12 2013 Remi Collet <rcollet@redhat.com> - 5.5.0-2
- add security fix for CVE-2013-4113
- add missing ASL 1.0 license
- 32k stack size seems ok for tests on both 32/64bits build

* Thu Jun 20 2013 Remi Collet <rcollet@redhat.com> 5.5.0-1
- update to 5.5.0 final

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.11.RC3
- also drop JSON from sources
- clean conditional for JSON (as removed from the sources)
- clean conditional for FPM (always build)

* Thu Jun 13 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.10.RC3
- drop JSON extension

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.9.RC3
- build with system GD >= 2.1.0

* Thu Jun  6 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.8.RC3
- update to 5.5.0RC3

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.7.RC2
- update to 5.5.0RC2
- add missing options in php-fpm.conf
- run php-fpm in systemd notify mode
- /etc/syconfig/php-fpm is deprecated (still used)
- add /systemd/system/php-fpm.service.d

* Wed May  8 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.6.RC1
- update to 5.5.0RC1
- remove reference to apache in some sub-packages description
- add option to disable json extension
- drop most (very old) "Obsoletes", add version to others

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.5.beta4
- update to 5.5.0beta4
- zend_extension doesn't requires full path
- refresh patch for system libzip
- drop opcache patch merged upstream
- add BuildRequires libvpx-devel for WebP support in php-gd
- php-fpm own /usr/share/fpm

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.4.beta3
- update to 5.5.0beta3
- allow wildcard in opcache.blacklist_filename and provide
  default /etc/php.d/opcache-default.blacklist
- clean spec, use only spaces (no tab)

* Thu Apr  4 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.3.beta2
- clean old deprecated options

* Thu Mar 28 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.2.beta2
- update to 5.5.0beta2
- Zend Optimizer+ renamed to Zend OPcache
- sync provided configuration with upstream

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.1.beta1
- update to 5.5.0beta1
  http://fedoraproject.org/wiki/Features/Php55
- new Zend OPcache extension in php-opccache new sub-package
- don't display XFAIL tests in report
- use xz compressed tarball
- build simplexml and xml extensions shared (moved in php-xml)
- build bz2, calendar, ctype, exif, ftp, gettext, iconv
  sockets and tokenizer extensions shared (in php-common)
- build gmp extension shared (in php-gmp new sub-package)
- build shmop extension shared (moved in php-process)
- drop some old compatibility provides (php-api, php-zend-abi, php-pecl-*)

* Thu Mar 14 2013 Remi Collet <rcollet@redhat.com> 5.4.13-1
- update to 5.4.13
- security fix for CVE-2013-1643
- Hardened build (links with -z now option)

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> -  5.4.13-0.2.RC1
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Thu Feb 28 2013 Remi Collet <rcollet@redhat.com> 5.4.13-0.1.RC1
- update to 5.4.13RC1
- drop patches merged upstream

* Sat Feb 23 2013 Karsten Hopp <karsten@redhat.com> 5.4.12-4
- add support for ppc64p7 arch (Power7 optimized)

* Thu Feb 21 2013 Remi Collet <rcollet@redhat.com> 5.4.12-3
- make ZTS build optional (still enabled)

* Wed Feb 20 2013 Remi Collet <rcollet@redhat.com> 5.4.12-2
- make php-mysql package optional and disabled

* Wed Feb 20 2013 Remi Collet <remi@fedoraproject.org> 5.4.12-1
- update to 5.4.12
- security fix for CVE-2013-1635
- drop gdbm because of license incompatibility

* Wed Feb 13 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.6.RC2
- enable tokyocabinet and gdbm dba handlers

* Wed Feb 13 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.5.RC2
- update to 5.4.12RC2

* Mon Feb 11 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.4.RC1
- upstream patch (5.4.13) to fix dval to lval conversion
  https://bugs.php.net/64142

* Mon Feb  4 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.3.RC1
- upstream patch (5.4.13) for 2 failed tests

* Fri Feb  1 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.2.RC1
- fix buit-in web server on ppc64 (fdset usage)
  https://bugs.php.net/64128

* Thu Jan 31 2013 Remi Collet <rcollet@redhat.com> 5.4.12-0.1.RC1
- update to 5.4.12RC1

* Mon Jan 28 2013 Remi Collet <rcollet@redhat.com> 5.4.11-3
- rebuild for new libicu

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 5.4.11-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Remi Collet <rcollet@redhat.com> 5.4.11-1
- update to 5.4.11

* Thu Jan 10 2013 Remi Collet <rcollet@redhat.com> 5.4.11-0.2.RC1
- fix php.conf to allow MultiViews managed by php scripts

* Thu Jan 10 2013 Remi Collet <rcollet@redhat.com> 5.4.11-0.1.RC1
- update to 5.4.11RC1

* Wed Dec 19 2012 Remi Collet <rcollet@redhat.com> 5.4.10-1
- update to 5.4.10
- remove patches merged upstream

* Tue Dec 11 2012 Remi Collet <rcollet@redhat.com> 5.4.9-3
- drop "Configure Command" from phpinfo output

* Tue Dec 11 2012 Joe Orton <jorton@redhat.com> - 5.4.9-2
- prevent php_config.h changes across (otherwise identical) rebuilds

* Thu Nov 22 2012 Remi Collet <rcollet@redhat.com> 5.4.9-1
- update to 5.4.9

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.5.RC1
- switch back to upstream generated scanner/parser

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.4.RC1
- use _httpd_contentdir macro and fix php.gif path

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.3.RC1
- improve system libzip patch to use pkg-config

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.2.RC1
- use _httpd_moddir macro

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- improves php.conf (use FilesMatch + SetHandler)
- improves filter (httpd module)
- apply ldap_r patch on fedora >= 18 only

* Fri Nov  9 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- clarify Licenses
- missing provides xmlreader and xmlwriter
- modernize spec
- change php embedded library soname version to 5.4

* Tue Nov  6 2012 Remi Collet <rcollet@redhat.com> 5.4.8-5
- fix _httpd_mmn macro definition

* Mon Nov  5 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix mysql_sock macro definition

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- fix installed headers

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 5.4.8-2
- use libldap_r for ldap extension

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-1
- update to 5.4.8
- define both session.save_handler and session.save_path
- fix possible segfault in libxml (#828526)
- php-fpm: create apache user if needed
- use SKIP_ONLINE_TEST during make test
- php-devel requires pcre-devel and php-cli (instead of php)

* Fri Oct  5 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-11
- provides php-phar
- update systzdata patch to v10, timezone are case insensitive

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-10
- fix typo in systemd macro

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-9
- php-fpm: enable PrivateTmp
- php-fpm: new systemd macros (#850268)
- php-fpm: add upstream patch for startup issue (#846858)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 5.4.7-8
- systemd integration, https://bugs.php.net/63085
- no odbc call during timeout, https://bugs.php.net/63171
- check sqlite3_column_table_name, https://bugs.php.net/63149

* Mon Sep 24 2012 Remi Collet <rcollet@redhat.com> 5.4.7-7
- most failed tests explained (i386, x86_64)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-6
- fix for http://bugs.php.net/63126 (#783967)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-5
- patch to ensure we use latest libdb (not libdb4)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- really fix rhel tests (use libzip and libdb)

* Tue Sep 18 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- fix test to enable zip extension on RHEL-7

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-2
- remove session.save_path from php.ini
  move it to apache and php-fpm configuration files

* Fri Sep 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-1
- update to 5.4.7
  http://www.php.net/releases/5_4_7.php
- php-fpm: don't daemonize

* Mon Aug 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-2
- enable php-fpm on secondary arch (#849490)

* Fri Aug 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-1
- update to 5.4.6
- update to v9 of systzdata patch
- backport fix for new libxml

* Fri Jul 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.5-1
- update to 5.4.5

* Mon Jul 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-4
- also provide php(language)%%{_isa}
- define %%{php_version}

* Mon Jul 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-3
- drop BR for libevent (#835671)
- provide php(language) to allow version check

* Thu Jun 21 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-2
- add missing provides (core, ereg, filter, standard)

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-1
- update to 5.4.4 (CVE-2012-2143, CVE-2012-2386)
- use /usr/lib/tmpfiles.d instead of /etc/tmpfiles.d
- use /run/php-fpm instead of /var/run/php-fpm

* Wed May 09 2012 Remi Collet <remi@fedoraproject.org> 5.4.3-1
- update to 5.4.3 (CVE-2012-2311, CVE-2012-2329)

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> 5.4.2-1
- update to 5.4.2 (CVE-2012-1823)

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-1
- update to 5.4.1

* Wed Apr 25 2012 Joe Orton <jorton@redhat.com> - 5.4.0-6
- rebuild for new icu
- switch (conditionally) to libdb-devel

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-5
- fix Loadmodule with MPM event (use ZTS if not MPM worker)
- split conf.d/php.conf + conf.modules.d/10-php.conf with httpd 2.4

* Thu Mar 29 2012 Joe Orton <jorton@redhat.com> - 5.4.0-4
- rebuild for missing automatic provides (#807889)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-3
- really use _httpd_mmn

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-2
- rebuild against httpd 2.4
- use _httpd_mmn, _httpd_apxs macros

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1
- update to PHP 5.4.0 finale

* Sat Feb 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.4.RC8
- update to PHP 5.4.0RC8

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.3.RC7
- update to PHP 5.4.0RC7
- provides env file for php-fpm (#784770)
- add patch to use system libzip (thanks to spot)
- don't provide INSTALL file

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.2.RC6
- all binaries in /usr/bin with zts prefix

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.1.RC6
- update to PHP 5.4.0RC6
  https://fedoraproject.org/wiki/Features/Php54

* Sun Jan 08 2012 Remi Collet <remi@fedoraproject.org> 5.3.8-4.4
- fix systemd unit

* Mon Dec 12 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-4.3
- switch to systemd

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 5.3.8-4.2
- Rebuild for new libpng

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.3.8-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 5.3.8-3.1
- rebuild with new gmp

* Wed Sep 28 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-3
- revert is_a() to php <= 5.3.6 behavior (from upstream)
  with new option (allow_string) for new behavior

* Tue Sep 13 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-2
- add mysqlnd sub-package
- drop patch4, use --libdir to use /usr/lib*/php/build
- add patch to redirect mysql.sock (in mysqlnd)

* Tue Aug 23 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-1
- update to 5.3.8
  http://www.php.net/ChangeLog-5.php#5.3.8

* Thu Aug 18 2011 Remi Collet <remi@fedoraproject.org> 5.3.7-1
- update to 5.3.7
  http://www.php.net/ChangeLog-5.php#5.3.7
- merge php-zts into php (#698084)

* Tue Jul 12 2011 Joe Orton <jorton@redhat.com> - 5.3.6-4
- rebuild for net-snmp SONAME bump

* Mon Apr  4 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-3
- enable mhash extension (emulated by hash extension)

* Wed Mar 23 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-2
- rebuild for new MySQL client library

* Thu Mar 17 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-1
- update to 5.3.6
  http://www.php.net/ChangeLog-5.php#5.3.6
- fix php-pdo arch specific requires

* Tue Mar 15 2011 Joe Orton <jorton@redhat.com> - 5.3.5-6
- disable zip extension per "No Bundled Libraries" policy (#551513)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> 5.3.5-5
- rebuild for icu 4.6

* Mon Feb 28 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-4
- fix systemd-units requires

* Thu Feb 24 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-3
- add tmpfiles.d configuration for php-fpm
- add Arch specific requires/provides

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-1
- update to 5.3.5
  http://www.php.net/ChangeLog-5.php#5.3.5
- clean duplicate configure options

* Tue Dec 28 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-2
- rebuild against MySQL 5.5.8
- remove all RPM_SOURCE_DIR

* Sun Dec 12 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-1.1
- security patch from upstream for #660517

* Sat Dec 11 2010 Remi Collet <Fedora@famillecollet.com> 5.3.4-1
- update to 5.3.4
  http://www.php.net/ChangeLog-5.php#5.3.4
- move phpize to php-cli (see #657812)

* Wed Dec  1 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-5
- ghost /var/run/php-fpm (see #656660)
- add filter_setup to not provides extensions as .so

* Mon Nov  1 2010 Joe Orton <jorton@redhat.com> - 5.3.3-4
- use mysql_config in libdir directly to avoid biarch build failures

* Fri Oct 29 2010 Joe Orton <jorton@redhat.com> - 5.3.3-3
- rebuild for new net-snmp

* Sun Oct 10 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-2
- add php-fpm sub-package

* Thu Jul 22 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-1
- PHP 5.3.3 released

* Fri Apr 30 2010 Remi Collet <Fedora@famillecollet.com> 5.3.2-3
- garbage collector upstream  patches (#580236)

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> 5.3.2-2
- rebuild for icu 4.4

* Sat Mar 06 2010 Remi Collet <Fedora@famillecollet.com> 5.3.2-1
- PHP 5.3.2 Released!
- remove mime_magic option (now provided by fileinfo, by emu)
- add patch for http://bugs.php.net/50578
- remove patch for libedit (upstream)
- add runselftest option to allow build without test suite

* Fri Nov 27 2009 Joe Orton <jorton@redhat.com> - 5.3.1-3
- update to v7 of systzdata patch

* Wed Nov 25 2009 Joe Orton <jorton@redhat.com> - 5.3.1-2
- fix build with autoconf 2.6x

* Fri Nov 20 2009 Remi Collet <Fedora@famillecollet.com> 5.3.1-1
- update to 5.3.1
- remove openssl patch (merged upstream)
- add provides for php-pecl-json
- add prod/devel php.ini in doc

* Tue Nov 17 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 5.3.0-7
- use libedit instead of readline to resolve licensing issues

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 5.3.0-6
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Joe Orton <jorton@redhat.com> 5.3.0-4
- rediff systzdata patch

* Thu Jul 16 2009 Joe Orton <jorton@redhat.com> 5.3.0-3
- update to v6 of systzdata patch; various fixes

* Tue Jul 14 2009 Joe Orton <jorton@redhat.com> 5.3.0-2
- update to v5 of systzdata patch; parses zone.tab and extracts
  timezone->{country-code,long/lat,comment} mapping table

* Sun Jul 12 2009 Remi Collet <Fedora@famillecollet.com> 5.3.0-1
- update to 5.3.0
- remove ncurses, dbase, mhash extensions
- add enchant, sqlite3, intl, phar, fileinfo extensions
- raise sqlite version to 3.6.0 (for sqlite3, build with --enable-load-extension)
- sync with upstream "production" php.ini

* Sun Jun 21 2009 Remi Collet <Fedora@famillecollet.com> 5.2.10-1
- update to 5.2.10
- add interbase sub-package

* Sat Feb 28 2009 Remi Collet <Fedora@FamilleCollet.com> - 5.2.9-1
- update to 5.2.9

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  5 2009 Joe Orton <jorton@redhat.com> 5.2.8-9
- add recode support, -recode subpackage (#106755)
- add -zts subpackage with ZTS-enabled build of httpd SAPI
- adjust php.conf to use -zts SAPI build for worker MPM

* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 5.2.8-8
- fix patch fuzz, renumber patches

* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 5.2.8-7
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
