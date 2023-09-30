---
title: "Experiment Configuration Files"
layout: post
excerpt: "Labbooks are for desk people too."
tags: Python ml
---

# IN THE LAB
In the lab, we write down every number we measure. We follow written instructions in an SOP, and we write down any details or deviations from that SOP. The point being that all information necessary to retrace your steps is captured. Experiments are useless if they can't be repeated.

What about *in-silico*?

# AT THE DESK
*In-silico* experiments are still experiments. Instead of worrying about writing down results, that much is obvious and automatic, we worry about writing down the *SOP*: how was the simulation run? How was that ML model trained?

What I suggest<sup>*</sup> to use is a config file.

A config file being a plain text file containing the parameters necessary to run an experiment. For machine learning, this file contains your *hyperparameters*: what datasets were used, what model architecture, batch size, learning rate, what loss function, what optimiser, what augmentations, and so on. Every time an experiment is run, a copy of the config is created and placed alongside the outputs. Then, if the run needs to be verified, it can be!

<div class="standout">*I <i>suggest</i> this approach, but I by no means claim that I started the trend. Ross Girshick wrote a <a href="https://github.com/rbgirshick/yacs">library</a> to aid this in 2018, and that library was already "yet another" library at time of release.</div>

It is vital that a config is the only way parameters can be changed, otherwise some important change may not be captured. While the format of the config file is not important, I use [`yacs`](https://github.com/rbgirshick/yacs) and it does the job.

# A STUPID SIMPLE EXAMPLE
To make explanation easier, here's a simple example. An image classifier that decides if an image is light, or dark. Simple. We'll use a ResNet for this. We will auto generate data so let's not worry about that. That leaves us with only the training hyperparameters and the model hyperparameters. We'll assume a loss function and optimiser, and let's forgo learning rate scheduling. Our hyperparameters are therefore:
 - model size,
 - learning rate,
 - batch size
 - number of epochs

Nice and simple. Let's configure this thing!

# GETTIN' CONFIGURED
The basic components of the configured experiment are:
 - a default config file containing all the configurable parameters,
 - a way of building your experiment from a given config file

The config file should have sensible defaults: you don't want to specify every parameter in every config file. It would be useful to only specify a couple of parameters because then it is easy to see at a glance what each config file is doing.

This default config should be set up in a function. For our simple example:

{% highlight python %}
# simpleyacs/config.py
from yacs import CfgNode

def get_config() -> CfgNode:

    cfg = CfgNode()

    # I like to include an 'action' key in my configs.
    # This lets you choose what to do with the model/data/hyperparams
    # for example, you might want to run a quick training to make sure
    # things are working ok before running in depth cross validation
    # using the same settings.
    cfg.action = 'train'

    # desribe the model
    cfg.model = CfgNode()

    # Here we only have one parameter relating to the model: n.
    cfg.model.n = 18 # Size of ResNet model. One of 18, 34, 50, 101, 152.

    # Parameters related to training
    cfg.training = CfgNode()

    cfg.training.lr = 1e-5

    # How many epochs?
    cfg.training.n_epochs = 5

    # Batch size - how many images to pass at once
    cfg.training.batch_size = 4

    # Data is stored here as we go.
    cfg.output_dir = 'training_results/{today}'

    return cfg
{% endhighlight %}

This config node is just a data store - a collection of settings in a key-value manner. Handily, settings can be organised into subnodes (see `training` and `model` above). The idea from here is to pass this object around and use it to build up the model/set up training/etc. For example, let's look at a ridiculously simple example of building a ML model:

{% highlight python %}
# simpleyacs/model.py
from typing import Literal

from torch import nn
from torchvision.models import resnet

from .config import CfgNode


class SimpleYacsModel(nn.Module):

    RESNET_SIZE = Literal[18, 34, 50, 101, 152]

    def __init__(self, n: RESNET_SIZE):
        super().__init__()
        resnet_func = getattr(resnet, f'resnet{n}')
        resnet_weights = getattr(resnet, f'ResNet{n}_Weights')
        self.resnet = resnet_func(weights=resnet_weights.DEFAULT)
        self.resnet.fc = nn.Sequential(
            nn.Linear(512, 128),
            nn.Linear(128, 1),
        )

    @classmethod
    def from_config(cls, cfg: CfgNode):
        return cls(n=cfg.model.n)

    def forward(self, x):
        return self.resnet(x)
{% endhighlight %}

So we can build up a model using settings stored in the config object, just by using the `.from_config(...)` factory method.

This isn't very useful, loading a default config and running it. How do we load custom values? `yacs` is great: this is very simple:

{% highlight python %}
from simpleyacs.config import get_config

cfg = get_config()
cfg.merge_from_file('/path/to/config_file.yaml')
{% endhighlight %}

This overrides every default value with those specified in the given YAML file. YAML is a simple markup language (a way of structuring data in a file). This is composed of keys and values, with colons in between. A value can also be a set of keys and values. For example:

{% highlight yaml %}
# experiments/exp_test.yaml
action: train
training:
  batch_size: 10
  n_epochs: 10
model:
  n: 18
{% endhighlight %}

The above yaml file has an `action` key with a string value `"train"`, `training` has a value which is another node with `batch_size` of integer `10` and `n_epochs` also of integer `10`.

To make the process of loading config easier, I typically write a `run.py` script which takes the given config file as an argument. In fact, it takes several. This allows you to queue up a bunch of experiments to run one after the other.

{% highlight python %}
import argparse
from tqdm import tqdm

from simpleyacs.run import run


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', nargs='+', help='experiment config file(s) to run')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for exp in tqdm(args.experiment, unit='experiments'):
        run(exp)
{% endhighlight %}

The full code for the above example is on GitHub [here](https://github.com/cbosoft/simpleyacs), peruse at will.

# SUM IT UP
1. Create a single object which contains all the options for your experiment and sensible defaults
2. Write config file(s)
3. Run your experiment(s)
4. Sit back with a cup of tea and wait for your results
