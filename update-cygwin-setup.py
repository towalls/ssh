# Released under the GNU General Public License version 3 by J2897.
import os
title = 'Cygwin Setup Updater'
os.system('title ' + title)
drive_letter = os.getenv('SYSTEMDRIVE')
tmp = os.getenv('TEMP')
userprofile = os.getenv('USERPROFILE')
pickle_cache = userprofile + '\\Cygwin.dat'
cygstore = drive_letter + '\\cygstore'
def stop():
	import sys
	sys.exit()
target = 'most recent version'
url = 'https://www.cygwin.com'
print 'Main target:			' + target
print 'URL:				' + url

# Get the web-page.
def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()
try:
	page = get_page(url)
except:
	print 'Could not download the page. You may not be connected to the internet.'
	stop()

# Get the current version information from the web-page.
def find_site_ver(page):
	A1 = page.find(target)
	if A1 == -1:
		return None, None, None
	A2 = page.find('>', A1+len(target))
	A3 = page.find('<', A2)
	site_ver = page[A2+1:A3]
	second_target = 'href="'
	B1 = page.find(second_target, A2) + len(second_target)
	B2 = page.find('"', B1)
	filename_32 = page[B1:B2]
	third_target = 'href="'
	C1 = page.find(third_target, B2) + len(third_target)
	C2 = page.find('"', C1)
	filename_64 = page[C1:C2]
	return filename_32, filename_64, site_ver # setup-x86.exe setup-x86_64.exe 2.3.0
try:
	site_filename_32, site_filename_64, site_ver = find_site_ver(page)
except:
	print 'Could not search the page.'
	stop()
if site_filename_32 == None:
	print 'The search target has not been found on the page. The formatting, or the text on the page, may have been changed.'
	stop()

# Detect the OS architecture.
def get_os_architecture():
	PA, PAW6432 = os.getenv('PROCESSOR_ARCHITECTURE'), os.getenv('PROCESSOR_ARCHITEW6432')
	if (PA == 'x86' and PAW6432 == None):
		return '32-Bit'
	else:
		return '64-Bit'
bit = get_os_architecture()

# Select the appropriate setup file.
if bit == '64-Bit':
	site_filename = site_filename_64
else:
	site_filename = site_filename_32
print 'Found ' + bit + ' setup file:	' + site_filename
print 'Site version:			' + site_ver

# Is the cache file in the user's profile folder?
import cPickle
if not os.path.isdir(cygstore):
	print 'Creating folder:			' + cygstore
	os.makedirs(cygstore)
elif os.path.isfile(pickle_cache):

	# Get the version information from the cache file (e.g. '2.2.0').
	def load_pickle_file():
		with open(pickle_cache, 'rb') as pickle_file:
			return cPickle.load(pickle_file)
	try:
		local_ver = load_pickle_file()
		print 'Local version:			' + local_ver
	except:
		print 'Could not load cache.'
		stop()

	# Is the local version the same as the site version?
	if local_ver == site_ver:
		print 'Match!'
		stop()

# Download the setup file.
try:
	import urllib
	urllib.urlretrieve(url + '/' + site_filename, tmp + '\\' + site_filename)
	if os.path.isfile(cygstore + '\\' + site_filename):
		os.remove(cygstore + '\\' + site_filename)
	os.rename(tmp + '\\' + site_filename, cygstore + '\\' + site_filename)
except:
	print 'Could not download the file.'
	stop()
else:
	print 'Downloaded.'
	
# Dump the site version information into the cache file.
def dump_pickle_file(cache_file, version):
	with open(cache_file, 'wb') as pickle_file:
		cPickle.dump(version, pickle_file)
try:
	dump_pickle_file(pickle_cache, site_ver)
except:
	print 'Could not dump the site version information to: ' + pickle_cache
	stop()
else:
	print 'Dumped cache:		' + pickle_cache
