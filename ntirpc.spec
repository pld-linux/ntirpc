#
# Conditional build:
%bcond_with	gssapi		# RPCSEC_GSS support (MIT Kerberos required)
%bcond_without	rdma		# RDMA support
%bcond_with	lttng		# LTTng tracing
%bcond_without	static_libs	# static libraries
#
Summary:	New Transport-independent RPC (TI-RPC) library
Summary(pl.UTF-8):	Nowa biblioteka Transport-independent RPC (TI-RPC)
Name:		ntirpc
Version:	4.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://download.nfs-ganesha.org/4/4.0/%{name}-%{version}.tar.gz
# Source0-md5:	17b0baada54936dcde80eba27bb6d88d
URL:		https://github.com/nfs-ganesha/ntirpc
BuildRequires:	cmake >= 2.6.3
%{?with_gssapi:BuildRequires:	krb5-devel}
%{?with_rdma:BuildRequires:	libibverbs-devel}
%{?with_rdma:BuildRequires:	librdmacm-devel}
%{?with_lttng:BuildRequires:	lttng-ust-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	userspace-rcu-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
New Transport-independent RPC (TI-RPC) library.

%description -l pl.UTF-8
Nowa biblioteka Transport-independent RPC (TI-RPC).

%package devel
Summary:	Header files for NTIRPC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki NTIRPC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for NTIRPC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki NTIRPC.

%prep
%setup -q

%build
install -d build
cd build
# ALLOCATOR: also jemalloc(default), tcmalloc
%cmake .. \
	-DALLOCATOR=libc \
	-DLIB_INSTALL_DIR:PATH=%{_lib} \
	%{!?with_gssapi:-DUSE_GSS=OFF} \
	%{?with_lttng:-DUSE_LTTNG=ON} \
	%{?with_rdma:-DUSE_RPC_RDMA=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libntirpc.so.4.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libntirpc.so
%{_includedir}/ntirpc
%{_pkgconfigdir}/libntirpc.pc
