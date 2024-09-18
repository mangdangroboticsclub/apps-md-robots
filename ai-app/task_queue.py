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
