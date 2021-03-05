---
title: Machine Learning Workflow
layout: post
excerpt: How do you do more with real data in machine learning?
---

# Introduction

Machine learning, as the innumerable medium articles will show you, is simple.
However, this is lies. To do the same "hello world" style application as all
those authors it is indeed very simple. However, do you really need to recognise
hand-written digits? Do you care about flow classification?  Not really! These
projects are useful to get to grips with the very basic concepts - but they are
unreal. The data isn't messy, the labels are all correct, and, mostly, the data
sets are small.

There is a wealth of complexity under the surface. Many libraries have made it
very easy to get started by abstracting the models away into a black box. This
is fantastic for those who just need something to pick out dogs from cats from a
bunch of pictures. For more niche uses, you'll want to roll your own, to some
extent.

As someone who learns by doing, I found this quite tricky to begin with. Many of
the articles out there only describe their approach *very simplistically*. If
you want to learn-by-doing, then you might not be able to re-create the result
and thus are unable to marry the approach into your own.

In this post I'm going to describe the approaches **for my very specific use
case** from the basic up to the complex.



# What kind of machine learning are we talking about here?

I am mostly interesting in image analysis. I am interested in sizing objects
accurately and discerning other details about the objects: shape, number
density. I'm therefore interested in image segmentation (classification): where
an input image is turned into a segmentation mask that describes, for each
pixel, what object it is. In my case, this is often simply black for no object,
white for object.

Adding to the complexity however, the objects are not always the same size, nor
are they always the same shape. They can be out of focus, they can overlap. I
need to find ways of dealing with all this.


# The basic workflow

You've probably read some the hundreds of articles and blog posts out
there about simple entry-level machine learning, but I'm going to bore you with
it once more. Quickly, I promise.

Images masks in to dumb machine; machine get smart. Images in to smart machine;
masks come out.

Phew. That was easy. As a flowchart:
![basic_flow](/img/ml_basic_flow.png)

And a simple python program to do the first part:

{% highlight python%}
from fastai.vision.all import *

# we could use fastai's built in datasets as an example, but I
# think that's unhelpful.

# Let's pretend there exists a function get_data().
# get_data() is a mysterious function which returns a list of
# pairs of input filename, and target filename.
data = get_data()

# e.g.
# get_data() -> [('0.bmp', '0_mask.bmp'), ('1.bmp', '1_mask.bmp') ... ]

# fastai uses DataLoaders to manage input of data to the model
dblock = DataBlock(
    blocks=(ImageBlock, MaskBlock(codes=['naw', 'aye'])),
    getters=(ItemGetter(0), ItemGetter(1))
)
dls = dblock.dataloaders(data)

# unet is a model architecture, resnet is a back bone
learner = unet_learner(dls, resnet34)
learner.fit_one_cycle(3, 1e-3)
{% endhighlight %}

That wee program will segment images into two categories. Category 0 (or 'naw')
for no ('naw') object, and cat 1 ('aye') for object present. Is that all you
want to do? No! This is a very basic approach.



# Let's add some complexity

Using standard datasets (MNist, iris dataset) is unrealistic. These datasets are
as clean as can be, they are perfectly classified with no false
positives/negatives. This is fine for teaching the basics, but useless when
trying to get to grips with *real data*.

Real data is noisy. It is blurry. It is confusing. Worst of all, a model trained
on real data, (and automatically segmented e.g. by traditional means) can be
*wrong*.

To overcome this, we need to be a bit flexible in our training, and we need to
be ready to fix up our data. The easiest way to improve is to stick a *human in
the loop*. This just means you manually correct any mistakes in the segmentation
results, the new masks being fed back in to re-train the model.

The process can be summarised on another unnecessary flowchart:

![flowchart1](/img/ml_flowchart_1.png)

The first step (`00 SEGMENT`) is what ever you do to get masks from images.
After this, you could check the annotations (`05 ANNOTATE`), or you can wait
until after training. The benefit of doing it now is you don't waste time
mis-training a mdoel. However, you also don't have the benefit of the model to
tell you what images were difficult to classify: you will end up annotating *the
entire training set* instead of only the unconfident set.

After this **backup your training set** (`07 BACKUP`). If you've manually
annotated, it is a good idea to make frequent backups and copies of your
dataset. You do not want to lose all the work you put in annotating it!

Next up, we train the mode (`10 TRAIN`). This step produces a model with the
weights optimised to perform the requested segmentation. At least, that's the
hope! We need to check the training results. How good was the training? If we
apply the model, do we get good masks out?

## Calculating confidence



# Under the bonnet

Neural networks have come a long way since their beginning (see [my first ML post]({% post_url 2020-02-22-neural_networks %}) )
for a run down on some of the history. Modern neural networks are more than just
connected layers; they have different operations gluing the layers together
performing edge and feature detection using convolution, creating highly
effective and highly efficient pattern recognition tools. - leaps and bounds
ahead of the linear function model they were back in the 50s!
