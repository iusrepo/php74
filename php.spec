# HTML cgi-bin directory exists under
#
%define contentdir /var/www


# Language sets that we bundle with php
#
%define manual_langs en pt_BR cs nl fr de hu it ja ko es tr


# For those willing to recompile with Oracle libraries
# for the oracle extension
# (ie rpm --rebuild --define 'oracle 1' php4.1.2-x.src.rpm)
#
%{!?oracle:%define oracle 0}


# When we're testing, we don't want all the manuals thank you
# (ie rpm --rebuild --define 'manuals 1' php4.1.2-x.src.rpm)
#
%{!?manuals:%define manuals 1}


# RPM Informational headers
#
Summary: The PHP HTML-embedded scripting language. (PHP: Hypertext Preprocessor)
Name: php
Version: 4.1.2
Release: 7.3.6
License: The PHP License, version 2.02
Group: Development/Languages
URL: http://www.php.net/


# The one true source and manuals
#
Source0: http://www.php.net/distributions/php-%{version}.tar.gz
%if %{manuals}
Source1: http://www.php.net/distributions/manual/php_manual_en.tar.bz2
Source2: http://www.php.net/distributions/manual/php_manual_pt_BR.tar.bz2
Source3: http://www.php.net/distributions/manual/php_manual_cs.tar.bz2
Source4: http://www.php.net/distributions/manual/php_manual_nl.tar.bz2
Source5: http://www.php.net/distributions/manual/php_manual_fr.tar.bz2
Source6: http://www.php.net/distributions/manual/php_manual_de.tar.bz2
Source7: http://www.php.net/distributions/manual/php_manual_hu.tar.bz2
Source8: http://www.php.net/distributions/manual/php_manual_it.tar.bz2
Source9: http://www.php.net/distributions/manual/php_manual_ja.tar.bz2
Source10: http://www.php.net/distributions/manual/php_manual_ko.tar.bz2
Source11: http://www.php.net/distributions/manual/php_manual_es.tar.bz2
Source12: http://www.php.net/distributions/manual/php_manual_tr.tar.bz2
%endif


# Patchs 
#
# Patch for https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=58801
Patch0: php-4.1.1-domxml.patch
# Patch for https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=60515
Patch1: php-4.1.2-mysql-path.patch
# Patch to tweak the default php.ini
Patch2: php-4.1.2-php.ini-dist.patch
# Patch in repsonse to bugzilla entry #60855
Patch3: php-4.1.2-bug-60855.patch
# Patch to enhance the mysql extension #64104
Patch4: php-4.1.2-mysql-4.2.1.patch
# Security fixes for CAN-2002-0985, CAN-2002-0986
Patch5: php-4.1.2-mailsec.patch


# Where are we going to build the install set to?
#
BuildRoot: %{_tmppath}/%{name}-root
ExclusiveArch: i386

# Kill off some old history that we no longer wish to see
#
Obsoletes: mod_php, php3, phpfi, php-dbg


# Ok, you wanna build it, you gotta have these packages around
# From: ldd /usr/bin/php | sort | cut -f 1 -d ' '
#       | xargs rpm -q --whatprovides | sort -u )
# That said, BuildRequires should be -devel packages where
# -devel packages exist as they generally have the header files
# associated with the libraries required. As a general rule of
# thumb, specifying a -devel package will always drag in the
# main package as well
#
BuildRequires: bzip2-devel
BuildRequires: curl-devel
BuildRequires: db3-devel
BuildRequires: expat-devel
BuildRequires: freetype-devel
BuildRequires: gd-devel
BuildRequires: gdbm-devel
BuildRequires: gmp-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: libxml2-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: pspell-devel
BuildRequires: apache-devel

# To install, you must be /this/ high...
# Basically it's a list of items php itself during the build doesn't
# directly touch eg fileutils for mkdir, perl for the install scripts
# etc.
#
BuildPrereq: bzip2
BuildPrereq: fileutils
PreReq: perl


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
Summary: An Apache module for PHP applications that use IMAP.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Obsoletes: mod_php3-imap
BuildRequires: krb5-devel
BuildRequires: openssl-devel


%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.


%package ldap
Summary: A module for PHP applications that use LDAP.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Obsoletes: mod_php3-ldap
BuildRequires: cyrus-sasl-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel


%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.


%if %{manuals}
%package manual
Summary: The PHP manual, in HTML format.
Group: Documentation
Obsoletes: mod_php3-manual
Prereq: php = %{version}-%{release}


%description manual
The php-manual package provides comprehensive documentation for the
PHP HTML-embedded scripting language, in HTML format. PHP is an
HTML-embedded scripting language.
%endif


%package mysql
Summary: A module for PHP applications that use MySQL databases.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl, grep
Provides: php_database
Obsoletes: mod_php3-mysql
BuildRequires: mysql-devel
Requires: mysql
Requires: zlib


%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php or mod_php package.


%package pgsql
Summary: A PostgreSQL database module for PHP.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Provides: php_database
Obsoletes: mod_php3-pgsql
BuildRequires: krb5-devel
BuildRequires: openssl-devel
BuildRequires: postgresql-devel
Requires: krb5-libs
Requires: openssl
Requires: postgresql-libs


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
Prereq: php = %{version}-%{release}, perl, grep
Summary: A module for PHP applications that use ODBC databases.
Provides: php_database
BuildRequires: unixODBC-devel
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
Summary: A module for PHP applications that use OCI8 databases.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
Provides: php_database


%description oci8
The php-oci8 package contains a dynamic shared object that will add
support for accessing OCI8 databases to PHP.
%endif


%package snmp
Summary: A module for PHP applications that query SNMP-managed devices.
Group: Development/Languages
Prereq: php = %{version}-%{release}, perl
BuildRequires: ucd-snmp-devel


%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.


%prep
%setup -q


# Weld the patchs into the main source
#
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0


# %doc gets confused about LICENSE & Zend/LICENSE
# lets just help it out,...
#
cp Zend/LICENSE Zend/ZEND_LICENSE


# We build php (normal cgi, apache_module)
# Need some spare directories for to do that
#
mkdir build-cgi
mkdir build-apache


%build


# Add -fPIC to RPM_OPT_FLAGS.
#
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS


# Add the Kerberos library path to the default LDFLAGS so that the IMAP checks
# will be able to find the GSSAPI libraries.
#
LDFLAGS="-L/usr/kerberos/lib"; export LDFLAGS


# Configure may or may not catch these (mostly second-order) dependencies.
#
LIBS="-lttf -lfreetype -lpng -ljpeg -lz -lnsl"; export LIBS


# This causes the shared extension modules to be installed into %{_libdir}/php4.
#
EXTENSION_DIR=%{_libdir}/php4; export EXTENSION_DIR


# This pulls the static /usr/lib/libc-client.a into the IMAP extension module.
#
IMAP_SHARED_LIBADD=-lc-client ; export IMAP_SHARED_LIBADD


# Shell function to configure and build a PHP tree.
#
build() {
ln -sf ../configure
%configure \
	--prefix=%{_prefix} \
	--with-config-file-path=%{_sysconfdir} \
	--enable-force-cgi-redirect \
	--disable-debug \
	--enable-pic \
	--disable-rpath \
	--enable-inline-optimization \
	--with-bz2 \
	--with-db3 \
	--with-curl \
	--with-dom=%{_prefix} \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-gd \
	--enable-gd-native-ttf \
	--with-ttf \
	--with-gdbm \
	--with-gettext \
	--with-ncurses \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-mm \
	--with-openssl \
	--with-png \
	--with-pspell \
	--with-regex=system \
	--with-xml \
	--with-expat-dir=%{_prefix} \
	--with-zlib \
	--with-layout=GNU \
	--enable-bcmath \
	--enable-debugger \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-safe-mode \
	--enable-sockets \
	--enable-sysvsem \
	--enable-sysvshm \
	--enable-discard-path \
	--enable-track-vars \
	--enable-trans-sid \
	--enable-yp \
	--enable-wddx \
	--without-oci8 \
	--with-imap=shared \
	--with-imap-ssl \
	--with-kerberos=/usr/kerberos \
	--with-ldap=shared \
	--with-mysql=shared,%{_prefix} \
%if %{oracle}
	--with-oci8=shared \
%endif
	--with-pgsql=shared \
	--with-snmp=shared,%{_prefix} \
	--with-snmp=shared \
	--enable-ucd-snmp-hack \
	--with-unixODBC=shared \
	--enable-memory-limit \
	--enable-bcmath \
	--enable-shmop \
	--enable-versioning \
	--enable-calendar \
	--enable-dbx \
	--enable-dio \
	--enable-mbstring \
	--enable-mbstr-enc-trans \
	$*


# Fixup the config_vars to not include the '-a' on lines which call apxs.
#
cat config_vars.mk > config_vars.mk.old
awk '/^INSTALL_IT.*apxs.*-a -n/ {sub("-a -n ","-n ");} {print $0;}' \
	config_vars.mk.old > config_vars.mk

make
}


# First, build a CGI tree. Remember that nice handy build() { ... } above?
#
pushd build-cgi
build \
	--enable-force-cgi-redirect
popd


# Second, build an Apache tree.
#
pushd build-apache


# Add the buildroot location to the front of the libexecdir.
# Again use the build() call
#
build \
	--with-apxs=%{_sbindir}/apxs
popd


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


# First, install the CGI tree.
#
pushd build-cgi
make install INSTALL_ROOT=$RPM_BUILD_ROOT 
popd


# Second, install the Apache tree.  Note that this overwrites the modules which
# were installed as part of the CGI build.  Lucky for us they're compatible.
#
pushd build-apache
make install INSTALL_ROOT=$RPM_BUILD_ROOT INSTALL_IT="echo "
popd


# Install the default configuration file and some icons which can be used to
# indicate that this site uses PHP.
#
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644    php.ini-dist $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/
 

# Gurrrr @!!$#? apxs/buildroot mess
#
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/apache
install -m 755 build-apache/libs/libphp4.so $RPM_BUILD_ROOT/usr/lib/apache


# Manuals -- we'll place English (en) in the location where the only version
# of the manual was before, and langify the rest.
%if %{manuals}
for lang in %{manual_langs} ; do
	if test x${lang} = xen ; then
		target_lang=""
	else
		target_lang=${lang}
	fi
	mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/${target_lang}
	bzip2 -dc $RPM_SOURCE_DIR/php_manual_${lang}.tar.bz2 | tar -x -C $RPM_BUILD_ROOT%{contentdir}/html/manual/mod/mod_php4/${target_lang} -f -
done
%endif


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%triggerpostun -- php < 4.0.0
	perl -pi -e 's|^#LoadModule php3_module|LoadModule php3_module|g' \
		/etc/httpd/conf/httpd.conf
	perl -pi -e 's|^#AddModule mod_php3.c|AddModule mod_php3.c|g' \
		/etc/httpd/conf/httpd.conf


%files
	%defattr(-,root,root)
	%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
	%doc Zend/ZEND_*
	%config(noreplace) %{_sysconfdir}/php.ini
	%{_bindir}/php
	%{_datadir}/pear
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
	%{_libdir}/php


# From here on in we need to make php-(extension) alter the php.ini
# file to activate usage of each module in installation and deactivation
# on removal. We'll do this using perl.
# Just to make things annoying, upstream has decided to change the default
# file extensions from .so to .dll .. <mutter>...
#


################################################################################
# pgsql ########################################################################
#
%files pgsql
	%defattr(-,root,root)
	%{_libdir}/php4/pgsql.so

%post pgsql
	%{__perl} -pi -e "s|^;extension=pgsql.so|extension=pgsql.so|" %{_sysconfdir}/php.ini
	%{__perl} -pi -e "s|^;extension=php_pgsql.dll|extension=pgsql.so|" %{_sysconfdir}/php.ini


%preun pgsql
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=pgsql.so|;extension=pgsql.so|" %{_sysconfdir}/php.ini
	fi


################################################################################
# mysql ########################################################################
#
%files mysql
	%defattr(-,root,root)
	%{_libdir}/php4/mysql.so


%post mysql
	if %{__grep} -q "extension=mysql.so" %{_sysconfdir}/php.ini; then
		%{__perl} -pi -e "s|^;extension=mysql.so|extension=mysql.so|" %{_sysconfdir}/php.ini
	else
		%{__perl} -pi -e "s|^;extension=php_mysql.dll|;extension=php_mysql.dll\nextension=mysql.so|" %{_sysconfdir}/php.ini
	fi

%preun mysql
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=mysql.so|;extension=mysql.so|" %{_sysconfdir}/php.ini
	fi


################################################################################
# odbc #########################################################################
#
%files odbc
	%defattr(-,root,root)
	%{_libdir}/php4/odbc.so


%post odbc
	if %{__grep} -q "extension=odbc.so" %{_sysconfdir}/php.ini; then
		%{__perl} -pi -e "s|^;extension=odbc.so|extension=odbc.so|" %{_sysconfdir}/php.ini
	else
		%{__perl} -pi -e "s|^;extension=php_odbc.dll|;extension=php_odbc.dll\nextension=odbc.so|" %{_sysconfdir}/php.ini
	fi

%preun odbc
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=odbc.so|;extension=odbc.so|" %{_sysconfdir}/php.ini
	fi


################################################################################
# oracle #######################################################################
#
%if %{oracle}
%files oci8
	%defattr(-,root,root)
	%{_libdir}/php4/oci8.so


%post oci8
	%{__perl} -pi -e "s|^;extension=oci8.so|extension=oci8.so|" %{_sysconfdir}/php.ini
	%{__perl} -pi -e "s|^;extension=php_oci8.dll|extension=oci8.so|" %{_sysconfdir}/php.ini


%preun oci8
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=oci8.so|;extension=oci8.so|" %{_sysconfdir}/php.ini
	fi
%endif


################################################################################
# imap #########################################################################
#
%files imap
	%defattr(-,root,root)
	%{_libdir}/php4/imap.so


%post imap
	%{__perl} -pi -e "s|^;extension=imap.so|extension=imap.so|" %{_sysconfdir}/php.ini
	%{__perl} -pi -e "s|^;extension=php_imap.dll|extension=imap.so|" %{_sysconfdir}/php.ini


%preun imap
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=imap.so|;extension=imap.so|" %{_sysconfdir}/php.ini
	fi


################################################################################
# ldap #########################################################################
#
%files ldap
	%defattr(-,root,root)
	%{_libdir}/php4/ldap.so


%post ldap
	%{__perl} -pi -e "s|^;extension=ldap.so|extension=ldap.so|" %{_sysconfdir}/php.ini
	%{__perl} -pi -e "s|^;extension=php_ldap.dll|extension=ldap.so|" %{_sysconfdir}/php.ini


%preun ldap
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=ldap.so|;extension=ldap.so|" %{_sysconfdir}/php.ini
	fi


################################################################################
# snmp #########################################################################
#
%files snmp
	%defattr(-,root,root)
	%{_libdir}/php4/snmp.so


%post snmp
	%{__perl} -pi -e "s|^;extension=snmp.so|extension=snmp.so|" %{_sysconfdir}/php.ini
	%{__perl} -pi -e "s|^;extension=php_snmp.dll|extension=snmp.so|" %{_sysconfdir}/php.ini


%preun snmp
	if [ $1 = 0 -a -f %{_sysconfdir}/php.ini ] ; then
	  %{__perl} -pi -e "s|^extension=snmp.so|;extension=snmp.so|" %{_sysconfdir}/php.ini
	fi

################################################################################


%if %{manuals}
%files manual
	%defattr(-,root,root)
	%{contentdir}/icons/*
	%dir %{contentdir}/html/manual/mod/mod_php4/
	%{contentdir}/html/manual/mod/mod_php4/*.html
	%lang(cs) %{contentdir}/html/manual/mod/mod_php4/cs
	%lang(de) %{contentdir}/html/manual/mod/mod_php4/de
	%lang(es) %{contentdir}/html/manual/mod/mod_php4/es
	%lang(fr) %{contentdir}/html/manual/mod/mod_php4/fr
	%lang(hu) %{contentdir}/html/manual/mod/mod_php4/hu
	%lang(it) %{contentdir}/html/manual/mod/mod_php4/it
	%lang(ja) %{contentdir}/html/manual/mod/mod_php4/ja
	%lang(ko) %{contentdir}/html/manual/mod/mod_php4/ko
	%lang(nl) %{contentdir}/html/manual/mod/mod_php4/nl
	%lang(pt) %{contentdir}/html/manual/mod/mod_php4/pt_BR
	%lang(tr) %{contentdir}/html/manual/mod/mod_php4/tr
%endif


%changelog
* Thu Sep 26 2002 Joe Orton <jorton@redhat.com> 4.1.2-7.3.6
- add security fixes for mail() function; CAN-2002-0985, CAN-2002-0986

* Tue Aug 20 2002 Philip Copeland <bryce@redhat.com> 4.1.2-7.3.4
- Humm. Seems we're somewhat bloated in the requires department.
  Major reworking of BuildRequires/Requires. I dunno what the
  answer for the oci8 people is but I'm leaving it blank for
  the moment.
  
* Fri Aug 2 2002 Philip Copeland <bryce@redhat.com> 4.1.2-7.3.3
- #67815 Include path not set fixup.

* Wed Jun 19 2002 Philip Copeland <bryce@redhat.com> 4.1.2-7.3.2
- Removed the dbg extension as that is to built as a
  new package in it's own right

* Thu Jun  6 2002 Philip Copeland <bryce@redhat.com> 4.1.2-7
- Tidy up the spec file
- munched the acincludes.m4 for autoconf
- (hopefully) have better php.ini defaults but really
  people should hand edit it for their local setup
  rather than relying on installed defaults
- For development purposes, added the ability
  to recompile the package without the manual
  set (rpm --define 'manuals 0' --rebuild...)
- Created 4 spec files for 7.0, 7.1, 7.2 and 7.3
  ie -7.2.1 = first revision for RH7.2
  main differance being the curl extension

* Tue Jun  4 2002 Philip Copeland <bryce@redhat.com> 4.1.2-7
- Humm mcal seems to have died a death. Removed it as
  a compile option
- dropped in the mysql extension from 4.2.1 into the
  4.2.1 base to get around #64104
- Added (long) Requires list to keep the zealots happy
- Minor tweaks to the default php.ini file

* Sun Apr 14 2002  Philip Copeland <bryce@redhat.com> 4.1.2-6
- %post for mysql has zlib in it?!? Bad cut/paste. Fixed.
- Added missing trigger entries to php.ini-dist
- Bumped release number.

* Sat Apr 13 2002  Philip Copeland <bryce@redhat.com> 4.1.2-6
- Oh joyous. buildconf doesn't correctly rebuild a
  configure script, consequently we get lex checking errors
  Strictly speaking this is autoconf's fault. Tweeked.

* Sun Apr 07 2002  Philip Copeland <bryce@redhat.com> 4.1.2-6
- Added in hook for the rather useful dbg addin
  http://dd.cron.ru/dbg/
  May not be able to provide a dbg rpm accomplyment
  to php for the official release but at least it'll
  make it easy to drop in at a later date.

* Mon Mar 25 2002  Philip Copeland <bryce@redhat.com> 4.1.2-5
- Accepted patches from Konstantin Riabitsev <icon@duke.edu>
  for the php.ini file which fix this damnable .dll/.so
  mess.
- Fixes for the modules. Every dll name is now prepended by php_,
  so the modules were NEVER enabled. Also, there is no longer
  php_mysql.dll or php_odbc.dll. Added workarounds for that.
- Jumped a number (-4) because of intresting after effects
  in the build system.

* Tue Mar 12 2002 Philip Copeland <bryce@redhat.com> 4.1.2-3
- Fix for crashing bug (#60855)

* Tue Mar 05 2002 Philip Copeland <bryce@redhat.com> 4.1.2-2
- Forgot the -with-png-dir=%{_prefix} config
  option (#55248)

* Mon Mar 04 2002 Philip Copeland <bryce@redhat.com> 4.1.2-2
- Minor patch for figuring out where the blasted
  mysql.sock named socket lives. (grumble)
- Added in --enable-exif. It's there for people who
  asked for it but I ain't supporting it if it
  breaks.
- Tweak the default php.ini file to turn off file upload by default
  and to tweak the default path for loadable modules

* Thu Feb 28 2002 Philip Copeland <bryce@redhat.com> 4.1.2-1
- Jumped to 4.1.2 for security...

* Wed Feb 13 2002 Philip Copeland <bryce@redhat.com> 4.1.1-4
- Added multibyte input/ouput support
  --enable-mbstring
  --enable-mbstr-enc-trans
- Added in a couple of BuildReq's
- Because db1,2,3 are ditched in the next RHAT release and only
  db4 exists, I've purposly NOT put in the db4-devel BuildReq
  as thers no way to differentiate this build for a 7.X and
  the new release.

* Fri Feb 08 2002 Philip Copeland <bryce@redhat.com> 4.1.1-3
- Added calendar, dbx, dio and mcal support into the build
  --enable-calendar
  --enable-dbx
  --enable-dio
  --enable-mcal

* Thu Feb 07 2002 Philip Copeland <bryce@redhat.com> 4.1.1-2
- Reformatted the spec file to be something more pretty to read
- Some wassak upstream changed the default php.ini file to
  winblows format (.dll) which broke the extension munching
  altered the post scripts to accomodate (#59195)
- Added in --enable-gd-native-ttf (#55199)

* Mon Jan 29 2002 Philip Copeland <bryce@redhat.com> 4.1.1-1
- Added in patch for DOM(xml)

* Mon Jan 28 2002 Philip Copeland <bryce@redhat.com> 4.1.1-0
- Rather than write a new spec file, borrowed the one from 4.0.6-13
  Initial build of 4.1.1 (note db2 is now obsoleted)
  Added --enable-memory-limit

===============================================================================
  Ditched the 4.0.x sources for 4.1.1
===============================================================================

* Wed Dec  5 2001 Philip Copeland <bryce@redhat.com> 4.0.6-13
- Minor tweak to the configure script to allow it to search fo the libxml
  installation in both */include/libxml/tree.h and
  include/libxml2/libxml/tree.h

* Tue Nov 20 2001 Nalin Dahyabhai <nalin@redhat.com> 4.0.6-12
- rebuild for Raw Hide, building snmp again

* Tue Nov 20 2001 Nalin Dahyabhai <nalin@redhat.com> 4.0.6-11
- don't build the snmp module
- don't activate the module for Apache when we install it into the buildroot

* Mon Nov 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- link the IMAP module with c-client.a

* Fri Nov 16 2001 Nalin Dahyabhai <nalin@redhat.com> 4.0.6-10
- use shared expat for XML support, add buildprereq on expat-devel
- update to latest manuals from the web site
- %{_datadir}/php -> %{_datadir}/pear
- miscellaneous cleanups

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove explicit dependency on krb5-libs

* Fri Nov  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable transparent session id support, configure freetype and gmp extensions
  (suggestion and patch Jason Costomiris)

* Mon Sep 17 2001 Tim Powers <timp@redhat.com> 4.0.6-9
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
