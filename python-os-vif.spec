%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library os-vif
%global module os_vif

Name:       python-%{library}
Version:    1.2.1
Release:    1%{?dist}
Summary:    OpenStack os-vif library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{module}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    OpenStack os-vif library
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  python-hacking
BuildRequires:  python-coverage
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-privsep
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python2-oslo-versionedobjects-tests

Requires:   python-pbr >= 1.6
Requires:   python-netaddr >= 0.7.12
Requires:   python-oslo-config >= 2:3.14.0
Requires:   python-oslo-log >= 1.14.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-privsep >=  1.9.0
Requires:   python-oslo-versionedobjects >= 1.13.0
Requires:   python-six >= 1.9.0
Requires:   python-stevedore >= 1.16.0
Requires:   python-oslo-concurrency >= 3.11.0

%description -n python2-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.


%package -n python2-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python-hacking
Requires:   python-coverage
Requires:   python-subunit
Requires:   python-oslotest
Requires:   python-testrepository
Requires:   python-testscenarios
Requires:   python-testtools
Requires:   python2-oslo-versionedobjects-tests


%description -n python2-%{library}-tests
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the library test files.

%package -n python-%{library}-doc
Summary:    OpenStack os-vif library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: python-reno

%description -n python-%{library}-doc
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack os-vif library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  python3-hacking
BuildRequires:  python3-coverage
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-privsep
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-oslo-versionedobjects-tests

Requires:   python3-pbr >= 1.6
Requires:   python3-netaddr >= 0.7.12
Requires:   python3-oslo-config >= 2:3.14.0
Requires:   python3-oslo-log >= 1.14.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-privsep >=  1.9.0
Requires:   python3-oslo-versionedobjects >= 1.13.0
Requires:   python3-six >= 1.9.0
Requires:   python3-stevedore >= 1.16.0
Requires:   python3-oslo-concurrency >= 3.11.0

%description -n python3-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.

%package -n python3-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-hacking
Requires:   python3-coverage
Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools
Requires:   python3-oslo-versionedobjects-tests


%description -n python3-%{library}-tests
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the library test files.

%endif # with_python3


%description
A library for plugging and unplugging virtual interfaces in OpenStack.

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/vif_plug_linux_bridge
%{python2_sitelib}/vif_plug_ovs
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/*/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/*/tests

%files -n python-%{library}-doc
%license LICENSE
%doc html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/vif_plug_linux_bridge
%{python3_sitelib}/vif_plug_ovs
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/*/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/*/tests
%endif # with_python3

%changelog
* Wed Sep 14 2016 Haikel Guemar <hguemar@fedoraproject.org> 1.2.1-1
- Update to 1.2.1

