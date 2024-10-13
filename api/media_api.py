#
# Copyright 2024 MangDang (www.mangdang.net)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Description: This Python script provides a comprehensive set of functionalities to capture and display images,
# resize images, and play GIF animations on a display using a webcam and an ST7789 display module.
#
# Taking Photo Displaying Test Method: Type 'photo', then press  enter.
# Displaying Photo from Path Test Method: Type 'path', press enter, then type the path to your desired photo, then press enter.
# Resizing Photo and Displaying Test Method: Type 'resize', press enter, then type the path to your desired photo, then press enter.
# Displaying GIF Test Method: Type 'gif', then press enter.
#

import logging
import cv2
import numpy as np
from PIL import Image
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from MangDang.LCD.ST7789 import ST7789
from api.gif import AnimatedGif

disp = ST7789()
disp.begin()

def take_photo():
    """
    Captures a photo from the webcam and returns it as a PIL Image object.

    Returns:
    - image (PIL.Image): The captured image or None if the webcam is not accessible.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    image = None
    if ret:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return image


def resize_image(image, target_width, target_height):
    """
    Resizes the image to fit within the specified dimensions while maintaining aspect ratio.

    Parameters:
    - image (PIL.Image): The original image.
    - target_width (int): The desired width.
    - target_height (int): The desired height.

    Returns:
    - new_image (PIL.Image): The resized and possibly padded image.
    """
    original_width, original_height = image.size

    width_ratio = target_width / original_width
    height_ratio = target_height / original_height
    scale_ratio = min(width_ratio, height_ratio)

    new_width = int(original_width * scale_ratio)
    new_height = int(original_height * scale_ratio)

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    new_image = Image.new('RGB', (target_width, target_height), (0, 0, 0))

    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2

    new_image.paste(resized_image, (paste_x, paste_y))

    return new_image


def resize_image_to_width(image, target_width):
    """
    Resizes the image while maintaining the aspect ratio based on the target width.

    Parameters:
    - image (PIL.Image): The original image.
    - target_width (int): The desired width.

    Returns:
    - resized_image (PIL.Image): The resized image.
    """
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)
    resized_image = image.resize((target_width, target_height), Image.LANCZOS)

    return resized_image


def show_image(image):
    """
    Displays the given image on the initialized display.

    Parameter:
    - image (PIL.Image): The image to display.
    """
    disp.display(image)

def show_image_from_path(image_path):
    """
    Displays an image from the given file path on the display.

    Parameter:
    - image_path (str): The file path of the image to display.
    """
    with Image.open(image_path) as image:
        disp.display(image)

def init_gifplayer(folder):
    """
    Initializes a GIF player for playing GIFs from the specified folder.

    Parameter:
    - folder (str): The folder containing GIF files.

    Returns:
    - gif_player (AnimatedGif): The initialized GIF player instance.
    """
    gif_player = AnimatedGif(disp, width=320, height=240, folder=folder)
    gif_player.preload()
    return gif_player


def show_gif(gifplayer):
    """
    Plays the GIF using the provided GIF player instance.

    Parameter:
    - gifplayer (AnimatedGif): The GIF player instance.
    """
    gifplayer.play()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO
    )


    while True:
        user_input = input("Enter function apis --- 'photo'/'resize' or 'exit' to quit: ").strip().lower()

        if user_input == 'exit':
           logging.info("Exit!")
           break
        elif user_input == 'photo':
            image = take_photo()

            if not image:
                logging.info("No image!")
            else:
                logging.info(f"image size: {image.width} x {image.height}")
                pil_image = image.resize((320, 240))
                show_image(pil_image)
                #disp.display(pil_image)
        elif user_input == 'path':
            origin_path = input("input the jpg file path: ").strip()
            show_image_from_path(origin_path)
        elif user_input == 'resize':
            origin_path = input("input the jpg file path: ").strip().lower()
            dimensions = [
                (720, 1080),
                (480, 720),
                (320, 480),
                (240, 320),
            ]
            with Image.open(origin_path) as image:
                for w,h in dimensions:
                    output_path = f'{w}p.jpg'
                    resize_img = resize_image(image, w, h)
                    resize_img.save(output_path)
                    logging.info(f"save {output_path}")
        elif user_input == 'gif':
            player = init_gifplayer("../cartoons/")
            show_gif(player)
        else:
            logging.info("Invalid command. Please enter 'photo' or 'exit'.")

if __name__ == '__main__':
    main()

