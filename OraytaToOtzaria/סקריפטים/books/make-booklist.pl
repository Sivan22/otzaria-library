#!/usr/bin/env perl
     
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

my @output;

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
    push @output, "$fname, $size, $date, $md5\n";

}

@output = sort @output;
print @output;

    
     
    exit 0;
