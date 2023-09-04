#!/usr/bin/env perl

use strict;
use warnings;
use CGI::Minimal;

use constant HTDOCS => '/usr/local/apache2/htdocs';

sub read_file {
	my ($file_path) = @_;
	my $fh;

	local $/;
	open($fh, "<", $file_path) or return "read_file error: $!";
	my $content = <$fh>;
	close($fh);

	return $content;
}

sub route_request {
	my ($page, $remote_addr) = @_;

	if ($page =~ /^about$/) {
		return HTDOCS . '/pages/about.txt';
	}

	if ($page =~ /^version$/) {
		return '/proc/version';
	}

	if ($page =~ /^cpuinfo$/) {
		return HTDOCS . '/pages/denied.txt' unless $remote_addr eq '127.0.0.1';
		return '/proc/cpuinfo';
	}

	if ($page =~ /^stat|io|maps$/) {
		return HTDOCS . '/pages/denied.txt' unless $remote_addr eq '127.0.0.1';
		return "/proc/self/$page";
	}

	return HTDOCS . '/pages/home.txt';
}

sub escape_html {
	my ($text) = @_;

	$text =~ s/</&lt;/g;
	$text =~ s/>/&gt;/g;

	return $text;
}

my $q = CGI::Minimal->new;

print "Content-Type: text/html\r\n\r\n";

my $file_path = route_request($q->param('page'), $ENV{'REMOTE_ADDR'});
my $file_content = read_file($file_path);

print escape_html($file_content);