#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

file_path = "/home/miner/output.txt"

def wrap_text(text, font, max_width):
    """Splits the text into lines that fit within the max width."""
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getbbox(line + words[0])[2] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

try:
    with open(file_path, 'r') as f:
        content = f.read()

    logging.info("E-ink display")
    epd = epd2in9_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    # epd.Clear(0xFF)
    
    fontRoboto = ImageFont.truetype(os.path.join(picdir, 'Roboto-Medium.ttf'), 16)
    
    # Drawing on the Horizontal image
    logging.info("1. Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(Himage)
    font_display = fontRoboto
    # Split the text into lines that fit within the screen width
    max_width = epd.height - 5  # Leave 5 pixels margin on each side
    lines = wrap_text(content, font_display, max_width)
    
    # Draw each line onto the image
    y_offset = 1  # Distance from the top
    # align left 
    # for line in lines:
    #     draw.text((5, y_offset), line, font=font_display, fill=0)
    #     y_offset += font_display.getbbox(line)[3] - font_display.getbbox(line)[1]  # Move down to the next line
    # 
    for line in lines:
        line_width, line_height = font_display.getbbox(line)[2:4]
        x_offset = (epd.height - line_width) // 2  # Center the line
        draw.text((x_offset, y_offset), line, font=font_display, fill=0)
        y_offset += line_height  # Move down to the next line


    Himage = Himage.rotate(0)

    epd.display(epd.getbuffer(Himage))
    time.sleep(1)
    logging.info("Clear...")
    # epd.init()
    # epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9_V2.epdconfig.module_exit(cleanup=True)
    exit()
