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
# Description: This script coordinates multiple concurrent tasks, utilizing queues for inter-task
# communication and synchronization, to create a responsive and interactive AI system.
#

import queue


# stt make input text into this queue, and gemini get text from this queue
input_text_queue = queue.Queue()


#gemini response text into this queue, and tts get text froom this queue
output_text_queue = queue.Queue()


#gif show, input True or False
gif_queue = queue.Queue()


#image show, input PIL image
image_queue = queue.Queue()


#movement, input movement text: "sit"/"walk"
movement_queue = queue.Queue()


# stt queue, when puppy is speaking, we should not stt, put False into the queue, after speak finish, put True into queue
stt_queue = queue.Queue()
