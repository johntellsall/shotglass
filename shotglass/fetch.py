#!/usr/bin/env python

'''
fetch.py -- check out interesting projects
'''

from __future__ import print_function
import os
import subprocess
import sys

# URLS = [
# 	'https://github.com/django/django',
# 	'https://github.com/pallets/flask.git',
# 	'https://github.com/odoo/odoo.git',
# 	'https://github.com/Pylons/pyramid.git',
# 	'https://github.com/zzzeek/sqlalchemy'
# ]

def get_name(url):
	name = os.path.split(url)[-1]
	if name.endswith('.git'):
		name = name.split('.git')[0]
	return name

def clone(url):
	name = get_name(url)
	print(name)
	cmd = 'git clone --depth=1'.split()
	cmd += [url]
	print('>>> {}'.format(' '.join(cmd)))
	subprocess.check_call(cmd)

def main():
	os.chdir('../SOURCE')
	for url in sys.argv[1:]:
		name = get_name(url)
		print('{}: '.format(name), end='')
		if os.path.exists(name):
			print('(exists, skipping)')
			continue
		print('downloading')
		clone(url)
		print('done')

if __name__ == '__main__':
	main()


