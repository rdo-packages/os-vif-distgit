%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

%global library os-vif
%global module os_vif

Name:       python-%{library}
Version:    3.2.0
Release:    1%{?dist}
Summary:    OpenStack os-vif library
License:    Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
export OS_TEST_PATH='./os_vif/tests/unit'
export PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e %{default_toxenv}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/vif_plug_linux_bridge
%{python3_sitelib}/vif_plug_ovs
%{python3_sitelib}/vif_plug_noop
%{python3_sitelib}/%{module}-*.dist-info
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
* Mon Sep 25 2023 RDO <dev@lists.rdoproject.org> 3.2.0-1
- Update to 3.2.0

