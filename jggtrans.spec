Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu� transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	1.1.0
Release:	3
License:	GPL
Group:		Applications/Communications
Source0:	http://www.bnet.pl/~jajcus/%{name}/%{name}-%{version}.tar.gz
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
BuildRequires:	libgadu-devel >= 0.9.0.20020528
BuildRequires:	glib-devel
Requires:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber communicate with GaduGadu server.

%description -l pl
Modu� ten umo�liwia u�ytkownikom Jabber komunikowa� si� z
u�ytkownikami GaduGadu.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install DESTDIR="$RPM_BUILD_ROOT"

install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

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
%doc AUTHORS ChangeLog README TODO README.Pl jggtrans.xml.Pl
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jggtrans
