#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?_ossiehome:  %define _ossiehome  /usr/local/redhawk/core}
%define _prefix %{_ossiehome}
Prefix:         %{_prefix}

Name:           redhawk-codegen
Version:        1.9.0
Release:        4%{?dist}
Summary:        Redhawk Code Generators

Group:          Applications/Engineering
License:        LGPLv3+
URL:            http://redhawksdr.org/
Source:         %{name}-%{version}.tar.gz
Vendor:         REDHAWK

# BuildRoot required for el5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:       python
Requires:       redhawk >= 1.9
Requires:       python-jinja2-26

BuildRequires:  python-devel >= 2.4

%description
REDHAWK Code Generators
 * Commit: __REVISION__
 * Source Date/Time: __DATETIME__


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --home=$RPM_BUILD_ROOT%{_prefix}
rm $RPM_BUILD_ROOT%{_prefix}/lib/python/redhawk/__init__.py*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/redhawk-codegen
%{_bindir}/codegen_version
%{_bindir}/update_project
%{_prefix}/lib/python/redhawk/codegen
%if 0%{?rhel} >= 6
%{_prefix}/lib/python/redhawk_codegen-%{version}-py%{python_version}.egg-info
%endif

