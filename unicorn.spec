# I love OpenSource :-(

%define name unicorn
%define version 0.9.3
%define mdkrelease 5
%define release %mkrel %{mdkrelease}

Summary:	unicorn utility for BeWan Architecture support.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	unicorn-%{version}.tar.bz2
Source1:	module_param.patch
#Patch0:		maxpacket.patch.bz2
#Patch0:		unicorn-0.8.7-fno-gnu-linker.patch.bz2
Patch1:		unicorn-0.9.0-kernel26-spinlock.patch
Patch2:		unicorn-0.9.3-smp.patch
Patch3:		unicorn-0.9.3-kernel2.6.22.patch
Patch4:		unicorn-0.9.3-build.patch
License:	BeWan 2004
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gtk-devel, automake1.4

%description -n %{name}
BeWan Architecture utility.

%package -n dkms-%{name}
Summary:	unicorn kernel module for BeWan Architecture support.
Group:		System/Kernel and hardware
Requires(post):		dkms
Requires(preun):		dkms
Requires:	gcc-c++

%description -n dkms-%{name}
unicorn Architecture support for Linux kernel %{kernel_version}

%prep
%setup -q -n %{name}
%patch1 -p1 -b .spinlock
%patch2 -p1 -b .smp
%patch3 -p1 -b .2.6.22
%patch4 -p1 -b .build

pushd adsl_status
%configure
popd

%build
%make -C adsl_status

%install
rm -rf $RPM_BUILD_ROOT
# utils 
%make -C adsl_status DESTDIR="$RPM_BUILD_ROOT" install
%find_lang bewan_adsl_status

# driver source
mkdir -p $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}
cp -r * $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}/patches/
cat > $RPM_BUILD_ROOT/%{_usr}/src/%{name}-%{version}/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}

DEST_MODULE_LOCATION[0]=/kernel/drivers/net
DEST_MODULE_LOCATION[1]=/kernel/drivers/net
DEST_MODULE_LOCATION[2]=/kernel/drivers/usb/net
DEST_MODULE_LOCATION[3]=/kernel/drivers/usb/net
BUILT_MODULE_NAME[0]=unicorn_pci_atm
BUILT_MODULE_LOCATION[0]=unicorn_pci
BUILT_MODULE_NAME[1]=unicorn_pci_eth
BUILT_MODULE_LOCATION[1]=unicorn_pci
BUILT_MODULE_NAME[2]=unicorn_usb_atm
BUILT_MODULE_LOCATION[2]=unicorn_usb
BUILT_MODULE_NAME[3]=unicorn_usb_eth
BUILT_MODULE_LOCATION[3]=unicorn_usb
MAKE[0]="make KERNEL_SOURCES=\${kernel_source_dir} modules"
CLEAN="make clean"

PATCH[0]=module_param.patch
PATCH_MATCH[0]="2.6.17.*"

AUTOINSTALL=yes
EOF

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %name -v %version
/usr/sbin/dkms --rpm_safe_upgrade build -m %name -v %version
/usr/sbin/dkms --rpm_safe_upgrade install -m %name -v %version

%preun -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %name -v %version --all

%clean
rm -rf $RPM_BUILD_ROOT

%files -f bewan_adsl_status.lang
%defattr(-,root,root)
%doc COPYING COPYING.GPL README
%{_bindir}/*
%{_datadir}/bewan_adsl_status/pixmaps/*

%files -n dkms-%{name}
%defattr(-,root,root)
%doc %{_docdir}/*/*
%dir %{_usr}/src/%{name}-%{version}
%{_usr}/src/%{name}-%{version}/*


