# Mini Pupper 2 Google Gemini Generative AI Demos
[MangDang](https://www.mangdang.net/) Online channel: [Discord](https://discord.gg/xJdt3dHBVw), [FaceBook](https://www.facebook.com/groups/716473723088464), [YouTube](https://www.youtube.com/channel/UCqHWYGXmnoO7VWHmENje3ug/featured), [Twitter](https://twitter.com/LeggedRobot)

Mini Pupper will make robotics easier for schools, homeschool families, enthusiasts and beyond.

- Generative AI: Support Google Gemini
- ROS: support ROS2(Humble) SLAM & Navigation robot dog at low-cost price
- OpenCV: support OpenCV official OAK-D-Lite 3D camera module and MIPI camera
- Open-source: DIY and customize what you want.
- Raspberry Pi: it’s super expandable, endorsed by Raspberry Pi.

## Overview

This repository is Google Gemini Demo APPs, it can be run on Mini Pupper2 and Mini Pupper. 
The default branch works on Mini Pupper2.
The new branch for Mini Pupper will be added soon.

## Preparation

Please make sure Mini Pupper 2 can walk first. 

- Download and flash the [pre-built base image file](https://drive.google.com/file/d/18hR9YZVKdxlTCJZxj67LTTbRUu9M8vbU/view?usp=sharing), or 
- Build the base environment by yourself. 

Step 1: Install the [BSP repo](https://github.com/mangdangroboticsclub/mini_pupper_2_bsp)

Step 2: Install the [quadruped repo](https://github.com/mangdangroboticsclub/StanfordQuadruped )


## Run on Mini Pupper 2: 

Clone this repo.
```
cd ~
git clone https://github.com/mangdangroboticsclub/gemini-md-bot
cd gemini-md-bot
./install.sh

```

Set your google cloud API key in env.example file and then enjoy.
 
```
# set your key in env.example, then 
cp env.example .env
```
Then add this line at the end of your .bashrc "export GOOGLE_APPLICATION_CREDENTIALS=/<your own  api key path>" by these steps:
```
vim ~/.bashrc
```
After adding, source it to .bashrc
```
source ~/.bashrc
```

Now you can try using the gemini-md-bot
```
python gemini-md-bot.py
```
