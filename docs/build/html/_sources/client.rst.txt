Client
======

Context
-------
In a world where the use of technology is growing in a large scale, the domotic area is growing up tendency. Domotics is a project made by a team of Computer & Telematics Engineering students in response to the challenge made by the subject of Software engineering.

Problem
-------
More and more intelligent houses exist and users do not always know how to control and monitor the existing technology, so there is a need for a simple platform that allows the visualization of all the data of an intelligent house. Thus was born the Domotics project.

Objectives
----------
The system we will implement is going to offer a way to visualize data gathered by sensors on web browsers referring to a real-time monitorization of a house, sending warnings when extreme conditions occur, show some historical data that is stored in our system or even alert the residents of the house with some alarm clocks of specific events like meetings.

Specifications
--------------
The data obtained is the product of a simulation of data that would come from actual sensors on a house.
The conditions observable in our system are: 

* Temperature.
* Humidity.
* Luminosity.
* Smoke levels.
* Movement.
* Use of energy by different home appliances.

Features
--------
* Show data from the sensors in real-time.
* Check previous values in charts. 
* Send alerts when the values are above/below the threshold.
* Define alarms (routine alarms or specific events).
* Be able to make changes depending on values read from sensors.

Risks and Challenges
--------------------
1. Sensors not working correctly.
2. Data values not corresponding to real values.

Technical requirements
----------------------
1. Data sensors to collect data from the house.
2. Network access and a web browser.

Architecture
------------

.. figure:: html/_static/ES_client.png
		
Figure 2: Architecture

Our system has many different components. For the user, the most important components are the **sensors** and the **dashboard**.
The sensors will give the user different information such as temperature, humidity, luminosity, smoke levels, movement in the house and use of energy by different home appliances.

The information given by the sensors is displayed in a web dashboard that is present to the user. The dashboard has two categories: real-time information and historic. In the **real-time** information, there are values in real-time from the sensors (presented in tables with fields such as: name of the room, room id and the value sent by the sensor). The **historic** has line charts where the user can visualize the different values in the past hours of the day. This values were previously saved in a database.

When some value given by the sensor is too high or too low compared to the advisable value, it will be presented to the user a notification and an **alarm** will be triggered in order to make some change in the house so the abnormal value can dicrease or increase, respectively.
