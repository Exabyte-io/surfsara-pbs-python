%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

### Abstract ###

Name: pbs_python
License: See LICENSE
Group: Development/Libraries
Summary: This package contains the PBS python module.
URL: https://oss.trac.surfsara.nl/pbs_python
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source: ftp://ftp.sara.nl/pub/outgoing/pbs_python.tar.gz 

### Dependencies ###
# None

### Build Dependencies ###

BuildRequires: torque-devel
BuildRequires: python-devel >= %{python_version}

%description
This package contains the pbs python module.

%prep
%setup -q -n pbs_python-%{version}

%build
%configure
#%{__python} setup.py build

%install
make install DESTDIR=$RPM_BUILD_DIR
#%{__python} ./setup.py install --prefix $RPM_BUILD_ROOT%{_prefix} ;
#%{__mkdir_p} $RPM_BUILD_ROOT%{_prefix}/bin
#%{__install} -m0655 examples/sara_nodes.py ${RPM_BUILD_ROOT}%{_prefix}/bin/sara_nodes
#%{__install} -m0655 examples/new_rack_pbsmon.py ${RPM_BUILD_ROOT}%{_prefix}/bin/pbsmon

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README TODO examples
%{python_sitearch}/pbs.pth
%{python_sitearch}/pbs/*
%{_prefix}/bin/*

%changelog
* Mon Aug 31 2015 Dennis Stam <dennis.stam@surfsara.nl>
- Simplified the rpm build process, version is set by the Makefile
* Tue Mar 24 2010 Ramon Bastiaans <ramon.bastiaans@sara.nl>
- Updates for new version
* Tue Oct 06 2009 Ramon Bastiaans <ramon.bastiaans@sara.nl>
- Fixed tmppath, %setup sourcedir
* Tue Mar 24 2009 David Chin <chindw@wfu.edu>
- Fedora-ize
* Sun Mar  9 2008 Michael Sternberg <sternberg@anl.gov>
- libdir and python defines
* Wed Nov 23 2005 Ramon Bastiaans <bastiaans@sara.nl>
- Fixed missing prep setup and added configure
* Tue Nov 22 2005 Martin Pels <pels@sara.nl>
- Changed default directory permissions
* Tue Nov 01 2005 Martin Pels <pels@sara.nl> 
- Initial version

