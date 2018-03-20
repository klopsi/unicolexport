# unicolexport
unicode block-character graphic exporter for GIMP

Fans of ascii/ansi art may have noticed that unicode provides additional types of block-drawing
characters, such as ▚ ▝ ▙.  These let us draw 4 pixels in the space of one character, with two 
simultaneous colors.

Finding no editor for unicode art, i made this python plugin for gimp that exports an image 
to unicode block graphics, using the 16-color mIRC palette.

It is an entertaining challenge to draw pictures at low resolution with very few colors. It's fun to share them too. Make your own art and paste it to IRC channel ##ascii on the Freenode IRC network. 

## Installation

Linux:   Copy unicolexport.py to your ~/.gimp-2.8/plug-ins

Windows: Install Linux


## Instructions

 0) Run GIMP, preferably from a terminal.
 1) Open the image to export in GIMP
 2) Resize image to something small, I prefer 144x58
    (Optional: To edit the image in the irc palette, convert image to indexed color mode with
     the mIRC 16-Color Palette)
 3) Change image mode to RGB
 4) Select "Export as" and set filename extension to .unc 
 5) Check the terminal for program output. It will notify you if lines are too long for IRC.
 6) Load the image into your irc client (e.g. in irssi /exec cat /path/to/file/filename.unc
    or to send the image to a channel, /exec -o cat /path/to/file/filename.unc)

## Examples

An early pic i did of a BMW e21 

![Examples](https://abload.de/img/cool-unicodebmws8sa8.png)


Famous people quotes are fun to do.

![Examples](https://i.imgur.com/kRhJbGol.png)

![Examples](https://abload.de/img/krugmancapsda9j.png)

![Examples](https://files.catbox.moe/b3uyji.png)

![Examples](https://abload.de/img/stallmanquotcapj3p9e.png)

There is no substitute for editing every pixel by hand.

![Examples](https://abload.de/img/logcap2uqp2.png)

![Examples](https://files.catbox.moe/tg9voc.png)

![Examples](https://abload.de/img/bitcoincapnqr8a.png)


The extended Mirc 99-color spec (Implemented by mIRC, Weechat and IRSSI so far)

![Examples](https://abload.de/img/98colors92kra.png)

99-colors poses special challenges - most color changes require the full 6 bytes, having more available colors means many color ramps requiring color changes per character, and no long runs of same color. Above image has a max line length of 481 Bytes after squishing.

![Examples](https://files.catbox.moe/d5dk8w.png)

Automated mapping to 99 or 16 color palettes never works as well as you'd wish.  Best to do the mapping yourself.

![Examples](https://a.pomfe.co/fqfikv.png)
