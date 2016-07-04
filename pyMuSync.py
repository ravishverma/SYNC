import os
import re
import sys
import getpass
import pwd

"""
Uses rsync to syncronize the Music files
in Hard Disk and MTP connected Android device
"""

device = sys.argv[1]
os.system("lsusb | grep %s >> temp.txt" % (device))
f = open("temp.txt",'rU')

username = getpass.getuser()
userid = pwd.getpwnam(username).pw_uid

mtpformat = re.compile(r'Bus[ \t]+([0-9]+)[ \t]+Device[ \t]+([0-9]+):[ \t]+ID[ \t]+[0-9a-z:]+[ \t]+([A-Za-z0-9. \t]+)',re.I)

data = f.read()
datalines = data.splitlines()
f.close()
os.system('rm temp.txt -f')

sc = '"/home/%s/Music/"' % (username)

if sys.argv[1]!='hd':
	for dataline in datalines:
		result = mtpformat.search(dataline)

		dest_base = '/run/user/%d/gvfs' % (userid)
		dest_dirs = os.listdir(dest_base)
		dest_id = '%%5Busb%%3A%s%%2C%s%%5D' % (result.group(1),result.group(2))
		dest_id_len = len(dest_id)

		for file_name in dest_dirs:
			if file_name[-dest_id_len:]==dest_id:
				xt = '"%s/%s/Internal storage/Music"' % (dest_base,file_name)
	hd = ''
elif sys.argv[1]=='hd':
	hd = '"/media/%s/My Passport/DC++/Music/"' % (username)
	xt = ''
	device = ''

print '----------------------------'
print ': Music Syncronization'
print ': Device      : ', device
print '----------------------------'
print ': Source      : ', sc
print ': Destination : ', hd, xt, '\n'

if len(sys.argv)!=3 or sys.argv[2]=='dry':
	if sys.argv[1]=='hd':
		os.system('rsync --ignore-existing -rhnvP %s %s' % (sc,hd))
	if sys.argv[1]!='hd':
		os.system('rsync --ignore-existing -rhnvP %s %s' % (sc,xt))
elif sys.argv[2]=='com':
	if sys.argv[1]=='hd':
		os.system('rsync --ignore-existing -rhvP %s %s' % (sc,hd))
	if sys.argv[1]!='hd':
		os.system('rsync --ignore-existing -rhvP %s %s' % (sc,xt))
