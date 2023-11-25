---
title: "Sustainability of Deep Learning"
layout: post
excerpt: "Deep Learning is certainly very powerful. It has allowed us to automate many tedious tasks that would otherwise have to be done manually. This comes at a significant energy cost. Let's look at how reasonable this is."
tags: ml Sustainability
---

# Energy usage
What exactly is the impact of deep learning? Energy draw? How does the energy efficiency of a deep learning application compare to non-DL application?

# accuracy vs power draw

# Testing
Could run the [house price challenge](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data) with various models and check cpu time usage as a predictor for energy consumption.
Models:
 - Deep Learning
   - FCN
   - CNN
- Classical
  - PCA
  - Linear Regression


# Literature
 - https://www.nature.com/articles/s41578-022-00490-5
 - https://www.sciencedirect.com/science/article/pii/S2667096822000507
 - https://spectrum.ieee.org/deep-learning-sustainability
 - https://www.nature.com/articles/s41467-019-14108-y

# Energy consumption of datacentres
 - https://learn.microsoft.com/en-us/answers/questions/630650/energy-consumption-in-azure-cloud
 - https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard?activetab=pivot:mostpopulartab
 - https://azure.microsoft.com/en-gb/explore/global-infrastructure/sustainability/#carbon-benefits
 - https://devblogs.microsoft.com/sustainable-software/how-can-i-calculate-co2eq-emissions-for-my-azure-vm/
 - https://medium.com/teads-engineering/estimating-aws-ec2-instances-power-consumption-c9745e347959
 - https://www.zdnet.com/home-and-office/sustainability/this-new-aws-tool-shows-customers-the-carbon-footprint-of-their-cloud-computing-usage/
 - https://aws.amazon.com/power-and-utilities/sustainability/
 - https://sustainability.aboutamazon.co.uk/environment/the-cloud?energyType=true

# Model training stats
 - https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md
 - hpopt/model selection https://lazypredict.readthedocs.io/en/stable/readme.html

# Model efficiency
 - reduce inference computation by distillation - https://towardsdatascience.com/model-distillation-and-compression-for-recommender-systems-in-pytorch-5d81c0f2c0ec
 - https://paperswithcode.com/paper/torchdistill-a-modular-configuration-driven