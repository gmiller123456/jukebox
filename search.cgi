#!/usr/bin/perl
require "./parse.pl";
&ReadParse(*input);

print "Content-type: text/html\n\n";
@words=split(/\s/,$input{keywords});
$f=pop(@words);
$s="grep -i $f index.txt";

while($f=pop(@words)){
    $s.=" | grep -i $f";
}

system($s);

