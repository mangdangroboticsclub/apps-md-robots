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
The default branch works on Mini Pupper2, please click the picture and refer to the demo video.

[![Run on MD-Puppy1](https://img.youtube.com/vi/mIDuIZCevIg/0.jpg)](https://www.youtube.com/watch?v=mIDuIZCevIg)

The new branch for Mini Pupper will be added soon, please click the picture and refer to the demo video.

[![Run on MD-Puppy1](https://img.youtube.com/vi/bvH-lA1IHig/0.jpg)](https://www.youtube.com/watch?v=bvH-lA1IHig)

## Preparation

Please make sure Mini Pupper 2 can walk first. 

- Download and flash the [pre-built base image file (like v2_stanford*.img) ](https://drive.google.com/drive/folders/1ZF4vulHbXvVF4RPWWGxEe7rxcJ9LyeEu?usp=sharing), or 
- Build the base environment by yourself. 

Step 1: Install the [BSP repo](https://github.com/mangdangroboticsclub/mini_pupper_2_bsp)

Step 2: Install the [quadruped repo](https://github.com/mangdangroboticsclub/StanfordQuadruped )


## Install

For the video guide, please click the picture and refer to the demo video.

[![Installation Guide](https://img.youtube.com/vi/1AkhJi2o8rM/0.jpg)](https://www.youtube.com/watch?v=1AkhJi2o8rM)


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

Run
=======
Set your Google Cloud API key in .env file and then enjoy.
 
```
cp env.example .env
```

Edit .env file and set your key path, then you can try using the gemini-md-bot

```
python gemini-md-bot.py
```
