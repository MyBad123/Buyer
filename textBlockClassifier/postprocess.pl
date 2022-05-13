my $n_line = 1;
my $n_cnt = 0;

sub is_price
{
  my $res = @_[0];
  if ($res =~ /^[\d\., ]+\$$/) {
    return 1;
  }
  if ($res =~ /^[\d\., ]+₽$/) {
    return 1;
  }
  if ($res =~ /^[\d\., ]+р\.?$/ || $res =~ /[\d\., ]+Р\.?$/) {
    return 1;
  }
  if ($res =~ /^[\d\., ]+руб\.?$/ || $res =~ /[\d\., ]+Руб\.?$/) {
    return 1;
  }
  return 0;
}

sub is_h1_or_href
{
  my $res = @_[0];
  #print ("is_h1_or_href($res)\n");

  if ($res =~ /^a\/\/.*/i) {
    return 1;
  }
  if ($res =~ /^h1\/\/.*/i) {
    return 1;
  }
  if ($res =~ /^title\/\/.*/i) {
    return 1;
  }
  return 0;
}

while(<>) {
  chomp;
  s/\".*?\"//g; # remove everything enclosed in " "
  my @values = split(/,/);

  $n_cnt = @values if (!$n_cnt);
  #if ($n_line >= 3045 && $n_line < 7698 || $n_line > 7777) { #cut of 4 parameters
  #  splice(@values, 30, 1); #remove ...ratio...
  #  splice(@values, 28, 1); #remove ???
  #  splice(@values, 27, 1); #remove saturation
  #  splice(@values, 26, 1); #remove hue
  #}

  if ($n_cnt != ($#values + 1)) {
    print "Line $n_line: incorrect number of elements $n_cnt <> ".($#values + 1)."\n";
  }
  elsif (is_price($values[2]) && $values[1] != 2) {
    print "Line $n_line: price is not detected ".$values[2]."\n";
    #$values[1] = 2;
  }
  elsif ($values[1] == 1 && !is_h1_or_href($values[29])) {
    print "Line $n_line: incorrect tags for 'nazvanie'\n";
    #$values[29] = 'a//' . $values[29];
  }
  $n_line++;
  #my $str = join( ',', @values );
  #print "$str\n";
}