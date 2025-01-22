#!/usr/bin/perl
use strict;
use warnings;

my $filename = $ARGV[0];
open(my $fh, '<', $filename) or die "Cannot open file: $!";

my %word_count;
while (my $line = <$fh>) {
    chomp $line;
    my @words = split(/\s+/, $line);
    foreach my $word (@words) {
        $word_count{lc $word}++;
    }
}

close($fh);

foreach my $word (sort keys %word_count) {
    print "$word: $word_count{$word}\n";
}
