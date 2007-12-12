Summary:	A dhcp client/server for ipv6
Name:		dhcpv6
Version:	0.85
Release:	%mkrel 3
License:	BSD
Group:		System/Servers
URL:		https://fedorahosted.org/dhcpv6/
Source0:	http://dcantrel.fedorapeople.org/dhcpv6/%{name}/%{name}-%{version}.tar.bz2
Patch0:		dhcp6.gcc4.patch
Patch1:		dhcp6-installfix.diff
BuildRequires: bison
BuildRequires: flex
BuildRequires: openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	dhcp6
Obsoletes:	dhcp6
Requires(preun):rpm-helper
Requires(post):	rpm-helper	

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

%description	server
DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart
to IPv6 stateless address autoconfiguration protocol. It can either be used
independently or it can coexist with its counterpart protocol. This protocol
uses client/server mode of operation but can also provide support through a
Relay Agent.

%prep

%setup -q 
%patch0 -p1 -b .gcc4
%patch1 -p0

%build
%configure

%make

%install

%makeinstall_std

mkdir -p %buildroot/%{_sysconfdir}
cat > %buildroot/%{_sysconfdir}/%{name}c.conf <<EOF
# sample %{name}c.conf - %version-%release

interface eth0 {
#   information-only;
    send rapid-commit;
    request prefix-delegation;
#   request temp-address;
};
EOF

cat > %buildroot/%{_sysconfdir}/%{name}s.conf <<EOF
# sample %{name}s.conf - %version-%release

# dns_server 2003::6:1 ibm.com;
prefer-life-time 10000;
valid-life-time 20000;
renew-time 5000;
rebind-time 8000;
interface eth0 {
    link AAA {
        # range 3ffe:ffff:100::10 to 3ffe:ffff:100::110/64;
        # prefix 3ffe:ffef:104::/64;
    }
#    group {
#        host host0 {
#            duid 00:00:00:00:a0:a0;
#            address {
#                3ffe:ffff:102::120/64;
#            }
#        }
#    }
}
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 dhcp6s.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/dhcp6s

perl -pi -e 's/^# chkconfig:/# chkconfig: 345 66 36/' dhcp6s.sh

mkdir -p %{buildroot}%{_initrddir}
install -m755 dhcp6s.sh %{buildroot}%{_initrddir}/dhcp6s

%post server
%_post_service %{name}s

%preun server
%_preun_service %{name}s

%clean
rm -rf %{buildroot}

%files client
%defattr(-,root,root)
%doc docs/*
%doc dhcp6c.conf
%config(noreplace) %{_sysconfdir}/%{name}c.conf
%_sbindir/dhcp6c
%_mandir/man?/dhcp6c*

%files server
%defattr(-,root,root)
%doc docs/*
%doc dhcp6s.conf
%config(noreplace) %{_sysconfdir}/%{name}s.conf
%config(noreplace) %{_sysconfdir}/sysconfig/dhcp6s
%{_initrddir}/dhcp6s
%_sbindir/dhcp6s
%_mandir/man?/dhcp6s*


