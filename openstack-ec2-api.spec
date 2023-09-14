%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%global pypi_name ec2-api

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order os-api-ref pylint
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global common_desc \
Support of EC2 API for OpenStack.

Name:           openstack-%{pypi_name}
Version:        17.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        OpenStack Ec2api Service

License:        Apache-2.0
URL:            https://launchpad.net/ec2-api
Source0:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#
# patches_base=17.0.0.0rc1
#

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
BuildRequires:  pyproject-rpm-macros
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires: python3-ec2-api = %{version}-%{release}

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{pypi_name}-doc
Summary:        Documentation for OpenStack EC2 API

%description -n python3-%{pypi_name}-doc
%{common_desc}

Documentation for OpenStack EC2 API
%endif

%package -n python3-%{pypi_name}-tests
Summary:    Tests for OpenStack EC2 API

Requires:   python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
Unit tests for OpenStack EC2 API

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Copy our own conf file
cp %{SOURCE5} etc/ec2api/ec2api.conf.sample

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
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
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

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
%{python3_sitelib}/ec2_api-*.dist-info

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
* Thu Sep 14 2023 RDO <dev@lists.rdoproject.org> 17.0.0-0.1.0rc1
- Update to 17.0.0.0rc1

