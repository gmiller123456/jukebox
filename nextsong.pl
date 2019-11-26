#!/usr/bin/perl
use strict;
use DBI;

print "Content-type: text/html\n\n";
my $dbh = DBI->connect("DBI:SQLite:dbname=/home/pi/www/jukebox.db", "", "", { RaiseError => 1 }) or die $DBI::errstr;

my $s=$dbh->prepare("select playlist,entry from activeplaylist;");
$s->execute();
my @row=$s->fetchrow_array();
if(!@row) {exit;}
my $playlist=$row[0];
my $entry=$row[1];

if($entry>0){
	$s=$dbh->prepare("select sort,path from playlists where playlist='$playlist' and sort>$entry;");
	$s->execute();
} else {
	$s=$dbh->prepare("select sort,path from playlists where playlist='$playlist' order by random() limit 1;");
	$s->execute();
}

@row=$s->fetchrow_array();
if(!@row) {
	$s=$dbh->prepare("select sort,path from playlists where playlist='$playlist' order by sort limit 1;");
	$s->execute();
	@row=$s->fetchrow_array();
}

if(!@row){exit;}

my $sort=$row[0];
my $path=$row[1];

$dbh->do("update activeplaylist set entry=$sort;");

playSong($path);

sub playSong(){
	my $s=shift;
	my $f;

	$s=~s/\r*\n*//gis;
    open($f,">>","/home/pi/www/fifo/mpg123");
    print $f "L $s\n";
    print "L $s\n";
    close($f);
}