import config

def merge(*a):
	return dict( reduce ((lambda a, b: a+b), [n.items() for n in a]) )

reset = {
	"box-sizing": "border-box",
	"-moz-box-sizing": "border-box",
	"padding": "0px",
	"margin": "0px"
}

background_fill = {
"-webkit-background-size": "cover",
"-moz-background-size": "cover",
"-o-background-size": "cover",
"background-size": "cover"
}

def dorgba(color, frac):
	return "rgba(%s, %s, %s, %s)"%(
		int("0x"+color[1:3], 16),
		int("0x"+color[3:5], 16),
		int("0x"+color[5:7], 16),
		frac)

def fullfold(sec, args):
	sec.css = merge(sec.css, {
	"width:": "100%",
	"height:": " 100%",
	"min-height": "%spx"%(config.WIDTH_SMALL)})

def genbgstatement(sec):
	return ((dorgba(config.getColor(
						sec.bgcolor[0]), 
						sec.bgcolor[1])+" " if hasattr(sec, "bgcolor") else "") +
		(sec.bkgimg if hasattr(sec, "bkgimg") else "") )

def bg(sec):
	sec.css["background"] = genbgstatement(sec)

def background(sec, args):
	fill = True
	tiled = False
	if isinstance(args, list):
		fill = (args[1] == fill)
		tiled = (args[1] == fill)

	if not (tiled or fill):
		raise Exception(args[1]+" not a valid thing")

	sec.bkgimg = (args[0] if isinstance(args,list) else args)

	bg(sec);

	sec.css = merge(sec.css, {
		"background-position":"center",
		}, (background_fill if fill else {"background-repeat": "repeat"}))
		

def bgfill(sec,args):
	sec.bgcolor = (args[0], (args[1] if len(args)>0 else 1))
	bg(sec)
	return ""

cssMap = {
	"fullfold": fullfold,
	"bgfill": bgfill,
	"background": background
}
