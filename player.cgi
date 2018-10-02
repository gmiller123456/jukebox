#!/usr/bin/perl
require "./parse.pl";
&ReadParse(*input);

print "Content-type: text/html\n\n";

if($input{playlist} eq "play"){
    print "Playlist\n";
    stop();
   system("nohup mpg123 --keep-open --random -@ /home/pi/www/top500fav.txt");
}

if($input{volume} ne ""){
   sendCommand("V ".$input{volume}."\r\n");
}

if($input{file} ne ""){
    stop();
   sendCommand('L '.$input{file}."\r\n");
}

if($input{command} eq "stop"){
    stop();
}

if($input{command} eq "startserver"){
   system("screen -wipe");
   system("nohup mpg123 --fifo /home/pi/www/fifo/mpg123 -R asdf | ./outputparser.pl");
   sleep(1);
   system("chmod a+w /home/pi/www/fifo/mpg123");
}

if($input{command} eq "wipe"){
   system("screen -wipe");
}

sub stop(){
   sendCommand("S\r\n");
   $p=`ps ax | grep mpg123 | grep random`;
   $p=~m/^\s*(\d+)/gis;
   system("kill -KILL $1");
   print "Killing: ".$1;
}

sub sendCommand(){
    my $s=shift;
    my $f;
    open($f,">>","/home/pi/www/fifo/mpg123");
    print $f $s;
    close($f);
    print "Sent: ".$s;
}

#Start screen server: screen -d -m -S Player mpg123 -R asdf
#Send command: screen -S Player -p 0 -X stuff "L Haddaway - What is Love   Lyrics.mp3^M"

#system('mpg123 "/home/pi/Music/Haddaway - What is Love   Lyrics.mp3"');


