Summary:	Standalone MPD Web GUI written in C
Name:		ympd
Version:	1.3.0
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/notandy/ympd/archive/v%{version}/%{name}-%{version}.zip
# Source0-md5:	89d339ee9b243bc02aef38baa8f5a823
Source1:	%{name}.service
Source2:	%{name}.sysconfig
Patch0:		%{name}-link.patch
URL:		http://www.ympd.org
BuildRequires:	cmake
BuildRequires:	libmpdclient-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Standalone MPD Web GUI written in C, utilizing Websockets and
Bootstrap/JS.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -D %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/ympd
%{systemdunitdir}/%{name}.service
%{_mandir}/man1/ympd.1*
