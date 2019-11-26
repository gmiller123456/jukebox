#!/usr/bin/perl

use DBI;
use strict;

my $dbh = DBI->connect("DBI:SQLite:dbname=jukebox.db", "", "", { RaiseError => 1 }) or die $DBI::errstr;

print "Opened database successfully\n";
