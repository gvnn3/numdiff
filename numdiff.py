#!/usr/bin/env python3
# Copyright (c) 2014, Neville-Neil Consulting
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the name of Neville-Neil Consulting nor the names of its 
# contributors may be used to endorse or promote products derived from 
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: George V. Neville-Neil
#
# Description: Diff two files, line by line, print the differences in 
# the numbers found.  Useful for comparing repeated sysctl dumps.

import sys
import argparse

def usage(error):

    print(sys.argv[0], " usage: ", sys.argv[0], "file1 file2 [sep]")
    print("Error: ", error)

def main():

    # Defaults
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug", action="store_true")
    parser.add_argument("-z", "--zero", help="print lines with 0 difference", 
                        action="store_true")
    parser.add_argument("-l", "--leading", help="number is at the start of a line", 
                        action="store_true")
    parser.add_argument("-s", "--sep", help="change default separator (:)", 
                        default=":")

    parser.add_argument("left", help="left hand file")
    parser.add_argument("right", help="right hand file")

    args = parser.parse_args()

    left_name = args.left
    right_name = args.right

    try:
        left = open(left_name)
    except:
        usage("File not found " % left_name)

    try:
        right = open(right_name)
    except:
        usage("File not found " % right_name)

    sep = args.sep

    for left_line in left:
        try:
            right_line = right.readline()
        except EOFError:
            print("file ", right_name, " has fewer lines than ", left_name)
            exit()

        left_line = left_line.lstrip()
        right_line = right_line.lstrip()

        # Remove all white space, tabs, newlines etc.
        if (sep != " "):
            left_line = ''.join(left_line.split())
            right_line = ''.join(right_line.split())
        else:
            left_line = left_line.replace('\n', '')
            right_line = right_line.replace('\n', '')

        # We ignore errors and move on, figuring the next lines
        # will bring us new matches.
        try:
            if (args.leading):
                left_num, left_str = left_line.split(sep, 1)
                right_num, right_str = right_line.split(sep, 1)
            else:
                left_str, left_num = left_line.split(sep, 1)
                right_str, right_num = right_line.split(sep, 1)
        except:
            continue

        if (left_str != right_str):
            if (args.debug):
                print (left_str, "not equal to", right_str)
            continue

        if (not left_num.isdigit()):
            if (args.debug):
                print ("left_num ", left_num)
            continue

        if (not right_num.isdigit()):
            if (args.debug):
                print ("right_num", right_num)
            continue

        diff = int(right_num) - int(left_num)
    
        if (diff == 0 and not args.zero):
            continue

        print ("{0}{1} {2}".format(left_str, sep , diff))

# The canonical way to make a python module into a script.
# Remove if unnecessary.
 
if __name__ == "__main__":
    main()

