#!/bin/env python
# -*- coding: utf-8 -*-
# convert old ~/.zsh_log to newer format: 
# username@hostname: -> username , hostname , 

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
		line = re.sub(' {1,}, {1,}' , ' , ', line)
		match =  re.search('\w+@[\w\.]+:', line)
		if match:
			m = match.group(0)
			span = match.span(0)			
			m = m.replace('@', ' , ')
			m = m.replace(':', ' , ')
			newline = line[0:span[0]] + m + line[span[1]:]
			logout.write(newline)

	logout.close()

if __name__ == '__main__':
	main()
