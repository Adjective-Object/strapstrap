import traceback, sys
from sssections import *
from parsing import *

def buildHTML(includes, styleblocks, docblock):

	return (
		"""<!DOCTYPE html>
		<html>
			<head>
			<meta name="viewport" content="width=device-width" />

			"""
			+ include_head + 	# generated css files placed in standalone files
								# and :::included css files

			+ embed_head + 		#generated css files embeded into the head
								# and :::included css files 
								# with the :embed property set
			"""
			</head>
			<body>
			"""
			+ include_top 		# nothing for now
			+ body				# body of text
			+ include_bottom 	# included js files,
			+ embed_bottom 		# included js files,
			+ """
			</body>
			"""
			+ include_tail +	# nothing for now
			"""
		</html>""")
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		printhelptext()
	else:
		try:
			print "opening " + sys.argv[1]
			include, styles, docblock = parseRootBlocks(open(sys.argv[1], "r"))
			buildHTML(include, styles, docblock)
		except Exception as e:
			if (isinstance(e, SSFormatException)):
				print "Parsing Error:" + str(e)
			else:
				print traceback.print_exc()