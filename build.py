from sssections import *
from parsing import *
import subprocess

class BuildException(Exception):
	def __init__(self, str):
		Exception.__init__(self,str)

def compileSass(sass):
	s = subprocess.Popen(["sass", "-s"])
	print s.communicate(sass)
	return "TODO SASS COMPILATION"

def compileSassToFile(name, sass):
	f = open(name+".css", "w")
	f.write( compileSass(sass) );
	f.close()
	return name+".css"

def compileSassFile(filename):
	s = subprocess.Popen(["sass", filename], 
		stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 	output = s.communicate()[1]

 	if "error" in output:
 		raise BuildException(output);
 	
	return ".".join(filename.split(".")[:-1])+".css"

def buildBody(docblock):
	return ""

def inc(includes, pos):
	return "\t"+"\n\t".join([include["exec"](include["filename"]) 
		for include in includes if 
		(not include["embed"] and include["pos"] == pos) ])

def buildHTML(includes, styleblocks, docblock):

	include_head = inc(includes, "head")
	embed_head = ""
	include_bottom = inc(includes, "bottom")
	embed_bottom = ""
	body = buildBody(docblock)

	return (
		"<!DOCTYPE html>\n"
		"<html>\n"
		"	<head>\n"
		"	<meta name=\"viewport\" content=\"width=device-width\" />\n" +
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
		"	\n" +
			embed_bottom +		# embeded js files,
		"	\n" +
		"	</body>\n" +
		"</html>\n")
	
