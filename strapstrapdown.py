import traceback, sys
from build import *
from parsing import *


def printhelptext():
	print "StrapStrapDown parse"
	print "usage:"
	print "\tssdown <input file> <output file>"


if __name__ == "__main__":
	if len(sys.argv) != 3:
		printhelptext()
	else:
		try:
			print "opening " + sys.argv[1]
			include, styles, docblock = parseRootBlocks(open(sys.argv[1], "r"))
			
			print

			f = open(sys.argv[2], "w")
			f.write(buildHTML(include, styles, docblock))
			f.close()

		except Exception as e:
			if (isinstance(e, SSFormatException)):
				print "Parsing Error:" + str(e)
			
			elif (isinstance(e, BuildException)):
				print str(e)
			
			else:
				print traceback.print_exc()