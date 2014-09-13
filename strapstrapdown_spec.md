#MktDown Syntax Rules

##Metadata Blocks

Metadata Blocks (metablocks) are denoted with a triple
colon, followed by some identifying information, and a
series of lines beginning with a single colon that set
some specific metadata for the document.

The first term of the first line of a metablock defines
what kind of metablock it is, and the remainder declares
the properties of the block.

Metadata blocks must be declared at the root level of the
document.

###Css Blocks
```
::: css <file-name>
	...
```

CSS blocks t2 <file-name>.css to the produced HTML document.

###Document blocks
```
::: document <header name>
```

Document blocks take a series of nested sections (see below),
and construct a HTML DOM from them. The title window/tab is set
by the `<header name>` argument, which may contain spaces.

If multiple document metablocks are declared in the same file,
an error will be thrown during compilation.


##Document Sections

Sections (divs) are denoted with a double colon, the name of 
the section, and any css classes it may have,
followed a series of lines
beginning with a single colon that denote the 
properties of the section.

The contents of the section are defined by indented
content following the section declaration.

i.e.,
```
:: example .someclass
: header-align left
: text-align center

	#Div Header

	hello
```
produces
```
<div id="example" class="someclass">
	<h1>Div Header</h1>
	<p>hello</p>
</div>
```

unnamed (anonymous) sections with properties set 
will have names generated for them on compile 

If more than one section shares a name, an error will 
be thrown during compilation


##Section Contexts

A section can exist in one of several 'contexts', or 
modes that determine how they are laid out.

the context of a section is determined by the 
context-specific attributes used on it.
When multiple conflicting context tags are used on the same
section, the one with the highest priority is chosen.

below is a list of all contexts in ascending order.


###Text-Block
text-block is the default text content. it represents
a block of default left-aligned text in an evenly 
padded container


###XYCentered
XYCentered sections are sections in which the text is
displayed in a box of size `width-small`.

Does not work in a multicolumn context (currently?)

*Defining attributes*:

 - `xycenter`


###Columns

Columned layouts split their children into some 
number of columns, as designated by the   
`columns <n>` property

direct children of the columns object can declare
the `column-width <n>` property to designate width
in multiples of default column width.

*Defining attributes*:
 - `columns <n>`

*Other Attributes*:
 - `column-width <n>`

###Images

In addition to typical attribute-based image embedding, 
images can be declared with the shorthand  
`:: image <url>` section header.

Images created like this will be named automatically 

by default, the alt attribute of the image will be the 
same as the url, unless otherwise specified with the 
`alt` attribute

*Defining attributes*:

 - `image <url>`

*Other Attributes*:

 - `width <w>`
 - `height <h>`
 - `shape <shape>`


###Tables

As with images, tables can be declared with a shorthand 
section header,  
`:: table <width> <height>`

The content of a table is parsed differently than
typical content, instead following a more human-readable
table format.

for example, 
```
:: SomeTable
:table 2 2

	| 1 | 2 |
	| 2 | 4 |
```
produces the following html:
```
<table>
	<tr>
		<td>1</td> <td>2</td>
	</tr>
	<tr>
		<td>2</td> <td>4</td>
	</tr>
</table>
```

*Defining attributes*:

 - `table <width> <height>`
