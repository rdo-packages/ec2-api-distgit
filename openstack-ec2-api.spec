%global pypi_name ec2-api

%if 0%{?fedora}
# FIXME: python3 clients are not packaged yet
%global with_python3 0
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Support of EC2 API for OpenStack.

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
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

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires: python2-ec2-api = %{version}-%{release}

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires: python-anyjson >= 0.3.3
Requires: python-babel >= 2.3.4
Requires: python-boto >= 2.32.1
Requires: python-botocore >= 1.0.0
Requires: python-eventlet >= 0.18.2
Requires: python-greenlet >= 0.3.2
Requires: python-httplib2 >= 0.7.5
Requires: python-iso8601 >= 0.1.9
Requires: python-jsonschema >= 2.0.0
Requires: python-keystoneauth1 >= 3.1.0
Requires: python-lxml >= 2.3
Requires: python-oslo-cache >= 1.5.0
Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-context >= 2.14.0
Requires: python-oslo-db >= 4.15.0
Requires: python-oslo-log >= 3.30.0
Requires: python-oslo-messaging >= 5.14.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-paramiko >= 1.13.0
Requires: python-paste
Requires: python-paste-deploy >= 1.5.0
Requires: python-pbr >= 2.0.0
Requires: python-pyasn1
Requires: python-pyasn1-modules
Requires: python-cinderclient >= 3.1.0
Requires: python-glanceclient >= 1:2.8.0
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-neutronclient >= 6.3.0
Requires: python-novaclient >= 1:9.1.0
Requires: python-openstackclient >= 3.3.0
Requires: python-routes >= 2.3.1
Requires: python-six >= 1.9.0
Requires: python-sqlalchemy >= 1.0.10
Requires: python-migrate >= 0.11.0
Requires: python-stevedore >= 1.3.0
Requires: python-webob >= 1.7.1
Requires: python-cryptography >= 1.6

%description -n python2-%{pypi_name}
%{common_desc}

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python-tools

Requires: python3-anyjson >= 0.3.3
Requires: python3-babel >= 1.3
Requires: python3-boto >= 2.32.1
Requires: python3-botocore >= 1.0.0
Requires: python3-eventlet >= 0.17.4
Requires: python3-greenlet >= 0.3.2
Requires: python3-httplib2 >= 0.7.5
Requires: python3-iso8601 >= 0.1.9
Requires: python3-jsonschema >= 2.0.0
Requires: python3-lxml >= 2.3
Requires: python3-oslo-cache >= 1.5.0
Requires: python3-oslo-config >= 2:4.0.0
Requires: python3-oslo-concurrency >= 3.5.0
Requires: python3-oslo-context >= 2.14.0
Requires: python3-oslo-db >= 4.1.0
Requires: python3-oslo-log >= 3.30.0
Requires: python3-oslo-messaging >= 4.0.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-service >= 1.0.0
Requires: python3-oslo-utils >= 3.20.0
Requires: python3-paramiko >= 1.13.0
Requires: python3-paste
Requires: python3-paste-deploy >= 1.5.0
Requires: python3-pbr >= 2.2.0
Requires: python3-pyasn1
Requires: python3-pyasn1-modules
Requires: python3-cinderclient >= 3.1.0
Requires: python3-glanceclient >= 1:2.8.0
Requires: python3-keystoneclient >= 1:1.6.0
Requires: python3-neutronclient >= 6.3.0
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-openstackclient >= 3.3.0
Requires: python3-routes >= 2.3.1
Requires: python3-six >= 1.9.0
Requires: python3-sqlalchemy >= 1.0.10
Requires: python3-migrate >= 0.11.0
Requires: python3-stevedore >= 1.3.0
Requires: python3-webob >= 1.7.1
Requires: python3-cryptography >= 1.6

%description -n python3-%{pypi_name}
%{common_desc}
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack EC2 API

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
%{common_desc}

Documentation for OpenStack EC2 API

%package -n python-%{pypi_name}-tests
Summary:        Tempest plugin and tests for OpenStack EC2 API

Requires:   python2-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-tests
Tempest plugin and unit tests for OpenStack EC2 API

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Copy our own conf file
cp %{SOURCE5} etc/ec2api/ec2api.conf.sample

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%global service ec2-api
# Create fake egg-info for the tempest plugin
%py2_entrypoint ec2_api %{service}

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/%{pypi_name} %{buildroot}%{_bindir}/python3-%{pypi_name}
popd
%endif

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd

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
mkdir -p %{buildroot}%{python2_sitelib}/buckets


%pre
# Using dynamic UID and GID for ec2api
getent group ec2api >/dev/null || groupadd -r ec2api
getent passwd ec2api >/dev/null || \
useradd -r -g ec2api -d %{_sharedstatedir}/ec2api -s /sbin/nologin \
-c "OpenStack EC2 API Daemons" ec2api
exit 0


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/ec2api
%exclude %{python2_sitelib}/ec2api/tests
%{python2_sitelib}/ec2_api-*-py?.?.egg-info

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

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/python3-%{pypi_name}
%{_bindir}/%{pypi_name}*
%{python3_sitelib}/ec2api*
%{python3_sitelib}/ec2_api*
%endif


%files -n python-%{pypi_name}-doc
%doc doc/build/html

%files -n python-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/ec2api/tests
%{python2_sitelib}/ec2_api_tests.egg-info

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/ec2-api/commit/?id=aaf1fc94f89b4b3fc312c6eb768b61e5fb3267c3
