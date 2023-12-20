%define pkgname efimirror
%global forgeurl https://github.com/danielkza/%{pkgname}
%global branch master

%forgemeta

%global debug_package %{nil}

Name:           %{pkgname}
Version:        0.1
Release:        1%{?dist}
Summary:        EFI Partition Redundancy
License:        GPL-2.0

URL:            %{forgeurl}
%if "%{?_project}" == ""
Source0:        %{forgesource}
%else
Source0: %{name}-%{version}.tar.gz
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
%forgesetup

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