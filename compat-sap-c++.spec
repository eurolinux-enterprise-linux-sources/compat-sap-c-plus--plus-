# SAP HACK: Start custom scl information for SAP build.
%global scl 1
%global scl_prefix compat-sap-
%global _root_prefix /opt/rh/SAP
%global _root_infodir %{_root_prefix}/%{_infodir}
%global _root_mandir %{_root_prefix}/%{_mandir}
# END SAP HACK.
%{?scl:%global __strip strip}
%{?scl:%global __objdump objdump}
%global DATE 20140120
%global SVNREV 206854
%global gcc_version 4.8.2
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 16
%global gmp_version 4.3.1
%global mpfr_version 2.4.1
%global mpc_version 0.8.1
%global ppl_version 0.10.1
%global cloog_version 0.18.0
%global graphviz_version 2.26.0
%global doxygen_version 1.8.0
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%global build_fortran 0
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%global build_libstdcxx_docs 0
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
%global multilib_32_arch i686
%else
%global multilib_32_arch i386
%endif
%endif
Summary: GCC version 4.8
Name: %{?scl_prefix}c++
ExclusiveArch: x86_64

Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_8-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: http://www.mpfr.org/mpfr-%{mpfr_version}/mpfr-%{mpfr_version}.tar.bz2
Source2: ftp://ftp.cs.unipr.it/pub/ppl/releases/%{ppl_version}/ppl-%{ppl_version}.tar.gz
Source3: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz
Source4: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
Source5: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{gmp_version}.tar.bz2
Source6: http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{graphviz_version}.tar.gz
Source7: ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%{doxygen_version}.src.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.17.50.0.2-8
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
#BuildRequires: systemtap-sdt-devel >= 1.3
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
%if 0%{?rhel} >= 6
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%else
BuildRequires: elfutils-devel >= 0.72
%endif
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
Requires: binutils >= 2.19.51.0.14-33
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
Requires: binutils >= 2.17.50.0.2-8
%endif
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= 4.1.2-43
Requires: libgomp >= 4.4.4-13
BuildRequires: gmp-devel >= 4.1.2-8
%if 0%{?rhel} >= 6
BuildRequires: mpfr-devel >= 2.2.1
%endif
%if %{build_libstdcxx_docs}
BuildRequires: libxml2
%if 0%{?rhel} < 6
# graphviz BRs:
BuildRequires: libpng-devel, libjpeg-devel, expat-devel, freetype-devel
BuildRequires: /bin/ksh, m4, flex, tk-devel, tcl-devel, swig
BuildRequires: fontconfig-devel, libtool-ltdl-devel
BuildRequires: libXaw-devel, libSM-devel, libXext-devel
BuildRequires: cairo-devel, pango-devel, gmp-devel
BuildRequires: gtk2-devel, libgnomeui-devel, gd-devel
BuildRequires: urw-fonts
%else
BuildRequires: graphviz
%endif
# doxygen BRs
BuildRequires: perl
%if 0%{?rhel} < 6
BuildRequires: tetex-dvips tetex-latex
%else
# SAP HACK: Removed texlive-utils
BuildRequires: texlive-dvips, texlive-latex
# END SAP HACK.
%endif
BuildRequires: ghostscript
%endif
AutoReq: true
AutoProv: false
%global oformat %{nil}
%global oformat2 %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%global oformat2 OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch ppc
%global oformat OUTPUT_FORMAT(elf32-powerpc)
%global oformat2 OUTPUT_FORMAT(elf64-powerpc)
%endif
%ifarch ppc64
%global oformat OUTPUT_FORMAT(elf64-powerpc)
%global oformat2 OUTPUT_FORMAT(elf32-powerpc)
%endif
%ifarch s390
%global oformat OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch s390x
%global oformat OUTPUT_FORMAT(elf64-s390)
%global oformat2 OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch ia64
%global oformat OUTPUT_FORMAT(elf64-ia64-little)
%endif
%if 0%{?rhel} >= 6
Requires: libstdc++ >= 4.4.4-13
%else
Requires: libstdc++ = 4.1.2
%endif

Patch0: gcc48-hack.patch
Patch1: gcc48-java-nomulti.patch
Patch2: gcc48-ppc32-retaddr.patch
Patch3: gcc48-rh330771.patch
Patch4: gcc48-i386-libgomp.patch
Patch5: gcc48-sparc-config-detection.patch
Patch6: gcc48-libgomp-omp_h-multilib.patch
Patch7: gcc48-libtool-no-rpath.patch
Patch8: gcc48-cloog-dl.patch
Patch9: gcc48-cloog-dl2.patch
Patch10: gcc48-pr38757.patch
Patch11: gcc48-libstdc++-docs.patch
Patch12: gcc48-no-add-needed.patch
Patch13: gcc48-pr56564.patch
Patch14: gcc48-pr56493.patch
Patch15: gcc48-color-auto.patch
Patch16: gcc48-pr28865.patch
Patch17: gcc48-libgo-p224.patch
Patch18: gcc48-pr60137.patch
Patch19: gcc48-pr60010.patch
Patch20: gcc48-pr60046.patch
Patch21: gcc48-pr59224.patch

Patch1000: gcc48-libstdc++-compat.patch
Patch1001: gcc48-gnu89-inline-dflt.patch
Patch1002: gcc48-ppc64-ld-workaround.patch
Patch1005: gcc48-gmp-4.0.1-s390.patch
Patch1006: gcc48-libgfortran-compat.patch
Patch1007: gcc48-alt-compat-test.patch
Patch1008: gcc48-libquadmath-compat.patch
Patch1009: gcc48-libstdc++44-xfail.patch
Patch1010: gcc48-rh1118870.patch

Patch2001: doxygen-1.7.1-config.patch
Patch2002: doxygen-1.7.5-timestamp.patch
Patch2003: doxygen-1.8.0-rh856725.patch

%if 0%{?rhel} >= 6
%global nonsharedver 44
%else
%global nonsharedver 41
%endif

%if 0%{?scl:1}
%global _gnu %{nil}
%else
%global _gnu 7E
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
This carries runtime compatibility libraries needed for SAP HANA.

%prep
%if 0%{?rhel} >= 7
%setup -q -n gcc-%{version}-%{DATE} -a 2 -a 3
%else
%if 0%{?rhel} >= 6
%setup -q -n gcc-%{version}-%{DATE} -a 2 -a 3 -a 4 -a 7
%else
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7
%endif
%endif
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%patch10 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch11 -p0 -b .libstdc++-docs~
%endif
%patch12 -p0 -b .no-add-needed~
%patch13 -p0 -b .pr56564~
%patch14 -p0 -b .pr56493~
%patch15 -p0 -b .color-auto~
%patch16 -p0 -b .pr28865~
%patch17 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch18 -p0 -b .pr60137~
%patch19 -p0 -b .pr60010~
%patch20 -p0 -b .pr60046~
%patch21 -p0 -b .pr59224~

%patch1000 -p0 -b .libstdc++-compat~
%if 0%{?rhel} < 6
%patch1001 -p0 -b .gnu89-inline-dflt~
%patch1002 -p0 -b .ppc64-ld-workaround~
%endif
%patch1006 -p0 -b .libgfortran-compat~
%ifarch %{ix86} x86_64
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1007 -p0 -b .alt-compat-test~
%endif
%if 0%{?rhel} < 7
%patch1008 -p0 -b .libquadmath-compat~
%endif
%if 0%{?rhel} == 6
%patch1009 -p0 -b .libstdc++44-xfail~
%endif
%patch1010 -p0 -b .rh1118870~

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 7
cd doxygen-%{doxygen_version}
%patch2001 -p1 -b .config~
%patch2002 -p1 -b .timestamp~
%patch2003 -p1 -b .rh856725~
cd ..
%endif
%endif
sed -i -e 's/4\.8\.3/4.8.2/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?rhel} >= 6
# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi
%endif
# Default to -fno-debug-types-section -grecord-gcc-switches
sed -i '/flag_debug_types_section/s/Init(1)/Init(0)/' gcc/common.opt
sed -i '/dwarf_record_gcc_switches/s/Init(0)/Init(1)/' gcc/common.opt

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 6
mkdir graphviz graphviz-install
cd graphviz
find ../../graphviz-%{graphviz_version} -type f '(' \
  -name '*.h' -or -name '*.c' ')' -exec chmod 644 {} ';'
../../graphviz-%{graphviz_version}/configure --with-x --disable-static \
  --disable-dependency-tracking --without-mylibgd --with-ipsepcola \
  --with-pangocairo --with-gdk-pixbuf --disable-sharp \
  --disable-ocaml --without-ming --disable-r --without-devil \
  --disable-perl --disable-java --disable-ruby --disable-php \
  --disable-python --disable-lua --with-expatlibdir=/usr/%{_lib}/ \
  CFLAGS="${CFLAGS:-%optflags} -ffast-math -fno-strict-aliasing" \
  CXXFLAGS="${CXXFLAGS:-%optflags} -ffast-math -fno-strict-aliasing" \
  --prefix=`cd ..; pwd`/graphviz-install
make %{?_smp_mflags}
make install
export LD_LIBRARY_PATH=`cd ..; pwd`/graphviz-install/lib/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
../graphviz-install/bin/dot -c
export PATH=`cd ..; pwd`/graphviz-install/bin/${PATH:+:${PATH}}
cd ..
%endif

mkdir doxygen-install
pushd ../doxygen-%{doxygen_version}
./configure --prefix `cd ..; pwd`/obj-%{gcc_target_platform}/doxygen-install \
  --shared --release --english-only

make %{?_smp_mflags} all
make install
popd
export PATH=`pwd`/doxygen-install/bin/${PATH:+:${PATH}}
%endif

%if 0%{?rhel} < 6
mkdir gmp gmp-install
cd gmp
../../gmp-%{gmp_version}/configure --disable-shared \
  --enable-cxx --enable-mpbsd --build=%{_build} --host=%{_host} \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..

mkdir mpfr mpfr-install
cd mpfr
../../mpfr-%{mpfr_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/mpfr-install --with-gmp=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..
%endif

mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
%if 0%{?rhel} < 6
  --with-gmp=`cd ..; pwd`/gmp-install --with-mpfr=`cd ..; pwd`/mpfr-install \
%endif
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
chmod +x g++64
CXX=`pwd`/g++64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
  cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
  chmod +x g++64
  CXX=`pwd`/g++64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Werror=format-security / -Wformat -Werror=format-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --disable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
%if 0%{?rhel} >= 6
	--enable-gnu-unique-object \
%else
	--disable-gnu-unique-object \
%endif
%if 0%{?rhel} >= 6 || 0%{?scl:1}
	--enable-linker-build-id \
%else
	--disable-linker-build-id \
%endif
%if %{build_fortran}
	--enable-languages=c,c++,fortran,lto \
%else
	--enable-languages=c,c++,lto \
%endif
	--enable-plugin --with-linker-hash-style=gnu \
%if 0%{?scl:1}
	--enable-initfini-array \
%else
%ifnarch ia64
%if 0%{?rhel} >= 7
	--enable-initfini-array \
%else
	--disable-initfini-array \
%endif
%endif
%endif
	--disable-libgcj \
	--with-gmp=`pwd`/gmp-install --with-mpfr=`pwd`/mpfr-install \
	--with-mpc=`pwd`/mpc-install \
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
%if 0%{?rhel} >= 6
	--with-arch=i686 \
%else
	--with-arch=i586 \
%endif
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
	--with-arch_32=i686 \
%else
	--with-arch_32=i586 \
%endif
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

%ifarch ia64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
# SAP HACK: Don't bootstrap.
# GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"
# END SAP HACK.
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,libstdc++-v3,libgomp}

for i in {gcc,gcc/cp,libstdc++-v3,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

%if %{build_fortran}
(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif

%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif

%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}
cd obj-%{gcc_target_platform}
cp ./x86_64-redhat-linux/libstdc++-v3/src/.libs/libstdc++.so.6.0.* %{buildroot}%{_root_prefix}/%{_lib}/compat-sap-c++.so

%check
cd obj-%{gcc_target_platform}

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

# SAP HACK: Use the system libstdc++.so.6.
# Test against the system libstdc++.so.6 + libstdc++_nonshared.a combo
#mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6{,.not_here}
#mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so{,.not_here}
#ln -sf %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 \
#  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6
#echo '/* GNU ld script
#   Use the shared library, but some functions are only in
#   the static library, so try that secondarily.  */
#%{oformat}
#INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' \
#  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so
#cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
#  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared.a
# END SAP HACK.

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
rm -rf gcc/testsuite.prev
mv gcc/testsuite{,.prev}
rm -f gcc/site.exp
make %{?_smp_mflags} -C gcc -k check-gcc check-g++ ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}' compat.exp struct-layout-1.exp" || :
mv gcc/testsuite/gcc/gcc.sum{,.sent}
mv gcc/testsuite/g++/g++.sum{,.sent}
( LC_ALL=C ../contrib/test_summary -o -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults2
rm -rf gcc/testsuite.compat
mv gcc/testsuite{,.compat}
mv gcc/testsuite{.prev,}
echo ====================TESTING=========================
cat testresults
echo ===`gcc --version | head -1` compatibility tests====
cat testresults2
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_root_prefix}
%dir %{_root_prefix}/%{_lib}
%{_root_prefix}/%{_lib}/compat-sap-c++.so

%changelog
* Wed May 20 2015 Marek Polacek <polacek@redhat.com> 4.8.2-16
- backport PR59224 fix again

* Wed Mar 18 2015 Marek Polacek <polacek@redhat.com> 4.8.2-15
- rebase to 4.8 (#1198501)

* Tue Apr 01 2014 Marek Polacek <polacek@redhat.com> 4.7.2-10
- backport PR59224 fix

* Tue Mar 25 2014 Marek Polacek <polacek@redhat.com> 4.7.2-9
- clarify description (#1080544)

* Wed Mar 12 2014 Marek Polacek <polacek@redhat.com> 4.7.2-8
- rename sap-compat-c++.so to compat-sap-c++.so

* Wed Mar 05 2014 Marek Polacek <polacek@redhat.com> 4.7.2-7
- run the testsuite
- fix up Provides
- update description

* Wed Mar 05 2014 Marek Polacek <polacek@redhat.com> 4.7.2-6
- build only compat-sap-c++, that only installs sap-compat-c++.so

* Tue Mar 04 2014 Jonathan Wakely <jwakely@redhat.com> 4.7.2-6
- adjust gcc47-ppl-check.patch
- remove gdb files from %files

* Mon Oct 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-5
- update from the 4.7 branch
  - GCC 4.7.2 release
- operator new[] overflow checking (#850911, PR c++/19351)
- selected debug info quality improvements (#851467)

* Fri Sep 14 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-8
- adjust doxygen configgen.py for older python (#856725)

* Wed Sep  5 2012 Marek Polacek <polacek@redhat.com> 4.7.1-7.3
- use --with-expatlibdir when building graphviz

* Thu Aug 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7.2
- redefine __strip and __objcopy macros

* Wed Aug 22 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7.1
- install gfortran.1 manual page and gfortran info pages (#850448)

* Mon Aug 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7
- update from the 4.7 branch
- backport -mrdseed, -mprfchw and -madx support

* Fri Jul 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-5
- update from the 4.7 branch

* Mon Jul 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-3
- update from the 4.7 branch
  - C++11 ABI change - std::list and std::pair in C++11 ABI compatible again
    with C++03, but ABI incompatible with C++11 in GCC 4.7.[01]
- backport -mrtm and -mhle support

* Fri Jun 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-1
- update from the 4.7 branch
  - GCC 4.7.1 release
- enable build_gfortran (#819596)

* Mon May 28 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5.2
- selected 4.7 backports (#825827)
  - fix i?86 8-bit mem += val ICE (PR target/53358)
  - alias handling fix (PR tree-optimization/53364)
  - vectorizer complex handling fix (PR tree-optimization/53366)
  - VRP bitfield fix (PRs tree-optimization/53438, tree-optimization/53505)
  - VRP NVR fix (PR tree-optimization/53465)

* Wed May  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5.1
- remove html docs from %{?scl_prefix}libstdc++%{!?scl:47}-devel
  package now that they are in %{?scl_prefix}libstdc++%{!?scl:47}-docs

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5
- update from 4.7 branch
- build libstdc++ docs with doxygen 1.8.0 instead of 1.7.1

* Fri May  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-4
- update from 4.7 branch
- fix up gcc-ar, gcc-nm and gcc-ranlib (#818311, PR plugins/53126)
%if 0%{?rhel} == 6
- configure for i686 rather than i586 by default
%endif
- add %{?scl_prefix}libstdc++%{!?scl:47}-docs subpackage

* Wed Apr 18 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-2
- update from 4.7 branch
%if 0%{?scl:1} && 0%{?rhel} == 5
- allow building of the package even when %{name} is already
  installed (#808628)
%endif

* Tue Mar 27 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-1.1
- update from trunk and 4.7 branch
  - GCC 25th Anniversary 4.7.0 release
%if 0%{?scl:1} && 0%{?rhel} == 5
- configure with --enable-build-id (#804963)
%endif
- enable libitm build (#800503)
- fix up libgomp.so, so that libgomp isn't linked always statically

* Mon Mar  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18.1
- add a few missing copyright boilerplates to libstdc++_nonshared.a
  sources

* Wed Feb 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18
- update from trunk
- apply patch0 (#797774)
- remove libquadmath.so.debug from debuginfo (#797781)
- add some further binaries (#797660)

* Sat Feb 25 2012 Jeff Law <law@redhat.com> 4.7.0-0.17
- xfail tests which are expected to fail

* Fri Feb 24 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.16
- new package
