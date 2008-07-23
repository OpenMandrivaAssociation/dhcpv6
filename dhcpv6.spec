%define old_name dhcp6
%define common_description DHCPv6 is a stateful address autoconfiguration protocol for IPv6, a counterpart\
to IPv6 stateless address autoconfiguration protocol. It can either be used\
independently or it can coexist with its counterpart protocol. This protocol\
uses client/server mode of operation but can also provide support through a\
Relay Agent.
%define client_name dhcp6client
%define api 1.0
%define major 2
%define client_libname %mklibname %{client_name} %{api} %{major}
%define client_develname %mklibname %{client_name} -d

Summary:	A DHCP client/server for IPv6
Name:		dhcpv6
Version:	1.0.3
Release:	%mkrel 3
License:	BSD
Group:		System/Servers
URL:		https://fedorahosted.org/dhcpv6/
Source0:	http://dcantrel.fedorapeople.org/%{name}/%{name}-%{version}.tar.gz
BuildRequires: bison
BuildRequires: flex
BuildRequires: openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	%{old_name}
Obsoletes:	%{old_name}

%define _sbindir /sbin

%description 
%{common_description}

The protocol is defined by IETF DHC WG (www.ietf.org).


%package -n     %{client_libname}
Summary:        Library for %{client_name}
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{client_libname}
This package contains the library needed to run programs dynamically
linked with %{client_name}.


%package -n     %{client_develname}
Summary:        Headers for developing programs that will use %{client_name}
Group:          Development/C
Requires:       %{client_libname} = %{version}
Provides:       %{client_name}-devel = %{version}-%{release}

%description -n %{client_develname}
This package contains the headers that programmers will need to develop
applications which will use %{client_name}.


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
%configure

%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -d %{buildroot}%{_localstatedir}/lib/%{name}

%if %mdkversion < 200900
%post -n %{client_libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{client_libname} -p /sbin/ldconfig
%endif

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

%files -n %{client_libname}
%{_libdir}/lib%{client_name}-%{api}.so.%{major}*

%files -n %{client_develname}
%dir %{_includedir}/%{client_name}
%{_includedir}/%{client_name}/*.h
%{_libdir}/lib%{client_name}.so
%{_libdir}/lib%{client_name}.a
%{_libdir}/lib%{client_name}.la
%{_libdir}/pkgconfig/lib%{client_name}.pc

%files common
%defattr(-,root,root)
%dir %{_localstatedir}/lib/%{name}

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
