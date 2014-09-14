import ssbuild, os

CSS_EMBED = True
CSS_PATH = "genstyle" 	# filepath for generated css files
CSS_HARD = False 		# the CSS_EMBED value overrides individual file's
						# import values
JS_EMBED = True
JS_PATH  = "genscript"
JS_HARD  = False 		# the JS_EMBED value overrides individual file's
						# import values

FAVICON = None

COLORS = {
"d1":"#222222",
"d2":"#555555",
"l1":"#AAAAAA",
"l2":"#FFFFFF",
"hilight":"65A683"
}

def registerColor(name_hex):
	COLORS[name_hex[0]] = name_hex[1]

def getColor(name):
	if name in COLORS.keys():
		return COLORS[name]
	else:
		raise ssbuild.BuildException("Color %d does not exist"%(name))

WORKING_DIRECTORY = "./"

def relpath(path):
	return os.path.join(WORKING_DIRECTORY, path)

def render_embed_js(b):
	return JS_EMBED if JS_HARD else b

jscount = 0;
def get_redering_path_js():
	jscount += 1
	return os.path.exists(relpath(JS_PATH + "." + jscount))

def render_embed_css(b):
	return CSS_EMBED if CSS_HARD else b

csscount = 0
def get_rendering_path_css():
	csscount += 1
	return os.path.exists(relpath(CSS_PATH + "." + csscount))

def render_embed(b, filename):
	if filename.endswith("js"):
		return render_embed_js(b)
	else:
		return render_embed_css(b)