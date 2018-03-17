#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################################
## This code is released under the GPL liscence by Raul Aguaviva (aguaviva--gmail.com)
## http://www.gnu.org/licenses/gpl.html
#####################################################################################
## The Gimp exporter 1bit bitmaps to a C language header file Textures
#####################################################################################
## * Installation
##
## Linux:  Copy this file in to your ~/.gimp-2.6/plug-ins
## Windows: Not sure how to install it in windows :-)
##
## * Instructions
##
## 1) Open the image to export in GIMP
## 2) Resize the image to 128x64
## 3) Convert the image to a "indexed image" ( /Image/Transform/Indexed/ )
##    a) Select black adn white (1-bit) palette
##    b) Select the dithering method (Floyd steinberg is a good one )
## 4) Select "Export as"  and look for the Unicode
##
#####################################################################################

import struct
import gimp
from gimpfu import *
from collections import Counter

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def python_unicolexport(img, drawable, filename, raw_filename):
    pdb.gimp_layer_resize_to_image_size(drawable)
    width = drawable.width
    height = drawable.height

    # compute the palette
    #(nbindex,colormap) = pdb.gimp_image_get_colormap(imageIndex)
    palette = pdb.gimp_context_get_palette()
    colors = pdb.gimp_palette_get_colors(palette)[1]
    #print(len(colors))
    irccols = [[255,255,255], [0,0,0], [0,0,127], [0,147,0], [255,0,0], [127,0,0], [156,0,156], [252,127,0], [255,255,0], [0,252,0], [0,147,147], [0,255,255], [0,0,252], [255,0,255], [127,127,127], [210,210,210], [71,0,0], [71,33,0], [71,71,0], [50,71,0], [0,71,0], [0,71,44], [0,71,71], [0,39,71], [0,0,71], [46,0,71], [71,0,71], [71,0,42], [116,0,0], [116,58,0], [116,116,0], [81,116,0], [0,116,0], [0,116,73], [0,116,116], [0,64,116], [0,0,116], [75,0,116], [116,0,116], [116,0,69], [181,0,0], [181,99,0], [181,181,0], [125,181,0], [0,181,0], [0,181,113], [0,181,181], [0,99,181], [0,0,181], [117,0,181], [181,0,181], [181,0,107], [255,0,0], [255,140,0], [255,255,0], [178,255,0], [0,255,0], [0,255,160], [0,255,255], [0,140,255], [0,0,255], [165,0,255], [255,0,255], [255,0,152], [255,89,89], [255,180,89], [255,255,113], [207,255,96], [111,255,111], [101,255,201], [109,255,255], [89,180,255], [89,89,255], [196,89,255], [255,102,255], [255,89,188], [255,156,156], [255,211,156], [255,255,156], [226,255,156], [156,255,156], [156,255,219], [156,255,255], [156,211,255], [156,156,255], [220,156,255], [255,156,255], [255,148,211], [0,0,0], [19,19,19], [40,40,40], [54,54,54], [77,77,77], [101,101,101], [129,129,129], [159,159,159], [188,188,188], [226,226,226], [255,255,255]]
    #print(irccols[2])
    for i in range(len(irccols)):
    #    color = colors[i]
        (rr,gg,bb) = irccols[i]
        print (rr,gg,bb)
        #try:
        #    print(colormap[i*3+0],colormap[i*3+1],colormap[i*3+2])
        #except IndexError:
        #    color = 0
        #fileOut.write(struct.pack("<H", color))
        #gimp.progress_update(float(i*(0.2/nbColors) + 0.8))

    fileOut = open(filename,"w")

    #remove path from filename and extension
    i = filename.rfind("/")
    p = filename.rfind(".")
    if ( i >= 0 ):
        if ( p == -1 ):
            filename = filename[i+1:len(filename) ]
        else:
            filename = filename[i+1:p ]
    bestindexlist = []
    gimp.progress_init(_("Saving as unicode image (16 colors)"))
    print("\n\nunicolexport begin")
    oldcfg=255
    oldcbg=255
    nuline=1
    bytecount=0
    for y in range(0,height-1, 2):
        #oldcfg=1
        #oldcbg=1
        #print("---------------------------------------------------------------")
        # Ensure that no line sent to irc is longer than 512 bytes including CR-LF
        linecount = 0
        for x in range(0,width-1, 2):
            #if (linecount > 620): # Stop writing if we exceed IRC's line limit
            #    print str(x),str(y),'Warning! Line exceeds IRC line-length limit! '
            #    break
            linecount +2 #Each utf-8 character is 2 bytes
            # Calculate the closest mIRC palette match for each pixel
            (channels,pixUL) = pdb.gimp_drawable_get_pixel(drawable,x, y)
            (channels,pixUR) = pdb.gimp_drawable_get_pixel(drawable,x+1, y)
            (channels,pixBL) = pdb.gimp_drawable_get_pixel(drawable,x, y+1)
            (channels,pixBR) = pdb.gimp_drawable_get_pixel(drawable,x+1, y+1)
            cbestUL= 255.0
            bestindexUL = 0
            cbestUR= 255.0
            bestindexUR = 0
            cbestBL= 255.0
            bestindexBL = 0
            cbestBR= 255.0
            bestindexBR = 0
            bestindexlist[:] = []
            #print("pixel ",x,"\n")
            for i in range(len(irccols)):
                (r0,g0,b0) = irccols[i]
                (r1,g1,b1) = (pixUL[0],pixUL[1],pixUL[2])
                (r2,g2,b2) = (pixUR[0],pixUR[1],pixUR[2])
                (r3,g3,b3) = (pixBL[0],pixBL[1],pixBL[2])
                (r4,g4,b4) = (pixBR[0],pixBR[1],pixBR[2])
                cdiffUL = math.sqrt((r0 - r1)**2 + (g0 - g1) ** 2 + (b0 - b1) **2)
                cdiffUR = math.sqrt((r0 - r2)**2 + (g0 - g2) ** 2 + (b0 - b2) **2)
                cdiffBL = math.sqrt((r0 - r3)**2 + (g0 - g3) ** 2 + (b0 - b3) **2)
                cdiffBR = math.sqrt((r0 - r4)**2 + (g0 - g4) ** 2 + (b0 - b4) **2)
                #print(cdiff,cbest)
                if (cdiffUL< cbestUL):
                    ibestUL = i
                    cbestUL = cdiffUL
                if (cdiffUR< cbestUR):
                    ibestUR = i
                    cbestUR = cdiffUR
                if (cdiffBL< cbestBL):
                    ibestBL = i
                    cbestBL = cdiffBL
                if (cdiffBR< cbestBR):
                    ibestBR = i
                    cbestBR = cdiffBR
            bestindexlist.append(ibestUL)
            bestindexlist.append(ibestUR)
            bestindexlist.append(ibestBL)
            bestindexlist.append(ibestBR)

            #Get a sorted list of two most prevalent colors (unused)
            #print(bestindexlist),
            #c = Counter(bestindexlist)
            #print(str(c.most_common(2)))
            #print(bestindexUL,bestindexUR,bestindexBL,bestindexBR)

            #Write the code (Ctrl+C) to set an irssi color pair (fg,bg)

            # Set foreground to most common color
            #fgc = c.most_common(2)[0][0]
            # If there is more than one color, seg background to 2nd most common
            #if (len(c.most_common(2)) > 1):
            #    bgc = c.most_common(2)[1][0]
            #else:
            #    bgc=1
            #fileOut.write(str(fgc))
            #fileOut.write(",")
            #fileOut.write(str(bgc))
            #print("Fore:",str(fgc)," Back:",str(bgc)),

            if (ibestUL == ibestUR == ibestBL == ibestBR):
                cfg = ibestUL
                cbg = ibestUR
                #if (cfg != oldcfg) or (cbg != oldcbg or nuline==1):
                if (cbg != oldcbg or nuline==1):
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))   # mIRC and QUassel need FG specified
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write(" ")
                linecount += 1 # Ascii char adds 1 byte
                    #print(str(x/2),' Fore:',str(ibestUL)),
                    #print('█')
# OLD WAY OF HANDLING NO MATCH
#            elif (ibestUL == ibestBL) and (ibestUL != ibestUR) and (ibestBL != ibestBR):
#            if (ibestUL == ibestUR == ibestBL == ibestBR):
#                cfg = ibestUL
#                cbg = ibestUR
#                if (cfg != oldcfg) or (cbg != oldcbg or nuline==1):
#                    oldcfg = cfg
#                    oldcbg = cbg
#                    if (cfg > 9): # Add two or three bytes to the linecount
#                        linecount += 3
#                    else:
#                        linecount += 2
#                    if (cbg > 9): # Add two or three bytes to the linecount
#                        linecount += 3
#                    else:
#                        linecount += 2
#                    linecount += 1 # Add a byte for the comma
#                    fileOut.write('\x03')
#                    fileOut.write(str(cfg))
#                    fileOut.write(",")
#                    fileOut.write(str(cbg))
#                fileOut.write("█")
                    #print(str(x/2),' Fore:',str(ibestUL)),
                    #print('█')
            elif (ibestUL == ibestBL) and (ibestUL != ibestUR) and (ibestBL != ibestBR):
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▌")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestUR)),
                    #print("▌")
            elif (ibestUR == ibestBR) and (ibestUL != ibestUR) and (ibestBL != ibestBR):
                cfg = ibestUR
                cbg = ibestUL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▐")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUR),' Back:',str(ibestUL)),
                    #print("▐")
            elif (ibestUR == ibestBR == ibestBL):
                cfg = ibestUR
                cbg = ibestUL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▟")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUR),' Back:',str(ibestUL)),
                    #print("▟")
            elif (ibestUL == ibestBR == ibestBL):
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▙")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestUR)),
                    #print("▙")
            elif (ibestUL == ibestUR == ibestBR):
                cfg = ibestUL
                cbg = ibestBL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▜")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestBL)),
                    #print("▜")
            elif (ibestUL == ibestUR == ibestBL):
                cfg = ibestUL
                cbg = ibestBR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▛")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestBR)),
                    #print("▛")
            elif (ibestUL == ibestBR) and (ibestBL != ibestUR):
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▚")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestUR)),
                    #print("▚")
            elif (ibestUL == ibestBR) and (ibestBL == ibestUR) and (ibestUL != ibestUR):
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▚")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' For2:',str(ibestUL),' Back:',str(ibestUR)),
                    #print("▚")
            elif (ibestUR == ibestBL) and (ibestUL != ibestBR):
                cfg = ibestUR
                cbg = ibestUL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▞")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUR),' Back:',str(ibestUL)),
                    #print("▞")
            elif (ibestUR == ibestBL) and (ibestUL == ibestBR) and (ibestUL != ibestUR):
                cfg = ibestUR
                cbg = ibestUL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▞")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' For2:',str(ibestUR),' Back:',str(ibestUL)),
                    #print("▞")
            elif (ibestUL == ibestUR) and (ibestBL != ibestBR) and (ibestUL != ibestBR) and (ibestUR != ibestBL):
                cfg = ibestUL
                cbg = ibestBL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▀")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestBL)),
                    #print("▀")
            elif (ibestUL == ibestUR) and (ibestBL == ibestBR) and (ibestUL != ibestBR) and (ibestUR != ibestBL):
                cfg = ibestUL
                cbg = ibestBL
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▀")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestBL)),
                    #print("▀")
            elif (ibestBL == ibestBR) and (ibestUL != ibestBL) and (ibestUR != ibestBR) and(ibestUL != ibestUR):
                cfg = ibestBR
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▄")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL),' Back:',str(ibestUR)),
                    #print("▄")
            elif (ibestUL != ibestUR) and (ibestUL != ibestBL) and (ibestUL != ibestBR):
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    fileOut.write(",")
                    fileOut.write(str(cbg))
                fileOut.write("▚")
                linecount += 3 # Unicode char adds 3 bytes
                    #print(str(x/2),' Fore:',str(ibestUL)),
                    #print('█')
            else:
                cfg = ibestUL
                cbg = ibestUR
                if (cfg != oldcfg) or (cbg != oldcbg) or nuline==1:
                    oldcfg = cfg
                    oldcbg = cbg
                    if (cfg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    if (cbg > 9): # Add two or three bytes to the linecount
                        linecount += 3
                    else:
                        linecount += 2
                    linecount += 1 # Add a byte for the comma
                    fileOut.write('\x03')
                    fileOut.write(str(cfg))
                    #fileOut.write(",") /// REDUNDANT
                    #fileOut.write(str(cbg))
                fileOut.write("█")
                linecount += 3 # Unicode char adds 3 bytes
                print(str(x),str(y),'No Match Found! ', str(ibestUL), str(ibestUR), str(ibestBL), str(ibestBR))
            nuline=0
            #else:
            #    fileOut.write(" ")
##            gimp.progress_update(float(x+y*width)/(width*height))
        fileOut.write( "\n" )
        nuline=1
        bytecount += linecount
        print "Line "+str(y)+" length:", linecount
    #fileOut.write( "\n" ) # Extra newline at end of file (needed?)
    print "Unicolexport end: wrote", bytecount, "bytes."

    # test
#    fileOut.write( "\n" )
#    for y in range(0,15, 1):
#        for x in range(0,15, 1):
#                fileOut.write('\x03')
#                fileOut.write(str(x))
#                fileOut.write(",")
#                fileOut.write(str(y))
#                fileOut.write("░")
#                fileOut.write("▒")
#                fileOut.write("▓")
#        fileOut.write( "\n" )

    gimp.progress_update(1)
    fileOut.close()

def register_save_unicol():
    gimp.register_save_handler("file-unicodecolexport99-save", "un9", "")

register(
        "file-unicodecolexport99-save",
        N_("Save in 99 color unicode format"),
        "Export an image to a .un9 file",
        "Raul Aguaviva and blap",
        "Raul Aguaviva and blap",
        "2017",
        N_("Unicode 99-color file"),
        "INDEXED",
        [
            (PF_IMAGE, "image", "Input image", None),
            (PF_DRAWABLE, "drawable", "Input drawable", None),
            (PF_STRING, "filename", "The name of the file", None),
            (PF_STRING, "raw-filename", "The name of the file", None),
        ],
        [],

        python_unicolexport, on_query=register_save_unicol,
        menu="<Save>", domain=("gimp20-python", gimp.locale_directory))
main()
