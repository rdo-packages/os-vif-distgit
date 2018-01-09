%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library os-vif
%global module os_vif

Name:       python-%{library}
Version:    XXX
Release:    XXX
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
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-os-testr
BuildRequires:  python-pyroute2
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-privsep
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python2-oslo-versionedobjects-tests

Requires:   python-pbr >= 2.0.0
Requires:   python-netaddr >= 0.7.13
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-privsep >=  1.9.0
Requires:   python-oslo-versionedobjects >= 1.17.0
Requires:   python-pyroute2
Requires:   python-six >= 1.9.0
Requires:   python-stevedore >= 1.20.0
Requires:   python-oslo-concurrency >= 3.11.0

%description -n python2-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.


%package -n python2-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python-subunit
Requires:   python-oslotest
Requires:   python-os-testr
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
BuildRequires: python-openstackdocstheme
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
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-os-testr
BuildRequires:  python3-pyroute2
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-privsep
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-oslo-versionedobjects-tests

Requires:   python3-pbr >= 2.0.0
Requires:   python3-netaddr >= 0.7.13
Requires:   python3-oslo-config >= 2:4.0.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-privsep >=  1.9.0
Requires:   python3-oslo-versionedobjects >= 1.17.0
Requires:   python3-pyroute2
Requires:   python3-six >= 1.9.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-oslo-concurrency >= 3.11.0

%description -n python3-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.

%package -n python3-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-os-testr
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
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
export OS_TEST_PATH='./os_vif/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr --test-path $OS_TEST_PATH run
%if 0%{?with_python3}
rm -rf .stestr
stestr-3 --test-path $OS_TEST_PATH run
%endif

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
%doc doc/build/html README.rst

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
