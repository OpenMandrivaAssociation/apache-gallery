%define module	Apache-Gallery

Name:		    apache-gallery
Version:	    1.0.2
Release:	    1
Summary:	    A mod_perl handler to create an image gallery
License:	    GPL or Artistic
Group:		    Networking/WWW
URL:		    http://apachegallery.dk/
Source0:	    http://apachegallery.dk/download/%{module}-%{version}.tar.gz
Patch0:		    %{name}-0.9.5.urlbase.patch
Requires:	    apache-mod_perl
Obsoletes:	    perl-Apache-gallery
Provides:	    perl-Apache-gallery
BuildRequires:	apache-mod_perl
# (tv) for testsuite:
BuildRequires:	perl(CGI)
BuildRequires:	perl(URI::Escape)
BuildRequires:	perl(Image::Imlib2)
BuildRequires:	perl(Image::Info)
BuildRequires:	perl(Image::Size)
BuildRequires:	perl(Text::Template)
BuildRequires:	perl(Test::MockObject)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl-devel
BuildArch:	    noarch

%description
Apache::Gallery creates an thumbnail index of each directory and
allows viewing pictures in different resolutions. Pictures are
resized on the fly and cached.

%prep
%setup -q -n %{module}-%{version}
#patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%install
%makeinstall_std
install -d -m 755 %{buildroot}%{_datadir}/apache-gallery/default
install -d -m 755 %{buildroot}/var/www/apache-gallery/static

for template in default new; do
    install -d -m 755 %{buildroot}%{_datadir}/apache-gallery/$template
    install -m 644 templates/$template/*.tpl %{buildroot}%{_datadir}/apache-gallery/$template
    install -m 644 templates/$template/gallery.css %{buildroot}/var/www/apache-gallery/static/$template.css
done

install -m 644 htdocs/* %{buildroot}/var/www/apache-gallery/static

install -d -m 755 %{buildroot}/var/www/apache-gallery/photos

install -d -m 755 %{buildroot}/var/cache/apache-gallery

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /apache-gallery/static /var/www/apache-gallery/static
Alias /apache-gallery /var/www/apache-gallery/photos

<IfModule mod_perl.c>
    PerlSetVar GalleryTemplateDir '/usr/share/apache-gallery/default'
    PerlSetVar GalleryCacheDir    '/var/cache/apache-gallery'
    PerlSetVar GalleryURLBase     '/apache-gallery/static'
    PerlOptions +GlobalRequest

    <Directory /var/www/apache-gallery>
        Allow from all
    </Directory>

    <Directory /var/www/apache-gallery/photos>
        SetHandler        modperl
        PerlResponseHandler       Apache::Gallery
    </Directory>

    <Directory /var/cache/apache-gallery>
        Allow from all
    </Directory>
</ifModule>
EOF

%check
#make test

%files
%doc README Changes INSTALL LICENSE TODO UPGRADE
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{perl_vendorlib}/Apache
%{_datadir}/%{name}
%attr(-,apache,apache) /var/cache/%{name}
/var/www/%{name}
%{_mandir}/*/*



%changelog
* Sat Feb 19 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.9mdv2011.0
+ Revision: 638766
- update urlbase patch to handle bugs #62482 and #61937

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.RC2.8mdv2011.0
+ Revision: 609982
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.7mdv2010.1
+ Revision: 513191
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Tue Sep 01 2009 Thierry Vignaud <tv@mandriva.org> 1.0-0.RC2.7mdv2010.0
+ Revision: 423977
- rebuild

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 1.0-0.RC2.6mdv2009.0
+ Revision: 135820
- restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 1.0-0.RC2.6mdv2008.1
+ Revision: 132461
- BR perl(CGI) for testsuite
- kill re-definition of %%buildroot on Pixel's request


* Thu Aug 31 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.6mdv2007.0
- buildrequires (URI::Escape)

* Fri Jun 30 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.5mdv2007.0
- relax buildrequires versionning
- buildrequires perl(Image::Size)

* Mon Jun 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.4mdv2007.0
- rebuild with corrected webapp macros

* Tue Jun 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.3mdv2007.0
- rename to apache-gallery, as it is not a perl library
- mv data files under /usr/share/apache-gallery, web files under /var/www/apache-gallery and temp files under /var/cache/apache-gallery
- fix stylesheet install
- drop previous patches
- new configurable base url patch
- default apache configuration

* Tue Jun 28 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.2mdk 
- requires apache-mod_perl
- drop useless patches
- include empty templates, otherwise the application crashes

* Thu Jun 02 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-0.RC2.1mdk 
- new version
- re-enable make test in %%check

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.1-4mdk
- spec file cleanups, remove the ADVX-build stuff
- disable make test for now

* Wed Jan 26 2005 Guillaume Rousse <guillomovitch@mandrake.org> 0.9.1-3mdk 
- fix non-jpg images issue
- fix icons path
- use /var/cache/gallery as cache location
- fix lowercase summary
- remove empty files
- change URL

* Fri Sep 17 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.9.1-2mdk 
- fixed mod_perl2 issue

* Sun Sep 12 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.9.1-1mdk
- new version  
- buildrequires

* Wed Jul 21 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.8-2mdk 
- rpmbuildupdate aware

* Wed Apr 07 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.8-1mdk
- new version
- correct source URL
- corrected buildrequires

* Wed Feb 25 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.7-4mdk
- fixed dir ownership (distlint)

* Mon Jan 12 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.7-3mdk
- buildrequires (slbd)

* Mon Dec 08 2003 Guillaume Rousse <guillomovitch@mandrake.org> 0.7-2mdk
- included missing templates and icons

* Mon Dec 08 2003 Guillaume Rousse <guillomovitch@mandrake.org> 0.7-1mdk
- first mdk release

