Summary:	A dhcp client/server for ipv6
Name:		dhcpv6
Version:	1.0.3
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
URL:		https://fedorahosted.org/dhcpv6/
Source0:	http://dcantrel.fedorapeople.org/%{name}/%{name}-%{version}.tar.gz
BuildRequires: bison
BuildRequires: flex
BuildRequires: openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	dhcp6
Obsoletes:	dhcp6

%define _sbindir /sbin

%description 
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent. 

The protocol is defined by IETF DHC WG (www.ietf.org).

%package	client
Summary:	DHCP client for ipv6
Group:		System/Servers

%description	client
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent.


%package	server
Summary:	DHCP server for ipv6
Group:		System/Servers
Requires(preun):rpm-helper
Requires(post):	rpm-helper	

%description	server
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent.

%package	relay
Summary:	DHCP relay agent for ipv6
Group:		System/Servers
Requires(preun):rpm-helper
Requires(post):	rpm-helper	

%description	relay
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent.

%package	doc
Summary:	Documentation about the DHCP ipv6 server/client
Group:		System/Servers

%description	doc
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent.

This packages contains RFC/API/protocol documentation about the DHCP
IPv6 server and client.

%prep

%setup -q 

%build
%configure

%make

%install
rm -rf %{buildroot}
%makeinstall_std

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
%doc docs/*

%files client
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dhcp6c.conf
%_sbindir/dhcp6c
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
