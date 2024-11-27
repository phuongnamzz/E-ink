#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont
import socket
from datetime import datetime
import time
import argparse
file_path = "/home/miner/.content.txt"


parser = argparse.ArgumentParser(description="Select refreh option: slow or fast.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--slow', action='store_true', help="refresh (slow).")
group.add_argument('--fast', action='store_true', help="refresh (fast).")

args = parser.parse_args()



start_time = time.time()
def get_date():
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y")
    return date_string


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




def get_ip_address():
    try:
        # Connect to an external server to determine the IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google's public DNS server
            ip_address = s.getsockname()[0]
        return ip_address
    except Exception as e:
        return f"Error: {e}"


def draw_symbol(epd, canvas, bmp_path, x, y):
    """
    Draw a BMP on top of an existing canvas without erasing previous content.
    
    :param epd: The e-paper display object.
    :param canvas: The existing PIL.Image canvas.
    :param bmp_path: Path to the BMP file.
    :param x: X-coordinate for the BMP placement.
    :param y: Y-coordinate for the BMP placement.
    """
    # Load the BMP file
    bmp_image = Image.open(bmp_path)
    bmp_image = bmp_image.rotate(180)
    # Paste the BMP onto the existing canvas
    canvas.paste(bmp_image, (x, y))

    # Display the updated canvas
    epd.displayPartial(epd.getbuffer(canvas))

try:

    ip = get_ip_address()
    # print(f"My Raspberry Pi IP Address: {ip}")


    with open(file_path, 'r') as f:
        content = f.read()

    epd = epd2in13_V4.EPD()

    epd.init_fast()
    fontRoboto14 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Medium.ttf'), 14)
    fontRoboto = ImageFont.truetype(os.path.join(picdir, 'Roboto-Medium.ttf'), 16)
    font_display = fontRoboto
    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(Himage)
    # draw.line([(0, 16),(epd.height, 16)], fill = 0,width = 2)
    draw.text((0 , epd.width - 16), ip, font = fontRoboto14, fill = 0)
    # battery symbols
    draw.rectangle([(epd.height -40, 0),(epd.height -1 ,16)],outline = 0, width = 2)
    draw.line([(epd.height -42, 4),(epd.height -42 , 12)], fill = 0,width = 3)
    # message frame
    draw.rounded_rectangle([(0, 0 + 18),(epd.height -1, epd.width -16)], radius = 5, outline = 0, width = 2)
    #
    draw.text((epd.height -38, 0), "100%", font = fontRoboto14, fill = 0)
    # date
    date_string = get_date()
    draw.text((0, 0), date_string, font = fontRoboto14, fill = 0 )
    # message number
    draw.text((epd.height - 30, epd.width - 16), "3/5", font = fontRoboto14, fill = 0)
    


    # Split the text into lines that fit within the screen width
    max_width = epd.height - 5  # Leave 5 pixels margin on each side
    lines = wrap_text(content, font_display, max_width)
    
    y_offset = 18  # Distance from the top
    for line in lines:
        line_width, line_height = font_display.getbbox(line)[2:4]
        x_offset = (epd.height - line_width) // 2 + 2  # Center the line
        draw.text((x_offset, y_offset), line, font=font_display, fill=0)
        y_offset += line_height  # Move down to the next line


    Himage = Himage.rotate(180)
    draw_symbol(epd, Himage, os.path.join(picdir, "bolt.bmp"), epd.height - 205, epd.width - 16)
    # draw_symbol(epd, Himage, os.path.join(picdir, "tick.bmp"), int(epd.height / 2), epd.width - 16)
    x_back_button = 120
    draw_symbol(epd, Himage, os.path.join(picdir, "back-button.bmp"), x_back_button , -1)
    draw_symbol(epd, Himage, os.path.join(picdir, "cart.bmp"), x_back_button - 20 , -1)
    draw_symbol(epd, Himage, os.path.join(picdir, "sell.bmp"), x_back_button - 2*20, -1 )
    draw_symbol(epd, Himage, os.path.join(picdir, "fast-forward.bmp"), x_back_button - 3*20, -1 )

    if args.fast:
        epd.displayPartial(epd.getbuffer(Himage))
    elif args.slow:
        epd.display(epd.getbuffer(Himage))
    
    
    # time.sleep(1)
    epd.sleep()
    # print("Done")
    print("--- %s seconds ---" % (time.time() - start_time))
except IOError as e:
    pass
    
except KeyboardInterrupt:    
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
