Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu³ transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	2.0.1
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/%{name}/%{name}-%{version}.tar.gz
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
Patch0:		%{name}-pidfile.patch
Url:		http://www.jabberstudio.org/projects/jabber-gg-transport/project/view.php
BuildRequires:	libgadu-devel >= 2:1.0
BuildRequires:	glib-devel
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with GaduGadu server.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami GaduGadu.

%prep
%setup -q
%patch0 -p1

%build
%configure %{?debug:--with-efence}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install DESTDIR="$RPM_BUILD_ROOT"

install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add jggtrans
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
	/sbin/chkconfig --del jggtrans
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO README.Pl jggtrans.xml.Pl
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jggtrans
