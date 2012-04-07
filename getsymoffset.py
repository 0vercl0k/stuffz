# -*- coding: utf-8 -*-
# By 0vercl0k
import sys
import re
import urllib2


def main():
	url = 'http://msdn.moonsols.com/'
	os2check = [
					'winxpsp1_x86', 'winxpsp2_x86', 'winxpsp3_x86',
					'winvistartm_x86', 'winvistasp1_x86', 'winvistasp2_x86',
					'win7rtm_x86'
				]
	regex = '/\*(0x[0-9A-F]{3})\*/ .* %s'

	if len(sys.argv) != 2:
		print 'Usage: ./%s <structure.field> ' % sys.argv[0]
		return 0

	try:
		struct = sys.argv[1].split('.')[0]
		field = sys.argv[1].split('.')[1]
	except:
		print '[!] Your structure is not correct.'
		return 0
	
	print '[*] Generate %s.%s offsets..' % (struct, field)
	
	rgx = re.compile(regex % field)
	for os in os2check:
		try:
			print '\t\'%s\' -> %s' % (os, rgx.findall(urllib2.urlopen('%s%s/%s.html' % (url, os, struct)).read())[0])
		except:
			print '[!] Your structure/field does not exist ?'
			return 0
	return 1
		
if __name__ == '__main__':
	sys.exit(main())