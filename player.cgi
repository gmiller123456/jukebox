#!/usr/bin/perl
require "./parse.pl";
&ReadParse(*input);

print "Content-type: text/html\n\n";

if($input{playlist} eq "play"){
    print "Playlist\n";
   system("screen -d -m -S top500fav mpg123 --random -@ /home/pi/www/top500.txt");
   #$t='screen -S top500 -p 0 -X stuff "LOADLIST >1 http://127.0.0.1/~pi/top500fav.txt^M"';
}

if($input{volume} ne ""){
   $t='screen -S Player2 -p 0 -X stuff "V '.$input{volume}.'^M"';
   print $t;
   system($t);
   #system('screen -S Player2 -p 0 -X stuff "V 100^M"');
}

if($input{file} ne ""){
   print "<h1>Now Playing: $input{file}</h1><br>\r\n";
   #system('screen -S Player2 -p 0 -X stuff "L /home/pi/Music/'.$input{file}.'^M"');
   system('screen -S Player2 -p 0 -X stuff "L '.$input{file}.'^M"');
}

if($input{command} eq "stop"){
   system('screen -S Player2 -p 0 -X stuff "S^M"');
   $p=`ps a | grep mpg123 | grep random`;
   $p=~m/^\s*(\d+)/gis;
   system("kill -KILL $1");
}

if($input{command} eq "startserver"){
   system("screen -wipe");
   system("screen -d -m -S Player2 mpg123 -R asdf");
}

if($input{command} eq "wipe"){
   system("screen -wipe");
}

#Start screen server: screen -d -m -S Player mpg123 -R asdf
#Send command: screen -S Player -p 0 -X stuff "L Haddaway - What is Love   Lyrics.mp3^M"

#system('mpg123 "/home/pi/Music/Haddaway - What is Love   Lyrics.mp3"');


