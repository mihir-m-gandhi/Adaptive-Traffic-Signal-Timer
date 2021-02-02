<p align="center">
  <a href="" rel="noopener">
 <img height=200px src="./traffic-signal.jpg" alt="Traffic Signal Timer"></a>
</p>

<h1 align="center">Adaptive Traffic Signal Timer</h1>

<div align="center">

[![License: Apache 2](https://img.shields.io/badge/License-Apache-yellow.svg)](https://www.apache.org/licenses/LICENSE-2.0)

<h4>This Adaptive Traffic Signal Timer uses live images from the cameras at traffic junctions for traffic density calculation using YOLO object detection and sets the signal timers accordingly, thus reducing the traffic congestion on roads, providing faster transit to people, and reducing fuel consumption.</h4>

</div>

-----------------------------------------
### Inspiration

* Traffic congestion is becoming one of the critical issues with the increasing population and automobiles in cities. Traffic jams not only cause extra delay and stress for the drivers but also increase fuel consumption and air pollution. 

* According to the [TomTom Traffic Index](https://www.tomtom.com/en_gb/traffic-index/ranking/), 3 of the top 10 countries facing the most traffic congestion are in India viz. Mumbai, Bengaluru, and New Delhi.  People are compelled to spend hours stuck in traffic jams, wasting away their precious time commuting. Current traffic light controllers use a fixed timer and do not adapt according to the real-time traffic on the road.

* In an attempt to reduce traffic congestion, we developed an improved traffic management system in the form of a Computer Vision-based traffic light controller that can autonomously adapt to the traffic situation at the traffic signal. 

------------------------------------------
### Implementation Details

This project can be broken down into 3 modules:

1. `Vehicle Detection Module` - This module is responsible for detecting the number of vehicles in the image received as input from the camera. More specifically, it will provide as output the number of vehicles of each vehicle class such as car, bike, bus, truck, and rickshaw.

2. `Signal Switching Algorithm` - This algorithm updates the red, green, and yellow times of all signals. These timers are set bases on the count of vehicles of each class received from the vehicle detection module and several other factors such as the number of lanes, average speed of each class of vehicle, etc. 

3. `Simulation Module` - A simulation is developed from scratch using [Pygames](https://www.pygame.org/news)) library to simulate traffic signals and vehicles moving across a traffic intersection.

Read more about object detection model used, working of the algorithm, and development of simulation [here]().

------------------------------------------
### Demo

* `Vehicle Detection`

<p align="center">
  <a href="" rel="noopener">
 <img height=300px src="./vecicle-detection.png" alt="Vehicle Detection"></a>
</p>


* `Signal Switching Algorithm and Simulation`

<p align="center">
    <img src="./Demo.gif">
</p>


------------------------------------------
### Installation



------------------------------------------
### Dissemination

* This project was showcased at a national level project competition organized by [Government Polytechnic Mumbai](http://www.gpmumbai.ac.in/). View our presentation video [here](https://youtu.be/OssY5pzOyo0).

* Our paper based on this project has been accepted for publication in IEEE International Conference on Recent Advances and Innovations in Engineering - [ICRAIE 2020](http://www.icraie.poornima.org/). View the paper manuscript [here](https://drive.google.com/file/d/164j58YuMQMCqxh2Nld3oxoxCQxBsczKp/view?usp=sharing).

------------------------------------------
### Authors

Mihir Gandhi - [mihir-m-gandhi](https://github.com/mihir-m-gandhi)

Devansh Solanki - [devanshslnk](https://github.com/devanshslnk/)

Rutwij Daptardar - [RDmaverick](https://github.com/RDmaverick)

------------------------------------------
### Acknowledgement

We would like to extend our sincere thanks to our mentor Mrs. Nirmala Shinde Baloorkar for her guidance and constant supervision. Her support and encouragement were imperative for the successful completion of this project. We would like to express our special gratitude and thanks to Mrs. Kavita Kelkar, the subject-matter expert for this project, for her expertise and time.

------------------------------------------
### License
This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.
