%define 	mod_name	frontpage
%define		arname		mod_%{mod_name}
%define         apxs            /usr/sbin/apxs

Summary:	The improved mod_frontpage module for the Apache Web server.
Name:		apache-mod_%{mod_name}
Version:	1.6.1
Release:	0.1
Group:		Networking/Daemons
URL:		http://home.edo.uni-dortmund.de/~chripo/
#Source0: http://home.edo.uni-dortmund.de/~chripo/download/%{name}-%{version}mdk-1.3.19.tar.bz2
#The patch is now maintained by FreeBSD
Source0:	http://people.freebsd.org/~mbr/distfiles/mod_frontpage-%{version}.tar.bz2
Patch0:		%{arname}-PLD.patch
Patch1:		%{arname}-Makefile.patch
Patch2:		%{arname}-fpexec-PLD.patch
License:	Apache License
Prereq:		grep
Prereq:		apache(EAPI)  >= 1.3.23
Prereq:		%{_sbindir}/apxs
Requires:	apache
BuildRequires:	apache(EAPI)-devel >= 1.3.23
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      %(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%description
This is a module for the Apache HTTP Server
<http://www.apache.org/httpd.html>. It replaces the Apache-FP patches
and module supplied with the FrontPage Server Extensions available
from Microsoft <http://www.microsoft.com> and Ready-to-Run Software
<http://www.rtr.com/fpsupport>.

Using this module allows you to use advanced features of the FrontPage
client with your Apache HTTP Server (e.g. creating FrontPage-extended
subwebs using the FrontPage client in contrast to creating them as
user "root" with "fpinstall.sh" or the "fpsrvadm.exe"-utility on the
system's shell).

%prep
%setup -q -n %{arname}-%{version}
%patch -p0
%patch1 -p0
%patch2 -p0

%build
perl Makefile.PL
%{__make} CFLAGS="%{rpmcflags} -DLINUX=22 -DINET6 -Dss_family=__ss_family -Dss_len=__ss_len -DDEV_RANDOM=/dev/random -DEAPI -DEAPI_MM"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sbindir}}
install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install fp{exec,static} $RPM_BUILD_ROOT%{_sbindir}

gzip -9nf {CHANGES,FEATURES,INSTALL,LICENSE,README}

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
	if [ "$1" = "0" ]; then
		%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
        if [ -f /var/lock/subsys/httpd ]; then
               /etc/rc.d/init.d/httpd restart 1>&2
        fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
%attr(4550,root,root) %{_sbindir}/fpexec
%attr(0555,root,root) %{_sbindir}/fpstatic
%doc *.gz

%clean
rm -rf $RPM_BUILD_ROOT
