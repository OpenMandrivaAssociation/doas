Name: doas
Version: 6.8.2
Release: 1
Source0: https://github.com/Duncaen/OpenDoas/releases/download/v%{version}/opendoas-%{version}.tar.xz
Source1: doas.pam
Source2: doas.conf
Summary: Tool to run commands as a different user
URL: https://github.com/Duncaen/OpenDoas
License: BSD
Group: System/Base
Provides: opendoas = %{EVRD}
BuildRequires: pkgconfig(pam)
BuildRequires: sed
BuildRequires: make

%description
A tool to run commands as a different user.

doas is similar to sudo, but with a much smaller codebase.

%prep
%autosetup -p1 -n opendoas-%{version}
# Looks like autoconf, but isn't -- don't use %%configure
./configure \
	--prefix=%{_prefix} \
	--with-timestamp
# We don't run "make install" as root, so
# let's not run commands that would require us to do so
sed -i -e 's,chown,true,g' GNUmakefile
# Optimize better...
sed -i -e "s|-O2|%{optflags}|g" GNUmakefile

%build
%make_build

%install
%make_install
cp -f %{S:1} %{buildroot}%{_sysconfdir}/pam.d/doas
cp -f %{S:2} %{buildroot}%{_sysconfdir}/

%files
%attr(4511,root,root) %{_bindir}/doas
%{_sysconfdir}/pam.d/doas
%config(noreplace) %{_sysconfdir}/doas.conf
%{_mandir}/man1/doas.1*
%{_mandir}/man5/doas.conf.5*
