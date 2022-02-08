---
title: "Getting to grips with Detectron 2"
layout: post
excerpt: "FAIR's Detectron 2 is phenomenal - but how does it work?"
tags: software-dev ml
---

The Detectron 2 is FAIR's new (ish, introduced in 2019) state-of-the-art RCNN. The structure and operation of this is quite intimidating it you are not familiar with the RCNN family of models (like I am). I've tinkered with it and used it to some success in my research. In this post, I'll detail my journey with Detectron 2 - focusing on how it makes decisions.

# Big up the documentation

Detectron 2's [documentation](https://detectron2.readthedocs.io/en/latest/) is outstanding (in comparison to other research-produced software I've come across). It has [tutorials](https://detectron2.readthedocs.io/en/latest/tutorials/index.html) with enough detail to give you a head start (however, they are only tutorials - they lack the detail of the API documentation).

The [API documentation](https://detectron2.readthedocs.io/en/latest/modules/index.html) is decent, but often I found I could get more from going direct to the [source code](https://github.com/facebookresearch/detectron2). It is good documentation still - but there's only so much detail you can fit into docstrings etc.

The final source of information (not part of the documentation, but still worth a mention) is a [series of medium articles](https://medium.com/@hirotoschwert/digging-into-detectron-2-47b2e794fabd) written about the structure of Detectron 2. I will be referencing this series a lot, and adding to the information available from it. Honda goes into detail on the structure, but leaves out the answers to some questions I had.

# Structure

Honda's Medium series goes in to detail of how Detectron 2 is structured. I could copy the description down here but that would be pointless plagiarism - I'll blast through a summary. I recommend reading the series in full, however.

<center>
<img width="80%" src="https://miro.medium.com/max/2000/1*5mz6xC1oLPVdu8CIqXio4w.png" alt="detectron2 structure diagram"/>
From <a href="https://medium.com/@hirotoschwert/digging-into-detectron-2-47b2e794fabd">"Digging into Detectron 2" by Hiroto Honda</a>
</center>


Detectron 2 consists of three components:
1. Feature Pyramid Network (FPN) AKA Backbone
2. Region Proposal Network (RPN)
3. Region Of Interest Head (ROI Head) AKA Box Head

The FPN extracts features from the input image at different scales. These features are fed into both of the next two parts: RPN and ROI head.

The RPN generates a list of regions (boxes) on the image along with an "object-ness" score - **deciding** whether the region contains an object (something in one of the classes) or background (a lack of object). These regions are **pooled** (reduced in number) within the RPN to give some longlist of proposed boxes. 

Proposed boxes are fed, along with the image features from earlier, into the ROI head where the objects are **classified** and the boxes are further **pooled** into a shortlist. This shortlist is the output - a list of regions and classes in the image. This is not all, though. Not shown in Honda's diagram is the mask head. This head segments the region adding information in the form of **segmenting object boundaries** and another. Finally, each instance is given an **overall confidence score**.

# Decisions and Logic

How does the detectron make decisions? How does it narrow down the bboxes? How is the thresholding performed? How does it calculate confidence? These are some very important questions for anyone using the Detectron (or any ML model). Answering these questions will give some confidence in the predictions of the model.

In the previous section, I highlighted the decisions made by the network: what is a good region? Does this region contain an object, or nah? What object is in this region? Where does the object begin/end?

## 1. Object-ness
## 2. Longlist ROI pooling
## 3. Classification
## 4. Shortlist ROI pooling
## 5. Segmentation
`mask_heads`
## 6. Overall score
overall score that drton gives you is the bbox score from `box_predictor`

# Reading list
1. [Detectron 2 Tutorials](https://detectron2.readthedocs.io/en/latest/tutorials/index.html)
2. ["Digging into Detectron 2" by Hiroto Honda](https://medium.com/@hirotoschwert/digging-into-detectron-2-47b2e794fabd)