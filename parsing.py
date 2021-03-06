from sssections import *
import ssbuild

# Helpers
tab = "\t"

#no newline
def peekline(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    if(line == ""):
    	return None
    return line[:-1]

#no newline
def readline(f):
	return f.readline().replace("\n","")

def firstline(s):
	return s.split("\n",1)[0]

def popfirstword(s):
	a = s.split(" ", 1)
	if (len(a) == 1):
		return (a[0], "")

	if (s[0] == ":"):
		c = 0
		for x in s:
			if x == ":":
				c += 1
			else:
				break
		return ":" * c, s.replace(":","").strip()

	return (a[0], a[1])

def poptabs(s):
	count = 0
	while s[0:len(tab)] == tab:
		s = s[len(tab):]
		count += 1
	return count, s

def curline(f):
	s = f.tell()
	f.seek(0)
	count = 0
	return 	f.read(s).count('\n')

def sameblock(f):
	return (
		peekline(f) != None and
		(
			len(peekline(f)) < 3 or 
			peekline(f) [0:3] != ":::")
	)

class SSFormatException(Exception):
	def __init__(self, s):
		Exception.__init__(self,s)

class SSDoc(object):

	filename = ""
	headers = []
	body = []

	def __init__(doc, name, headers):
		doc.filename = name
		doc.headers = headers

	def hasAttr(doc, name):
		return any([name == i[0] for i in doc.headers])

	def getAttr(doc, name):
		return doc.getAttrs(name)[0]

	def getAttrs(doc, name):
		return [i[1] for i in doc.headers if (i[0] == name)]


class CssBlock(object):

	css = ""
	filename = "undefined.css"
	
	def __init__(block, name, css):
		block.filename = name + ".css"
		block.css = css

class SassBlock(object):

	sass = ""
	filename = "undefined.css"
	
	def __init__(block, name, sass):
		block.filename = name + ".css"
		block.sass = sass

def parseBlockHeader(f):
	attrs = []
	#print "\tbeginning with '%s'"%(peekline(f))

	if peekline(f)!= None and peekline(f)[0:2] == ": ":
		print "\theader line", curline(f)

	while peekline(f)!= None and peekline(f)[0:2] == ": ":
		line = readline(f)
		line = popfirstword(line)[1]
		name, content = popfirstword(line)
		spl = content.split(" ")
		attrs.append( [name , (spl if (len(spl) != 1) else spl[0]) ] )

	print

	return attrs

def parseSectionHeader(rootindent, f):
	attrs = []

	secname = popfirstword(poptabs(readline(f))[1])[1]

	"""
	print "\t"*rootindent + (
		"parsing section header %s (line %s)"%(
			(secname if secname != "" else "<anonymous>"),
			curline(f)
		))
	"""
	while poptabs(peekline(f))[1][0:2] == ": ":
		line = poptabs(readline(f))[1][2:]
		name, content = popfirstword(line)

		cs = content.split(" ")
		if len(cs) == 1:
			cs = cs[0]

		attrs.append( [name , cs] )

	"""
	for i in attrs:
		print rootindent * "\t" + str(i)
	"""
	return secname, attrs

def parseSectionBody(rootindent, f):
	def endbody():
		body.append(MarkdownSection("\n".join(mkdwnlines)))
		#for i in body:
		#	print rootindent * "\t" + i.__class__.__name__
		return body

	body = [] #TODO
	
	#print "\t"*rootindent + "parsing section body (line %s)"%(curline(f))
	
	mkdwnlines = []

	pre = False;

	while (peekline(f) != None and 
			not peekline(f).startswith(":::")):

		indent, line = poptabs(peekline(f))
		if line.startswith ("```"):
			pre = not pre

		if (line != "" and indent < rootindent and not pre):
			#indent decrease
			#print "<", rootindent, indent, "\"%s\""%line
			return endbody()
		
		elif line.startswith("::") and not pre:
			#print rootindent, indent;
			if(len(mkdwnlines) > 0):
				body.append(MarkdownSection("\n".join(mkdwnlines)))
				mkdwnlines = []
			
			body.append(makeSection(
				parseSectionHeader(rootindent, f),
				parseSectionBody(indent+1, f)
			))

		else:
			mkdwnlines.append("\t" * (indent - rootindent -1) + line)
			#it's markdown
			#print rootindent * "\t" + "M>", mkdwnlines[-1]
			f.readline()

	#EOF, return body
	return endbody()

def parseDocumentBlock(filename, f):
	document = SSDoc(filename, parseBlockHeader(f))

	print "\tdocument body line %s"%(curline(f))
	#print "\tbeginning with '%s'"%(peekline(f))

	document.body = []
	while sameblock(f):
		document.body += parseSectionBody(0, f)
		#print peekline(f)
	return document, f

def parseCssBlock(name, f, sass=False):
	header = parseBlockHeader(f)
	lines = []

	while (sameblock(f)):
		lines.append(f.readline());

	if sass:
		return CssBlock(name, "".join(lines)), f
	else:
		return SassBlock(name, "".join(lines)), f


def parseIncludeBlock(f):
	header = parseBlockHeader(f)
	
	embed = any(["embed" == h[0] for h in header])
	embed = any(["noembed" == h[0] for h in header])
	if not embed:
		embed = None;


	files = []

	while (sameblock(f)):
		filename = readline(f);
		name = filename.strip()
		if name != "":

			badformat = SSFormatException((
						"Error in include block, (line %s)\n"
						+ "improperly formatted include. '%s'\n"
						+ "proper format is <filename> <filetype> or "
						+ "<filename>.<extension>") %(curline(f), name))

			if (len(name.split(" ")) == 2):
				#filename <formatname>
				if all(
					[name[1] not in ssbuild.supportedExt[ext] 
						for x in ssbuild.supportedExt.keys()]):
					raise SSFormatException(
						("Error in include block, (line %s)\n"
						+ "file %s of unsupported type.") %(curline(f), ext))
				files.append(name)

			elif (len(name.split(" ")) == 1):
				#filename.extension

				ext = name.split(".")
				ext = ext[-1]

				matches = [
					sup for sup in ssbuild.supportedExt.keys()
					 if (ext in ssbuild.supportedExt[sup]["ext"])
				]
				if len(matches) == 0:
					raise SSFormatException(
						("Error in include block, (line %s)\n"
						+ "filetype %s of unsupported type.") %(curline(f), ext))

				files.append({
					"embed":embed, 
					"filename":filename,
					"pos":ssbuild.supportedExt[matches[0]] ["position"],
					"decode":ssbuild.supportedExt[matches[0]]["fname -> content"],
					"execinto":ssbuild.supportedExt[matches[0]] ["superembedder"],
					"exec":ssbuild.supportedExt[matches[0]] ["embedder"]})
			else:
				raise badformat

	return files, f


def parseRootBlocks(f):
	include = []
	styles = []
	docblock = None

	while (peekline(f) != None):

		line = readline(f)
		start, line = popfirstword(line)
		while line == "":
			line = readline(f)
			start, line = popfirstword(line)


		if not start == ":::":
			raise SSFormatException(("(line %s) metadata block must begin with" 
				+ "':::' \n Instead, starts with '%s'")%(curline(f), line))

		blocktype, line = popfirstword(line)

		if (blocktype == "document"):
			if(docblock != None):
				raise SSFormatException("Only one document block permitted")
			print "parsing document block line %s"%(curline(f) -1)
			docblock, f = parseDocumentBlock(line, f)
		elif (blocktype == "css"):
			print "parsing css block line %s"%(curline(f) -1)
			block, f = parseCssBlock(line, f)
			styles.append(block)
		elif (blocktype == "sass"):
			print "parsing sass block line %s"%(curline(f) -1)
			block, f = parseCssBlock(line, f, sass=True)
			styles.append(block)
		elif (blocktype == "include"):
			print "parsing include block %s"%(curline(f) -1)
			inc, f = parseIncludeBlock(f)
			include += inc
		else:
			raise SSFormatException("(line %s) %s not a valid document block"%
				(curline(f),blocktype))

		if (not docblock):
			raise SSFormatException("no document block declared")


	return include, styles, docblock