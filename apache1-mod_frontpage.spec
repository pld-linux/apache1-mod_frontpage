%define 	mod_name	frontpage
%define		arname		mod_%{mod_name}
%define		apxs		/usr/sbin/apxs

Summary:	The improved mod_frontpage module for the Apache Web server
Summary(pl):	Ulepszony modu³ mod_frontpage dla serwera Apache
Name:		apache-mod_%{mod_name}
Version:	1.6.2
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mirfak/mod_%{mod_name}_mirfak-%{version}.tar.bz2
# Source0-md5:	f7480918382067ce16e7afc40a633be4
Source1:	%{name}.pl
Patch0:		%{name}-mirfak.patch
URL:		http://mirfak.sourceforge.net/
BuildRequires:	apache(EAPI)-devel >= 1.3.23
BuildRequires:	perl
PreReq:		apache(EAPI) >= 1.3.23
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	mod_frontpage

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
This is a module for the Apache HTTP Server
<http://www.apache.org/httpd.html>. It replaces the Apache-FP patches
and module supplied with the FrontPage Server Extensions available
from Microsoft <http://www.microsoft.com/> and Ready-to-Run Software
<http://www.rtr.com/fpsupport/>.

Using this module allows you to use advanced features of the FrontPage
client with your Apache HTTP Server (e.g. creating FrontPage-extended
subwebs using the FrontPage client in contrast to creating them as
user "root" with "fpinstall.sh" or the "fpsrvadm.exe"-utility on the
system's shell).

%description -l pl
To jest modu³ dla serwera HTTP Apache. Zastêpuje ³aty Apache-FP oraz
modu³ dodawany do FrontPage Server Extensions dostêpnych od Microsoftu
i Ready-to-Run Software (<http://www.rtr.com/fpsupport/>).

U¿ycie tego modu³u pozwala na u¿ywanie zaawansowanych mo¿liwo¶ci
klienta FrontPage z serwerem Apache (np. tworzenie podstron z
rozszerzeniami FrontPage przy u¿yciu klienta FrontPage zamiast przez
uruchamiania fpinstall.sh lub fpsrvadm.exe z pow³oki systemowej).

%prep
%setup -q -n %{arname}_mirfak-%{version}
%patch0 -p1

%build
perl %{SOURCE1}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sbindir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install fp{exec,static} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES FEATURES LICENSE README
%attr(755,root,root) %{_pkglibdir}/*
%attr(4750,root,root) %{_sbindir}/fpexec
%attr(755,root,root) %{_sbindir}/fpstatic
