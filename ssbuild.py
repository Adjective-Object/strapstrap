from sssections import *
from parsing import *
from pprint import pprint
import subprocess, config
import sass, re

supportedExt = {
	"javascript": {
		"ext":["js"],
		"position": "bottom", #bottom. top. head, tail
		"superembedder":(lambda content: 
			"<script type=\"text/javascript\">\n%s\n\t</script>"%
			(content )
			),
		"fname -> content": (lambda fname: ssbuild.readFile(fname,1)),
		"embedder": (lambda filename: 
			"<script type=\"text/javascript\" src=\"%s\"></script>"%
			(filename))

		},
	"css": {
		"ext":["css"],
		"position": "head",
		"superembedder":(lambda content: 
			"\t<style type=\"text/css\">\n%s\n\t</style>"%
			(content)
			),
		"fname -> content": (lambda fname: readFile(fname, 2)),
		"embedder": (lambda filename: 
			"\t<link href=\"%s\" rel='stylesheet' type='text/css' />"%
			(filename))
		},
	"sass": {
		"ext":["scss", "sass"],
		"position": "head",
		"superembedder":(lambda content: 
			"\t<style type=\"text/css\">\n%s\n\t\t</style>"%
			( content )
			),
		"fname -> content": (lambda fname: ssbuild.compileSassFile(fname) ),
		"embedder": (lambda filename: 
			"\t<link href=\"%s\" rel='stylesheet' type='text/css' />"%
			( ssbuild.compileSassToFile(filename, 
				re.sub(filename ("(\\.scss|\\.sass)", "\\.css") )) ))
		},
}

class BuildException(Exception):
	def __init__(self, str):
		Exception.__init__(self,str)

def compileSass(sassstr):
	return sass.compile_string(sassstr)

def compileSassFile(filename):
	return compileSass(readFile(filename, 0))

def compileSassToFile(filename, outfil):
	f = open(outfil)
	f.write(compileSassFile(filename))
	f.close()


def readFile(filename, indent):
	filename = config.relpath(filename)
	print "reading " + filename
	try:

		f = open(filename)
		a = ("\t" * indent) + ("\t" * indent).join(f.readlines())
		f.close()
		return a

	except Exception as e:
 		raise BuildException("Build Error: could not read %s"%
 			(filename));

def buildCSS(docblock):
	c = []
	for i in docblock.body:
		c.append(i.buildCSS())
	return c

def fetchCSS(lst):
	css = dict()
	for i in lst:
		if hasattr(i, "name") and not i.name in css.keys():
			css[i.name] = i.css

		if (hasattr(i, "children")):
			css = merge(css, fetchCSS(i.children) )
	return css

def buildBody(docblock):
	b = docblock.body
	

	return "\n".join(
		[b[i].renderToHTML(None, i) for i in range(len(b))]);

def inc(includes, pos):
	return "\t"+"\n\t".join(
		[include["exec"](include["filename"]) 
		for include in includes if 
		(not config.render_embed(include["embed"], include["filename"]) and include["pos"] == pos) ])

def bld(includes, pos):
	return "\t"+"\n\t\n\t".join(
		[include["execinto"]( include["decode"] (include["filename"])) 
		for include in includes if 
		(config.render_embed(include["embed"], include["filename"]) and include["pos"] == pos) ])

def dokblok(b, docblock, attr):
	n = docblock.getAttr(attr)
	if isinstance(n, list):
		for e in range(len(n)):
			#print n[e], "hard", n[e]=="hard", n[e-1]
			if n[e] == "css":
				config.CSS_EMBED = b
			elif n[e] == "js":
				config.JS_EMBED = b
			elif n[e] == "hard":
				if e-1 >= 0:
					if n[e-1] == "css":
						config.CSS_HARD = True
					elif n[e-1] == "js":
						config.JS_HARD = True

	elif(n == "css"):
		config.CSS_EMBED = b
	elif(n == "js"):
		config.JS_EMBED = b

def registerGlobals(docblock):

	#pprint(docblock.headers)


	if docblock.hasAttr("noembed"):
		dokblok(False, docblock, "noembed")

	if docblock.hasAttr("embed"):
		dokblok(True, docblock, "embed")

	if docblock.hasAttr("icon"):
		config.FAVICON = docblock.getAttr("icon")

	if docblock.hasAttr("js-path"):
		config.JS_PATH = docblock.getAttr("js-path")

	if docblock.hasAttr("css-path"):
		config.CSS_PATH = docblock.getAttr("css-path")

	for i in docblock.getAttrs("color"):
		config.registerColor(i)
	"""
	print "js"

	print "embed", config.JS_EMBED
	print "hard ", config.JS_HARD

	print "css"

	print "embed", config.CSS_EMBED
	print "hard ", config.CSS_HARD
	"""

def buildFromBlocks(styleblocks):
	contents = []
	for block in styleblocks:
		if isinstance(block, CssBlock):
			contents.append(block.css)
		elif isinstance(block, SassBlock):
			contents.append(compileSass(block.sass))
		else:
			contents.append("FUCK { }")
	return contents

def buildHTML(includes, styleblocks, docblock):

	css = buildCSS(docblock)
	heads = fetchCSS(docblock.body)
	pprint(heads)

	registerGlobals(docblock)
	fromblocks = ("\n".join(
				[supportedExt["css"]["superembedder"](a).replace("\n","\n\t\t")
				for a in buildFromBlocks(styleblocks)]))

	fromblocks= fromblocks.replace(
		"\t</style>","</style>").replace(
		"</style>\n\t<style", "</style>\n\t\t<style")

	include_head = (bld(includes, "head") + fromblocks)
	embed_head = inc(includes, "head")
	include_bottom = bld(includes, "bottom")
	embed_bottom = inc(includes, "bottom")

	body = buildBody(docblock)

	return (
		"<!DOCTYPE html>\n"
		"<html>\n"
		"	<head>\n" +
		("		<link rel='icon' type='image/png' href='%s'>\n"%
			(config.FAVICON) if config.FAVICON else "") +
		"		<meta name=\"viewport\" content=\"width=device-width\" />\n" +
			include_head + 		# generated css files placed in standalone files
								# and :::included css files
		"	\n" +
			embed_head + 		#generated css files embeded into the head
								# and :::included css files 
								# with the :embed property set
		"	\n" +
		"	</head>\n" +
		"	<body>\n" +
			body +				# body of text
		"	\n" +
			include_bottom + 	# included js files,
		"	\n 	\n" +
			embed_bottom +		# embeded js files,
		"	\n" +
		"	</body>\n" +
		"</html>\n")
	
