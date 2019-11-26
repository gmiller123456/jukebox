#!/usr/bin/perl
$|=1;
use DBI;

print "Content-type: text/html\n\n";
my $dbh = DBI->connect("DBI:SQLite:dbname=/home/pi/www/jukebox.db", "", "", { RaiseError => 1 }) or die $DBI::errstr;

require "./parse.pl";
&ReadParse(*input);

if($input{playlist} eq "main"){
	stop();

	$dbh->do("delete from activeplaylist;");
	$dbh->do("insert into activeplaylist (playlist,entry) values ('default',0);");

	system("/home/pi/www/nextsong.pl");

}

if($input{playlist} eq "play"){
    print "Playlist\n";
    stop();
    #system("screen -d -m -S Random mpg123 --keep-open --random -@ /home/pi/www/top500fav.txt > log/log.txt");
    system("screen -d -m -S Random mpg123 --keep-open --random -@ /home/pi/www/top500fav.txt");
    #system("nohup mpg123 --keep-open --random -@ /home/pi/www/top500fav.txt > log/log.txt &");
}

if($input{playlist} eq "christmas"){
    print "Playlist Christmas\n";
    stop();
    #system("screen -d -m -S Random mpg123 --keep-open --random --fifo /home/pi/www/fifo/mpg123 -@ /home/pi/www/christmas.txt > /home/pi/www/log/log.txt");
    #sendCommand("LOADLIST 1 /home/pi/www/christmas.txt\r\n");
	#mpg123 --fifo /home/pi/www/fifo/mpg123 -R asdf > /home/pi/www/log/log.txt &

	$dbh->do("delete from activeplaylist;");
	$dbh->do("insert into activeplaylist (playlist,entry) values ('christmas',-1);");

	system("/home/pi/www/nextsong.pl");
}

if($input{command} eq "list"){
	my $pl=$dbh->quote($input{playlist});
	my $sql = "select id,sort,playlist,path from playlists where playlist=$pl;";
	my $s=$dbh->prepare($sql);
	$s->execute();
	while(my @row=$s->fetchrow_array()){
		print "$row[0]|$row[1]|$row[2]|$row[3]\r\n";
	}
}

if($input{command} eq "add"){
	my $pl=$dbh->quote($input{playlist});
	my $sql="select max(sort),max(id) from playlists where playlist=$pl;";

	my $sth = $dbh->prepare( $sql );
	my $rv = $sth->execute() or die $DBI::errstr;
	my @row = $sth->fetchrow_array();
	my $sort=$row[0]+1;
	my $id=$row[1]+1;

	$input{addfile}=~s/\s*$//gis;
	$sql="insert into playlists (id,sort,playlist,path) values ($id,$sort,$pl,".$dbh->quote($input{addfile}).");";
	$sth=$dbh->prepare($sql);
	$sth->execute();
}

if($input{command} eq "deleteFromPlaylist"){
	if($input{id}=~m/[^0-9]/){exit;}
	my $sql="delete from playlists where id=".$input{id};
	$dbh->do($sql);
}

sub stop(){
   my $file;
   open($file,">/home/pi/www/playlistentry.txt");
   print $file "-1";
   close($file);

   print "Stop\n";
   sendCommand("S\r\n");
   my $p=`ps ax | grep mpg123 | grep random | grep -iv screen`;
   $p=~m/^\s*(\d+)/gis;
   system("kill -KILL $1");
   print "Killing: ".$1."\n";

}

sub sendCommand(){
    my $s=shift;
    my $f;
    print "Sending: ".$s;
    open($f,">>","/home/pi/www/fifo/mpg123");
    print $f $s;
    close($f);
    print "Sent: ".$s;
}
