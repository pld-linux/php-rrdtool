%define		_modname	rrdtool
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	RRDtool PHP module
Summary(pl):	Modu³ PHP RRDtool
Name:		php-rrdtool
Version:	1.0.50
Release:	0.1
License:	GPL
Group:		Applications/Databases
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/pub/rrdtool-1.0.x/rrdtool-%{version}.tar.gz
# Source0-md5:	c466e2e7df95fa8e318e46437da87686
URL:		http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cgilibc-devel
BuildRequires:	php-devel >= 4:5.0
BuildRequires:	rrdtool-devel
BuildRequires:	gd-devel
Requires(post,preun):	php-common
Requires:	%{_sysconfdir}/conf.d
%requires_eq_to php-common php-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RRDtool module for PHP.

%description -n php-rrdtool -l pl
Modu³ RRDtool dla PHP.

%prep
%setup -q -n rrdtool-%{version}

%build
cd contrib/php4
export EXTENSION_DIR="%{extensionsdir}"
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-openssl \
	--with-php-config=php-config \
	--includedir="%{_includedir}/php"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{_examplesdir}/%{name}-%{version}}

cd contrib/php4
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

cp -a examples/*.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc contrib/php4/USAGE
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
%{_examplesdir}/%{name}-%{version}
