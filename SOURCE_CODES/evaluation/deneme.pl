#!/usr/bin/perl

print("hello");

$curdir=getcwd;
$ROUGE="../ROUGE-1.5.5.pl";
chdir("sample-test");

print($curdir);

$cmd="$ROUGE -e ../data -c 95 -2 -1 -U -r 1000 -n 4 -w 1.2 -a /tmp/tmpcfO0IT/rouge.xml > ../sample-output/erol.out";
print $cmd,"\n";
system($cmd);

