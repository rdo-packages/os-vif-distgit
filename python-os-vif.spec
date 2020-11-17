%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library os-vif
%global module os_vif

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack os-vif library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{module}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{library}/%{module}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{library}
Summary:    OpenStack os-vif library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-os-testr
BuildRequires:  python3-pyroute2
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-privsep
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-oslo-versionedobjects-tests
BuildRequires:  python3-ovsdbapp
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios

Requires:   python3-debtcollector >= 1.19.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-oslo-config >= 2:5.1.0
Requires:   python3-oslo-log >= 3.30.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-privsep >= 1.23.0
Requires:   python3-oslo-versionedobjects >= 1.28.0
Requires:   python3-pyroute2 >= 0.5.2
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-oslo-concurrency >= 3.20.0
Requires:   python3-ovsdbapp >= 0.12.1
Requires:   python3-netaddr >= 0.7.18

%description -n python3-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.


%package -n python3-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-os-testr
Requires:   python3-testtools
Requires:   python3-oslo-versionedobjects-tests
Requires:   python3-testrepository
Requires:   python3-testscenarios


%description -n python3-%{library}-tests
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the library test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack os-vif library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-reno

%description -n python-%{library}-doc
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the documentation.
%endif

%description
A library for plugging and unplugging virtual interfaces in OpenStack.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
export OS_TEST_PATH='./os_vif/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
PYTHON=%{__python3} stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/vif_plug_linux_bridge
%{python3_sitelib}/vif_plug_ovs
%{python3_sitelib}/vif_plug_noop
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/*/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/*/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
