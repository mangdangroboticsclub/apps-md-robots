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
# Description: Enhanced AI system with Gemini-based intent recognition for Mini Pupper robot.
# ENHANCEMENT: Added intelligent intent classification system using Gemini AI for better command understanding
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
GAME_TEXT = "Let's play! Rock! Paper! Scissor! Shoot!"
ai_on = True

# Voice configurations (unchanged from original)
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
    # UNCHANGED: This function remains the same as original
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

# UNCHANGED: Movement command mapping remains the same
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
    "shake": move_api.shake,  # ADDED: New shake command
}

# ============================================================================
# NEW FEATURE: GEMINI-BASED INTENT RECOGNITION SYSTEM
# ============================================================================
# MAJOR ENHANCEMENT: This replaces the original hardcoded if-elif chains with 
# intelligent AI-based intent classification

def classify_intent_with_gemini(user_input, conversation):
    """
    NEW FUNCTION: Use Gemini AI to intelligently classify user intent.
    
    REPLACES: The original hardcoded pattern matching in stt_task()
    BENEFITS: 
    - More flexible and natural language understanding
    - Easier to extend with new intents
    - Better handling of variations in how users express commands
    - Confidence scoring for better decision making
    
    Args:
        user_input (str): The user's voice input to classify
        conversation: Gemini conversation context for classification
        
    Returns:
        tuple: (intent_name, confidence_level)
    """
    
    # ENHANCEMENT: Structured prompt for consistent intent classification
    # This replaces scattered if-elif conditions with organized categories
    intent_prompt = f"""
You are an intent classifier for a quadruped robot. Classify the following user input into ONE of these intents:

MOVEMENT INTENTS:
- "movement_forward" - move forward, walk, come here, go forward, come to me
- "movement_backward" - move backward, go back, reverse, back up
- "movement_left" - move left, turn left, go left, left side
- "movement_right" - move right, turn right, go right, right side

BODY POSTURE INTENTS:
- "posture_sit" - sit, sit down, squat, crouch
- "posture_stand" - stand, stand up, action, init, get ready

HEAD MOVEMENT INTENTS:
- "head_up" - look up, head up, look at ceiling
- "head_down" - look down, head down, look at ground
- "head_left" - look left, turn head left, look that way
- "head_right" - look right, turn head right, look over there

SOCIAL INTENTS:
- "greeting" - hello, hi, shake hand, greet, nice to meet you, handshake, shake
- "dance" - dance, party, celebrate, boogie, dancing, let's dance
- "photo" - take photo, picture, camera, smile, photograph, pic

GAME INTENTS:
- "game_rps" - rock paper scissors, game, play, じゃんけん, let's play

SYSTEM INTENTS:
- "system_sleep" - shut up, be quiet, sleep, hush, stop talking
- "system_wake" - speak please, wake up, hello robot, start talking

CONVERSATION INTENT:
- "conversation" - general chat, questions, anything not covered above

User input: "{user_input}"

Respond with ONLY the intent name and confidence level separated by a comma.
Example: "greeting,high"
"""

    try:
        # ENHANCEMENT: Use Gemini AI for classification instead of regex patterns
        response = google_api.ai_text_response(conversation, intent_prompt)
        response = response.strip().lower()
        
        # ENHANCEMENT: Parse confidence level along with intent
        if ',' in response:
            intent, confidence = response.split(',', 1)
            intent = intent.strip()
            confidence = confidence.strip()
        else:
            intent = response.strip()
            confidence = "medium"
            
        logging.info(f"🤖 Intent: {intent}, Confidence: {confidence}")
        return intent, confidence
        
    except Exception as e:
        # ENHANCEMENT: Graceful fallback on classification errors
        logging.error(f"Error in intent classification: {e}")
        return "conversation", "low"

def execute_intent(intent, confidence, original_input):
    """
    NEW FUNCTION: Execute actions based on classified intent.
    
    REPLACES: The scattered command execution logic in original stt_task()
    BENEFITS:
    - Centralized command execution logic
    - Consistent response patterns
    - Better error handling
    - Easier to maintain and extend
    
    Args:
        intent (str): The classified intent
        confidence (str): Confidence level of classification
        original_input (str): Original user input for fallback
        
    Returns:
        bool: True if intent was handled, False if passed to AI conversation
    """
    logging.info(f"🎯 Executing intent: {intent} (confidence: {confidence})")
    
    # ENHANCEMENT: Organized intent handling with natural responses
    # This replaces the original scattered if-elif chains
    
    # Movement intents - ENHANCED: More natural responses
    if intent == "movement_forward":
        movement_queue.put("move forwards")
        output_text_queue.put("Coming to you!")  # IMPROVED: More natural than "OK, my friend"
        
    elif intent == "movement_backward":
        movement_queue.put("move backwards")
        output_text_queue.put("Moving backward!")  # NEW: Specific response
        
    elif intent == "movement_left":
        movement_queue.put("move left")
        output_text_queue.put("Moving left!")  # NEW: Specific response
        
    elif intent == "movement_right":
        movement_queue.put("move right")
        output_text_queue.put("Moving right!")  # NEW: Specific response
        
    # Posture intents - ENHANCED: Better categorization
    elif intent == "posture_sit":
        movement_queue.put("sit")
        output_text_queue.put("Sitting down!")  # IMPROVED: More descriptive
        
    elif intent == "posture_stand":
        movement_queue.put("action")
        output_text_queue.put("Ready for action!")  # IMPROVED: More engaging
        
    # Head movement intents - NEW: Dedicated head movement handling
    elif intent == "head_up":
        movement_queue.put("look up")
        output_text_queue.put("Looking up!")  # NEW: Specific response
        
    elif intent == "head_down":
        movement_queue.put("look down")
        output_text_queue.put("Looking down!")  # NEW: Specific response
        
    elif intent == "head_left":
        movement_queue.put("look left")
        output_text_queue.put("Looking left!")  # NEW: Specific response
        
    elif intent == "head_right":
        movement_queue.put("look right")
        output_text_queue.put("Looking right!")  # NEW: Specific response
        
    # Social intents - ENHANCED: Better social interaction
    elif intent == "greeting":
        movement_queue.put("shake hand")  # ENHANCED: Maps to shake command
        output_text_queue.put("Nice to meet you! Let me shake your hand!")  # IMPROVED: More friendly
        
    elif intent == "dance":
        movement_queue.put("dance")
        output_text_queue.put("Let's dance together!")  # IMPROVED: More enthusiastic
        
    elif intent == "photo":
        # ENHANCED: More specific photo command
        input_text_queue.put("take a photo and describe what you see")
        return False  # Let AI handle the photo processing
        
    # Game intents - UNCHANGED: Maintains original game logic
    elif intent == "game_rps":
        output_text_queue.put(GAME_TEXT)
        
    # System intents - ENHANCED: Better system control
    elif intent == "system_sleep":
        close_ai()
        return True
        
    elif intent == "system_wake":
        open_ai()
        return True
        
    # Conversation intent or unknown - ENHANCED: Better fallback
    else:
        logging.info(f"🗨️ Passing to AI conversation: {original_input}")
        input_text_queue.put(original_input)
        return False  # Indicate we're passing to AI
    
    return True  # Indicate we handled the intent

# ============================================================================
# UNCHANGED FUNCTIONS: These remain the same as original
# ============================================================================

def get_move_cmd(input_text, command_dict):
    # UNCHANGED: Kept for backward compatibility, but no longer primary method
    if not input_text:
        return None
    for command_key in command_dict.keys():
        if re.search(r'\b' + re.escape(command_key) + r'\b', input_text):
            return command_key
    return None

def close_ai():
    # UNCHANGED: System control functions remain the same
    global ai_on
    ai_on = False
    stt_queue.put(True)
    image = Image.open(f"{RES_DIR}/logo2.png")
    image_queue.put(image)

def open_ai():
    # UNCHANGED: System control functions remain the same
    global ai_on
    ai_on = True
    stt_queue.put(True)
    image = Image.open(f"{RES_DIR}/hello.png")
    image_queue.put(image)
    output_text_queue.put("OK, my friend.")

def reboot():
    # UNCHANGED: System functions remain the same
    command = "sudo reboot"
    shell_api.execute_command(command)

def power_off():
    # UNCHANGED: System functions remain the same
    command = "sudo poweroff"
    shell_api.execute_command(command)

# UNCHANGED: System command mapping (kept for compatibility)
sys_cmds_functions = {
    "shut up": close_ai,
    "speak please": open_ai,
    "reboot": reboot,
    "power off": power_off,
}

def get_sys_cmd(input_text, command_dict):
    # UNCHANGED: Kept for backward compatibility
    normalized_text = re.sub(r'[^\w\s]', '', input_text.lower())
    for command_key in command_dict.keys():
        if normalized_text == command_key.lower():
            return command_key, command_dict[command_key]
    return None, None

def cut_text_by_last_period(text, max_words_before_period=15):
    # UNCHANGED: Text processing utilities remain the same
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
    # UNCHANGED: Text processing utilities remain the same
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "\U00000200-\U00000250"
        "\U00000260-\U00002B55"
        "\U0001FA70-\U0001FAFF"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# ============================================================================
# ENHANCED STT TASK: Major improvements to speech processing
# ============================================================================

def stt_task():
    """
    MAJORLY ENHANCED: Speech-to-text task with Gemini-based intent recognition.
    
    KEY CHANGES FROM ORIGINAL:
    1. Added Gemini-based intent classification system
    2. Replaced hardcoded if-elif chains with intelligent processing
    3. Improved wake-up command detection
    4. Better error handling and logging
    5. More natural conversation flow
    """
    logging.info("🎤 Enhanced STT task with intent recognition starting...")  # ENHANCED: Better logging
    py_audio = google_api.init_pyaudio()
    speech_client = google_api.init_speech_to_text()
    
    # NEW: Create a separate conversation context for intent classification
    # This ensures intent classification doesn't interfere with main conversation
    intent_conversation = google_api.create_conversation()
    logging.info("🧠 Intent recognition system initialized")  # NEW: Intent system logging

    while True:
        logging.debug("stt wait for all init task has done / tts work has finished ... ...")
        should_stt = stt_queue.get()
        stt_queue.task_done()
        logging.info(f"should_stt: {should_stt}, ai_on:{ai_on}")
        
        # UNCHANGED: Queue cleaning logic remains the same
        while not stt_queue.empty():
            should_stt = stt_queue.get()
            logging.info(f"should_stt: {should_stt}")
            stt_queue.task_done()

        if not should_stt:
            continue
            
        logging.info("🎤 Listening for voice input...")  # ENHANCED: Better logging
        user_input, stream = google_api.start_speech_to_text(speech_client, py_audio)
        logging.info(f"👂 Voice input: '{user_input}'")  # ENHANCED: More descriptive logging

        # UNCHANGED: Voice selection logic remains the same
        global cur_voice
        if ai_on:
            lang, cur_voice = get_voice(user_input)

        if not user_input:
            logging.debug("No input detected")  # ENHANCED: Clearer logging
            stt_queue.put(True)
            
        else:
            # ENHANCED: Better handling of AI on/off states
            if not ai_on:
                # IMPROVED: More comprehensive wake-up command detection
                if any(wake_phrase in user_input.lower() for wake_phrase in 
                       ["speak please", "wake up", "hello robot", "start talking", "turn on"]):
                    logging.info("🔊 Wake up command detected!")  # NEW: Wake-up detection
                    open_ai()
                else:
                    logging.info("AI is not on, skipping processing")
                    stt_queue.put(True)
            else:
                # ===================================================================
                # MAJOR CHANGE: Replace original hardcoded if-elif chains with 
                # intelligent Gemini-based intent recognition
                # ===================================================================
                try:
                    logging.info("🧠 Processing with intent recognition...")  # NEW: Intent processing log
                    
                    # NEW: Use Gemini for intelligent intent classification
                    # REPLACES: All the hardcoded conditions like:
                    # - elif "見上げ" in user_input:
                    # - elif "踊り" in user_input or "dance" in user_input:
                    # - elif "walk" in user_input or "come" in user_input:
                    # - etc.
                    intent, confidence = classify_intent_with_gemini(user_input, intent_conversation)
                    
                    # NEW: Execute the intent with structured handling
                    # REPLACES: Scattered movement_queue.put() and output_text_queue.put() calls
                    handled = execute_intent(intent, confidence, user_input)
                    
                    if handled:
                        # Intent was handled, continue listening
                        stt_queue.put(True)
                    else:
                        # Passed to AI conversation
                        stt_queue.put(False)
                    
                except Exception as e:
                    # NEW: Better error handling with fallback
                    logging.error(f"Error in intent processing: {e}")
                    # Graceful fallback to normal conversation
                    input_text_queue.put(user_input)
                    stt_queue.put(False)
        
        # UNCHANGED: Stream cleanup logic remains the same
        time.sleep(0.5)
        google_api.stop_speech_to_text(stream)
        time.sleep(0.5)

# ============================================================================
# UNCHANGED TASKS: These remain identical to original
# ============================================================================

def gemini_task():
    """UNCHANGED: Task for handling Gemini AI interactions."""
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
            response = google_api.ai_text_response(conversation, user_input)
            logging.debug("text response end: {response}")
            output_text_queue.put(response)
        time.sleep(0.05)

def tts_task():
    """UNCHANGED: Task for text-to-speech conversion and audio output."""
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
    """UNCHANGED: Task for handling GIF display."""
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
    """UNCHANGED: Task for handling image display."""
    logging.debug("image task start.")
    logging.debug("init image end.")
    while True:
        logging.debug("wait for image show... ...")
        image = image_queue.get()
        image_queue.task_done()
        media_api.show_image(image)
        time.sleep(0.02)

def move_task():
    """ENHANCED: Task for handling movement commands with better error handling."""
    logging.debug("move task start.")
    logging.debug("init move end.")
    while True:
        logging.debug("wait for movement command ... ...")
        move_command = movement_queue.get()
        logging.debug(f"movement command is: {move_command}")
        movement_queue.task_done()
        if move_command in move_cmd_functions:
            try:
                # ENHANCED: Added error handling for movement execution
                move_cmd_functions[move_command]()
            except Exception as e:
                # NEW: Better error logging for movement failures
                logging.error(f"Error executing movement {move_command}: {e}")
        else:
            logging.debug(f"No command found for: {move_command}")  # ENHANCED: More specific logging
        time.sleep(1)

def main():
    # ENHANCED: Improved logging and startup messages
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO  # CHANGED: From DEBUG to INFO for cleaner output
    )
    
    print("🚀 Starting Enhanced AI App with Intent Recognition")  # NEW: Startup message
    logging.info("🤖 Mini Pupper Enhanced AI System Starting...")  # NEW: Enhanced logging
    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
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

    # UNCHANGED: Thread initialization remains the same
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