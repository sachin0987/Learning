#!/usr/bin/perl

use strict;
use warnings;

# Check if a CSV file is provided as a command-line argument
if (@ARGV != 1) {
    die "Usage: $0 <csv_file_path>\n";
}

my $csv_file = $ARGV[0];

# Call the csv_to_hash subroutine
my @data = csv_to_hash($csv_file);

# Print the resulting array of hashes (you can modify this part as per your requirements)
print "Array of hashes representation of CSV file:\n";
print_hash_array(@data);

# Subroutine to convert CSV file to an array of hashes
sub csv_to_hash {
    my ($csv_file) = @_;

    # Open the CSV file for reading
    open my $fh, '<', $csv_file or die "Could not open CSV file '$csv_file': $!\n";

    # Read the header row to get the column names
    my $header_row = <$fh>;
    chomp $header_row;
    my @column_names = split /,/, $header_row;

    # Read the rest of the rows and convert them to a hash
    my @data;
    while (my $row = <$fh>) {
        chomp $row;
        my @values = split /,/, $row;
        my %entry;
        @entry{@column_names} = @values;
        push @data, \%entry;
    }

    # Close the CSV file
    close $fh;

    return @data;
}

# Function to print an array of hashes
sub print_hash_array {
    my @data = @_;

    for my $entry (@data) {
        print_hash($entry);
        print "\n";
    }
}

# Function to print a hash
sub print_hash {
    my ($hash) = @_;

    for my $key (keys %$hash) {
        my $value = $hash->{$key};
        print "$key: $value\n";
    }
}
