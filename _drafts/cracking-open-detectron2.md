---
title: "Cracking open Detectron 2 like an egg, reserving only the yolk."
layout: post
excerpt: "Facebook's Detectron 2 framework is an odd one."
tags: ml
---

# Machine learning

Ah machine learning; the all-purpose tool for when you don't know exactly how to do something. Training a model is where the bulk of the computational effort is spent (human effort comes in at either end; developing the dataset and evaluating the model). 

Typically, training is organised into **"epochs"** where one epoch is one run through of all the training data you have. This data is split into manageable chunks called "batches". After one epoch of training, you might want to quickly check to see how the model is doing. You use a second set of data for this (the test set). You run through all the test data you have and you evaluate the model before going back to the training set for another epoch. This is repeated until a desired number of epochs is completed.

# Detectron 2 is *odd*

Facebook AI Research (FAIR) released the [Detectron 2](https://github.com/facebookresearch/detectron2) machine learning framework in 2019 as a state-of-the-art image segmentation *platform*. The code is well [documented](https://detectron2.readthedocs.io/en/latest/tutorials/getting_started.html), has good [examples](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5) and the codebase is well structured and commented (see [the repo](https://github.com/facebookresearch/detectron2/tree/main/detectron2)).

They [claim](https://github.com/facebookresearch/detectron2/blob/main/README.md) the platform is to be "used as a library to support building research projects on top of it". I interpret this to mean that it has the intended purpose of facilitating image analysis projects, with a particular focus on model flexibility. (Or, perhaps, on machine learning architecture development.) Either way, they have gone about the design of the default


# Let's fix Detectron 2