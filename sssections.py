import sys
import markdown
from pprint import pprint
from cssMap import *

class SSSection(object):
	css = dict()

	def renderToHTML(self, parent, childno):
		return "not implemented lol"
	
	def validate():
		return True

	def hasHeader(self, name):
		return any([name == i[0] for i in self.header])

	def getHeader(self, name):
		return self.getHeaders(name)[0]

	def getHeaders(self, name):
		return [i[1] for i in self.header if (i[0] == name)]

	def renderToHTML(self, parent, childno, indent=0):
		ind = "\t" * indent
		inner = ""
		for childno in range(len(self.children)):
			inner += self.children[childno].renderToHTML(parent, childno, indent+1)
		return "%s<section %s>\n%s\n%s</section>\n" % (ind, genName(self), inner, ind)

	def bldcss(self):
		self.css=dict()
		for attr in self.header:
			if attr[0] in cssMap.keys():
				cssMap[attr[0]](self, attr[1])
		return self.css

	def buildCSS(self):
		self.bldcss()

		return ([self.css] if self.css != "" else []) + [c.buildCSS() for c in self.children]

anoncount = 0

def genName(bod):
	name = bod.name
	if name == "":
		if bod.css != None:
			name = "anon-%s"%(anoncount)
		else:
			return ""

	a = []
	for i in name.split(" "):
		if i.startswith("."):
			a.append( "class=\"%s\""%(i[1:]) )
		else:
			a.append( "id=\"%s\""%(i) )
	return " ".join(a)

class BlockSection(SSSection):
	css = None

	def __init__(self, name, header, children):
		self.name = name
		self.header = header
		self.children = children

	def validate():
		return True



class XYCenteredSection(SSSection):
	def __init__(self, name, header, children):
		self.name = name
		self.header = header
		self.children = children
	
	def validate():
		return True
	
	def renderToHTML(self, parent, childno, indent=0):
		ind = "\t" * indent
		inner = ""
		for childno in range(len(self.children)):
			inner += self.children[childno].renderToHTML(parent, childno, indent+1)
		return "%s<section %s><section class=\"xycenteredinner\">\n%s\n%s</section></section>\n" % (ind, genName(self), inner, ind)


class ColumnSection(BlockSection):
	def __init__(self, name, header, children, indent=0):
		self.name = name
		self.header = header
		self.children = children
	
	def validate():
		return True

class ImageSection(SSSection):
	def __init__(self, name, header):
		self.name = name
		self.header = header
		if not self.hasHeader("alt"):
			self.header.append(["alt", self.getHeader("image")])

	def renderToHTML(self, parent, childno, indent=0):
		return "\t"*indent + "<img src=\"%s\" alt=\"%s\">"%(
			self.getHeader("image"), 
			self.getHeader("alt"))
	
	def validate():
		return True

	def buildCSS(self):
		c = self.bldcss()
		return [c if c != "" else []]

class TableSection(SSSection):
	def __init__(self, name, header, strapstrapdown):
		self.name = name
		self.header = header
		self.strapstrapdown = strapstrapdown

	def renderToHTML(self, parent, childno, indent=0):
		return "not implemented lol"
	
	def validate():
		return True
	
class MarkdownSection(SSSection):

	text = "<FUCK>"

	def __init__(self, text):
		ident = False
		t = []
		for c in text.split("\n"):
			if c.startswith("```"):
				ident = not ident
			else:
				if ident:
					t.append ("\t" + c)
				else:
					t.append (c)
		t = "\n".join(t)
		print t
		self.text = t

	def renderToHTML(self, parent, childno, indent=0):
		#print self.text
		return markdown.markdown(self.text).replace(
			">", ">\n").replace("<", "\n<").replace(
			"\n", "\n"+"\t" * indent)[0:-indent]

	def buildCSS(self):
		return []


def validateTextBlock ():
	return True

def validateXYCentered ():
	return True

def validateColumnedLayout ():
	return True

def validateImage ():
	return True

def validateTable ():
	return True


validators = {
	"text-block": validateTextBlock,
	"xycentered": validateXYCentered,
	"columns": validateColumnedLayout,
	"image": validateImage,
	"table": validateTable
}


def makeTextBlock(node, parent, childno):
	pass

def makeXYCentered(node, parent, childno):
	pass

def makeColumnedLayout(node, parent, childno):
	pass

def makeImage(node, parent, childno):
	pass

def makeTable(node, parent, childno):
	pass


generators = {
	"text-block": makeTextBlock,
	"xycentered": makeXYCentered,
	"columns": makeColumnedLayout,
	"image": makeImage,
	"table": makeTable
	}

contexts = [	
	"text-block",
	"xycentered",
	"columns",
	"image",
	"table"
]

assigners = {
	"xycentered":"xycentered",
	"columns": "columns",
	"image": "image",
	"table": "table"
}

def getContext(headers):
	context = "text-block"
	for asn in assigners:
		if asn in [i[0] for i in headers]:
			context = assigners[asn]
	print ">", context
	return context

def makeSection((name, header), body):
	context = getContext(header)

	if (context == "text-block"):
		return BlockSection(name, header, body)
	elif (context == "xycentered"):
		return XYCenteredSection(name, header, body)
	elif (context == "columns"):
		return ColumnSection(name, header, body)
	elif (context == "image"):
		return ImageSection(name, header)
	elif (context == "table"):
		return TableSection(name, header)
	else:
		raise Exception("FUCK %s"%( context ) )