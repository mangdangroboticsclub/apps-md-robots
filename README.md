# MD Robot Starter Kits AI Demos
[MangDang](https://www.mangdang.net/) Online channel: [Discord](https://discord.gg/xJdt3dHBVw), [FaceBook](https://www.facebook.com/groups/716473723088464), [YouTube](https://www.youtube.com/channel/UCqHWYGXmnoO7VWHmENje3ug/featured), [Twitter](https://twitter.com/LeggedRobot)

MD Robot Starter Kits: Unlock your AI Dream Job.
Make robotics easier for schools, homeschool families, enthusiasts and beyond.

- Generative AI: Support ChatGPT, Gemini and Claude
- ROS: support ROS2(Humble) SLAM & Navigation robot dog at low-cost price
- OpenCV: support OpenCV official OAK-D-Lite 3D camera module and single MIPI camera
- Open-source: DIY and customize what you want.
- Raspberry Pi: it’s super expandable, endorsed by Raspberry Pi.

## Overview

The AI applications can be run on MD legged Robot Kits. 
The default branch works on Mini Pupper2(G), please click the picture and refer to the demo video.

[![Run on MD-Puppy1](https://img.youtube.com/vi/mIDuIZCevIg/0.jpg)](https://www.youtube.com/watch?v=mIDuIZCevIg)

The new branch for Mini Pupper will be added soon, please click the picture and refer to the demo video.

[![Run on MD-Puppy1](https://img.youtube.com/vi/bvH-lA1IHig/0.jpg)](https://www.youtube.com/watch?v=bvH-lA1IHig)

## Preparation

Please make sure Mini Pupper 2(G) can walk first. 

- Download and flash the [pre-built base image file (like v2_stanford*.img) ](https://drive.google.com/drive/folders/1ZF4vulHbXvVF4RPWWGxEe7rxcJ9LyeEu?usp=sharing), or 
- Build the base environment by yourself. 

Step 1: Install the [BSP repo](https://github.com/mangdangroboticsclub/mini_pupper_2_bsp)

Step 2: Install the [quadruped repo](https://github.com/mangdangroboticsclub/StanfordQuadruped )


## Install

For the video guide, please click the picture and refer to the demo video.

[![Installation Guide](https://img.youtube.com/vi/1AkhJi2o8rM/0.jpg)](https://www.youtube.com/watch?v=1AkhJi2o8rM)


Clone this repo, and install denpendency libs.
```
cd ~
git clone https://github.com/mangdangroboticsclub/apps-md-robots
cd apps-md-robots
sudo apt-get install -y python3-pyaudio
sudo pip install -r requirements.txt

```


Set your google cloud API key in env.example file and then start.
 
```
cp env.example .env

#and then edit .env file, set your key path in .env file, like: API_KEY_PATH=/home/ubuntu/xxxx.josn 
vim .env



```

## Run
run app demos, eg. ai_apps
 
```
cd ai_apps/
python ai_app.py
```

