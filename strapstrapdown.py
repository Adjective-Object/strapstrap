import traceback, sys, os
import ssbuild, config
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
			config.WORKING_DIRECTORY = os.path.dirname(sys.argv[1])

			print "working directory is " + config.WORKING_DIRECTORY
			include, styles, docblock = parseRootBlocks(open(sys.argv[1], "r"))
			
			print

			f = open(sys.argv[2], "w")
			f.write(ssbuild.buildHTML(include, styles, docblock))
			f.close()

		except Exception as e:
			if (isinstance(e, SSFormatException)):
				print "Parsing Error:" + str(e)
			
			elif (isinstance(e, ssbuild.BuildException)):
				print str(e)
			
			else:
				print traceback.print_exc()