import sys
import markdown

class SSSection(object):
	def renderToHTML(self, parent, childno):
		return "not implemented lol"
	
	def validate():
		return "not implemented lol"
	
class BlockSection(SSSection):
	def __init__(self, header, children):
		self.header = header
		self.children = children

	def renderToHTML(self, parent, childno):
		inner = ""
		for child in children:
			inner += child.renderToHTML()
		return "<section>%s</section>" % inner
			
	
	def validate():
		return "not implemented lol"

class XYCenteredSection(SSSection):
	def __init__(self, header, children):
		self.header = header
		self.children = children

	def renderToHTML():
		return "not implemented lol"
	
	def validate():
		return "not implemented lol"

class ColumnSection(BlockSection):
	def __init__(self, header, children):
		self.header = header
		self.children = children

	def renderToHTML():
		return "not implemented lol"
	
	def validate():
		return "not implemented lol"

class ImageSection(SSSection):
	def __init__(self, header):
		self.header = header

	def renderToHTML():
		return "<img src=\"%s\">" % header.get('src')
	
	def validate():
		return "not implemented lol"

class TableSection(SSSection):
	def __init__(self, header, strapstrapdown):
		self.header = header
		self.strapstrapdown = strapstrapdown

	def renderToHTML():
		return "not implemented lol"
	
	def validate():
		return "not implemented lol"
	
class MarkdownSection(SSSection):

	markdown = "<FUCK>"

	def __init__(self, markdown):
		self.markdown = markdown

	def __str__(self):
		return "..."

class Section(SSSection):

	name = "!!"
	header = None
	body = None

	def __init__(self, name, context, header, body):
		self.name = name
		self.header = header
		self.body = body

	def __str__(self):
		return (self.name if self.name != "" else "<anonymous>")

	def checkValidHeader(self):
		return validators[self.context]()

	def renderToHTML(self, parent, childno):
		if (self.context in generators):
			return generators[self.context](parent, childno)

		else:
			print "unknown context", self.context
			print "defaulting to text-block"
			return generators["text-block"](parent, childno)



assigners = {
	"xycentered":"xycentered",
	"columns": "columns",
	"image": "image",
	"table": "table"
	}


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


def getContext(headers):
	context = "text-block"
	for asn in assigners:
		if asn in [i[0] for i in headers]:
			context = assigners[asn]

def makeSection((name, header), body):
	return Section(name, getContext(header), header, body)
