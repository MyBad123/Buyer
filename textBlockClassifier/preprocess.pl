# preprocessing of CSV dataset
# call perl x.pl input.csv > output.csv

$n_skip = 0;

while(<>) {
  chomp;
  my @values = split(/,/);

  foreach (@values) {
    $_ = 1 if (/True/i);
    $_ = 0 if (/False/i);    
  }
  if (!length($values[1])) {
    $n_skip++;
    next if ($n_skip < 8); # 8 is heuristic    

    $values[1] = 3; # class=3 <=> "неизвестно"
    $n_skip = 0;
  }
  elsif ($values[1] =~ /название/i || $values[1] =~ /Название/i) {
    $values[1] = 1; # class=1 <=> "название"
  }
  elsif ($values[1] =~ /цена/i || $values[1] =~ /Цена/i) {
    $values[1] = 2; # class=2 <=> "название"
  }
  elsif ($values[1] =~ /описание/i || $values[1] =~ /Описание/i) {
    $values[1] = 3; # class=3 <=> "название"
  }
  my $str = join( ',', @values );
  print "$str\n";
}