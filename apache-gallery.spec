%define name	apache-gallery
%define module	Apache-Gallery
%define version	1.0
%define pre	RC2
%define release	%mkrel 0.%{pre}.8

Name:		    %{name}
Version:	    %{version}
Release:	    %{release}
Summary:	    A mod_perl handler to create an image gallery
License:	    GPL or Artistic
Group:		    Networking/WWW
URL:		    http://apachegallery.dk/
Source0:	    http://apachegallery.dk/download/%{module}-%{version}%{pre}.tar.bz2
Patch0:		    %{name}-0.9.5.urlbase.patch
Requires:	    apache-mod_perl
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
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
BuildArch:	    noarch
BuildRoot:	    %{_tmppath}/%{name}-%{version}

%description
Apache::Gallery creates an thumbnail index of each directory and
allows viewing pictures in different resolutions. Pictures are
resized on the fly and cached.

%prep
%setup -q -n %{module}-%{version}%{pre}
%patch0 -p 1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%install
rm -rf %{buildroot}
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
make test

%clean 
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc README Changes INSTALL LICENSE TODO UPGRADE
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{perl_vendorlib}/Apache
%{_datadir}/%{name}
%attr(-,apache,apache) /var/cache/%{name}
/var/www/%{name}
%{_mandir}/*/*

