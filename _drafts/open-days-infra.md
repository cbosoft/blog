---
title: "Infrastructure in an Automated Lab"
layout: post
excerpt: "Adventures in joining together robotics and deep learning and databases."
tags: Python ml
---

# CMAC Hub DataFactory
At work we're building a high throughput automated laboratory leveraging **robots** to build up a high quality machine-learning-ready database. As a data scientist, this sounds fantastic. Gotta get there first!

Essentially, we have three components to link together:
 - Dosing instrument
 - Measurement instrument
 - Robotic arm

We have active pharmaceutical ingredients (APIs) to test, these are dosed by the *dosing instrument*. We need to make measurements using the *measurment instrument* (funnily enough) and the dosed vials of API need to be moved around to do this: this is where the robotic arm comes in.

I'm gonna be a bit light on specifics for some things in this post as this represents a lot of unpublished work. I'm gonna touch on some of the challenges we faced and discuss how we tackled them especially with regards to the software infrastructure (my purview).

# The Doser 🥄
The *doser* is controlled by [LabView](https://www.ni.com/en/shop/labview.html) via the [Modbus](https://www.ni.com/en/shop/seamlessly-connect-to-third-party-devices-and-supervisory-system/the-modbus-protocol-in-depth.html) protocol. It will dose out an amount of *stuff* as specified by a CSV file. Actual amounts dosed (these things are never 100% accurate afterall) are output to another CSV file. 

<div class="standout">
LabView, if you're not familiar, is a bizarre hellscape of click-and-drag widgets asynchronous programming used widely for lab automation. For some reason. My colleague in charge of the hardware will defend LabView at every turn while simultaneously trying to use as little of it as possible.
</div>

The dosing process can almost entirely be automated through the TCP connection, however some minor things, like **starting the dosing procedure** require mouse input in the doser control UI. (So it's just set up and output capture that can be automated via Modbus.)

# The Instrument 🌡
The measurement *instrument* takes a vial and does *stuff* to it and reports its findings in a SQLite database (gzip compressed for good measure). This includes images taken via microscope and temperatures and other scalar data. The instrument is controlled via it's proprietary software. The instrument manufacturer has been very helpful and added a gRPC API just for us (...and to sell to others I guess). gRPC is supported in LabView, but as alluded to earlier, LabView is a nightmare. We will use python to control this (mostly to ease dealing with images). Each of these instruments has multiple bays for vials and we actually have three of these instruments.

<div class="standout">
I am very grateful for the rapid and bespoke implementation of the gRPC API in the instrument software. However this API was not without issues. (What software is truly bug-free?) We had issues with the instrument control server crashing when API commands were sent too quickly. Apparently there's some rate limiting controls missing on their end. I had a hunch that sending commands too quickly might be the culprit, confirmed by adding a small delay between sending commands.
</div>

The measurements in this instrument take anywhere up to 30 hours to run. We can end experiments early to increase efficiency (and get more of that lovely data into the database).

# The Robot 🤖
Robot arm moves the stuff from *doser* to *instrument*. It needs to be programmed for every potential movement it could make (i.e. positioning vials in any of the many potential vial bays) which my colleague meticulously did at great effort. It looked painstaking and mind numbing. I do not envy him. It is controlled by LabView and Modbus again. At least it is completely automatable.

# The Software 🖥
I developed a series of python scripts to join everything together. LabView, unfortunately, was at the centre of it all. This was used to set the ball rolling on starting dosing and controlling the robot arm. The instruments were controlled by LabView too, via extensive python code.

Due to the oddities of the measurement instrument control software, they required controlling from separate computers. (This is due to static IPs set for each instrument, unfortunately not user changeable.) A **control server** ran on each of these machines. The server listens for commands from LabView (via a python script as LabView's TCP/IP connection stuff is apparently broken). LabView needs to know what vial bay is free (so the arm knows where to put stuff), it needs to start experiments, and it needs to know when an experiment is finished so it can clear the vial from the bay.

<div class="standout">
This set up actually gave us our first big issue. We had each of the instrument PCs connected to the control PC on a local network. This network had IPs on the <code>192.168.1</code> subnet. We numbered each of the instrument PCs sequentially (<code>.1</code>, <code>.2</code>, <code>.3</code>). The control PC was on <code>.10</code> to allow for potential additional instruments (we're optimistic about future growth). However, due to a misconfiguration, the control PC was also given the IP <code>192.168.1.2</code> on another network, meaning it was unable to communicate with instrument #2. One panicked afternoon of debugging and one wireshark install later, we found the issue. 
</div>

In addition to tracking available bays, the server needs to run and manage experiments in the instrument. Images are obtained live via gRPC and are analysed by deep learning model. This information is used to inform outcomes of the experiments, and (in future) will feed into increasing experimental efficiency by early stopping. Unfortunately, this was not available in the API at the time.

To give an overall picture of the status of the many concurrent experiments, I built a simple **dashboard** to show live image analysis results as well as temperature and other scalar data. This was displayed on a large monitor in the lab during lab tours.

To summarise, I built two software components:
 - control client & server
 - dashboard

<div style="display: flex; align-items: center;">
<div style="width: 70%;">
<h2>Control Server</h2>
<p>The diagram on the right shows, loosely, the flow of control through the server. A command is given by the client on the control PC via TCP to the server on an instrument's PC. (The client tries each server in turn until it gets the answer it wants.)</p>

<p>The server reacts to the incoming command and sends back a reply (<code>OK</code> or some data or an error). Part of this could involve the starting of a new experiment. The server will spawn a new process (not thread! Thanks, GIL.) which monitors the experiment as it proceeds.</p>

<p>Images and scalar data recorded from experiment are passed to one of the two image analysis processes running alongside. These processes run the deep learning model and obtain answers. The answer to what? Wouldn't you like to know.</p>

<p>Results are collated and stored in a PostgreSQL database running on a server near to (but outside) the lab. Images are stored on the filesystem and are pointed to by the database.</p>
</div>
<pre class="mermaid" style="width: 30%">
  graph TD
  O[Client] -. TCP Command .-> T
  T -. Command .-> B[<i>Instrument</i><br/>management process]
  B -. Response .-> T[TCP connection<br/>listener]
  B -- on experiment start --> C[Experiment management<br/>process]
  C -. Images .-> D[Image analysis<br/>processes]

  D -. Results .->F[(Database)]

  T -. TCP Response .-> O

</pre>
</div>

## Dashboard

# Touring the Automated Lab
During the 2023 CMAC Open Days event we gave 16 tours to groups of academics and industrial representatives. We demonstrated the automated lab, including showing off the robotics and our image analysis. The audience all looked impressed with out pitch, I'd say the event was a success! 🎉
