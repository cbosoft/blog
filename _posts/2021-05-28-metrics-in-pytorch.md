---
title: Metrics in Pytorch
layout: post
excerpt: "Metrics are used in machine learning to gauge how well a model is performing; in this post I discuss some of the terminology and how to calculate the metrics using `Pytorch`/`torchmetrics` and displayed using the excellent `tensorboard`."
tags: ml software-dev Python PyTorch
---

# Training and Metrics

When training a model you need to keep track of its performance. This tells you
when the model is finished training (preventing [overfit](https://en.wikipedia.org/wiki/Overfitting)),
or whether your training is proceeding as expected, or otherwise allows you to
gauge the effectiveness of your model/training set/hyper parameters.

The basic training loop is simply
- init model
- calculate loss for a training data set
- use loss to calculate gradients
- pass this on to optimiser

{% highlight python %}
import torch
from torch.utils.data import DataLoader

model = YourNeuralNetworkHere()

###########
# options #
###########
n_epochs = 50
learning_rate = 1e-3
batch_size = 4
opt = torch.optim.Adam(model.parameters(), lr=learning_rate)
loss_func = torch.nn.CrossEntropyLoss()
###########

loader_kw = dict(batch_size=batch_size)
train_dl = DataLoader(your_training_dataset, **loader_kw)
test_dl = DataLoader(your_test_dataset, **loader_kw)
valid_dl = DataLoader(your_validation_dataset, **loader_kw)

for i in range(n_epochs):
    for batch in train_dl:
        inp = batch['input']
        tgt = batch['target']
        opt.zero_grad()
        out = model(inp)
        loss = loss_func(out, tgt)
        loss.backward()
        opt.step()
{% endhighlight %}

And that's all well and good; but how can you decide how good the model is at
the end of the day? Well you could just check the loss, and that's not a bad
idea. Let's update this training scheme, and track the loss over batches using
`tensorboard`.

# Tensorboard
[Tensorboard](https://www.tensorflow.org/tensorboard) is a great library for
storing and visualising machine learning model meta data and training
information.

Tensorboard is [included in](https://pytorch.org/docs/stable/tensorboard.html) `pytorch`:
{% highlight python %}
from torch.utils.tensorboard import SummaryWriter
{% endhighlight %}

The library keeps track of metrics by writing them out using helper objects.
Here, we've imported the `SummaryWriter` object, instantiated below:
{% highlight python %}
writer = SummaryWriter()
{% endhighlight %}

This object will let you store metrics during the training process.

{% highlight python %}
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

model = YourNeuralNetworkHere()

###########
# options #
###########
n_epochs = 50
learning_rate = 1e-3
batch_size = 4
opt = torch.optim.Adam(model.parameters(), lr=learning_rate)
loss_func = torch.nn.CrossEntropyLoss()
###########

# Create a summary writer object
writer = SummaryWriter()

loader_kw = dict(batch_size=batch_size)
train_dl = DataLoader(PolyEDataset(train), **loader_kw)
test_dl = DataLoader(PolyEDataset(test), **loader_kw)
valid_dl = DataLoader(PolyEDataset(valid), **loader_kw)

tbn = 0

for i in range(n_epochs):
    for batch in train_dl:
        inp = batch['input']
        tgt = batch['target']
        opt.zero_grad()
        out = model(inp)
        loss = loss_func(out, tgt)
        loss.backward()
        opt.step()
        # Store a loss value
        writer.add_scalar('Training/Loss', float(loss), tbn)
{% endhighlight %}

Then we can view the logs (if you're using a Jupyter notebook, and gosh-darn it
you should be) with

{% highlight python %}
% load_ext tensorboard
% tensorboard --logdir=runs
{% endhighlight %}

Which looks something like:
![tensorboard_screenshot](/img/tensorboard_screenshot.png)

In that screenshot I've included the learning rate, which shows the versatility
and utility of tensorboard; you can put anything on it! Looking on the bottom
left of the screenshot, there is a garble of text; this is a way of
discriminating between runs. You set this by changing the target logging
directory in the `SummaryWriter` constructor:

{% highlight python %}
today = datetime.now().strftime('%Y-%m-%d_%H%M%S')
log_dir = 'runs/{hyper_params_str},{today}'
writer = SummaryWriter(log_dir=log_dir)
{% endhighlight %}

where `hyper_params_str` is some text describing the run.

# Metrics

Ah! I haven't talked properly about any metrics yet. D'oh!

A metric is a measurement of a pair of predictions and targets which describes
how close the two are. The one that comes to find is 'accuracy' but there are
others:

- precision
- recall
- F-Score
- Intersection over union

Quickly putting some maths to this, let's start with the basics: true and false
positives and negatives: The *true positives* (TP) are predictions made by the
model which are positive and correct. That means, if the model is designed to
detect dogs, it is "positive" if it says "yes that is dog" and correct if it
indeed was shown a dog. *True negatives* (TN) are negative and correct (shown a
cat and responds "that is not dog"). *False positives* (FP) and *false
negatives* (FN) are where the model has gone wrong. Wikipedia has a nice image
for this:

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/700px-Precisionrecall.svg.png" width="50%"/>
<a href="https://en.wikipedia.org/wiki/Precision_and_recall">from wikipedia</a>
</center>

From TP, TN, FP, FN we derive precision, recall, and accuracy:

$$precision = \frac{TP}{TP + FP} $$

$$recall = \frac{TP}{TP + FN} $$

$$accuracy = \frac{TP + TN}{TP + FP + TN + FN} $$

We don't need to implement these in `pytorch` (although it wouldn't be difficult
to do so). We can use the
[`torchmetrics`](https://torchmetrics.readthedocs.io/en/latest/) library which
contains a whole bunch more (saving a heap of time):

{% highlight python %}
from torchmetrics.functional import accuracy, precision, recall, f1

metrics = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': f1
}
{% endhighlight %}

This initialises a dictionary with a couple metric calculating functions, each
called in a similar way:

{% highlight python %}
metric_value = metric_function(prediction, target)
{% endhighlight %}

With this set up, we can add a section to our training loop to calculate the
metrics and write them out to tensorboard.

# Final

Putting all this together yields a training script which records the hyper
parameters used, several metrics and both the training and validation loss
(cross entropy in this case):

{% highlight python %}
from datetime import datetime

import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchmetrics.functional import accuracy, precision, recall, f1

metrics = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': f1
}

model = YourNeuralNetworkHere()

###########
# options #
###########
n_epochs = 50
learning_rate = 1e-3
batch_size = 4
opt = torch.optim.Adam(model.parameters(), lr=learning_rate)
loss_func = torch.nn.CrossEntropyLoss()
hyper_params = dict(
    n_epochs=n_epochs,
    learning_rate=learning_rate,
    batch_size=batch_size,
    opt=str(opt.__class__),
    loss_func=str(loss_func.__class__)
)
hyper_params_str = ','.join([f'{k}={v}' for k, v in hyper_params.items()])
###########

today = datetime.now().strftime('%Y-%m-%d_%H%M%S')
log_dir = 'runs/{hyper_params_str},{today}'
writer = SummaryWriter(log_dir=log_dir)

loader_kw = dict(batch_size=batch_size)
train_dl = DataLoader(your_training_dataset, **loader_kw)
test_dl = DataLoader(your_test_dataset, **loader_kw)
valid_dl = DataLoader(your_validation_dataset, **loader_kw)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'  # uncomment to aid debugging if 'device side assert triggered' error appears
model = model.to(device)

tbn = 0
vbn = 0
for i in trange(n_epochs, unit='epochs'):
    for batch in train_dl:
        inp = batch['input'].to(device)
        tgt = batch['target'].to(device).squeeze(1)
        opt.zero_grad()
        out = model(inp)
        loss = loss_func(out, tgt)
        writer.add_scalar('Loss/train', float(loss), tbn)
        loss.backward()
        opt.step()
        tbn += 1
    with torch.no_grad():
        for batch in valid_dl:
            inp = batch['input'].to(device)
            tgt = batch['target'].to(device).squeeze(1)
            if (inp.shape[0] == 1):
                continue
            out = model(inp)
            loss = loss_func(out, tgt)
            writer.add_scalar('Loss/valid', float(loss), vbn)
            probs = torch.softmax(out, 1)
            for mname, mf in metrics.items():
                writer.add_scalar(f'Metrics/{mname}', float(mf(probs, tgt, mdmc_average='global')), vbn)
            vbn += 1
writer.close()
{% endhighlight %}

# Further Reading
- https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html
- https://towardsdatascience.com/a-complete-guide-to-using-tensorboard-with-pytorch-53cb2301e8c3
- https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html
