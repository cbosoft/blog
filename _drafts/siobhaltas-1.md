---
title: "Sìobhaltas 1: Modelling"
excerpt: " .. "
layout: post
tags: games software-dev C++
comments: true
---

# Modelling a civilisation

# Brainstorm: aspects of a civilisation
## Main Statistics
- population (#) how many people are currently alive. combined with area to give density - decides happiness, productivity, etc
- health (%) happiness
- happiness (%) general mood of the population - what percentage of the population are, on balance, more happy than not
- safety (%) perc of population living in a safe place

## Resources
- food needs (%) more food scarcity means lower growth, higher unhappiness and so on
- material resource needs (%) how fulfilled are the needs of the society (construction materials, ores, common minerals)
- uncommon resource needs (%) rare minerals etc. 
- power needs (%) how fulfilled are the power needs of the society. below 100% and productivity and happiness falls. too far above and economy takes a hit

# Economy
- productive ability (%) what percentage of the living population are in work
- productivity (f) how effective are people when they are working. imagine this like normalised person-hours per person per hour kind of thing. An unmotivated person may have a score less than one, while an especially motivated person will have a multiplier greater than one. Tops out at 2, bottoms out at 0. Affects economics, happiness
- economic productivity (f) amount of economic turnover in the civilisation. larger number indicates larger turnover and thus indicates more productive society. 

## Culture
- Interests
  - Economy
  - Religion
  - Family
  - Independence
  - Social
  - Knowledge
  - Safety
  - Music
- preoccupation, [science, art, history, socialisation, military, environment, futurism, religion] (%) percentage of the population with a serious interest in the given field. May sum to more than 100% as people can have multiple interests.
- political leaning [authoritarian, liberal, socialist, conservative] - dictates the political desires of the population. affects happiness, productivity.

# implementation notes
- complex interplay of differential equations
- could use fourier transform to simplify
- want something perhaps never 100% stable
- zero/poles analysis to ensure (some) instability