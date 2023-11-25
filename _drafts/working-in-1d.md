---
title: "1D CNNs"
layout: post
excerpt: "Sometimes we need to interpret 1D data (e.g. spectra, timeseries, histogram, ...). In pharma, we typically build PLS models for this interpretation. These models are normally non-transferable and liable to drift. Can we instead build a more flexible CNN model? Should we?"
tags: ml Python
---

Sometimes we need to interpret 1D data (e.g. spectra, timeseries, histogram, ...). In pharma, we typically build PLS models for this interpretation. These models are normally non-transferable and liable to drift.

Can we instead build a more flexible CNN model? Should we?

Yes, and maybe.

The challenge of building a 1D model is trivial - swap out `torch.nn.Conv2d` for `torch.nn.Conv1d` and update layers accordingly. There are some problems to solve though!

## Convolutions in 2D

In 2D, we visualise the effect of convolutions quite naturally. This [article](https://towardsdatascience.com/visualizing-the-fundamentals-of-convolutional-neural-networks-6021e5b07f69) has some good information. A filter is [passed over an image](https://ezyang.github.io/convolution-visualizer/), and the result is another image. The convolution will pick up the presence of a feature in the image (e.g. edges) and the output image will indicate where (if) that feature is in the input.

For example, edge detection:

<center>
<img src="{{site.baseurl}}/img/1dcnn/duke.jpg" style="display: inline-block; width: 40%;"/>
</center>

```
kernel = [
    [0,  1, 0],
    [1, -4, 1],
    [0,  1, 0]
]
```

<center>
<img src="{{site.baseurl}}/img/1dcnn/duke_edges.jpg" style="display: inline-block; width: 40%;"/>
</center>


A great website for gaining some intuition on CNNs is live [here](https://www.cs.ryerson.ca/~aharley/vis/conv/flat.html) - visualises neuron activation for the task of handwriting detection (MNIST dataset).

A CNN builds up channels of many convolutions and then builds up super-features by applying more layers of convolution. In this way a CNN can recognise features in the images it sees as input.

# Convolutions in 1D

Similarly to 2D, in 1D, a kernel is convolved with some input data to yield some information about the presence of a feature in the input. Continuing with edge detection...

```
kernel = [-1, 2, -1]
```
<center>
<img src="{{site.baseurl}}/img/1dcnn/1d_edge_det.png" style="display: inline-block; width: 40%;"/>
<br /> Input in blue, results of convolution in orange.
</center>

We can see in the above the "edge" in blue is detected by the derivative around it and results in a peak (and trough). Similarly as for the 2D case, a 1D CNN builds up complexity of recognised features by recognising features in features.

# A Toy Problem

To illustrate the challenges, let's confront a trivial problem first, before diving into a more realistic example.

Let's categorise probability density functions into whether they are normal (i.e. Gaussian) or not. So basically, if the given vector resembles a bell-curve, it's normal. If it has another shape (could be anything), then it's not normal.


# Recognising Diabetes from Raman Spectra


# Conclusions