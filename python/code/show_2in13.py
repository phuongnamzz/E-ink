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
import subprocess
import time
import argparse
file_path = "/home/miner/.content.txt"


parser = argparse.ArgumentParser(description="Select refreh option: slow or fast.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--slow', action='store_true', help="refresh (slow).")
group.add_argument('--fast', action='store_true', help="refresh (fast).")
parser.add_argument('-b', "--battery_percent", type=int, required=True, help="battery percent with integer")
parser.add_argument('-u', "--username_truth", type=str, required=True, help="user name of truth terminal")
parser.add_argument('-e', "--eai_value", type=str, required=True, help="EAI value")



args = parser.parse_args()



start_time = time.time()

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


def get_wifiName():
    try:
        result = subprocess.check_output(['iwgetid', '--raw'], stderr=subprocess.STDOUT)

        wifi_name = result.decode('utf-8').strip()
        return wifi_name if wifi_name else "Currently, not connected"
    except subprocess.CalledProcessError:
        return "Can not get Wifi name"
    
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

    with open(file_path, 'r') as f:
        content = f.read()

    epd = epd2in13_V4.EPD()

    epd.init_fast()
    fontRoboto14 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Medium.ttf'), 14)
    fontRoboto16 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Medium.ttf'), 16)
    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    #draw battery
    percent_battery = args.battery_percent
    x_battery_line = 3
    if percent_battery >= 80:
        draw.line([(x_battery_line, 0),(x_battery_line, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 5, 0),(x_battery_line + 5, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 10, 0),(x_battery_line + 10, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 15, 0),(x_battery_line + 15, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 20, 0),(x_battery_line + 20, 12)], fill = 0, width = 3)
    elif percent_battery >=60 and percent_battery < 80:
        draw.line([(x_battery_line, 0),(x_battery_line, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 5, 0),(x_battery_line + 5, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 10, 0),(x_battery_line + 10, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 15, 0),(x_battery_line + 15, 12)], fill = 0, width = 3)
    elif percent_battery >=40 and percent_battery < 60:
        draw.line([(x_battery_line, 0),(x_battery_line, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 5, 0),(x_battery_line + 5, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 10, 0),(x_battery_line + 10, 12)], fill = 0, width = 3)
    elif percent_battery >= 20 and percent_battery < 40:
        draw.line([(x_battery_line, 0),(x_battery_line, 12)], fill = 0, width = 3)
        draw.line([(x_battery_line + 5, 0),(x_battery_line + 5, 12)], fill = 0, width = 3)
    elif percent_battery < 20:
         draw.line([(x_battery_line, 0),(x_battery_line, 12)], fill = 0, width = 3)
    # message frame
    draw.rounded_rectangle([(0, 0 + 15),(epd.height -1, epd.width -15)], radius = 5, outline = 0, width = 2)
    #draw EAI
    # EAI = "0.001 EAI"
    eai_value = args.eai_value
    draw.text((epd.height - 62, 0), eai_value, font = fontRoboto14, fill = 0)
    # draw wifi name
    draw.text((30, -2), get_wifiName(), font = fontRoboto14, fill = 0 )
    # draw user
    # user = "@truth_terminal (0.0001 EAI +- 0.05%)"
    user = args.username_truth
    draw.text((0, epd.width - 14), user, font = fontRoboto14, fill = 0)
    


    # Split the text into lines that fit within the screen width
    max_width = epd.height - 5  # Leave 5 pixels margin on each side
    lines = wrap_text(content, fontRoboto16, max_width)
    
    y_offset = 15  # Distance from the top
    for line in lines:
        line_width, line_height = fontRoboto16.getbbox(line)[2:4]
        x_offset = (epd.height - line_width) // 2 + 2  # Center the line
        draw.text((x_offset, y_offset), line, font=fontRoboto16, fill=0)
        y_offset += line_height  # Move down to the next line


    Himage = Himage.rotate(180)


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