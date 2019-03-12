# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library os-vif
%global module os_vif

Name:       python-%{library}
Version:    1.15.1
Release:    1%{?dist}
Summary:    OpenStack os-vif library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{module}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python%{pyver}-%{library}
Summary:    OpenStack os-vif library
%{?python_provide:%python_provide python%{pyver}-%{library}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-pyroute2
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-oslo-privsep
BuildRequires:  python%{pyver}-oslo-versionedobjects
BuildRequires:  python%{pyver}-oslo-versionedobjects-tests
BuildRequires:  python%{pyver}-ovsdbapp
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios

Requires:   python%{pyver}-debtcollector >= 1.19.0
Requires:   python%{pyver}-pbr >= 2.0.0
Requires:   python%{pyver}-oslo-config >= 2:5.1.0
Requires:   python%{pyver}-oslo-log >= 3.30.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-privsep >= 1.23.0
Requires:   python%{pyver}-oslo-versionedobjects >= 1.28.0
Requires:   python%{pyver}-pyroute2
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-stevedore >= 1.20.0
Requires:   python%{pyver}-oslo-concurrency >= 3.20.0
Requires:   python%{pyver}-ovsdbapp >= 0.12.1
Requires:   python%{pyver}-netaddr >= 0.7.18

%description -n python%{pyver}-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.


%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python%{pyver}-%{library} = %{version}-%{release}
Requires:   python%{pyver}-subunit
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-os-testr
Requires:   python%{pyver}-testtools
Requires:   python%{pyver}-oslo-versionedobjects-tests
Requires:   python%{pyver}-testrepository
Requires:   python%{pyver}-testscenarios


%description -n python%{pyver}-%{library}-tests
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the library test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack os-vif library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-reno

%description -n python-%{library}-doc
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the documentation.
%endif

%description
A library for plugging and unplugging virtual interfaces in OpenStack.

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
export OS_TEST_PATH='./os_vif/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/vif_plug_linux_bridge
%{pyver_sitelib}/vif_plug_ovs
%{pyver_sitelib}/vif_plug_noop
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/*/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/*/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 1.15.1-1
- Update to 1.15.1

