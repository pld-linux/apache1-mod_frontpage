#!/usr/bin/perl

$sbindir="/usr/sbin";
$apxs="$sbindir/apxs";
$confdir=`$apxs -q SYSCONFDIR`; 
$confdir =~ s|\n||;
$cc=`$apxs -q CC`;
$cc =~ s|\n||;
$cflags=`$apxs -q CFLAGS`;
$cflags =~ s|\n||;
$includedir=`$apxs -q INCLUDEDIR`;
$includedir =~ s|\n||;
$libexecdir=`$apxs -q LIBEXECDIR`;
$libexecdir =~ s|\n||;

### Create Makefile
$install=`which install`;
chop $install;
open(MTMP,"Makefile.in") or die "Can't find Makefile.tmpl\n";
open(MAKF,"> Makefile") or die "Can't create Makefile\n";
print "Creating Makefile\n";
while(<MTMP>) {
$_=~ s|\$\(apxs\)|$apxs|;
$_=~ s|\$\(apachectl\)|/usr/sbin/apachectl|;
$_=~ s|\$\(cc\)|$cc|;
$_=~ s|\$\(includedir\)|$includedir|;
$_=~ s|\$\(cflags\)|$cflags|;
$_=~ s|\$\(sbindir\)|/usr/sbin|;
$_=~ s|\$\(install\)|$install|;
$_=~ s|\$\(fpexec_uidcaller\)|http|;
$_=~ s|\$\(fpexec_gidcaller\)|http|;
$_=~ s|\$\(fpexec_uidmin\)|1000|;
$_=~ s|\$\(fpexec_gidmin\)|1000|;
$_=~ s|\$\(fpexec_logexec\)|/var/log/httpd/fpexec_log|;
$_=~ s|\$\(fpexec_userdir\)|public_html|;
$_=~ s|\$\(fpexec_docroot\)|/home/services/httpd/html|;
$_=~ s|"\$\(fpexec_bin\)|\\\\\"$sbindir\/fpexec\\\\|;
$_=~ s|"\$\(fpstatic_bin\)|\\\\\"$sbindir\/fpstatic\\\\|;
print MAKF $_;
}
