import sys

class SSSection(object):
	def renderToHTML():
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

		self.context = getContext(header)

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


def makeTextBlock(parent, childno):
	pass

def makeXYCentered(parent, childno):
	pass

def makeColumnedLayout(parent, childno):
	pass

def makeImage(parent, childno):
	pass

def makeTable(parent, childno):
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