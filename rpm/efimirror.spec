%define pkgname efimirror
%global repourl https://github.com/danielkza/%{pkgname}

%global debug_package %{nil}

Name:           %{pkgname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        EFI Partition Redundancy
License:        GPL-2.0

URL: %{repourl}

# For OBS, dont be smart with naming artifacts for git refs
%if %{?_obs:1}%{!?_obs:0}

Source0: %{pkgname}-%{version}.tar.gz
%else

%if %{?commit:1}%{!?commit:0}
%define gitref %{commit}
%elif %{?gittag:1}%{!?gittag:0}
%define gitref %{gittag}
%else
%define gitref master
%endif

%define archivename %{pkgname}-%{gitref}
Source0: %{repourl}/archive/%{gitref}/%{archivename}.tar.gz

%endif

BuildRequires: meson
BuildRequires: systemd-rpm-macros

Requires: lsyncd
Requires: systemd >= 249
Requires: efibootmgr
Requires: bash

BuildArch: noarch

%description
EFI Partition Redundancy

%prep
%autosetup -n %{archivename}

%build
%meson \
  -D"systemd-generator-dir=%{_systemdgeneratordir}" \
  -D"config-env-dir=%{_sysconfdir}/sysconfig/"
%meson_build

%install
%meson_install

%check

%post
systemctl daemon-reload
systemctl start local-fs.target

%postun
if [ $1 == 0 ]; then
  systemctl daemon-reload
  systemctl reset-failed
fi

%files
%license LICENSE
%doc README.md
%{_libexecdir}/%{pkgname}/*
%{_systemdgeneratordir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{pkgname}
