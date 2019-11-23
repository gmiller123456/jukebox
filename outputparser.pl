#!/usr/bin/perl
use strict;

print "Starting outputparser\n";
my $log;
open($log,"/home/pi/www/log/log.txt");
my $l;
while(1){
   $l=<$log>;
   $l=~s/\r*\n*//gs;
   if($l ne ""){ print "$l\n";}
   if(length($l)<2){ next;}
   if(substr($l,0,1) ne '@'){next;}
   my $c=substr($l,1,1);
   if($c eq "F"){parseFrame($l);}
   if($c eq "I"){parseInfo($l);}
   if($c eq "P"){parseState($l);}
   if($c eq "S"){parseExtraInfo($l);}
   if($c eq "V"){parseVolume($l);}
}
print "Exiting outputparser\n";

sub parseVolume(){
	my $l=shift;
	my ($temp,$volume)=split(/ /,$l);
	$volume=~s/\%//gis;
	writeField(155,10,$volume);
}

my $lastTime=0;
sub parseFrame(){
	my $l=shift;
	my ($temp,$frameNum,$framesLeft,$time,$timeLeft)=split(/ /,$l);
	if($frameNum==0){
		writeField(125,10,$timeLeft);
	}
	if($time-$lastTime>.5){
		writeField(135,10,$time);
		$lastTime=$time;
	}
}

sub parseInfo(){
	my $l=shift;
	#print "Ifno $l";
	if(substr($l,0,15) eq "\@I ID3v2.title:"){writeTitle(substr($l,15,30));}
	if(substr($l,0,16) eq "\@I ID3v2.artist:"){writeArtist(substr($l,16,30));}
	if(substr($l,0,15) eq "\@I ID3v2.album:"){writeAlbum(substr($l,15,30));}
	if(substr($l,0,14) eq "\@I ID3v2.year:"){writeYear(substr($l,14,4));}
	if(substr($l,0,15) eq "\@I ID3v2.genre:"){wrietGenre(substr($l,15,30));}
	$lastTime=0;
}

sub writeField {
	my $pos=shift;
	my $length=shift;
	my $text=shift;
	
	my $file;
	$text.=" " x ($length-length($text));
	open($file,"+<","/home/pi/public_html/playinfo.txt");
	seek($file,$pos,0);
	print $file $text;
	close($file);
}

sub writeTitle(){
	my $f=shift;
    $f=~s/[^a-zA-Z ]//gis;
	writeField(0,30,$f);
}
sub writeArtist(){
	my $f=shift;
    $f=~s/[^a-zA-Z ]//gis;
	writeField(30,30,$f);
}
sub writeAlbum(){
	my $f=shift;
    $f=~s/[^a-zA-Z ]//gis;
	writeField(60,30,$f);
}
sub writeYear(){
	my $f=shift;
    $f=~s/[^a-zA-Z ]//gis;
	writeField(120,5,$f);
}
sub wrietGenre(){
	my $f=shift;
    $f=~s/[^a-zA-Z ]//gis;
	writeField(90,30,$f);
}

sub parseState(){
	my $l=shift;
	my $s=substr($l,3,1);
	writeField(145,10,$s);
	if($s==0){
		system("/home/pi/public_html/nextsong.pl");
	}
}

sub parseExtraInfo(){
	my $l=shift;
	#print "Extra $l";
}
