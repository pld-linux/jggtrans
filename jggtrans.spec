%bcond_with	libgadu_snapshot

Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu³ transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	2.0.9
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	748ccd31a0f300e80d019780c4635881
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
Patch0:		%{name}-pidfile.patch
Patch1:		%{name}-spooldir.patch
URL:		http://www.jabberstudio.org/projects/jabber-gg-transport/project/view.php
BuildRequires:	glib-devel
BuildRequires:	libgadu-devel >= 2:1.0
BuildRequires:	pkgconfig
Requires:	jabber-common
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/usr/bin/perl
Requires(pre):	jabber-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with GaduGadu server.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami GaduGadu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	%{?debug:--with-efence} \
	%{?with_libgadu_snapshot:--with-libgadu-snapshot} \
	--sysconfdir=/etc/jabber
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d,/etc/sysconfig,/var/lib/jggtrans}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT" 

install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in jggtrans.xml..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/jggtrans.xml
	fi
fi
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
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%attr(770,root,jabber) /var/lib/jggtrans
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jggtrans
