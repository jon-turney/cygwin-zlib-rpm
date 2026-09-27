%{?cygwin_package_header}

Name:           cygwin-zlib
Version:        1.3.2
Release:        1%{?dist}
Summary:        Cygwin zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            https://zlib.net/
BuildArch:      noarch

Source0:        https://zlib.net/zlib-%{version}.tar.gz
Patch101:       zlib-1.3.2-vpath.patch
Patch102:       zlib-1.3.2-configure.patch
Patch103:       zlib-1.3.2-gzopen_w.patch

BuildRequires:  cygwin32-filesystem >= 11
BuildRequires:  cygwin32-gcc
BuildRequires:  cygwin32-binutils

BuildRequires:  cygwin64-filesystem >= 11
BuildRequires:  cygwin64-gcc
BuildRequires:  cygwin64-binutils

BuildRequires:  cygwin-aarch64-filesystem >= 151
BuildRequires:  cygwin-aarch64-gcc
BuildRequires:  cygwin-aarch64-binutils

BuildRequires:  make

%description
Cygwin zlib compression library.

%package -n cygwin32-zlib
Summary:        Cygwin i686 zlib compression library
Group:          Development/Libraries

%description -n cygwin32-zlib
zlib compression library for Cygwin i686 toolchain.

%package -n cygwin64-zlib
Summary:        Cygwin x86_64 zlib compression library
Group:          Development/Libraries

%description -n cygwin64-zlib
zlib compression library for Cygwin x86_64 toolchain.

%package -n cygwin-aarch64-zlib
Summary:        Cygwin aarch64 zlib compression library
Group:          Development/Libraries

%description -n cygwin-aarch64-zlib
zlib compression library for Cygwin aarch64 toolchain.

%package -n cygwin32-zlib-static
Summary:        Static libraries for Cygwin i686 zlib development
Group:          Development/Libraries
Requires:       cygwin32-zlib = %{version}-%{release}

%description -n cygwin32-zlib-static
The cygwin32-zlib-static package contains static library for cygwin x86 zlib development.

%package -n cygwin64-zlib-static
Summary:        Static libraries for cygwin x86_64 zlib development
Group:          Development/Libraries
Requires:       cygwin64-zlib = %{version}-%{release}

%description -n cygwin64-zlib-static
The cygwin64-zlib-static package contains static library for cygwin x86_64 zlib development.

%package -n cygwin-aarch64-zlib-static
Summary:        Static libraries for cygwin aarch64 zlib development
Group:          Development/Libraries
Requires:       cygwin-aarch64-zlib = %{version}-%{release}

%description -n cygwin-aarch64-zlib-static
The cygwin-aarch64-zlib-static package contains static library for cygwin aarch64 zlib development.



%{?cygwin_debug_package}


%prep
%autosetup -p2 -n zlib-%{version}

%build
unset CC
unset CFLAGS

mkdir -p build_32bit
pushd build_32bit
ln -s ../zlib.h ../zlib.pc.in .
CHOST=%{cygwin32_target} ../configure
make -f ../win32/Makefile.gcc \
  CC=%{cygwin32_cc} AR=%{cygwin32_ar} RC=%{cygwin32_windres} STRIP=: \
  CFLAGS="%{cygwin32_cflags} -std=c90" \
  SHAREDLIB=cygz.dll IMPLIB=libz.dll.a \
  VPATH=.. \
  all
popd

mkdir -p build_64bit
pushd build_64bit
ln -s ../zlib.h ../zlib.pc.in .
CHOST=%{cygwin64_target} ../configure
make -f ../win32/Makefile.gcc \
  CC=%{cygwin64_cc} AR=%{cygwin64_ar} RC=%{cygwin64_windres} STRIP=: \
  CFLAGS="%{cygwin64_cflags} -std=c90" \
  SHAREDLIB=cygz.dll IMPLIB=libz.dll.a \
  VPATH=.. \
  all
popd

mkdir -p build_aarch64
pushd build_aarch64
ln -s ../zlib.h ../zlib.pc.in .
CHOST=%{cygwin_aarch64_target} ../configure
make -f ../win32/Makefile.gcc \
  CC=%{cygwin_aarch64_cc} AR=%{cygwin_aarch64_ar} RC=%{cygwin_aarch64_windres} STRIP=: \
  CFLAGS="%{cygwin_aarch64_cflags} -std=c90" \
  SHAREDLIB=cygz.dll IMPLIB=libz.dll.a \
  VPATH=.. \
  all
popd


%install
pushd build_32bit
make -f ../win32/Makefile.gcc \
  DESTDIR=$RPM_BUILD_ROOT \
  BINARY_PATH=%{cygwin32_bindir} \
  INCLUDE_PATH=%{cygwin32_includedir} \
  LIBRARY_PATH=%{cygwin32_libdir} \
  SHARED_MODE=1 \
  SHAREDLIB=cygz.dll \
  IMPLIB=libz.dll.a \
  VPATH=.. \
  install
popd

pushd build_64bit
make -f ../win32/Makefile.gcc \
  DESTDIR=$RPM_BUILD_ROOT \
  BINARY_PATH=%{cygwin64_bindir} \
  INCLUDE_PATH=%{cygwin64_includedir} \
  LIBRARY_PATH=%{cygwin64_libdir} \
  SHARED_MODE=1 \
  SHAREDLIB=cygz.dll \
  IMPLIB=libz.dll.a \
  VPATH=.. \
  install
popd

pushd build_aarch64
make -f ../win32/Makefile.gcc \
  DESTDIR=$RPM_BUILD_ROOT \
  BINARY_PATH=%{cygwin_aarch64_bindir} \
  INCLUDE_PATH=%{cygwin_aarch64_includedir} \
  LIBRARY_PATH=%{cygwin_aarch64_libdir} \
  SHARED_MODE=1 \
  SHAREDLIB=cygz.dll \
  IMPLIB=libz.dll.a \
  VPATH=.. \
  install
popd

# Remove the documentation and manpages which duplicate Fedora native
rm -rf $RPM_BUILD_ROOT/%{cygwin32_mandir}
rm -rf $RPM_BUILD_ROOT/%{cygwin64_mandir}
rm -rf $RPM_BUILD_ROOT/%{cygwin_aarch64_mandir}


%files -n cygwin32-zlib
%{cygwin32_bindir}/cygz.dll
%{cygwin32_includedir}/zconf.h
%{cygwin32_includedir}/zlib.h
%{cygwin32_libdir}/libz.dll.a
%{cygwin32_libdir}/pkgconfig/zlib.pc

%files -n cygwin32-zlib-static
%{cygwin32_libdir}/libz.a

%files -n cygwin64-zlib
%{cygwin64_bindir}/cygz.dll
%{cygwin64_includedir}/zconf.h
%{cygwin64_includedir}/zlib.h
%{cygwin64_libdir}/libz.dll.a
%{cygwin64_libdir}/pkgconfig/zlib.pc

%files -n cygwin64-zlib-static
%{cygwin64_libdir}/libz.a

%files -n cygwin-aarch64-zlib
%{cygwin_aarch64_bindir}/cygz.dll
%{cygwin_aarch64_includedir}/zconf.h
%{cygwin_aarch64_includedir}/zlib.h
%{cygwin_aarch64_libdir}/libz.dll.a
%{cygwin_aarch64_libdir}/pkgconfig/zlib.pc

%files -n cygwin-aarch64-zlib-static
%{cygwin_aarch64_libdir}/libz.a


%changelog
* Sun Sep 27 2026 Jon Turney <jon.turney@dronecode.org.uk> - 1.3.2-1
- new version

* Sun Sep 27 2026 Jon Turney <jon.turney@dronecode.org.uk> - 1.2.11-3
- Add aarch64

* Mon Jan 10 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.11-2
- Drop minizip subpackage.

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.11-1
- new version

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.8-3
- Fix build on EL6

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.8-2
- Add Fedora patches and build fixes

* Sun Jun 30 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.2.8-1
- Version bump.
- Update for new Cygwin packaging scheme.

* Wed May 23 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.2.7-1
- Version bump.
- Added minizip subpackage.

* Thu Feb 17 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.2.5-2
- Added debuginfo package.

* Wed Feb 16 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.2.5-1
- Initial RPM release, largely based on mingw32-zlib.
