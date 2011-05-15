#!/usr/bin/perl
# episode rename
# 2010 easyb

use utf8;
use File::Basename;
use Clipboard;

$debug = 0;

$usage = $#ARGV + 1;
 
if($usage < 1)
{
  print("First copy episode list from www.epguides.com to the clipboard.\n");
  print("usage: ./epren.pl files\n");
  exit;
}

########## prepare episode list ###########

$cb = Clipboard->paste;

print("The clipboard contains:\n" . $cb);

@lines = split('\n', $cb);

$names = "";

foreach(@lines)
{
  $line=$_;
  
  if($line =~ m/(\d)-(.\d)/)
  {
    $epnr = $1 . $2;
    $epnr =~ s/ /0/;
    
    $line =~ m/(\d?\d(\/|\s|\.)[A-Za-z]{3}(\/|\s|\.)\d\d)(.*)$/;
    $title = $+;
    $title =~ s/\s?\[Recap\]//;
    $title =~ s/\s?\[Trailer\]//;
    $title =~ s/^\s+//; #remove leading spaces
    $title =~ s/\s+$//; #remove trailing spaces
    
    $names = $names . $epnr . " - " . $title . "\n";
  }
}

#print $names;

print("\n\n");

########## process files ###########

foreach $_ (@ARGV) {
   #print $_ . "\n";
   $oldfnm = $_;
   $dirpath = dirname($oldfnm) . "/";
   
   $_ =~ m/0?(\d)[eExX]?(\d{2})/;
   $epnr = $1 . $2;
   
   $_ =~ m/(\.\w+$)/;
   $ext = $1;
   
   if($epnr && ($names =~ m/$epnr(.+)/g))
   {
      $newfnm = $dirpath . $epnr . $1 . $ext;
      
      print "renameing $oldfnm to: $newfnm\n";
      
      select(undef, undef, undef, 0.05); # wait 50ms
      
      if(!$debug) { rename($oldfnm, $newfnm) unless $oldfnm eq $newfn; }     
   }
}