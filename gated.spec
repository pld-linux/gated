Summary:	The GateD routing daemon
Summary(pl):	GateD - demon routingu
Name:		gated
Version:	3.5.10
%define		src_version	%(echo %version | sed 's/\\./-/g')
Release:	9
Copyright:	distributable
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.gated.org/net-research/gated/%{name}-%{src_version}.tar.gz
Source1:	gated.init
Source2:	gated-3.5.10-Config
Source3:	gated-3.5.10-gated.conf
Source4:	gated-3.5.9-krt_ifread_ioctl.c
Patch0:		gated-3.5.7-linux.patch
Patch1:		gated-3.5.10-glibc.patch
Patch2:		gated-3.5.10-config.patch
Patch4:		gated-3.5.10-dump.patch
Patch5:		gated-3.5.x-linuxmc.patch
Patch6:		gated-3.5.10-ospfmonauth.patch
Patch7:		gated-3.5.10-kern22.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Url:		http://www.gated.org/

%description
GateD is a modular software program consisting of core services, a
routing database, and protocol modules which support multiple routing
protocols (RIP versions 1 and 2, DCN HELLO, OSPF version 2, EGP
version 2, BGP versions 2 through 4). GateD is designed to handle
dynamic routing with a routing database built from the information
exchanged by routing protocols.

%description -l pl
GateD jest modu³owym programem sk³adaj±cym siê z rdzennych us³ug, bazy
danych routingu oraz modu³ów protoko³owych, które obs³uguja wiele
protoko³ów rutowania (wersje 1 i 2 RIP, DCN HELLO, 2 wersja OSPF, 2
wersja EGP oraz BGP w wersji od 2 do 4). GateD pracuje z dynamicznym
routingiem za pomoc± bazy danych rutowania zbudowanej z informacji
wymianianych miêdzy protoko³ami rutujacymi.

%prep
%setup -q -n gated-3-5-10

# patch0 not applied
%patch1 -p1
%patch2 -p1
# patch3 doesn't exist
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

cd src
cp %SOURCE4 krt_ifread_ioctl.c

mkdir obj.`util/archtype`
#cp configs/linux-2.0 obj.`util/archtype`/Config
cp %SOURCE2 obj.`util/archtype`/Config

%build
cd src
%{__make} config
%{__make} CC=egcs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{sbindir},%{_bindir},%{_mandir}/man8},/etc/rc.d/init.d}

%{__make} -C src install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir}

%{__make} MANDIR=$RPM_BUILD_ROOT%{_mandir} install-man

install -d $RPM_BUILD_ROOT/var/gated
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/gated
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/gated.conf.sample

%post
/sbin/ldconfig
/sbin/chkconfig --add gated

%preun
if [ $1 = 0 ] ; then
        /sbin/chkconfig --del gated
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/gated
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*
/var/gated

%doc Acknowledgements BUGS CHANGES CHANGES.1
%doc Consortium_Agreeemnt Copyright Copyright.ISIS Copyright.OSPF Licensing
%doc INSTALL ISIS-config.ps README README.bgp README.make RELEASE TODO
%doc conf doc src/configs/linux-README
%doc man/gated-2.0-impl.txt

%attr(754,root,root) /etc/rc.d/init.d/gated
%config %{_sysconfdir}/gated.conf.sample

%clean
rm -rf $RPM_BUILD_ROOT
