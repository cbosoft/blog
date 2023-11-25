---
title: "Better Black Boxes By Bayesian B...optimisation"
layout: post
excerpt: "Training a deep learning model is costly. Optimising the model hyperparameters, even more so. We can learn lessons from lab experiment design and apply it to hyperparameter optimisation to reduce the amount of training required"
tags: Python ml sustainability
---

# Hyperparameter Optimisation

A deep learning model is big and needs training carefully to achieve good results. The large model is very capable of overfitting to a problem and being useless when applied outside its training set. We need to ensure this doesn't happen by carefully choosing the manner in which it is trained. This process of deciding how to train the model  is called hyperparameter optimisation. (This also includes choosing other meta-parameters like model architecture, or augmentation.)

To perform hyperparameter optimisation, a model is trained and validated (ideally by some form of cross-validation) to give a baseline. Then, the hyperparameters are changed and the training repeated. In a brute force approach, this process is repeated until all combinations of hyperparameters have been investigated and the best choice (decided by performance on validation set) is found.

For example, say we have a ResNet image classifier. We have a couple sizes of the model to choose from (18 or 34 layers), and we are deciding whether to apply random cropping during training, or not. Our hyperparameter space has four points:
 1. ResNet18 and no random crop,
 2. ResNet34 and no random crop,
 3. ResNet18 and random crop,
 4. ResNet34 and random crop.

A model is trained using each approach and the best of the four is chosen. This is a small space and only 4 experiments are required. However, what if we were choosing from all possible resnets? What if we were looking at more augmentations, or different optimisers? The combinatorics mean the space explodes in size very quickly.

In a more heuristic approach, the ML engineer may choose some set of hyperparameters they feel is best and start from there. They may change one at a time and arrive at a "good" solution; a set of hyperparameters that will get the job done. However, they may be missing a really good set of parameters that results in a performant yet quickly trained model.

# Bayesian Boptimisation
In the face of expensive and time consuming experiments, scientists employ design of experiments (DoE) to efficiently explore their parameter space. One such method employes Bayes' theorem to estimate the areas of space which have highest error. We can use this to efficiently map out the space, using only experiments which will give us the most information. For example, if we know that n=8 works better than n=10 and n=6, we probably won't gain much by investigating n=4 or n=12.

In Bayesian Optimisation, uncertainty is estimated and used to target the investigation. The next experiment is chosen at the point of maximum uncertainty, thus guaranteeing the most information can be gained for each experiment.

# Gaussian Processes
A gaussian process is a model of a process, including an estimation of uncertainty. Perfect for Bayesian optimisation. As an example, a Gaussian process can be used to model a sine function.

<center class="standout">
<img src="{{site.baseurl}}/img/bayesian-bop/sine-est/2.png" style="display: inline-block; width: 30vw;">
<img src="{{site.baseurl}}/img/bayesian-bop/sine-est/3.png" style="display: inline-block; width: 30vw;">
<p>Sine function in black, gaussian process estimated from two points. Shaded area shows uncertainty and red point shows next point to be investigated, chosen by maximum uncertainty.</p>
</center>

In Python, Gaussian process models can be fit to data using the scikit-learn library.

{% highlight python %}
from sklearn.gaussian_process import GaussianProcessRegressor

model = GaussianProcessRegressor()

x = ... # all possible inputs
samples_x = ... # x values which have been run and we have corresponding y values for
samples_y = ... # y values corresponding to samples_x

model.fit(np.array(samples_x)[:, np.newaxis], samples_y)
my, myerr = model.predict(x[:, np.newaxis], return_std=True)
{% endhighlight %}

This gives model y, `my` and estimate of the variance/uncertainty/error in the model (`myerr`) for each `x` we pass to it (including points we haven't investigated yet). For hyperparameter optimisation we might want to find the parameters which minimise the error of our model. We use the Gaussian process model error to tell us which of the points we haven't investigated should be: the goal being to minimise total `myerr` (GP model error) and thus find the minimum value of `y` (maximising DL model performance).

Too many models? Sorry about that. Maybe an example would help...

# 🎶 Black Box Bayes Bop 🎵
To demonstrate Bayesian hyperparameter optimisation, let's look at a real deep learning model I'm working with. This model training process has a four hyper parameters:
 1. Encoder size $n$.
 2. Decoder architecture: "A" or "B".
 3. Whether to use dropout, and the probability with which it is applied.
 4. What strength of Gaussian noise should be added to the input (as data augmentation).

The process of Bayesian optimisation is fairly simple. We take a couple seed samples to fit an initial Gaussian process - we need to run a couple training experiments. The initial points chosen can be the extreme values of the search space (largest and smallest $n$, either decoder, no dropout and frequent dropout, no noise and max noise): this gives 16 experiments to run in total. I've found that we can get away with just seeding with four or so random points: the GP isn't that fussy about its starting information.

<div class="standout">
Your mileage may vary! My colleague found the Gaussian Process model to be relatively sensitive to starting point and recommended starting with the corners. His use-case was different, however, so that may explain the difference in sensitivity.
</div>

**TODO**: plots of starting point

**TODO**: plot of error after first run

**TODO**: plots of error after convergence

**TODO**: how many experiments? how many if brute forcing?

# Conclusions
**TODO**
