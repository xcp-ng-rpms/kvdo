Name: vdo-modules
Summary: Kernel Modules for Virtual Data Optimizer
Version: 6.2.1.138
Release: 1%{?dist}
License: GPLv2+

Source0: https://github.com/dm-vdo/kvdo/archive/%{version}/kvdo-%{version}.tar.gz 

BuildRequires: gcc
BuildRequires: kernel-devel
#BuildRequires: libuuid-devel

Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the kernel modules for VDO.

%prep
%autosetup -p1 -n kvdo-%{version}

%build
make -C /usr/src/kernels/%{kernel_version}-x86_64 M=$(pwd)

%install
install -d %{buildroot}/lib/modules/%{kernel_version}/extra
install -m 744 uds/uds.ko %{buildroot}/lib/modules/%{kernel_version}/extra
install -m 744 vdo/kvdo.ko %{buildroot}/lib/modules/%{kernel_version}/extra

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/extra/uds.ko
/lib/modules/%{kernel_version}/extra/kvdo.ko

%changelog
* Tue Sep 10 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 6.2.1.138-1
- Import kvdo, custom spec file from XCP-ng
