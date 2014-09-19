numdiff
=======

A simple program to show numeric differences in log files.

Given the output of two runs of a program that generates line by line
output, such as sysctl on FreeBSD, calculate the differences of the
numeric output.

Example
=======

    sysctl dev.igb.0 > before
    sleep 10
    sysctl dev.igb.0 > after
    numdiff before after

If you want to see lines even if the difference is 0 use -z

    numdiff -z before after

For netstat output you wind up with files where the separator is a
space and the number is at the start of the line.  For this case use
the --leading (aka -l) and --sep (aka -s) flags.

    netstat -s -p tcp > before
    sleep 10
    netstat -s -p tcp > after
    numdiff -l -s " " before after
