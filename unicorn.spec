# I love OpenSource :-(

Summary:	unicorn utility for BeWan Architecture support
Name:		unicorn
Version:	0.9.3
Release:	9
Source0:	unicorn-%{version}.tar.bz2
Source1:	module_param.patch
Source2:	dkms-unicorn-update-irq-flags.patch
Source3:	dkms-unicorn-SET_MODULE_OWNER-removal.patch
Source4:	dkms-unicorn-urb-lock-removal.patch
Source5:	dkms-unicorn-update-int-handler-definition.patch
Source100:	unicorn.rpmlintrc
#Patch0:		maxpacket.patch.bz2
#Patch0:		unicorn-0.8.7-fno-gnu-linker.patch.bz2
Patch1:		unicorn-0.9.0-kernel26-spinlock.patch
Patch2:		unicorn-0.9.3-smp.patch
Patch3:		unicorn-0.9.3-kernel2.6.22.patch
Patch4:		unicorn-0.9.3-build.patch
License:	BeWan 2004
Group:		System/Kernel and hardware
BuildRequires:	gtk+-devel
BuildRequires:	automake1.4

%description -n %{name}
BeWan Architecture utility.

%package -n dkms-%{name}
Summary:	unicorn kernel module for BeWan Architecture support
Group:		System/Kernel and hardware
Requires(post):		dkms
Requires(preun):		dkms
Requires:	gcc-c++

%description -n dkms-%{name}
unicorn Architecture support for Linux kernel.

%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

pushd adsl_status
%configure
popd

%build
%make -C adsl_status

%install
rm -rf %{buildroot}
# utils 
%make -C adsl_status DESTDIR="%{buildroot}" install
%find_lang bewan_adsl_status

# driver source
mkdir -p %{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}
cp -r * %{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}
cp %{SOURCE1} %{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}/patches/
cat > %{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}

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
PATCH[1]="dkms-unicorn-update-irq-flags.patch"
PATCH_MATCH[1]="^2\.6\.(2[4-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[2]="dkms-unicorn-SET_MODULE_OWNER-removal.patch"
PATCH_MATCH[2]="^2\.6\.(2[4-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[3]="dkms-unicorn-urb-lock-removal.patch"
PATCH_MATCH[3]="^2\.6\.(2[4-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[4]="dkms-unicorn-update-int-handler-definition.patch"
PATCH_MATCH[4]="^2\.6\.(19)|([2-9][0-9]+)|([1-9][0-9][0-9]+)"

AUTOINSTALL=yes
EOF

for p in %{_sourcedir}/dkms-unicorn-update-irq-flags.patch \
         %{_sourcedir}/dkms-unicorn-SET_MODULE_OWNER-removal.patch \
         %{_sourcedir}/dkms-unicorn-urb-lock-removal.patch \
         %{_sourcedir}/dkms-unicorn-update-int-handler-definition.patch;
do
	cp $p %{buildroot}/%{_usrsrc}/unicorn-%{version}-%{release}/patches
done

%post -n dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade add -m %name -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade build -m %name -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade install -m %name -v %version-%release
exit 0

%preun -n dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %name -v %version-%release --all
exit 0

%files -f bewan_adsl_status.lang
%doc COPYING COPYING.GPL README
%{_bindir}/*
%{_datadir}/bewan_adsl_status/pixmaps/*

%files -n dkms-%{name}
%dir %{_usr}/src/%{name}-%{version}-%{release}
%{_usr}/src/%{name}-%{version}-%{release}/*

