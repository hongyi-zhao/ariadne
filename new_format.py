#!/bin/env python
# -*- coding: utf-8 -*-
# convert old ~/.zsh_log to newer format: 
#  old format was from original history recording function
# username@hostname: -> username , hostname , 
# replace 'path1 -> path2' for 'cd' entries

import argparse
import re

def main():
	parser = argparse.ArgumentParser()	
	parser.add_argument("-l","--logfile",type=str,help="Log file")
	parser.add_argument("-o","--newlogfile",type=str,help="New log file")

	args = parser.parse_args()

	logf = open(args.logfile,'r')
	logout = open(args.newlogfile,'w')

	for line in logf:
		line_orig = line
		# remove extra spaces
		line = re.sub(' {1,}, {1,}' , ' , ', line)
		newline = line

		# split user@host:path into comma delimited format
		match =  re.search('\w+@\w+:', line)
		if match:
			m = match.group(0)
			span = match.span(0)			
			m = m.replace('@', ' , ')
			m = m.replace(':', ' , ')
			newline = line[0:span[0]] + m + line[span[1]:]
			# logout.write(newline)
		line = newline

		# # replace 'path1 -> path2' entries to 'path1' for 'cd path2' entries, no longer necessary
		# match = re.search('.+ -> .+',line)
		# if match:
		# 	sp = match.group(0).split(' -> ')
		# 	span = match.span(0)
		# 	path1 = sp[0]
		# 	newline = line[0:span[0]] + path1 + line[span[1]:]
		
		logout.write(newline)


	logout.close()

if __name__ == '__main__':
	main()
