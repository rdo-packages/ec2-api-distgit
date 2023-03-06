%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name ec2-api

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Support of EC2 API for OpenStack.

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Ec2api Service

License:        ASL 2.0
URL:            https://launchpad.net/ec2-api
Source0:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source1:        openstack-ec2-api.service
Source2:        openstack-ec2-api-metadata.service
Source3:        openstack-ec2-api-s3.service
Source4:        openstack-ec2-api-manage.service
Source5:        ec2api.conf.sample
Source6:        policy.json
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires: python3-ec2-api = %{version}-%{release}

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires: python3-botocore >= 1.9.7
Requires: python3-eventlet >= 0.20.0
Requires: python3-greenlet >= 0.4.13
Requires: python3-keystoneauth1 >= 3.14.0
Requires: python3-oslo-cache >= 1.29.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-context >= 2.20.0
Requires: python3-oslo-db >= 4.40.0
Requires: python3-oslo-log >= 3.37.0
Requires: python3-oslo-serialization >= 2.25.0
Requires: python3-oslo-service >= 1.30.0
Requires: python3-oslo-utils >= 3.36.0
Requires: python3-pbr >= 3.1.1
Requires: python3-cinderclient >= 3.5.0
Requires: python3-glanceclient >= 1:2.16.0
Requires: python3-keystoneclient >= 1:3.15.0
Requires: python3-neutronclient >= 6.7.0
Requires: python3-novaclient >= 1:10.1.0
Requires: python3-openstackclient >= 3.14.0
Requires: python3-routes >= 2.4.1
Requires: python3-sqlalchemy >= 1.2.5
Requires: python3-webob >= 1.7.4
Requires: python3-cryptography >= 2.1.4
Requires: python3-httplib2 >= 0.10.3
Requires: python3-lxml >= 4.1.1
Requires: python3-paste >= 2.0.3
Requires: python3-paste-deploy >= 1.5.2
Requires: python3-migrate >= 0.11.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{pypi_name}-doc
Summary:        Documentation for OpenStack EC2 API
%{?python_provide:%python_provide python3-%{pypi_name}-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python3-%{pypi_name}-doc
%{common_desc}

Documentation for OpenStack EC2 API
%endif

%package -n python3-%{pypi_name}-tests
Summary:    Tests for OpenStack EC2 API
%{?python_provide:%python_provide python3-%{pypi_name}-tests}

Requires:   python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
Unit tests for OpenStack EC2 API

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Copy our own conf file
cp %{SOURCE5} etc/ec2api/ec2api.conf.sample

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build -W -b html -d doc/build/doctrees doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

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
mkdir -p %{buildroot}%{python3_sitelib}/buckets


%pre
# Using dynamic UID and GID for ec2api
getent group ec2api >/dev/null || groupadd -r ec2api
getent passwd ec2api >/dev/null || \
useradd -r -g ec2api -d %{_sharedstatedir}/ec2api -s /sbin/nologin \
-c "OpenStack EC2 API Daemons" ec2api
exit 0


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/ec2api
%exclude %{python3_sitelib}/ec2api/tests
%{python3_sitelib}/ec2_api-*-py%{python3_version}.egg-info

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
%files -n python3-%{pypi_name}-doc
%doc doc/build/html
%endif

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/ec2api/tests

%changelog
