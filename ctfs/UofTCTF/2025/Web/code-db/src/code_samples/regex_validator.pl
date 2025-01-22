#!/usr/bin/perl
use strict;
use warnings;

print "Enter a string to validate as email: ";
chomp(my $input = <STDIN>);

if ($input =~ /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/) {
    print "Valid email address.\n";
} else {
    print "Invalid email address.\n";
}
