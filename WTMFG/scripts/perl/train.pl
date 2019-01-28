use strict;
use warnings;
use FindBin;

### 0. initialize env variables
my $home_dir = "$FindBin::Bin";
$home_dir =~ s/\/bin$//;
#print "$home_dir\n";
if (defined $ENV{'PERL5LIB'}) {
    $ENV{'PERL5LIB'} = "$ENV{PERL5LIB}:$home_dir/lib/perl";
} else {
    $ENV{'PERL5LIB'} = "$home_dir/lib/perl";
}


my $clean = 1;
my $is_train = 1;

die "Usage:  perl  train.pl  model_dir  train_file \n" if (@ARGV != 2);

my $model_dir = $ARGV[0];
my $train_file = $ARGV[1];

# if ($train_file ne "$model_dir/texts.txt") {
#     `cp $train_file $model_dir/texts.txt`;
# }


### 1. preprocess text
my $cmd;
$cmd = "perl  $home_dir/preprocess.pl  $model_dir/texts.txt  $model_dir/train.clean";
print "[step 1]: $cmd\n\n";
`$cmd`;


### 2. change to matlab format
$cmd = "perl $home_dir/change_format.pl  $model_dir  1  $model_dir/train.clean  $model_dir/train.ind";
print "[step 2]: $cmd\n\n";
`$cmd`;

