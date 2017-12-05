%{?cygwin_package_header}

Name:           cygwin-zlib
Version:        1.2.11
Release:        1%{?dist}
Summary:        Cygwin zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
BuildArch:      noarch

Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
Patch0:         zlib-1.2.5-minizip-fixuncrypt.patch
Patch100:       zlib-1.2.7-minizip-cygwin.patch
Patch101:       zlib-1.2.8-vpath.patch
Patch102:       zlib-1.2.11-gzopen_w.patch

BuildRequires:  cygwin32-filesystem >= 11
BuildRequires:  cygwin32-gcc
BuildRequires:  cygwin32-binutils

BuildRequires:  cygwin64-filesystem >= 11
BuildRequires:  cygwin64-gcc
BuildRequires:  cygwin64-binutils

BuildRequires:  autoconf automake cygwin-libtool-base

%description
Cygwin zlib compression library.

%package -n cygwin32-zlib
Summary:        Cygwin32 zlib compression library
Group:          Development/Libraries

%description -n cygwin32-zlib
zlib compression library for Cygwin i686 toolchain.

%package -n cygwin64-zlib
Summary:        Cygwin64 zlib compression library
Group:          Development/Libraries

%description -n cygwin64-zlib
zlib compression library for Cygwin x86_64 toolchain.

%package -n cygwin32-zlib-static
Summary:        Static libraries for cygwin32-zlib development.
Group:          Development/Libraries
Requires:       cygwin32-zlib = %{version}-%{release}

%description -n cygwin32-zlib-static
The cygwin32-zlib-static package contains static library for cygwin32-zlib development.

%package -n cygwin64-zlib-static
Summary:        Static libraries for cygwin64-zlib development.
Group:          Development/Libraries
Requires:       cygwin64-zlib = %{version}-%{release}

%description -n cygwin64-zlib-static
The cygwin64-zlib-static package contains static library for cygwin64-zlib development.

%package -n cygwin32-minizip
Summary:        Minizip library for Cygwin32 toolchain
Group:          Development/Libraries
Requires:       cygwin32-zlib = %{version}-%{release}

%description -n cygwin32-minizip
Minizip library for the Cygwin i686 cross-compiler toolchain.

%package -n cygwin64-minizip
Summary:   Minizip library for Cygwin64 toolchain
Group:     Development/Libraries
Requires:  cygwin64-zlib = %{version}-%{release}

%description -n cygwin64-minizip
Minizip library for the Cygwin x86_64 cross-compiler toolchain.


%{?cygwin_debug_package}


%prep
%setup -q -n zlib-%{version}
%patch0 -p1
%patch100 -p2
%patch101 -p2
%patch102 -p2
iconv -f windows-1252 -t utf-8 <ChangeLog >ChangeLog.tmp
pushd contrib/minizip
%cygwin_autoreconf
popd

%build
mkdir -p build_32bit
pushd build_32bit
ln -s ../zlib.h ../zconf.h ../zlib.pc.in .
../configure
make -f ../win32/Makefile.gcc \
  CC=%{cygwin32_cc} AR=%{cygwin32_ar} RC=%{cygwin32_windres} STRIP=: \
  CFLAGS="%{cygwin32_cflags}" \
  SHAREDLIB=cygz.dll IMPLIB=libz.dll.a \
  VPATH=.. \
  all
popd

mkdir -p build_64bit
pushd build_64bit
ln -s ../zlib.h ../zconf.h ../zlib.pc.in .
../configure
make -f ../win32/Makefile.gcc \
  CC=%{cygwin64_cc} AR=%{cygwin64_ar} RC=%{cygwin64_windres} STRIP=: \
  CFLAGS="%{cygwin64_cflags}" \
  SHAREDLIB=cygz.dll IMPLIB=libz.dll.a \
  VPATH=.. \
  all
popd

pushd contrib/minizip
%cygwin_configure --disable-static
CYGWIN32_MAKE_ARGS="zlib_top_builddir=../../../build_32bit"
CYGWIN64_MAKE_ARGS="zlib_top_builddir=../../../build_64bit"
%cygwin_make %{?_smp_flags}
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

pushd contrib/minizip
%cygwin_make install DESTDIR=$RPM_BUILD_ROOT
popd

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove the documentation and manpages which duplicate Fedora native
rm -rf $RPM_BUILD_ROOT/%{cygwin32_mandir}
rm -rf $RPM_BUILD_ROOT/%{cygwin64_mandir}


%files -n cygwin32-zlib
%{cygwin32_bindir}/cygz.dll
%{cygwin32_includedir}/zconf.h
%{cygwin32_includedir}/zlib.h
%{cygwin32_libdir}/libz.dll.a
%{cygwin32_libdir}/pkgconfig/zlib.pc

%files -n cygwin32-zlib-static
%{cygwin32_libdir}/libz.a

%files -n cygwin32-minizip
%{cygwin32_bindir}/cygminizip-1.dll
%{cygwin32_includedir}/minizip/
%{cygwin32_libdir}/libminizip.dll.a
%{cygwin32_libdir}/pkgconfig/minizip.pc

%files -n cygwin64-zlib
%{cygwin64_bindir}/cygz.dll
%{cygwin64_includedir}/zconf.h
%{cygwin64_includedir}/zlib.h
%{cygwin64_libdir}/libz.dll.a
%{cygwin64_libdir}/pkgconfig/zlib.pc

%files -n cygwin64-zlib-static
%{cygwin64_libdir}/libz.a

%files -n cygwin64-minizip
%{cygwin64_bindir}/cygminizip-1.dll
%{cygwin64_includedir}/minizip/
%{cygwin64_libdir}/libminizip.dll.a
%{cygwin64_libdir}/pkgconfig/minizip.pc


%changelog
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
