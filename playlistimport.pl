#!/usr/bin/perl
use DBI;

my $playlist="christmas";

my $dbh = DBI->connect("DBI:SQLite:dbname=/home/pi/www/jukebox.db", "", "", { RaiseError => 1 }) or die $DBI::errstr;
my $s=$dbh->prepare("select max(id) from playlists");
$s->execute();
my @row=$s->fetchrow_array();
my $id=0;
if(@row){$id=$row[0]+1;}

print $id;
my $sort=1;

while($l=<>){
	$l=~s/\r*\n*$//gis;
	my $sql="insert into playlists (id,sort,playlist,path) values ($id,$sort,'$playlist',".$dbh->quote($l).");";
	print "$sql\r\n";
	$dbh->do($sql);
	$id++;
	$sort++;
}

