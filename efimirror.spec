%define pkgname efimirror
%global forgeurl https://github.com/danielkza/%{pkgname}
%global branch master

%forgemeta

Name:           %{pkgname}
Version:        0.1
Release:        1%{?dist}
Summary:        EFI Partition Redundancy
License:        GPL-2.0

URL:            %{forgeurl}
Source:         %{forgesource}

BuildRequires: meson
BuildRequires: systemd-rpm-macros

Requires: lsyncd
Requires: systemd >= 249
Requires: efibootmgr
Requires: bash

%description
EFI Partition Redundancy

%prep
%forgesetup

%build
%meson -D"systemd-generator-dir=%{_systemdgeneratordir}"
%meson_build

%install
%meson_install

%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libexecdir}/%{pkgname}/*
%{_systemdgeneratordir}/*
