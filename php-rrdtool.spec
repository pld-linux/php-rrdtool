%define		_modname	rrdtool
Summary:	RRDtool PHP module
Summary(pl):	Modu³ PHP RRDtool
Name:		php-rrdtool
Version:	1.0.50
Release:	8
License:	GPL
Group:		Applications/Databases
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/pub/rrdtool-1.0.x/rrdtool-%{version}.tar.gz
# Source0-md5:	c466e2e7df95fa8e318e46437da87686
Patch0:		rrdtool-php-config.patch
Patch1:		%{name}-new.patch
URL:		http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/
BuildRequires:	cgilibc-devel
BuildRequires:	gd-devel
BuildRequires:	openssl-devel >= 0.9.5
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	rrdtool-devel >= 1.2.10
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes a dynamic shared object (DSO) that adds RRDtool
bindings to the PHP HTML-embedded scripting language.

%description -l pl
Ten pakiet zawiera dynamiczny modu³ (DSO) dodaj±cy dowi±zania RRDtoola
do jêzyka skryptowego PHP.

%prep
%setup -q -n rrdtool-%{version}
%patch0 -p0
%patch1 -p1

%build
cd contrib/php4
phpize
%configure \
	--with-openssl \
	--includedir="%{_includedir}/php"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{_examplesdir}/%{name}-%{version}}

cd contrib/php4
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

cp -a examples/*.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc contrib/php4/USAGE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
%{_examplesdir}/%{name}-%{version}
