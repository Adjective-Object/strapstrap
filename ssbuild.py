from sssections import *
from parsing import *
import subprocess, config

supportedExt = {
	"javascript": {
		"ext":["js"],
		"position": "bottom", #bottom. top. head, tail
		"superembedder":(lambda fname: 
			"<script type=\"text/javascript\">\n%s\n\t</script>"%
			(ssbuild.readFile(fname,1) )
			),
		"embedder": (lambda filename: 
			"<script type=\"text/javascript\" src=\"%s\"></script>"%
			(filename))

		},
	"css": {
		"ext":["css"],
		"position": "head",
		"superembedder":(lambda fname: 
			"\t<style type=\"text/css\">\n%s\n\t</style>"%
			(readFile(fname, 2))
			),
		"embedder": (lambda filename: 
			"\t<link href=\"%s\" rel='stylesheet' type='text/css' />"%
			(filename))
		},
	"sass": {
		"ext":["scss", "sass"],
		"position": "head",
		"superembedder":(lambda fname: 
			"\t<style type=\"text/css\">\n%s\n\t\t</style>"%
			( ssbuild.readFile(ssbuild.compileSassFile(fname), 2))
			),
		"embedder": (lambda filename: 
			"\t<link href=\"%s\" rel='stylesheet' type='text/css' />"%
			( ssbuild.compileSassFile(filename)) )
		},
}

class BuildException(Exception):
	def __init__(self, str):
		Exception.__init__(self,str)

def compileSassToFile(name, sass):
	print "compiling sass to file %s.css"%(name)
	f = open(name+".css", "w")
	f.write( compileSass(sass) );
	f.close()
	return name+".css"

def compileSassFile(filename):
	print "compiling %s"%(filename)
	s = subprocess.Popen(["sass", filename], 
		stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 	output = s.communicate()[1]

 	if "error" in output:
 		raise BuildException(output);
 	
	return ".".join(filename.split(".")[:-1])+".css"

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

def buildBody(docblock):
	return ""

def inc(includes, pos):
	return "\t"+"\n\t".join([include["exec"](include["filename"]) 
		for include in includes if 
		(not include["embed"] and include["pos"] == pos) ])

def bld(includes, pos):
	return "\t"+"\n\t\n\t".join([include["execinto"](include["filename"]) 
		for include in includes if 
		(not include["embed"] and include["pos"] == pos) ])

def registerGlobals(docblock):

	if docblock.hasAttr("icon"):
		config.FAVICON = docblock.getAttr("icon")

	for i in docblock.getAttrs("color"):
		s = i[1].split(" ")
		config.registerColors(s[0], s[1])

def buildHTML(includes, styleblocks, docblock):

	registerGlobals(docblock)

	include_head = bld(includes, "head")
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
	
