#!/usr/bin/env perl
# based on make-booklist.pl
# this will update all files listed OraytaBookList to match the current files in this dir.
# usage: perl update-booklist.pl
  
  
use warnings;
use strict;
use POSIX;
use Digest::MD5;
use File::Find;
    
sub md5sum{
  my $file = shift;
  my $digest = "";
  eval{
    open(FILE, $file) or die "Can't find file $file\n";
    my $ctx = Digest::MD5->new;
    $ctx->addfile(*FILE);
    $digest = $ctx->hexdigest;
    close(FILE);
  };
  if($@){
    print $@;
    return "";
  }
  return $digest;
}

sub getDate {
    my $file =shift;
    my $date = POSIX::strftime( 
	  "%d/%m/%y", 
	  localtime( 
	      ( stat $file )[9]
	      )
	  );
	  
    return $date;
}

# begin here:
my $path =shift;
if (!$path ){
      $path =".";
}
chdir $path;

my %output;

File::Find::find({wanted => \&wanted_, no_chdir=>1}, "."); #go through path and execute 'wanted' on overy file.
sub wanted_ {
      my $longName = $File::Find::name;
      return if ($longName =~ m|/\.|) ; #dont process hidden files.
      return if ($_ eq "."); #dont process this folder twice.
      return if (! ($_ =~ /.*\.(obk|folder)$/i)); #process only files with .obk or .folder suffix

  my $fname = $_;
  my $md5 =  md5sum($fname);
  my $date = getDate($fname);
  my $size = -s $fname ;
#    push @output, "$fname, $size, $date, $md5\n";
      $output{$fname} = "$size, $date, $md5";

}

#@output = sort @output;

# try to update OraytaBookList
eval {
      my @holder; #holds the contents of the output file
      open(BOOKLIST_FILE, "<:encoding(utf8)", "./OraytaBookList") or die "Can't find OraytaBookList\n";
  while (<BOOKLIST_FILE>){
      if ($_ =~ /^(\.[^,]+),/){
	      my $currentFilename = $1;
	      if (exists $output{$currentFilename}){
		      push @holder, "$currentFilename, $output{$currentFilename}\n";	
		      next;	
	      }
	      
      } 
      push @holder, $_;

  }
  
  close(BOOKLIST_FILE);
  
      open(BOOKLIST_FILE, ">:encoding(utf8)", "./OraytaBookList") or die "Can't write to OraytaBookList\n";
  
  foreach (@holder) {print BOOKLIST_FILE $_};
      
  close(BOOKLIST_FILE);
      print "success!\n"
}
#print %output;

  
    
#    exit 0;
