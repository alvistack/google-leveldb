# Copyright 2026 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: leveldb
Epoch: 100
Version: 1.23
Release: 1%{?dist}
Summary: Fast key-value storage library
License: BSD-3-Clause
URL: https://github.com/google/leveldb/tags
Source0: %{name}_%{version}.orig.tar.gz
Patch0001: 0001-Allow-leveldbjni-build.patch
Patch0002: 0002-Added-a-DB-SuspendCompations-and-DB-ResumeCompaction.patch
Patch0003: 0003-allow-Get-calls-to-avoid-copies-into-std-string.patch
Patch0004: 0004-bloom_test-failure-on-big-endian-archs.patch
Patch0006: 0006-revert-no-rtti.patch
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: devtoolset-11-libatomic-devel
%endif
BuildRequires: cmake4
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: snappy-devel

%description
LevelDB is a fast key-value storage library written at Google that
provides an ordered mapping from string keys to string values.

%prep
%setup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .
%autopatch -p1

%build
mkdir -p build
pushd build && \
    cmake \
        .. \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DLEVELDB_BUILD_BENCHMARKS=OFF \
        -DLEVELDB_BUILD_TESTS=OFF \
        -DCMAKE_POLICY_VERSION_MINIMUM=3.5 && \
popd
pushd build && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
popd

%install
pushd build && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd

%if 0%{?suse_version} >= 1500
%package -n libleveldb1
Summary: Fast key-value storage library

%description -n libleveldb1
LevelDB is a fast key-value storage library written at Google that
provides an ordered mapping from string keys to string values.

%package -n leveldb-devel
Summary: Fast key-value storage library
Requires: libleveldb1 = %{epoch}:%{version}-%{release}

%description -n leveldb-devel
LevelDB is a fast key-value storage library written at Google that
provides an ordered mapping from string keys to string values.

%post -n libleveldb1 -p /sbin/ldconfig
%postun -n libleveldb1 -p /sbin/ldconfig

%files
%license LICENSE

%files -n libleveldb1
%{_libdir}/*.so.*

%files -n leveldb-devel
%dir %{_libdir}/cmake/leveldb/
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/leveldb/*
%endif

%if !(0%{?suse_version} >= 1500)
%package -n leveldb-devel
Summary: Fast key-value storage library
Requires: leveldb = %{epoch}:%{version}-%{release}

%description -n leveldb-devel
This package contains the development files required to build programs
against leveldb.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files -n leveldb-devel
%dir %{_libdir}/cmake/leveldb/
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/leveldb/*
%endif

%changelog
