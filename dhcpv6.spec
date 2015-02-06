%define old_name dhcp6
%define common_description DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart\
to IPv6 stateless address autoconfiguration protocol. It can either be used\
independently or it can coexist with its counterpart protocol. This protocol\
uses client/server mode of operation but can also provide support through a\
Relay Agent.
%define client_name dhcp6client

#disable format security error flags, it doesn't play nice with lex
##%define Werror_cflags %nil

Summary:	A DHCP client/server for IPv6
Name:		dhcpv6
Version:	1.2.0
Release:	2
License:	LGPLv2+
Group:		System/Servers
URL:		https://fedorahosted.org/dhcpv6/
Source0:	https://fedorahosted.org/releases/d/h/dhcpv6/%{name}/%{name}-%{version}.tar.gz
BuildRequires: bison
BuildRequires: flex
BuildRequires: openssl-devel
BuildRequires: libnl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	%{old_name}
Obsoletes:	%{old_name}

%description 
%{common_description}

The protocol is defined by IETF DHC WG (www.ietf.org).


%package	common
Summary:	Common files for DHCP IPv6
Group:		System/Servers
Provides:	%{old_name}-client
Obsoletes:	%{old_name}-client

%description	common
%{common_description}

This package contains common files for DHCP IPv6.


%package	client
Summary:	DHCP client for IPv6
Group:		System/Servers
Provides:	%{old_name}-client
Obsoletes:	%{old_name}-client
Requires:	%{name}-common = %{version}-%{release}

%description	client
%{common_description}

This package contains the DHCP client for IPv6.


%package	server
Summary:	DHCP server for IPv6
Group:		System/Servers
Requires(preun):rpm-helper
Requires(post):	rpm-helper	
Provides:	%{old_name}-server
Obsoletes:	%{old_name}-server
Requires:	%{name}-common = %{version}-%{release}

%description	server
%{common_description}

This package contains the DHCP server for IPv6.


%package	relay
Summary:	DHCP relay agent for IPv6
Group:		System/Servers
Requires(preun):rpm-helper
Requires(post):	rpm-helper	

%description	relay
%{common_description}

This package contains the DHCP relay agent for IPv6.


%package	doc
Summary:	Documentation about the DHCP IPv6 server/client
Group:		System/Servers

%description	doc
%{common_description}

This package contains RFC/API/protocol documentation about the DHCP
server and client for IPv6.


%prep

%setup -q 

%build
%configure2_5x

%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %buildroot/sbin %buildroot%{_localstatedir}/lib/%{name}
mv %buildroot%_sbindir/dhcp6c %buildroot/sbin

%post server
%_post_service dhcp6s

%preun server
%_preun_service dhcp6s

%post relay
%_post_service dhcp6r

%preun relay
%_preun_service dhcp6r

%clean
rm -rf %{buildroot}

%files doc
%defattr(-,root,root)
%doc

%files common
%defattr(-,root,root)
%dir %{_localstatedir}/lib/%{name}

%files client
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dhcp6c.conf
/sbin/dhcp6c
%_mandir/man?/dhcp6c*

%files server
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dhcp6s.conf
%config(noreplace) %{_sysconfdir}/sysconfig/dhcp6s
%{_initrddir}/dhcp6s
%_sbindir/dhcp6s
%_mandir/man?/dhcp6s*

%files relay
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/dhcp6r
%{_initrddir}/dhcp6r
%_sbindir/dhcp6r
%_mandir/man?/dhcp6r*


%changelog
* Sun Jul 26 2009 Emmanuel Andry <eandry@mandriva.org> 1.2.0-1mdv2010.0
+ Revision: 400290
- New version 1.2.0
- reenable werror cflag

* Wed Jan 07 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-1mdv2009.1
+ Revision: 326761
- Release 1.1.0
- kill lib packages, library has been killed upstream

* Sat Nov 29 2008 Olivier Thauvin <nanardon@mandriva.org> 1.0.21-2mdv2009.1
+ Revision: 307861
- don't relocate _sbindir to sbin, just move client into /sbin instead, otherwise init.d/* get broken and servers don't go into right place

* Tue Aug 26 2008 Emmanuel Andry <eandry@mandriva.org> 1.0.21-1mdv2009.0
+ Revision: 276349
- New version
- fix license

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed Dec 12 2007 Olivier Blin <oblin@mandriva.com> 1.0.3-1mdv2008.1
+ Revision: 119112
- add /var/lib/dhcpv6 in a dhcpv6-common subpackage for lease files
- add library and devel package for dhcp6client
- enhance descriptions
- factorize description
- fix case for DHCP/IPv6 in summaries
- obsolete/provide dhcp6 subpackages for client/server
- move docs in a dhcpv6-doc subpackage
- add dhcpv6-relay subpackage
- move preun/post requirements in the server package
- fix dhcp6s service name in post/preun scripts
- remove manual installation of dhcp6s service
- use default conf files instead of custom ones
- remove buildroot at beginning of install section
- 1.0.3
- drop old patches (gcc4 and install fixes are not required anymore)
- rename as dhcpv6 and obsolete/provide dhcp6
- rename as dhcpv6
- update URL

