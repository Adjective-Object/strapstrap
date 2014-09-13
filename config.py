from ssbuild import BuildException

CSS_PATH = "embed.css" 	# filepath for generated css files
CSS_HARD = False 		# the CSS_EMBED value overrides individual file's
						# import values

JS_PATH  = "embed.js"
JS_HARD  = False 		# the JS_EMBED value overrides individual file's
						# import values

FAVICON = None

COLORS = {}

def registerColor(namespacehex):
	name, hexx = namespacehex.split(" ")
	COLORS[name] = hexx

def getColor(name):
	if name in COLORS.keys():
		return COLORS[name]
	else:
		raise BuildException("Color %d does not exist"%(name))

