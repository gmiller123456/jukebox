#!/usr/bin/perl
printDir("/home/pi/Music");

sub printDir(){
	my $d;
	my $dir=shift;
	opendir($d,$dir);
	while($f=readdir($d)){
	   if(substr($f,0,1) eq ".") {next;}
	   if(-d $dir."/".$f){
           printDir($dir."/".$f);
   	   } else {
           print "$dir/$f\r\n";
	   }
	}
}
