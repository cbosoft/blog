---
title: "Literature mapping and visualisation"
layout: post
excerpt: "Literature review is a hefty and important task. Wouldn't it be useful to visualise the connections between journal papers?"
tags: software-dev
---

# What?

Jumping into a new field is intimidating - there is this amorphous blog of
literature staring you in the face. To help make sense of how *stuff* is
connected, we can visualise the literature, and its inter-connections
(citations) as a network or graph:

<center><img src="/img/twl_ex1.png" width="80%" /></center>

The above screen shot is static; but the resulting dash web-app is
*interactive*. Each point is a paper, hovering over it yields its name. Clicking
on the point takes you to the paper on Google Scholar. (or tries to, at least.)
In this way, we can see potentially important papers that are frequently
discussed that may be overlooked, or otherwise gain quick access to the
citations in your literature collection.

# How?
The script works in three steps:
1. Scrape a directory of paper PDFs for citations
2. Form a [graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) of
   the citations
3. Visualise the graph


# References
- [sigmajs](http://sigmajs.org/)
