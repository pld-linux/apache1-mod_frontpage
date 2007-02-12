%define 	mod_name	frontpage
%define		apxs		/usr/sbin/apxs1
Summary:	The improved mod_frontpage module for the Apache Web server
Summary(pl.UTF-8):   Ulepszony moduł mod_frontpage dla serwera Apache
Name:		apache1-mod_%{mod_name}
Version:	1.6.2
Release:	3
License:	Apache
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mirfak/mod_%{mod_name}_mirfak-%{version}.tar.bz2
# Source0-md5:	f7480918382067ce16e7afc40a633be4
Source1:	%{name}.pl
Patch0:		%{name}-mirfak.patch
URL:		http://mirfak.sourceforge.net/
BuildRequires:	%{__perl}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_frontpage <= 1.6.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is a module for the Apache HTTP Server
<http://httpd.apache.org/>. It replaces the Apache-FP patches and
module supplied with the FrontPage Server Extensions available from
Microsoft <http://www.microsoft.com/> and Ready-to-Run Software
<http://www.rtr.com/fpsupport/>.

Using this module allows you to use advanced features of the FrontPage
client with your Apache HTTP Server (e.g. creating FrontPage-extended
subwebs using the FrontPage client in contrast to creating them as
user "root" with "fpinstall.sh" or the "fpsrvadm.exe"-utility on the
system's shell).

%description -l pl.UTF-8
To jest moduł dla serwera HTTP Apache. Zastępuje łaty Apache-FP oraz
moduł dodawany do FrontPage Server Extensions dostępnych od Microsoftu
i Ready-to-Run Software (<http://www.rtr.com/fpsupport/>).

Użycie tego modułu pozwala na używanie zaawansowanych możliwości
klienta FrontPage z serwerem Apache (np. tworzenie podstron z
rozszerzeniami FrontPage przy użyciu klienta FrontPage zamiast przez
uruchamiania fpinstall.sh lub fpsrvadm.exe z powłoki systemowej).

%prep
%setup -q -n mod_%{mod_name}_mirfak-%{version}
%patch0 -p1

%build
%{__perl} %{SOURCE1}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d,%{_sbindir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install fp{exec,static} $RPM_BUILD_ROOT%{_sbindir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.6.2-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc *.html CHANGES FEATURES README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
%attr(4750,root,root) %{_sbindir}/fpexec
%attr(755,root,root) %{_sbindir}/fpstatic
