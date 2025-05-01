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
# Description: This script is designed to control a robot by sending various commands through UDP communication to simulate
# joystick inputs. It includes functions for different robot movements and an interactive command-line interface to issue these commands.
#
# Movement Test Method: Type the following commands and press enter: 'init', 'lower', 'raise', 'left roll', 'right roll', 'trot',
# 'trot1', 'squat', 'forward', 'backward', 'left', 'right', 'look up', 'look down', 'loow left', 'look upper left', 'look lower left',
# 'look right', 'look upper right', 'look lower right'
#

import logging
import os
import asyncio
import sys
import time
import threading
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.UDPComms import Publisher


fake_joy = Publisher(8830, "127.0.0.1")
#fake_joy = Publisher(8830, "192.168.1.101")

_MSG = {"L1": False,
        "R1": False,
        "L2": -1.0,
        "R2": -1.0,
        "x": False,
        "square": False,
        "circle": False,
        "triangle": False,
        "lx": 0.0,
        "ly": 0.0,
        "rx": 0.0,
        "ry": 0.0,
        "dpadx": 0,
        "dpady": 0,
        "message_rate": 20
        }

MSG_L1_TRUE = {**_MSG, "L1": True}
MSG_L1_FALSE = {**_MSG, "L1": False}
MSG_R1 = {**_MSG, "R1": True}
MSG_X = {**_MSG, "x": True}
MSG_SQUARE = {**_MSG, "square": True}
MSG_CIRCLE = {**_MSG, "circle": True}
MSG_TRIANGLE = {**_MSG, "triangle": True}
MSG_RATE_10 = {**_MSG, "message_rate": 10}
UPDATE_INTERVAL = 0.1

def send_msgs(msgs):
    """
    Send a series of messages with a delay between each.

    Parameters:
    - msgs (list): A list of messages to be sent.
    """

    def send_updates():
        for msg in msgs:
            fake_joy.send(msg)
            time.sleep(UPDATE_INTERVAL)

    thread = threading.Thread(target=send_updates)
    thread.start()

# Active pupyy, fake "L1" button
def init_movement():
    """
    Activate the robot and initiate a movement by simulating the "L1" button press.
    """
    msg_raise = {**_MSG, "dpady": 1}
    send_msgs([MSG_L1_TRUE, MSG_L1_FALSE, msg_raise])

# Active pupyy, send command to do lower movement
def lower_body(duration=2):
    """
    Make the robot lower its body.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "dpady": -1}
    stop_msg = {**_MSG, "dpady": 0.8}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def raise_body(duration=2):
    """
    Make the robot raise its body.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "dpady": 1}
    stop_msg = {**_MSG, "dpady": -0.8}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def left_body(duration=2):
    """
    Make the robot twist left its body.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "dpadx": -1}
    stop_msg = {**_MSG, "dpadx": 0.8}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def right_body(duration=2):
    """
    Make the robot twist right its body.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "dpadx": 1}
    stop_msg = {**_MSG, "dpadx": -0.8}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def trot():
    """
    Make the robot start trot.

    """
    msg_press = {**_MSG, "R1": True}
    msg_release = {**_MSG, "R1": False}
    msg = [msg_press, msg_release]
    send_msgs(msg)

def delay_trot(delay):
    time.sleep(delay)
    trot()

def trot_duration(duration=1):
    """
    Make the robot trot.

    Parameters:
    - duration (float): The duration of the movement.
    """
    trot()
    thread = threading.Thread(target=delay_trot, args=(duration,))
    thread.start()

def squat(duration=4):
    """
    Make the robot squat.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "ry": 1.0}
    stop_msg = {**_MSG, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def move_forward(duration=2):
    """
    Make the robot move forward.

    Parameters:
    - duration (float): The duration of the movement.
    """
    msg_trot_press = {**_MSG, "R1": True}
    msg_trot_release = {**_MSG, "R1": False}
    start_msg = {**_MSG, "ly": 1.0}
    stop_msg = {**_MSG, "ly": 0.0}
    msgs = [msg_trot_press, msg_trot_release]
    num = int(duration / UPDATE_INTERVAL)
    start_msgs = [start_msg] * num
    msgs.extend(start_msgs)
    msgs.append(stop_msg)
    msgs.append(msg_trot_press)
    msgs.append(msg_trot_release)
    send_msgs(msgs)

def move_backward(duration=2):
    """
    Make the robot move backward.

    Parameters:
    - duration (float): The duration of the movement.
    """
    msg_trot_press = {**_MSG, "R1": True}
    msg_trot_release = {**_MSG, "R1": False}
    start_msg = {**_MSG, "ly": -1.0}
    stop_msg = {**_MSG, "ly": 0.0}
    msgs = [msg_trot_press, msg_trot_release]
    num = int(duration / UPDATE_INTERVAL)
    start_msgs = [start_msg] * num
    msgs.extend(start_msgs)
    msgs.append(stop_msg)
    msgs.append(msg_trot_press)
    msgs.append(msg_trot_release)
    send_msgs(msgs)

def move_left(duration=2):
    """
    Make the robot move left.

    Parameters:
    - duration (float): The duration of the movement.
    """
    msg_trot_press = {**_MSG, "R1": True}
    msg_trot_release = {**_MSG, "R1": False}
    start_msg = {**_MSG, "lx": -0.5}
    stop_msg = {**_MSG, "ly": 0.0}
    msgs = [msg_trot_press, msg_trot_release]
    num = int(duration / UPDATE_INTERVAL)
    start_msgs = [start_msg] * num
    msgs.extend(start_msgs)
    msgs.append(stop_msg)
    msgs.append(msg_trot_press)
    msgs.append(msg_trot_release)
    send_msgs(msgs)

def move_right(duration=2):
    """
    Make the robot move right.

    Parameters:
    - duration (float): The duration of the movement.
    """
    msg_trot_press = {**_MSG, "R1": True}
    msg_trot_release = {**_MSG, "R1": False}
    start_msg = {**_MSG, "lx": 0.5}
    stop_msg = {**_MSG, "ly": 0.0}
    msgs = [msg_trot_press, msg_trot_release]
    num = int(duration / UPDATE_INTERVAL)
    start_msgs = [start_msg] * num
    msgs.extend(start_msgs)
    msgs.append(stop_msg)
    msgs.append(msg_trot_press)
    msgs.append(msg_trot_release)
    send_msgs(msgs)

def look_up(duration=2):
    """
    Make the robot look up.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "ry": 1.0}
    stop_msg = {**_MSG, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_down(duration=2):
    """
    Make the robot look down.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "ry": -1.0}
    stop_msg = {**_MSG, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_left(duration=2):
    """
    Make the robot look left.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": -0.3}
    stop_msg = {**_MSG, "rx": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_upperleft(duration=2):
    """
    Make the robot look upper left.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": -0.6, "ry": 1.0}
    stop_msg = {**_MSG, "rx": 0.0, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_leftlower(duration=2):
    """
    Make the robot look left lower.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": -0.6, "ry": -1.0}
    stop_msg = {**_MSG, "rx": 0.0, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_right(duration=2):
    """
    Make the robot look right.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": 0.3}
    stop_msg = {**_MSG, "rx": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_upperright(duration=2):
    """
    Make the robot look upper right.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": 0.6, "ry": 1.0}
    stop_msg = {**_MSG, "rx": 0.0, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def look_rightlower(duration=2):
    """
    Make the robot look right lower.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": 0.6, "ry": -1.0}
    stop_msg = {**_MSG, "rx": 0.0, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

def dance(duration=2):
    """
    Make the robot dance.

    Parameters:
    - duration (float): The duration of the movement.
    """
    start_msg = {**_MSG, "rx": -0.3}
    stop_msg = {**_MSG, "rx": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

    time.sleep(duration*1.5)
 
    trot()
    thread = threading.Thread(target=delay_trot, args=(duration,))
    thread.start()

    time.sleep(duration*1.5)

    start_msg = {**_MSG, "dpady": 1}
    stop_msg = {**_MSG, "dpady": -0.8}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

    time.sleep(duration*1.5)

    start_msg = {**_MSG, "rx": 0.3}
    stop_msg = {**_MSG, "rx": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

    time.sleep(duration*1.5)

    start_msg = {**_MSG, "ry": 1.0}
    stop_msg = {**_MSG, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)

    time.sleep(duration*1.5)

    start_msg = {**_MSG, "ry": -1.0}
    stop_msg = {**_MSG, "ry": 0.0}
    num = int(duration / UPDATE_INTERVAL)
    reduction_count = num // 2
    msgs = [start_msg] * (num - reduction_count)
    stop_msgs = [stop_msg] * reduction_count
    msgs.extend(stop_msgs)
    send_msgs(msgs)


import argparse
async def main(args):
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO
    )

    current_file_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_file_path))
    logging.debug(f"init chdir: {os.path.dirname(current_file_path)}")

    logging.debug("logging setup!\n")
    #init_movement()
    move_api_map = {
        "init": init_movement,
        "lower": lower_body,
        "raise": raise_body,
        "left roll": left_body,
        "right roll": right_body,
        "trot": trot,
        "trot1": trot_duration,
        "squat": squat,
        "forward": move_forward,
        "backward": move_backward,
        "left": move_left,
        "right": move_right,
        # "bow": bow,
        "look up": look_up,
        "look down": look_down,
        "look left": look_left,
        "look upper left": look_upperleft,
        "look lower left": look_leftlower,
        "look right": look_right,
        "look upper right": look_upperright,
        "look lower right": look_rightlower,
        "dance": dance,
    }
    async_move_api_map = {
        #"trot": trot,
        #"trot1": trot_for_1sec,
    }

    if args.api:
        func = move_api_map[args.api]
        func()
        sys.exit()

    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input == "exit":
            break
        elif user_input in async_move_api_map:
            logging.info(f"{user_input} start:")
            await async_move_api_map[user_input]()
            logging.info(f"{user_input} end:")
        elif user_input in move_api_map:
            logging.info(f"{user_input} start:")
            move_api_map[user_input]()
            logging.info(f"{user_input} end:")
        else:
            user_input = "init"
            move_api_map[user_input]()
            print("Unknown command. Please try again.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute move api.')
    parser.add_argument('--api', type=str, help='Execute the move api without interactive prompt.')

    args = parser.parse_args()
    asyncio.run(main(args))
