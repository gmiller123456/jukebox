#!/usr/bin/perl
use strict;

my $file;
open($file,"/home/pi/public_html/playlistentry.txt");
my $e=join('',<$file>);
close($file);

if($e < 0){exit;}

open($file,"/home/pi/public_html/playlist.txt");

my @lines=<$file>;
close($file);
my $total=scalar @lines;

playSong($lines[$e]);

$e++;
if($e>=$total){$e=0;}
open($file,">/home/pi/public_html/playlistentry.txt");
print $file $e;
close($file);

sub playSong(){
	my $s=shift;
	my $f;

	$s=~s/\r*\n*//gis;
    open($f,">>","/home/pi/www/fifo/mpg123");
    print $f "L $s\n";
    print "L $s\n";
    close($f);

}