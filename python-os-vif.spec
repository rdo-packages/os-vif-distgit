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
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git
BuildRequires:  python2-subunit
BuildRequires:  python2-oslotest
BuildRequires:  python2-os-testr
BuildRequires:  python2-pyroute2
BuildRequires:  python2-testtools
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python2-oslo-privsep
BuildRequires:  python2-oslo-versionedobjects
BuildRequires:  python2-oslo-versionedobjects-tests
%if 0%{?fedora} > 0
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
%else
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
%endif

Requires:   python2-pbr >= 2.0.0
Requires:   python2-oslo-config >= 2:5.1.0
Requires:   python2-oslo-log >= 3.30.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-oslo-privsep >= 1.23.0
Requires:   python2-oslo-versionedobjects >= 1.28.0
Requires:   python2-pyroute2
Requires:   python2-six >= 1.10.0
Requires:   python2-stevedore >= 1.20.0
Requires:   python2-oslo-concurrency >= 3.20.0
%if 0%{?fedora} > 0
Requires:   python2-netaddr >= 0.7.18
%else
Requires:   python-netaddr >= 0.7.18
%endif

%description -n python2-%{library}
A library for plugging and unplugging virtual interfaces in OpenStack.


%package -n python2-%{library}-tests
Summary:    OpenStack os-vif library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python2-subunit
Requires:   python2-oslotest
Requires:   python2-os-testr
Requires:   python2-testtools
Requires:   python2-oslo-versionedobjects-tests
%if 0%{?fedora} > 0
Requires:   python2-testrepository
Requires:   python2-testscenarios
%else
Requires:   python-testrepository
Requires:   python-testscenarios
%endif


%description -n python2-%{library}-tests
A library for plugging and unplugging virtual interfaces in OpenStack.

This package contains the library test files.

%package -n python-%{library}-doc
Summary:    OpenStack os-vif library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-reno

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
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-oslo-config >= 2:5.1.0
Requires:   python3-oslo-log >= 3.30.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-privsep >= 1.23.0
Requires:   python3-oslo-versionedobjects >= 1.28.0
Requires:   python3-pyroute2
Requires:   python3-six >= 1.10.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-oslo-concurrency >= 3.20.0

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
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
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
