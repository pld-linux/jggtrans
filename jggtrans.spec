Summary:	GaduGadu transport module for Jabber
Summary(pl):	Modu³ transportowy GaduGadu dla systemu Jabber
Name:		jabber-gg-transport
Version:	0.9
Release:	1
License:	GPL
Group:		Applications/Communications
Group(de):	Applikationen/Kommunikation
Group(pl):	Aplikacje/Komunikacja
Source0:	http://www.bnet.pl/~jajcus/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-startup.patch
BuildRequires:	libgg
BuildRequires:	glib
Requires:	jabber
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/jabber

%description
This module allows Jabber communicate with GaduGadu server.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabber komunikowaæ siê 
z u¿ytkownikami GaduGadu

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR="$RPM_BUILD_ROOT"
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install ggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS ChangeLog README TODO README.Pl ggtrans.xml.Pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -r /var/lock/subsys/jabberd ]; then
	if [ -r /var/lock/subsys/jabber-ggtrans ]; then
        	/etc/rc.d/init.d/jabberd restart ggtrans >&2
	else
        	echo "Run \"/etc/rc.d/init.d/jabberd start ggtrans\" to start GG transport."
	fi
else
        echo "Run \"/etc/rc.d/init.d/jabberd start\" to start Jabber server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-ggtrans ]; then
		/etc/rc.d/init.d/jabberd stop ggtrans >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
