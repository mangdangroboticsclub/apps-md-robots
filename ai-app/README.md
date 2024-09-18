# Mini Pupper generative ai app
This is an app run on mini pupper, we integrate gemini(google llm), we can talk with mini pupper, you can set language as you like. 

## Install dependency libs.
```
cd ~/apps-md-robots/ai-app/
sudo apt-get install -y python3-pyaudio
sudo pip install -r requirements.txt
```

## Config environment: edit ".env" file.

Set your google cloud API key and your language in .env file. Set your key path in .env file like: API_KEY_PATH=/home/ubuntu/xxxx.json, and set your language code and name refer to: https://cloud.google.com/text-to-speech/docs/voices
 
```
cp ../env.example ../.env

vim ../.env

```

## Run app
```
python ai_app.py
```
