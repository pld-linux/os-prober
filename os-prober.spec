Summary:	Utilities that detect other operating system installs on a set of drives
Name:		os-prober
Version:	1.44
Release:	1
License:	GPL
Group:		Base/Kernel
URL:		http://packages.qa.debian.org/o/os-prober.html
Source0:	http://ftp.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.gz
# Source0-md5:	44781dbc2fd748a678fe9d2f29f862ef
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# no binary blobs
%define		_enable_debug_packages	0

%description
This is a small package that may be depended on by any bootloader
installer package to detect other filesystems with operating systems
on them, and work out how to boot other linux installs.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}"
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/%{name},%{_bindir},%{_datadir}/%{name},%{_libdir}/%{name}}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}
install -p linux-boot-prober $RPM_BUILD_ROOT%{_bindir}
cp -a common.sh $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p newns $RPM_BUILD_ROOT%{_libdir}/%{name}

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
	cp -a os-probes/mounted/powerpc/20macosx $RPM_BUILD_ROOT%{_libdir}/os-probes/mounted
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO debian/changelog debian/copyright
%attr(755,root,root) %{_bindir}/*prober
%dir %{_libdir}/os-probes
%attr(755,root,root) %{_libdir}/os-probes/*
%dir %{_libdir}/os-prober
%attr(755,root,root) %{_libdir}/os-prober/newns
%dir %{_libdir}/linux-boot-probes
%attr(755,root,root) %{_libdir}/linux-boot-probes/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/common.sh
%dir /var/lib/os-prober
