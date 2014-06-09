import os
import struct
import sys

PYTHON_BITS = 8 * struct.calcsize("P")
SCRIPT_PATH = os.path.dirname(sys.argv[0])

class Package(object):
	def __init__(self, name):
		self.name = name
		self.installer = {
			32: name + ".win32-py2.7.exe",
			64: name + ".win-amd64-py2.7.exe",
		}

	def install(self):
		os.system(os.path.join(SCRIPT_PATH, self.installer[PYTHON_BITS]))


# Installers from http://www.lfd.uci.edu/~gohlke/pythonlibs/#distribute
PACKAGES = [
	Package("distribute-0.6.38"),
	Package("pip-1.3.1"),
]

def main():
	print "Installing %s bit packages." % PYTHON_BITS

	for package in PACKAGES:
		print "Installing %s." % package.name
		package.install()

if __name__ == "__main__":
	main()