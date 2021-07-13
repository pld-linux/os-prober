Summary:	Utilities that detect other operating system installs on a set of drives
Summary(pl.UTF-8):	Narzędzia wykrywające instalacje innych systemów operacyjnych na dyskach
Name:		os-prober
Version:	1.79
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.xz
# Source0-md5:	08d3bfff00f1f7c068ce509656728eba
URL:		http://packages.qa.debian.org/o/os-prober.html
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	mount
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/lib

%description
This is a small package that may be depended on by any bootloader
installer package to detect other filesystems with operating systems
on them, and work out how to boot other Linux installs.

%description -l pl.UTF-8
Ten mały pakiet może być wykorzystywany przez dowolne instalatory
bootloaderów w celu wykrycia innych systemów plików zawierających
systemy operacyjne i określenia sposobu uruchomienia innych instalacji
Linuksa.

%prep
%setup -q -n %{name}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{name},%{_bindir},%{_datadir}/%{name},%{_libdir}/%{name}}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}
install -p linux-boot-prober $RPM_BUILD_ROOT%{_bindir}
cp -p common.sh $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p newns $RPM_BUILD_ROOT%{_libdir}/%{name}

ARCH=other
%ifarch m68k
ARCH=m68k
%endif
%ifarch ppc ppc64
ARCH=powerpc
%endif
%ifarch sparc sparc64
ARCH=sparc
%endif
%ifarch %{ix86} %{x8664}
ARCH=x86
%endif
for probes in os-probes os-probes/mounted os-probes/init \
			  linux-boot-probes linux-boot-probes/mounted; do \
	install -d $RPM_BUILD_ROOT%{_libdir}/$probes
	cp -a $probes/common/* $RPM_BUILD_ROOT%{_libdir}/$probes
	if [ -e "$probes/$ARCH" ]; then
		cp -a $probes/$ARCH/* $RPM_BUILD_ROOT%{_libdir}/$probes
	fi
done

if [ "$ARCH" = x86 ]; then
	cp -p os-probes/mounted/powerpc/20macosx $RPM_BUILD_ROOT%{_libdir}/os-probes/mounted
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO debian/changelog debian/copyright
%attr(755,root,root) %{_bindir}/linux-boot-prober
%attr(755,root,root) %{_bindir}/os-prober
%dir %{_libdir}/linux-boot-probes
%attr(755,root,root) %{_libdir}/linux-boot-probes/50mounted-tests
%dir %{_libdir}/linux-boot-probes/mounted
%attr(755,root,root) %{_libdir}/linux-boot-probes/mounted/*
%dir %{_libdir}/os-prober
%attr(755,root,root) %{_libdir}/os-prober/newns
%dir %{_libdir}/os-probes
%attr(755,root,root) %{_libdir}/os-probes/50mounted-tests
%dir %{_libdir}/os-probes/init
%attr(755,root,root) %{_libdir}/os-probes/init/*
%dir %{_libdir}/os-probes/mounted
%attr(755,root,root) %{_libdir}/os-probes/mounted/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/common.sh
%dir /var/lib/os-prober
