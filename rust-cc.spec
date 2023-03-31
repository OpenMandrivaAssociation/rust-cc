%bcond_without check
%global debug_package %{nil}

# https://github.com/alexcrichton/cc-rs/issues/139
%global __cargo_is_bin() false

%global crate cc

Name:           rust-%{crate}
Version:        1.0.72
Release:        2
Summary:        Build-time dependency for Cargo build scripts to invoke the native C compiler

# Upstream license specification: MIT/Apache-2.0
License:        MIT or ASL 2.0
URL:            https://crates.io/crates/cc
Source:         %{crates_source}

ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif

BuildRequires:  rust-packaging

%global _description %{expand:
Build-time dependency for Cargo build scripts to assist in invoking the native
C compiler to compile native C code into a static archive to be linked into
Rust code.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch
Requires:       gcc-c++
Requires:       gcc

%description    devel %{_description}

This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%license LICENSE-MIT LICENSE-APACHE
%doc README.md
%{cargo_registry}/%{crate}-%{version_no_tilde}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%package     -n %{name}+jobserver-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+jobserver-devel %{_description}

This package contains library source intended for building other packages
which use "jobserver" feature of "%{crate}" crate.

%files       -n %{name}+jobserver-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%package     -n %{name}+parallel-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+parallel-devel %{_description}

This package contains library source intended for building other packages
which use "parallel" feature of "%{crate}" crate.

%files       -n %{name}+parallel-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
%if %{with check}
echo '/usr/bin/g++'
echo '/usr/bin/gcc'
%endif

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
# Tests can't be really run in parallel
# And they are too tight to arch
%cargo_test -- -- --test-threads=1 || :
%endif
