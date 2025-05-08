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
# Description: This script imports necessary modules and sets up tasks for an interactive AI system.
# It handles speech-to-text, text-to-speech, AI interactions, image and GIF display, and physical movement commands using threading for concurrent operation.
#

import logging
import os
import time
import re
import numpy as np
from PIL import Image
import pyaudio
import sounddevice as sd
import soundfile as sf
from io import BytesIO
import asyncio
import threading
from google.cloud import texttospeech
from langchain_google_vertexai import ChatVertexAI
import random

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task_queue import input_text_queue, output_text_queue, gif_queue, image_queue, movement_queue, stt_queue
from api import media_api, google_api, move_api, shell_api


RES_DIR = "cartoons"

# Game text for the rock-paper-scissors game
GAME_TEXT = "Let's play! Rock! Paper! Scissor! Shoot!"
ai_on = True

# Define voice parameters for different languages and a default voice
voice0 = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-E")
voice_man = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Neural2-D")
voice_JP = texttospeech.VoiceSelectionParams(language_code="ja-JP", name="ja-JP-Neural2-B")
voice_CN = texttospeech.VoiceSelectionParams(language_code="cmn-CN", name="cmn-CN-Standard-C")
voice_IT = texttospeech.VoiceSelectionParams(language_code="it-IT", name="it-IT-Standard-B")
voice_DE = texttospeech.VoiceSelectionParams(language_code="de-DE", name="de-DE-Neural2-D")
voice_FR = texttospeech.VoiceSelectionParams(language_code="fr-FR", name="fr-FR-Standard-C")
lang_voices = {
    "Japanese": voice_JP,
    "Chinese": voice_CN,
    "Italian": voice_IT,
    "German": voice_DE,
    "French": voice_FR,
}
cur_voice = voice0

def get_voice(prompt=None):
    """
    Determine the voice to be used based on the input prompt.

    Parameters:
    - prompt (str, optional): The input prompt that may contain language or voice type instructions.

    Returns:
    - lang (str, optional): The detected language from the prompt.
    - voice (texttospeech.VoiceSelectionParams): The selected voice parameters.
    """
    if not prompt:
        logging.debug(f"select key voice: None,default is voice0")
        return None, voice0
    if "man" in prompt:
        logging.debug(f"select key voice: Man")
        return None, voice_man
    for key, value in lang_voices.items():
        if key in prompt:
            logging.info(f"select key: {key}")
            return key, value
    logging.info(f"no mapping, default is voice0")
    return None, voice0

move_cmd_functions = {
                 "action": move_api.init_movement,
                 "sit": move_api.squat,
                 "move forwards": move_api.move_forward,
                 "move backwards": move_api.move_backward,
                 "move left": move_api.move_left,
                 "move right": move_api.move_right,
                 "look up": move_api.look_up,
                 "look down": move_api.look_down,
                 "look left": move_api.look_left,
                 "look upper left": move_api.look_upperleft,
                 "look lower left": move_api.look_leftlower,
                 "look right": move_api.look_right,
                 "look upper right": move_api.look_upperright,
                 "look lower right": move_api.look_rightlower,
                 "dance": move_api.dance,
             }

def get_move_cmd(input_text, command_dict):
    """
    Find the command key in the input text based on the command dictionary.

    Parameters:
    - input_text (str): The input text to search within.
    - command_dict (dict): The dictionary of command keys.

    Returns:
    - command_key (str, optional): The found command key or None if not found.
    """
    if not input_text:
        return None
    for command_key in command_dict.keys():
        if re.search(r'\b' + re.escape(command_key) + r'\b', input_text):
            return command_key
    return None

def close_ai():
    global ai_on
    ai_on = False
    stt_queue.put(True)
    image = Image.open(f"{RES_DIR}/logo2.png")
    image_queue.put(image)

def open_ai():
    global ai_on
    ai_on = True
    stt_queue.put(True)
    image = Image.open(f"{RES_DIR}/hello.png")
    image_queue.put(image)
    output_text_queue.put("OK, my friend.")

def reboot():
    command = "sudo reboot"
    shell_api.execute_command(command)

def power_off():
    command = "sudo poweroff"
    shell_api.execute_command(command)

sys_cmds_functions = {
        "shut up": close_ai,
        "speak please": open_ai,
        "reboot": reboot,
        "power off": power_off,
        }

def get_sys_cmd(input_text, command_dict):
    normalized_text = re.sub(r'[^\w\s]', '', input_text.lower())

    for command_key in command_dict.keys():
        if normalized_text == command_key.lower():
            return command_key, command_dict[command_key]

    return None, None


def cut_text_by_last_period(text, max_words_before_period=15):
    """
    Cut the text by the last period within a specified number of words.

    Parameters:
    - text (str): The text to cut.
    - max_words_before_period (int): The maximum number of words before the last period.

    Returns:
    - cut_text (str): The text cut by the last period.
    """
    words = text.split()

    last_period_index = -1
    for i, word in enumerate(words[:max_words_before_period]):
        if '.' in word:
            last_period_index = i

    if last_period_index != -1:
        return ' '.join(words[:last_period_index+1])

    first_period_index = -1
    for i, word in enumerate(words):
        if '.' in word:
            first_period_index = i
            break

    return ' '.join(words[:first_period_index+1]) if first_period_index != -1 else text

def remove_emojis(text):
    """
    Remove emojis from the text.

    Parameters:
    - text (str): The text to remove emojis from.

    Returns:
    - text (str): The text with emojis removed.
    """
    # This pattern matches most emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00000200-\U00000250"  # General Punctuation
        "\U00000260-\U00002B55"  # Various symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


def stt_task():
    """
    Task for speech-to-text conversion.
    """
    logging.debug("stt task start.")
    py_audio = google_api.init_pyaudio()
    speech_client = google_api.init_speech_to_text()
    logging.debug("init stt.")

    while True:
        logging.debug("stt wait for all init task has done / tts work has finished ... ...")
        should_stt = stt_queue.get()
        stt_queue.task_done()
        logging.info(f"should_stt: {should_stt}, ai_on:{ai_on}")
        while not stt_queue.empty(): # clean queue, get the last element, stt need just one
            should_stt = stt_queue.get()
            logging.info(f"should_stt: {should_stt}")
            stt_queue.task_done()

        if not should_stt:
            continue
        logging.debug("stt task start loop, listening ... ...")
        user_input, stream = google_api.start_speech_to_text(speech_client, py_audio)
        logging.debug(f"voice input: {user_input}")

        move_key = get_move_cmd(user_input, move_cmd_functions)
        sys_cmd_key, sys_cmd_func = get_sys_cmd(user_input, sys_cmds_functions)
        global cur_voice
        if ai_on:
            lang, cur_voice = get_voice(user_input)

        if not user_input:
            logging.debug(f"no input!")
            stt_queue.put(True)
        elif sys_cmd_key:
            logging.debug(f"sys cmd: {sys_cmd_key}")
            sys_cmd_func()
        elif "見上げ" in user_input:
            movement_queue.put("look up")
            output_text_queue.put("OK, my friend.")
        elif "踊り" in user_input or "dance" in user_input:
            #movement_queue.put(move_key)
            movement_queue.put("dance")
            output_text_queue.put("OK, let's dance.")
        elif "sit" == move_key or "action" == move_key :
            movement_queue.put(move_key)
            output_text_queue.put("OK, my friend.")
        elif "walk" in user_input or "come" in user_input or "go" in user_input or "行" in user_input:
            movement_queue.put("move forwards")
            output_text_queue.put("My friend, here I come.")
        elif move_key:
            movement_queue.put(move_key)
            output_text_queue.put(f"OK, my friend, {move_key} immediatly.")
        elif not ai_on:
            logging.info(f"ai is not on, do not use gemini")
            stt_queue.put(True)
            time.sleep(0.5)
            google_api.stop_speech_to_text(stream)
            time.sleep(0.5)
            continue
        elif "game" in user_input or "play" in user_input or "じゃんけん" in user_input:
            #movement_queue.put("trot")
            output_text_queue.put(GAME_TEXT)
        elif lang:
            logging.debug(f"switch language: {lang}")
            user_input += f", Please reply in {lang}."
            input_text_queue.put(user_input)
            stt_queue.put(False)
        else:
            logging.debug(f"put voice text to input queue: {user_input}")
            input_text_queue.put(user_input)
            stt_queue.put(False)
        time.sleep(0.5)
        google_api.stop_speech_to_text(stream)
        time.sleep(0.5)


def gemini_task():
    """
    Task for handling Gemini AI interactions.
    """
    logging.debug("gemini task start.")
    conversation = google_api.create_conversation()
    init_input =  "From here on, always answer as if a human being is saying things off the top of his head which is always concise, relevant and contains a good conversational tone. so you will only and only answer in one breathe responses. If the input contains a language other than English, for example, language A, please answer the question in language A."
    response = google_api.ai_text_response(conversation, init_input)
    logging.debug(f"init llm and first response: {response}")

    multi_model = ChatVertexAI(model="gemini-2.0-flash")
    with Image.open(f"{RES_DIR}/Trot.jpg") as image:
        logging.debug(f"Opened image: 320p")
        if image is None:
            logging.debug("No image captured!")
        else:
            text_prompt = "what is this?"
            response = google_api.ai_image_response(multi_model, image=image, text=text_prompt)
    logging.debug(f"init vision model and first response: {response}")
    stt_queue.put(True)
    image = Image.open(f"{RES_DIR}/hello.png")
    image_queue.put(image)

    while True:
        logging.debug("tts wait for gemini responese text... ...")
        input_text = input_text_queue.get()
        input_text_queue.task_done()
        if not ai_on:
            continue

        logging.debug(f"user input from voice: {input_text}")
        stt_queue.put(False)
        user_input = input_text
        response = ""
        if not user_input:
            logging.debug(f"no input!")

        elif "photo" in user_input or "picture" in user_input or "xpression" in user_input or "写真" in user_input:
            ms_start = int(time.time() * 1000)
            logging.debug(f"detect pic start!")
            image = media_api.take_photo()
            logging.debug(f"take photo finish!")

            if image:
                image = media_api.resize_image_to_width(image, 320)
                logging.debug(f"resize photo finish!")
                #response = google_api.ai_image_response(multi_model, image=image, text="この写真を読んで俳句を作ってください。大喜利大会なのでそれも踏まえて考えてください。俳句の前には必ず「いい写真ですね。では一句。」とつけてください。")
                response = google_api.ai_image_response(multi_model, image=image, text=user_input)
                image_queue.put(image)
            else:
                response = google_api.ai_text_response(conversation, user_input)

            logging.debug(f"detect pic end!")
            ms_end = int(time.time() * 1000)
            logging.debug(f"ai_response end, delay = {ms_end - ms_start}ms")
            logging.debug("picture response end: {response}")
            output_text_queue.put(response)

        elif "rock paper scissors" in user_input:
            ms_start = int(time.time() * 1000)
            logging.debug(f"play game take photo")
            human_image = media_api.take_photo()
            logging.debug(f"play game take photo finish")
            #human_image = media_api.resize_image_to_width(human_image, 320)
            #logging.debug(f"resize photo finish!")

            gestures = ["rock", "paper", "scissors"]
            random.seed(int(time.time()))
            puppy_gesture = random.choice(gestures)
            logging.debug(f"puppy_gesture is: {puppy_gesture}")
            puppy_image = Image.open(f"{RES_DIR}/{puppy_gesture}.jpg")
            image_queue.put(puppy_image)

            human_gesture = google_api.ai_image_response(multi_model, image=human_image, text=user_input)
            human_gesture = human_gesture.replace(' ', '')
            logging.debug(f"human_gesture is: {human_gesture}")

            win_conditions = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
            result = "You win!" if win_conditions.get(human_gesture) == puppy_gesture else ("It's a tie!" if human_gesture == puppy_gesture else "You lose!")
            response = result
            output_text_queue.put(response)
            image = Image.open(f"{RES_DIR}/logo.png")
            image_queue.put(image)
        else:
            logging.debug("text response start!")
            #gif_queue.put(True)
            response = google_api.ai_text_response(conversation, user_input)
            logging.debug("text response end: {response}")
            output_text_queue.put(response)
        time.sleep(0.05)


def tts_task():
    """
    Task for text-to-speech conversion and audio output.
    """
    logging.debug("tts task start.")
    os.system("amixer -c 0 sset 'Headphone' 100%")
    tts_client, voice, audio_config = google_api.init_text_to_speech()
    global voice0, cur_voice
    voice0 = voice
    cur_voice = voice
    logging.debug("init tts end.")
    while True:
        logging.debug("tts wait for gemini responese text... ...")
        out_text = output_text_queue.get()
        out_text = cut_text_by_last_period(out_text)
        output_text_queue.task_done()
        out_text = remove_emojis(out_text).replace('*', '')
        if not out_text or not ai_on:
            stt_queue.put(True)
            continue

        stt_queue.put(False)
        google_api.text_to_speech(out_text, tts_client, cur_voice, audio_config)
        
        if GAME_TEXT == out_text:
            text = "I am playing rock paper scissors. Tell me what is this? rock paper or scissors? Only in one word, no punctuation and all in lowercase."
            input_text_queue.put(text)
        else:
            time.sleep(0.02)
            stt_queue.put(True)


def gif_task():
    """
    Task for handling GIF display.
    """
    logging.debug("gif task start.")
    gif_player = media_api.init_gifplayer(f"{RES_DIR}/")
    logging.debug("init gif end.")
    while True:
        logging.debug("wait for gif show... ...")
        should_show_gif = gif_queue.get()
        gif_queue.task_done()
        if should_show_gif:
            media_api.show_gif(gif_player)
        time.sleep(0.02)

def image_task():
    """
    Task for handling image display.
    """
    logging.debug("image task start.")
    logging.debug("init image end.")
    while True:
        logging.debug("wait for image show... ...")
        image = image_queue.get()
        image_queue.task_done()
        media_api.show_image(image)
        time.sleep(0.02)

def move_task():
    """
    Task for handling movement commands.
    """
    logging.debug("move task start.")
    logging.debug("init move end.")
    while True:
        logging.debug("wait for movement command ... ...")
        move_command = movement_queue.get()
        logging.debug(f"movement command is: {move_command}")
        movement_queue.task_done()
        if move_command in move_cmd_functions:
            move_cmd_functions[move_command]()
        else:
            logging.debug("No this command")
        time.sleep(1)

def main():
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.DEBUG
    )
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    #parent_dir = os.path.dirname(current_dir)
    os.chdir(os.path.dirname(current_dir))
    logging.debug(f"init chdir: {current_dir}")

    from dotenv import load_dotenv
    load_dotenv(dotenv_path='./.env')
    api_path = os.environ.get('API_KEY_PATH', '')
    logging.debug(f"api key path: {api_path}")
    if os.path.exists(api_path):
        logging.debug("init credentials start.")
        google_api.init_credentials(api_path)
        logging.debug("init credentials end.")
    else:
        logging.debug("credentials file not exist.")

    lang_code = os.environ.get('LANGUAGE_CODE', 'en-US')
    lang_name = os.environ.get('LANGUAGE_NAME', 'en-US-Standard-E')
    google_api.set_language(lang_code, lang_name)

    stt_thread = threading.Thread(target=stt_task)
    stt_thread.start()
    logging.debug("stt thread start.")

    gemini_thread = threading.Thread(target=gemini_task)
    gemini_thread.start()
    logging.debug("gemini thread start.")

    tts_thread = threading.Thread(target=tts_task)
    tts_thread.start()

    gif_thread = threading.Thread(target=gif_task)
    gif_thread.start()

    image_thread = threading.Thread(target=image_task)
    image_thread.start()

    move_thread = threading.Thread(target=move_task)
    move_thread.start()

    stt_thread.join()
    gemini_thread.join()
    tts_thread.join()
    gif_thread.join()
    image_thread.join()
    move_thread.join()


if __name__ == '__main__':
    main()
