#
# Conditional build:
%bcond_with internal_libgadu	# Build with transport's internal libgadu

Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu³ transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	2.2.1
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://files.jabberstudio.org/jabber-gg-transport/%{name}-%{version}.tar.gz
# Source0-md5:	a202536d6af2f1a280d0aab3cf19cc2c
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
Patch0:		%{name}-pidfile.patch
Patch1:		%{name}-spooldir.patch
Patch2:		%{name}-external.patch
Patch3:		%{name}-acl.patch
URL:		http://www.jabberstudio.org/projects/jabber-gg-transport/project/view.php
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel >= 1.95.1
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
%{!?with_internal_libgadu:BuildRequires:	libgadu-devel}
BuildRequires:	libidn-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/usr/bin/perl
Requires(pre):	jabber-common
Requires:	jabber-common
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
%{!?with_internal_libgadu:%patch2 -p1}
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?debug:--with-efence} \
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
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jggtrans
%attr(770,root,jabber) /var/lib/jggtrans
