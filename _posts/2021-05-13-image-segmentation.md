---
title: Image Segmentation and Machine Learning
layout: post
excerpt: Working with real data when segmenting images
tags: ml Python PyTorch
---

Time to write the "Hello, World!" of data science blogging; a tutorial on
machine learning in python.

# Image segmentation

Image segmentation is a classification problem: we have an image and we want to
know what is in it on a pixel level. This is in contrast to instance
segmentation, which picks out objects more generally but not necessarily their
exact bounds.

<center><img src="/img/unet_seg_example.png"/>Taken from <a href="https://arxiv.org/abs/1505.04597">https://arxiv.org/abs/1505.04597</a><br/></center>
<br/>

This is of interest especially in microscopy - finding the location and size of
cells on slides, in industries for performing automatic maintenance checking
(looking for cracking on pipes), or in pharmaceuticals where we use it to find
accurate size and shape information of pharmaceutical ingredients as they
crystallise out of solution.


# In `python`
 Image segmentation is really, really easy at a very very high level using the
`fastai` library:

{% highlight python %}
from fastai.vision.all import *
{% endhighlight %}

[`fastai`](https://www.fast.ai/) is a nice wrapper around `pytorch`. It is easy to use and hides away a
lot of the difficult or boring parts and provides a *lot* of nice helper
functions.

We need some way of getting data, let's just assume you've got a magical
function which gets a list of paths to your input images:
{% highlight python%}
data = get_data()
# e.g.
# get_data() -> [('0.bmp', '0_mask.bmp'), ('1.bmp', '1_mask.bmp') ... ]
{% endhighlight %}
This could scrape a directory or do glob matching or similar.

As in `pytorch`, `fastai` uses a `DataLoader` to pass data to the network. We
could use their built in ones, but they also provide a very easy way to compose
a datablock (from which we can get the loader)
{% highlight python%}

# fastai uses DataLoaders to manage input of data to the model
dblock = DataBlock(
    blocks=(ImageBlock, MaskBlock(codes=['naw', 'aye'])),
    getters=(ItemGetter(0), ItemGetter(1))
)
dls = dblock.dataloaders(data)
{% endhighlight %}

Then build the model, which is a unet, with a resnet backbone.
{% highlight python%}
# unet is a model architecture, resnet is a back bone
learner = unet_learner(dls, resnet34)
{% endhighlight %}

Fianlly, we train the model.
{% highlight python%}
learner.fit_one_cycle(3, 1e-3)
{% endhighlight %}

Done. Easy peasy.


# I glossed over a lot

The model we used is a [U-Net](https://arxiv.org/abs/1505.04597)

<center><img src="/img/unet_structure.png"/>Taken from <a href="https://arxiv.org/abs/1505.04597">https://arxiv.org/abs/1505.04597</a><br/></center>

With a
[ResNet](https://towardsdatascience.com/an-overview-of-resnet-and-its-variants-5281e2f56035)
("Residual Network") *backbone* - this does the *feature* extraction, the bulk
of the detection. This is then refined by passing further into the UNet which
decodes features and upsamples back to the image size. I'm not 100% on the
backbone and how it works - I'd be very grateful for any info ([tweet
me](https://twitter.com/cbosoft)).

# Where does the learning happen?

The training process is done by the `fit_one_cycle` function to which we passed
two arguments: the first is the number of epochs, and the second is the learning
rate. I could give a broad overview, but I don't think I could add anything to
the wealth of incredible information available out there! [Towards data
science](https://towardsdatascience.com/machine-learning-for-beginners-an-introduction-to-neural-networks-d49f22d238f9)
has some good information.

# Further Reading

- [Image Segmentation in 2021: Architectures, Losses, Datasets, and Frameworks](https://neptune.ai/blog/image-segmentation-in-2020)
- [Image Segmentation Using Deep Learning: A Survey](https://medium.com/swlh/image-segmentation-using-deep-learning-a-survey-e37e0f0a1489)
