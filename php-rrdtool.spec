%define		_modname	rrdtool
Summary:	RRDtool PHP module
Summary(pl):	Modu� PHP RRDtool
Name:		php-rrdtool
Version:	1.2
Release:	2
License:	GPL
Group:		Applications/Databases
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/pub/contrib/php_rrdtool.tgz
# Source0-md5:	c86a45cfc54517b9066c480bbc589d43
URL:		http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
BuildRequires:	rrdtool-devel >= 1.2.10
BuildRequires:	sed >= 4.0
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes a dynamic shared object (DSO) that adds RRDtool
bindings to the PHP HTML-embedded scripting language.

%description -l pl
Ten pakiet zawiera dynamiczny modu� (DSO) dodaj�cy dowi�zania RRDtoola
do j�zyka skryptowego PHP.

%prep
%setup -q -n rrdtool

sed -i -e 's,/lib\>,/%{_lib},' config.m4

%build
phpize
%configure \
	--with-rrdtool=shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
