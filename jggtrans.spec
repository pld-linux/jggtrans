Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu³ transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	0.9.9
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.bnet.pl/~jajcus/%{name}/%{name}-%{version}.tar.gz
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
BuildRequires:	libgadu-devel >= 0.9.0.20020223
BuildRequires:	glib-devel
Requires:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber communicate with GaduGadu server.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabber komunikowaæ siê z
u¿ytkownikami GaduGadu

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR="$RPM_BUILD_ROOT"
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d,/etc/sysconfig}
install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

gzip -9nf AUTHORS ChangeLog README TODO README.Pl jggtrans.xml.Pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -r /var/lock/subsys/jggtrans ]; then
       	/etc/rc.d/init.d/jggtrans restart >&2
else
        echo "Run \"/etc/rc.d/init.d/jggtrans start\" to start Jabber GaduGadu transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jggtrans ]; then
		/etc/rc.d/init.d/jggtrans stop >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jggtrans.xml
%attr(755,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jggtrans
