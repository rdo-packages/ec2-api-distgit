%global pypi_name ec2-api

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

Name:           openstack-%{pypi_name}
Version:        2.0.0
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

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.6
BuildRequires:  systemd

Requires: python-anyjson >= 0.3.3
Requires: python-babel >= 1.3
Requires: python-boto >= 2.32.1
Requires: python-eventlet >= 0.18.2
Requires: python-greenlet >= 0.3.2
Requires: python-httplib2 >= 0.7.5
Requires: python-iso8601 >= 0.1.9
Requires: python-jsonschema >= 2.0.0
Requires: python-lxml >= 2.3
Requires: python-oslo-config >= 2:3.7.0
Requires: python-oslo-concurrency >= 3.5.0
Requires: python-oslo-context >= 0.2.0
Requires: python-oslo-db >= 4.1.0
Requires: python-oslo-log >= 1.14.0
Requires: python-oslo-messaging >= 4.0.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.0.0
Requires: python-oslo-utils >= 3.5.0
Requires: python-paramiko >= 1.13.0
Requires: python-paste
Requires: python-paste-deploy >= 1.5.0
Requires: python-pbr >= 1.6
Requires: python-pyasn1
Requires: python-pyasn1-modules
Requires: python-cinderclient >= 1.3.1
Requires: python-glanceclient >= 1:2.0.0
Requires: python-keystoneclient >= 1:1.6.0
Requires: python-neutronclient >= 2.6.0
Requires: python-novaclient >= 1:2.29.0
Requires: python-openstackclient >= 2.1.0
Requires: python-routes >= 1.12.3
Requires: python-six >= 1.9.0
Requires: python-sqlalchemy >= 1.0.10
Requires: python-migrate >= 0.9.6
Requires: python-stevedore >= 1.3.0
Requires: python-webob >= 1.2.3
Requires: python2-ec2-api = %{version}-%{release}
 
%description
Support of EC2 API for OpenStack.

%package -n     python2-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Support of EC2 API for OpenStack

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires: python3-anyjson >= 0.3.3
Requires: python3-babel >= 1.3
Requires: python3-boto >= 2.32.1
Requires: python3-eventlet >= 0.18.2
Requires: python3-greenlet >= 0.3.2
Requires: python3-httplib2 >= 0.7.5
Requires: python3-iso8601 >= 0.1.9
Requires: python3-jsonschema >= 2.0.0
Requires: python3-lxml >= 2.3
Requires: python3-oslo-config >= 2:3.7.0
Requires: python3-oslo-concurrency >= 3.5.0
Requires: python3-oslo-context >= 0.2.0
Requires: python3-oslo-db >= 4.1.0
Requires: python3-oslo-log >= 1.14.0
Requires: python3-oslo-messaging >= 4.0.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-service >= 1.0.0
Requires: python3-oslo-utils >= 3.5.0
Requires: python3-paramiko >= 1.13.0
Requires: python3-paste
Requires: python3-paste-deploy >= 1.5.0
Requires: python3-pbr >= 0.6
Requires: python3-pyasn1
Requires: python3-pyasn1-modules
Requires: python3-cinderclient >= 1.3.1
Requires: python3-glanceclient >= 1:2.0.0
Requires: python3-keystoneclient >= 1:1.6.0
Requires: python3-neutronclient >= 2.6.0
Requires: python3-novaclient >= 1:2.29.0
Requires: python3-openstackclient >= 2.1.0
Requires: python3-routes >= 1.12.3
Requires: python3-six >= 1.9.0
Requires: python3-sqlalchemy >= 1.0.10
Requires: python3-migrate >= 0.9.6
Requires: python3-stevedore >= 1.3.0
Requires: python3-webob >= 1.2.3

%description -n python3-%{pypi_name}
Support of EC2 API for OpenStack
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack EC2 API

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
Documentation for OpenStack EC2 API

%prep
%autosetup -n %{pypi_name}-%{version}
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
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

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
%{python2_sitelib}/ec2_api-%{version}-py?.?.egg-info

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
%doc html


%changelog
* Wed Jul 06 2016 Haikel Guemar <hguemar@fedoraproject.org> 2.0.0-1
- Update to 2.0.0

* Thu Mar 24 2016 Haikel Guemar <hguemar@fedoraproject.org> 1.0.2-1
- Update to 1.0.2

* Tue Dec  1 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-1
- Upstream 1.0.0 (liberty)

* Thu Oct 15 2015 Marcos Fermin Lobo <marcos.fermin.lobo@cern.ch> - 0.1.0-1
- First RPM
