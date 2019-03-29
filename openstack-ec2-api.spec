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
%global pypi_name ec2-api

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Support of EC2 API for OpenStack.

Name:           openstack-%{pypi_name}
Version:        8.0.0
Release:        1%{?dist}
Summary:        OpenStack Ec2api Service

License:        ASL 2.0
URL:            https://launchpad.net/ec2-api
Source0:        https://pypi.io/packages/source/e/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-ec2-api.service
Source2:        openstack-ec2-api-metadata.service
Source3:        openstack-ec2-api-s3.service
Source4:        openstack-ec2-api-manage.service
Source5:        ec2api.conf.sample
Source6:        policy.json

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires: python%{pyver}-ec2-api = %{version}-%{release}

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires: python%{pyver}-babel >= 2.3.4
Requires: python%{pyver}-botocore >= 1.5.1
Requires: python%{pyver}-eventlet >= 0.18.2
Requires: python%{pyver}-greenlet >= 0.4.10
Requires: python%{pyver}-iso8601 >= 0.1.9
Requires: python%{pyver}-jsonschema >= 2.0.0
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-oslo-cache >= 1.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-concurrency >= 3.25.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-db >= 4.27.0
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-cinderclient >= 3.3.0
Requires: python%{pyver}-glanceclient >= 1:2.8.0
Requires: python%{pyver}-keystoneclient >= 1:3.8.0
Requires: python%{pyver}-neutronclient >= 6.7.0
Requires: python%{pyver}-novaclient >= 1:9.1.0
Requires: python%{pyver}-openstackclient >= 3.12.0
Requires: python%{pyver}-routes >= 2.3.1
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-sqlalchemy >= 1.0.10
Requires: python%{pyver}-webob >= 1.7.1
Requires: python%{pyver}-cryptography >= 1.7.2

# Handle python2 exception
%if %{pyver} == 2
Requires: python-anyjson >= 0.3.3
Requires: python-httplib2 >= 0.9.1
Requires: python-lxml >= 3.2.1
Requires: python-paste
Requires: python-paste-deploy >= 1.5.0
Requires: python-migrate >= 0.11.0
%else
Requires: python%{pyver}-anyjson >= 0.3.3
Requires: python%{pyver}-httplib2 >= 0.9.1
Requires: python%{pyver}-lxml >= 3.2.1
Requires: python%{pyver}-paste
Requires: python%{pyver}-paste-deploy >= 1.5.0
Requires: python%{pyver}-migrate >= 0.11.0
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
# Documentation package
%package -n python%{pyver}-%{pypi_name}-doc
Summary:        Documentation for OpenStack EC2 API
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{pypi_name}-doc
%{common_desc}

Documentation for OpenStack EC2 API
%endif

%package -n python%{pyver}-%{pypi_name}-tests
Summary:    Tests for OpenStack EC2 API
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-tests}

Requires:   python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
Unit tests for OpenStack EC2 API

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Copy our own conf file
cp %{SOURCE5} etc/ec2api/ec2api.conf.sample

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Create log dir
mkdir -p %{buildroot}/var/log/ec2api/

# Install data file
install -p -D -m 640 etc/ec2api/api-paste.ini %{buildroot}%{_sysconfdir}/ec2api/api-paste.ini
install -p -D -m 640 %{SOURCE5} %{buildroot}%{_sysconfdir}/ec2api/ec2api.conf
install -p -D -m 640 %{SOURCE6} %{buildroot}%{_sysconfdir}/ec2api/policy.json

# Install services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-ec2-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-ec2-api-metadata.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-ec2-api-s3.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-ec2-api-manage.service

# Install log file
install -d -m 755 %{buildroot}%{_localstatedir}/log/ec2api

# Create butckets dir
mkdir -p %{buildroot}%{pyver_sitelib}/buckets


%pre
# Using dynamic UID and GID for ec2api
getent group ec2api >/dev/null || groupadd -r ec2api
getent passwd ec2api >/dev/null || \
useradd -r -g ec2api -d %{_sharedstatedir}/ec2api -s /sbin/nologin \
-c "OpenStack EC2 API Daemons" ec2api
exit 0


%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/ec2api
%exclude %{pyver_sitelib}/ec2api/tests
%{pyver_sitelib}/ec2_api-*-py?.?.egg-info

%files
%{_bindir}/%{pypi_name}*
%dir %attr(0750, root, ec2api) %{_sysconfdir}/ec2api
%attr(0644, root, ec2api) %{_sysconfdir}/ec2api/api-paste.ini
%attr(0644, root, ec2api) %{_sysconfdir}/ec2api/ec2api.conf
%attr(0644, root, ec2api) %{_sysconfdir}/ec2api/policy.json
%{_unitdir}/openstack-ec2-api.service
%{_unitdir}/openstack-ec2-api-metadata.service
%{_unitdir}/openstack-ec2-api-s3.service
%{_unitdir}/openstack-ec2-api-manage.service
%dir %attr(0750, ec2api, ec2api) %{_localstatedir}/log/ec2api

%if 0%{?with_doc}
%files -n python%{pyver}-%{pypi_name}-doc
%doc doc/build/html
%endif

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/ec2api/tests

%changelog
* Fri Mar 29 2019 RDO <dev@lists.rdoproject.org> 8.0.0-1
- Update to 8.0.0

