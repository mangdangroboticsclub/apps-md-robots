# Mini Pupper generative ai demos
[MangDang](https://www.mangdang.net/) Online channel: [Discord](https://discord.gg/xJdt3dHBVw), [FaceBook](https://www.facebook.com/groups/716473723088464), [YouTube](https://www.youtube.com/channel/UCqHWYGXmnoO7VWHmENje3ug/featured), [Twitter](https://twitter.com/LeggedRobot)

Mini Pupper will make robotics easier for schools, homeschool families, enthusiasts and beyond.

- ROS: support ROS2(Humble) SLAM & Navigation robot dog at low-cost price
- OpenCV: support OpenCV official OAK-D-Lite 3D camera module and MIPI camera
- Open-source: DIY and customize what you want.
- Raspberry Pi: it’s super expandable, endorsed by Raspberry Pi.

## Overview

This repository is the Demos APPs for Mini Pupper2. You should setup Mini Pupper2 before use this demos:1. setup bsp: https://github.com/mangdangroboticsclub/mini_pupper_2_bsp. 2. setup quadruped: https://github.com/mangdangroboticsclub/StanfordQuadruped 


## Run on mini pupper 2: 

Clone this repo, before run ai_bot.py, you should set your own google cloud api key in .env files.

```
cp env.example .env
```
edit .env file, set your google cloud api key file path. And run:
```
python ai_bot.py
```

### GPL source code in this repository
* [FuelGauge](./FuelGauge)
