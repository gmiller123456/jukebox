#!/usr/bin/perl
$|=1;
require "./parse.pl";
&ReadParse(*input);

print "Content-type: text/html\n\n";

if($input{playlist} eq "main"){
    print "Playlist\n";
    stop();

   my $file;
   open($file,">/home/pi/www/playlistentry.txt");
   print $file "0";
   close($file);

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
    system("screen -d -m -S Random mpg123 --keep-open --random -@ /home/pi/www/christmas.txt");
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

if($input{command} eq "add"){
    my $file;
    open($file,">>/home/pi/www/playlist.txt");
    print $file "\n".$input{addfile};
    close($file);
}

if($input{command} eq "startserver"){
    startServer();
}

if($input{command} eq "stopserver"){
    killServer();
    #startServer();
}

if($input{command} eq "wipe"){
   system("screen -wipe");
}

sub killServer(){
   $p=`ps ax | grep mpg123`;
   $p=~m/^\s*(\d+)/gis;
   system("kill -KILL $1");
   print "Killing: ".$1."\n";

   $p=`ps ax | grep outputparser.pl | grep perl`;
   $p=~m/^\s*(\d+)/gis;
   system("kill -KILL $1");
   print "Killing: ".$1."\n";
}

sub startServer(){
   system("screen -wipe");
   print "Starting";
   #system("screen -d -m -S Player \"sh -c 'mpg123 --fifo /home/pi/www/fifo/mpg123 -R asdf | /home/pi/www/outputparser.pl > /home/pi/www/log/log.txt\n'\"");
   #system("screen -d -m -S Player mpg123 --fifo /home/pi/www/fifo/mpg123 -R asdf");
   system("screen -d -m -S Player /home/pi/www/startserver.sh");
   print "Started";
   sleep(1);
   system("chmod a+w /home/pi/www/fifo/mpg123");
}

sub stop(){
   my $file;
   open($file,">/home/pi/www/playlistentry.txt");
   print $file "-1";
   close($file);

   print "Stop\n";
   sendCommand("S\r\n");
   $p=`ps ax | grep mpg123 | grep random | grep -iv screen`;
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

#Start screen server: screen -d -m -S Player mpg123 -R asdf
#Send command: screen -S Player -p 0 -X stuff "L Haddaway - What is Love   Lyrics.mp3^M"

#system('mpg123 "/home/pi/Music/Haddaway - What is Love   Lyrics.mp3"');


