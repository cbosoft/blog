---
title: A Neural Network so simple its SINNfull
excerpt: In this post I look at the basics of Neural Networks, and build (a very simple) one from scratch.
layout: post
tags: ml software-dev C++
---

# Motivation
A little while ago a friend of mine showed me his stock trading bot. The bot
was given a bit of cash, a trading platform API key, and some simple rules to
follow. If a stock was rising, buy. If it started to fall, sell. There were
some buffer regions too, but that's the gist. I asked him if he'd thought
about incorporating some simple machine learning into the project, he seemed
unsure, he liked the simplicity of his solution I think. I started thinking
about doing this myself, it sounded like a fairly simple idea. And with high
level tools like Tensorflow available, it should be fairly easy to implement.

However, I am quite interested in the nuts and bolts of machine learning, so
I'm not going to use a high level package. I'm going to write my own neural
network, hopefully learning a lot along the way.

I'll start by looking at the basics and some of the history of machine
learning and neural networks, then I'll start going into the implementation
details.

The result is on my github [here](https://github.com/cbosoft/sinn").

## Machine Learning
Machine Learning (ML) started life in the 1950s as Artificial Intelligence
(AI). Programs were built to "reason" solutions to problems and identify
patterns. Neural Networks are one of the first forms of practical artificial
intelligence. They are modelled after the human brain: a series of neurons
which are either "firing" or "quiet" depending on the value of other neurons
or inputs. The first Neural Network machine was the SNARC built in 1951 and
designed by influential computer scientist Marvin Minsky (unfortunately
someone who was involved with that Epstein bloke).

<center>
  <img src="/img/snarc_neuron.png" width="60%"/>
  from: <a href="https://www.the-scientist.com/foundations/machine--learning--1951-65792">The Scientist article "Machine, Learning, 1951"</a>
</center>

<div class="message">
I have been trying to find a diagram of the SNARC, but no luck. It is probably
in Minsky's PhD thesis (University of Princeton, 1954), but I cannot access a
full version of the thesis. I have found a <a href="https://search.proquest.com/docview/301998727">preview version</a>, which only covers
the first 24 pages.

Unfortunately, his thesis is proving <i>really</i> tough to track down. I can find
no electronic copy anywhere, and no physical copies held by libraries willing
to lend. Sigh. I hope to someday see the designs for the electro-mechanical
learning machine!

Update March 2021: I have found a copy of the thesis! I'll need to devote a wee
bit of time to pouring through it to find any interesting notes.
</div>

A Neural Network is a common machine learning method, but there are others:
decision tree, hierarchical clustering, random forest, and even linear
regression. (I found <a href="https://machinelearningmastery.com/a-tour-of-machine-learning-algorithms/">this</a> article which has a lot more examples and some
information on each.) I was surprised to see that linear regression made the
list of machine learning algorithms. I guess I fell into the trap of AI: if I
understand it then it can't possible be real machine learning. (I definitely
read about that somewhere but I can't remember where.) 

I'll concentrate on the Neural Network, since it was one of the first, and is
still a top contender today (through its new form: deep neural networks).

# Neural Networks
A neural network is a network of neurons, of on-or-off binary signals,
connected by "dendrites". Neurons fire depending on the value of other
neurons. This is modelled by weighting the value of the all the dendrites,
edges, feeding into the neuron and summing. If the value passes a threshold,
it is firing. Otherwise, it is quiet.

For a neuron $$j$$, its value $$z_{j}$$ is the sum of the values of the neurons
input to it, **weighted** each by a factor $$w$$ plus a bias:

$$ z_{j} =  \sum_{i=0}^{N }v_{i}w_{i} + bias $$

The neuron value is then passed to an **activation function** which decides if
the neuron fires or stays quiet. This stage is very important and affects the
speed at which the network is trained and the effectiveness of the resulting
network. Essentially the function determines how the neuron responds to input:
how quickly a change in input changes the output, what thresholds there might
be and so on. The training methods (briefly described later on) rely on
*gradients*, as in the derivative of the output with respect to the input. The
derivative of the activation function therefore plays an important role in
training and must be chosen appropriately.

The "learning" aspect enters in by the evolution of the weights. Weights are
chosen so that a set of sample inputs gives an expected sample output. These
sample sets of inputs and outputs make up the **training dataset**. The process
of changing the weights is called training, and this is the key part of the
algorithm which teaches the net how to perform the desired task.

How are the weights found? The training set and expected output are key here:
the output from the network compared with the expected output gives us an
error. We can find the ideal weights by a few different methods, mediated by
the error. Gradient descent is a common method. Imagine the weights of a
network of two neurons. Plot the values of the error for each value of the two
weights giving us a surface plot. We want to minimise the error, so we want to
find the lowest amplitude location in our phase space (the landscape formed by
our weights and error plot). Gradient descent describes the path of walking
down this landscape to the minimum error by looking at the gradient of error
with respect to the weights.

There are other methods of finding this minimum point, and we have reduced the
complex task we want the network to do, to a minimisation problem! The task of
recognising the genus of a lilly plant based on the shape of its leaves is
just minimisation! Prediction of stock market prices is minimisation!
Classification of animals into bird, cat, or other is minimisation! 

Neural networks make it (relatively) easy to answer complex questions about
data, however it doesn't unveil much about the neural network's "thinking"
process. This is therefore a "black box" method, where the result is obtain by
an unknown method and therefore must come with a pinch of salt. This pinch of
salt is normally given as a confidence or certainty probability quoted
alongside the answer.

<center>
<img src="/img/serval.jpg"/><br />
from: <a href="https://bigcatrescue.org/pharaoh/">Big Cat Rescue</a> - Pharaoh the white serval
</center>

Even this has some caveats. The simple classification problem decribed above
of splitting all animals into cat or bird or other becomes quite tough when we
consider that many animals share aspects of cats. Is a serval a cat? What
about a puma? Or a whippet? Are lions? What about seals? Many of these
animals, purely via image analysis, could easily be confused for a cat via
similar body shapes, or straight up close genetic make-up. The neural network
used to answer the question needs to have complexity enough to fully encompass
the solution. It needs to pick up on subtle differences between the serval and
the cat, or it will mis-classify.

In the wall of text I have spouted here we can identify the two components of
a successful neural network: **sufficient complexity** (i.e. enough neurons) to
describe the solution fully, and **good quality training data** to create the
pattern in the network.

## Layers
I've talked about a Neuron, the nodes in our graph network, but how are the
neurons connected?

<center>
<img src="/img/neural_network_example.png"/><br />
</center>

<p>
Neurons are grouped together in "layers". Layers could be thought of as
performing a specific action: taking input, performing an elaboration, or
giving output. Each layer's neurons are each connected to every neuron in the
previous and subsequent layer.
</p>

<p>
We have an input layer, which takes information from <i>somewhere</i> and its
neurons fire or are quiet depending on the values input.
</p>

<p>
There may or may not be layers in the middle called "hidden layers". Neural
networks can operate without a hidden layer, but many may perform better with
one. I reason them as being used to filter out the inputs to give the
important ones, or to convert the inputs into another form, internally.
</p>

<p>
Then there's the output layer; this takes a pattern of neuron fires/quiets
and produces a final value.
</p>

<p>
Deciding upon the number of neurons in a layer is an important design
question that must be answered. There are, thankfully, some very smart people
on the web with answers to these questions. <a href="https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw">This post</a> on StackExchange has
some handy information (although a little bit dated - question was
posted 2011) about how to design a neural net layer.
</p>

<p>
Input layers should have enough neurons to capture the complexity of what is
being analysed. If the input is an image, the input layer should be able to
read the value of the pixels in the image. If the input is a number of
features ("has ears", "has wings", "lays eggs", etc), then there needs to be
a neuron for each feature.
</p>

<p>
Output layers need neurons sufficient to convey the result. If output is a
label, then a neuron per possible label is required. (This type of output is
termed a "classifier".) If output is a continuous number (e.g. a price, a
size, a liklihood&#x2026;) then a single output node is required. (Or, a node per
desired value).
</p>

<p>
Hidden layers are the hard part. They're difficult to reason: should the
intermediary layers be intermediary in size? Or perhaps larger to emaphsise
subtlety in the input? In fact, how many hidden layers should there be? None?
Just the one? More?
</p>

<p>
The StackExchange post cites a book (<i>"Introduction to Neural Networks for
Java"</i> by Jeff Heaton, 2008) which gives a little insight into the effect of
hidden layers:
</p>

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">Number of hidden layers</th>
<th scope="col" class="org-left">Result</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-right">0</td>
<td class="org-left">Only capable of representing linear separable functions or decisions.</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-left">Can approximate any function that contains a continuous mapping from one finite space to another.</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-left">Can represent an arbitrary decision boundary to arbitrary accuracy with rational activation functions and can approximate any smooth mapping to any accuracy.</td>
</tr>
</tbody>
</table>

<p>
So more hidden layers, means more complexity that can be captured, and gives
more confidence in fine-grain output. The first layer sees patterns in the
input, subsequent layers see patterns in the patterns.
</p>

<p>
The wikipedia <a href="https://en.wikipedia.org/wiki/Deep_learning">article</a> on deep learning is quite good and has a lot of
information. It include a fantastic image which gives an intuition for the
hidden layers:
</p>

<center>
  <img src="/img/deep_learning.jpg" width="60%"/><br />
  from: <a href="https://commons.wikimedia.org/wiki/File:Deep_Learning.jpg">Wikimedia Commons</a>: Deep Learning.jpg by Sven Behnke <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC-BY-SA 4.0</a>
</center>

<p>
The first layer sees basic patterns: edges in the image. The second layer is
taught to recognise shapes, third then recognises an ear, or the shape of a
head, perhaps a leg. Then the output is able to recognise the elephant. Each
layer adds a step of clarity, a layer of construction. I guess the intuition
here is that the initial layer blows up the input into its smallest
components, which may be enough to go direct to an output layer. If the
pattern you're looking for is hidden under layers of complexity, then hidden
layers are needed to use the pieces extracted from the input layer to build
up something that can be recognised.
</p>

<h2 id="org20cc5b1">Training</h2>
<p>
I briefly touch upon the concept of training earlier: the process of choosing
weights correctly such that the output of the net given a sample input is what
is expected. I mentioned the gradient descent algorithm (walking down a hilly
landscape to the basin - representing the minimisation of the error in
results), but there are other <b>optimisation algorithms</b>:
</p>

<ul class="org-ul">
<li>Newton's method</li>
<li>Conjugate Gradient</li>
<li>Quasi-Newton</li>
<li>Levenberg-Marquardt</li>
</ul>

<p>
And more. I'm going to use gradient descent as it is simple, and this is a
simple neural network. Information on the others mentioned above in this
<a href="https://www.neuraldesigner.com/blog/5_algorithms_to_train_a_neural_network">article</a>. Regardless of the optimisation method you use, the process is the same:
</p>

<center>
  <img src="/img/nn_training_flowchart.png"/><br />
</center>

<p>
Update weight values using the optimiser, then check to see if we're at an
acceptably low error. If so, end. Otherwise, optimise again.
</p>

<p>
Error is calculated using a <b>training dataset</b>. This is a set of data which
contains inputs, and the corresponding outputs. This could be a bunch of
handwritten numbers as input, and the integer representation of the numbers as
output. The error is a measure of how "far" the neural network's output is
from the expected output. This is measured over the whole of the training
dataset: with each input and output pair adding to the total error.
</p>

<p>
One pass through the entire learning dataset is called an <b>epoch</b>.
</p>

<p>
As you can imagine, datasets are (normally) large. Very large. This can make
computation of an epoch difficult, in which case it can be useful to split up
the epoch into batches. The batches are iterated over until the epoch is
calculated. This <a href="https://towardsdatascience.com/epoch-vs-iterations-vs-batch-size-4dfb9c7ce9c9">article</a> goes in to more detail about the difference between
epochs, batches, iterations.
</p>

<p>
Once the entire dataset is processed and the weights are updated, we may have
a rough solution. How rough? We analyse this using the error.
</p>

<p>
We want the error to be zero, in an ideal world. However, this is not
practical so we just want the error to be low. In fact, if the error <i>was</i>
zero, then it is likely that we have <b>over fit</b> our network to our
training dataset. This means that instead of learning how to do the generic
action of converting input to output, it has learned to do the more specific
task of converting <i>training input</i> into <i>training output</i> and it may not work
on other, real world, data. (This is like a student studying the answers for
an exam, not the method.)
</p>

<p>
With the threat of over-training, we need to train just enough to meet our
target accuracy <b>and no more</b>. This has the added benefit of being
computationally efficient: no wasting time getting to 0.0001% error, when 1%
will do.
</p>

<p>
On the other hand, if we don't train the network enough, we get
<b>underfitting</b>: a poor performing neural network which mis-classifies too
often.
</p>

<p>
Choosing the number of epochs, the right amount of training, is a difficult
question. The answer I've found so far is to use trial and error.
</p>

<h2 id="orgbef4e1c">Testing</h2>
<p>
I'm building up from nothing, so I'll need some way of testing the network and
the training process to check they're working as expected. Luckily, this
process is pretty much the same as the training process, involving the same
data too. I'll need a dataset of test inputs with their corresponding
outputs. This means I can check the 'net is working by training it against
some members of the set, then verifying it with the rest of the set. 
</p>

<p>
What sets this apart from just more training, is that the training algorithm
itself will be analysed: does the error fall as training proceeds? If not, why
not? What's broken?
</p>

<p>
For this stage, I'll need a variety of test data and sample networks. Starting
from the absurdly simple linear regression case, moving up in complexity to
something which closer resembles my end goal.
</p>

<ol class="org-ol">
<li><p>
Simple Linear Regression
</p>

<p>
A linear function \(f(x)\) gives an output \(y\):
</p>

<p>
\[ y = f(x) = mx + c \]
</p>

<p>
This is the simplest case I could think of. The input layer has only a single
neuron, as does the output. Therefore there is a single weight to find (the
gradient) and a single bias (the intercept).
</p>

<p>
This case will test the training algorithm's ability to find and settle upon
weights and biases.
</p></li>

<li><p>
Next in series (1)
</p>

<p>
Given a vector, a function \(f(\vec{x})\) gives the next item in the series:
</p>

<p>
\[ x_{n+1} = f([x_{n} + x_{n-1} + x_{n-2} + ... + x_{2} + x_{1}]) \]
</p>

<p>
This is a little more abstract, a little more complex. The series in
question is series of natural numbers (whole numbers from 1 to N):
</p>

<p>
\[ y_{i+1} = y_{i} + 1 \]
\[ y_{1} = 1 \]
</p>

<p>
or
</p>

<p>
\[ y_{i} = i \]
</p></li>
</ol>

<h2 id="org64e6397">Implementing a Neural Network</h2>
<p>
Alright, so how do we go about building a neural network? Well the quick
answer is to use a library like <code>Tensorflow</code>, <code>Theano</code>, <code>scikit-learn</code>, or
anything else that floats your boat. The whole idea here however is that I'd
like to start a bit lower to get a good grasp of how these higher level
libraries are implemented, so I'll build up in <code>C++</code>.
</p>

<p>
A quick recap: a neural network is composed of a bunch of neurons, organised
into layers. The network performs a task, for which it is trained. The
training process decides the value of the weight values for passing
information forward from neuron to neuron.
</p>

<p>
A layer is composed of a number of neurons, each connected to every other
neuron in the layer preceding it. The number of neurons in a successive layer
is used to reduce complexity down to the final output. If a net is being
designed to find an answer to a yes/no question, the final layer (before the
output layer) might only have a few neurons, the output layer having only one
(which fires for "yes" and is quiet for "no").
</p>

<h3 id="org8989472">Neuron</h3>
<p>
Let's start with the basic building block: the neuron. This object will
contain a reference to its input connections, and their associated weights.
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/neuron.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;vector&gt;</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">Neuron</span> {

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">Neuron</span>() =<span style="color: #9cdcfe;">default</span>;
      <span style="color: #9cdcfe;">virtual</span> ~<span style="color: #dcdcaa;">Neuron</span>() =<span style="color: #9cdcfe;">default</span>;

      <span style="color: #9cdcfe;">virtual</span> <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_value</span>() =0;
  };

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
The Neuron base class is never intended to be used directly, only through its
sub-classes. The only common method through all Neuron sub-classes is
<code>get_value()</code>, which calculates the value of a Neuron based on its weights,
bias, and inputs. I've included this here as a pure virtual function, ready
to be overridden by the sub classes.
</p>

<p>
This base class will provide a standard interface to the derived
classes. (How great is polymorphism in <code>C++</code>?) With our base interface in
place, let's derive a neuron for the hidden and output layers:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/hidden_neuron.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"activation_functions/activation_function.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">NeuralNetwork</span>;
  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">HiddenNeuron</span> : <span style="color: #9cdcfe;">public</span> <span style="color: #569cd6;">Neuron</span> {

    <span style="color: #9cdcfe;">private</span>:

      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">Neuron</span> *&gt; <span style="color: #fff;">in</span>;
      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">weights</span>;
      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">substitute_weights</span>;
      <span style="color: #569cd6;">double</span> <span style="color: #fff;">bias</span>;
      <span style="color: #569cd6;">double</span> <span style="color: #fff;">substitute_bias</span>;
      <span style="color: #569cd6;">ActivationFunction</span> *<span style="color: #fff;">activation_function</span>;

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">HiddenNeuron</span>(<span style="color: #569cd6;">ActivationFunction</span> *<span style="color: #fff;">actfunc</span>);
      ~<span style="color: #dcdcaa;">HiddenNeuron</span>() =<span style="color: #9cdcfe;">default</span>;

      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_value</span>() <span style="color: #9cdcfe;">override</span>;
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">add_weighted_input</span>(<span style="color: #569cd6;">Neuron</span> *<span style="color: #fff;">neuron</span>, <span style="color: #569cd6;">double</span> <span style="color: #fff;">weight</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_activation_function</span>(<span style="color: #569cd6;">ActivationFunction</span> *<span style="color: #fff;">activation_function</span>);

      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_bias</span>();
      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_substitute_bias</span>();
      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_weight</span>(<span style="color: #569cd6;">int</span>);
      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_substitute_weight</span>(<span style="color: #569cd6;">int</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_bias</span>(<span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_substitute_bias</span>(<span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_weight</span>(<span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_substitute_weight</span>(<span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">swap_weights_and_bias</span>();

      <span style="color: #9cdcfe;">friend</span> <span style="color: #569cd6;">NeuralNetwork</span>;

  };

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
The Hidden Neuron is a neuron in a hidden (or output) layer. These neurons
take input from a previous layer of neurons, which are weighted and summed
with bias to form an output. So in this header I've declared the override
<code>get_value()</code> method, as well as methods for linking the neuron to an input
Neuron, setting weights and biases, and setting the activation function.
</p>

<p>
The <code>get_value()</code> function is pretty simple, just adding the weighted values
of the inputs:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/hidden_neuron.cpp</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"hidden_neuron.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #569cd6;">double</span> <span style="color: #569cd6;">HiddenNeuron</span>::<span style="color: #dcdcaa;">get_value</span>()
  {
    <span style="color: #569cd6;">double</span> <span style="color: #fff;">total</span> = 0.0;

    <span style="color: #9cdcfe;">for</span> (<span style="color: #569cd6;">size_t</span> <span style="color: #fff;">i</span> = 0; i &lt; <span style="color: #9cdcfe;">this</span>-&gt;in.size(); i++) {
      <span style="color: #569cd6;">Neuron</span> *<span style="color: #fff;">neuron</span> = <span style="color: #9cdcfe;">this</span>-&gt;in[i];
      <span style="color: #569cd6;">double</span> <span style="color: #fff;">weight</span> = <span style="color: #9cdcfe;">this</span>-&gt;weights[i];
      total += neuron-&gt;get_value()*weight;
    }
    <span style="color: #9cdcfe;">return</span> <span style="color: #9cdcfe;">this</span>-&gt;activation_function-&gt;calculate_value(total);
  };

}; <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
This is the main functionality of the hidden- and output-layer neurons:
process information from an upstream layer of neurons. What about the input?
For this implementation, input "neurons" are just placeholders, taking a
value and returning it as their own.
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/input_neuron.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neuron.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">InputNeuron</span> : <span style="color: #9cdcfe;">public</span> <span style="color: #569cd6;">Neuron</span> {

    <span style="color: #9cdcfe;">private</span>:

      <span style="color: #569cd6;">double</span> <span style="color: #fff;">value</span>;

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">InputNeuron</span>(<span style="color: #569cd6;">double</span> <span style="color: #fff;">value</span>);
      ~<span style="color: #dcdcaa;">InputNeuron</span>() =<span style="color: #9cdcfe;">default</span>;

      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_value</span>() <span style="color: #9cdcfe;">override</span>;
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_value</span>(<span style="color: #569cd6;">double</span> <span style="color: #fff;">value</span>);

  };

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
The constructor this time takes a value as input, which the neuron can then
return when asked for its value:
</p>

<pre class="src src-C++"><span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #569cd6;">InputNeuron</span>::<span style="color: #dcdcaa;">get_value</span>()
  {
    <span style="color: #9cdcfe;">return</span> <span style="color: #9cdcfe;">this</span>-&gt;value;
  }

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<h3 id="org0cb1296">Layer</h3>
<p>
Next up, organising neurons into Layers. Layers, for this API, are nice ways
of constructing a number of neurons with specified weights.
</p>

<p>
As with the Neuron, I'll start with an abstract base which will be overridden
by more specific sub-classes:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/layer.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;vector&gt;</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neuron.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {
  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">NeuralNetwork</span>;
  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">Layer</span> {

    <span style="color: #9cdcfe;">protected</span>:

      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">Neuron</span> *&gt; <span style="color: #fff;">neurons</span>;

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">Layer</span>() =<span style="color: #9cdcfe;">default</span>;
      <span style="color: #9cdcfe;">virtual</span> ~<span style="color: #dcdcaa;">Layer</span>();

      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">add_neuron</span>(<span style="color: #569cd6;">Neuron</span> *<span style="color: #fff;">neuron</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">clear_neurons</span>();

      <span style="color: #9cdcfe;">friend</span> <span style="color: #569cd6;">NeuralNetwork</span>;

  };
} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
A <code>Layer</code> consists of a vector of <code>Neurons</code>, and that's it. It's friends with
the <code>NeuralNetwork</code> class, good for them. (It's handy to be able to access
<code>Neurons</code> directly from the NN.)
</p>

<p>
Nothing really special here. As with the <code>Neurons</code> there are Input and Hidden
derived classes, however there is also an Output derivation. The
<code>HiddenLayer</code> subclass is just to keep the nomenclature the same, really, bar
a small <code>generate_neurons(int n)</code> method which allows for the easy creation
of neurons:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/hidden_layer.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"hidden_neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"layer.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">HiddenLayer</span> : <span style="color: #9cdcfe;">public</span> <span style="color: #569cd6;">Layer</span> {

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">HiddenLayer</span>(<span style="color: #569cd6;">int</span> <span style="color: #fff;">n</span>);
      ~<span style="color: #dcdcaa;">HiddenLayer</span>() =<span style="color: #9cdcfe;">default</span>;


      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">generate_neurons</span>(<span style="color: #569cd6;">int</span> <span style="color: #fff;">n</span>);

  };

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
The <code>InputLayer</code> is a little more different, constructed with not a number of
neurons, but a vector of the values for the <code>InputNeurons</code> that make up the
layer:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">TODO</span>
</pre>

<p>
And the <code>OutputLayer</code>:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">TODO</span>
</pre>

<h3 id="org14b2101">Network</h3>
<p>
With the organisational stuff out of the way, on to the meat of the thing!
The <code>NeuralNetwork</code> is a network of <code>Neurons</code>, abstracted through <code>Layers</code>. I
suppose the Network class is another "organisational thing", but this one
does stuff too! It takes data (vector of float) and processes through the
network and returns the result. Also, it can <i>learn</i>!
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/neural_network.hpp</span>
<span style="color:  #dcdcaa;">#pragma</span> once

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;string&gt;</span>

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"layer.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #9cdcfe;">class</span> <span style="color: #569cd6;">NeuralNetwork</span> {

    <span style="color: #9cdcfe;">private</span>:

      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">Layer</span> *&gt; <span style="color: #fff;">layers</span>;
      <span style="color: #569cd6;">double</span> <span style="color: #fff;">last_error</span>;

    <span style="color: #9cdcfe;">public</span>:

      <span style="color: #dcdcaa;">NeuralNetwork</span>();


      <span style="color: #5C6370;">// </span><span style="color: #5C6370;">nn_print.cpp</span>
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">print</span>();

      <span style="color: #5C6370;">// </span><span style="color: #5C6370;">train.cpp</span>
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">train</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_inputs</span>, 
                 <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_outputs</span>, 
                 <span style="color: #569cd6;">double</span> <span style="color: #fff;">learning_rate</span>, <span style="color: #569cd6;">double</span> <span style="color: #fff;">dWeight</span>=1e-5);
      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_error</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_inputs</span>, 
                       <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_outputs</span>);

      <span style="color: #5C6370;">// </span><span style="color: #5C6370;">nn_dot.cpp</span>
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">as_dot</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">string</span> <span style="color: #fff;">filename</span>) <span style="color: #9cdcfe;">const</span>;

      <span style="color: #5C6370;">// </span><span style="color: #5C6370;">neural_network.cpp</span>
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">link_layers_weighted</span>(<span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">link_layers_normal</span>(<span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">double</span>, <span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">link_layers_uniform</span>(<span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">int</span>, <span style="color: #569cd6;">double</span>, <span style="color: #569cd6;">double</span>);

      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">add_layer_weighted</span>(<span style="color: #569cd6;">Layer</span> *<span style="color: #fff;">layer</span>, <span style="color: #569cd6;">double</span> <span style="color: #fff;">weight</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">add_layer_normal</span>(<span style="color: #569cd6;">Layer</span> *<span style="color: #fff;">layer</span>, <span style="color: #569cd6;">double</span>, <span style="color: #569cd6;">double</span>);
      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">add_layer_uniform</span>(<span style="color: #569cd6;">Layer</span> *<span style="color: #fff;">layer</span>, <span style="color: #569cd6;">double</span>, <span style="color: #569cd6;">double</span>);

      <span style="color: #569cd6;">void</span> <span style="color: #dcdcaa;">set_input</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">input</span>);
      <span style="color: #569cd6;">double</span> <span style="color: #dcdcaa;">get_last_error</span>() <span style="color: #9cdcfe;">const</span>;
      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #dcdcaa;">get_output</span>() <span style="color: #9cdcfe;">const</span>;
      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #dcdcaa;">get_output</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">input</span>);

      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #9cdcfe;">operator</span><span style="color: #dcdcaa;">()</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">input</span>)
      {
        <span style="color: #9cdcfe;">return</span> <span style="color: #9cdcfe;">this</span>-&gt;get_output(input);
      }

  };

} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
Notable methods here are <code>train()</code> and <code>get_error()</code>.
</p>

<p>
Layers are added one by one, starting from the furthest upstream (an
<code>InputLayer</code>). As they are added, their <code>Neurons</code> are linked together,
forming the Network:
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/neural_network.cpp</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;iostream&gt;</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;sstream&gt;</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;fstream&gt;</span>

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"util.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"exception.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"hidden_neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neural_network.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"input_neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"output_layer.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #569cd6;">void</span> <span style="color: #569cd6;">NeuralNetwork</span>::<span style="color: #dcdcaa;">add_layer_weighted</span>(<span style="color: #569cd6;">Layer</span> *<span style="color: #fff;">layer</span>, <span style="color: #569cd6;">double</span> <span style="color: #fff;">weight</span>)
  {
    <span style="color: #9cdcfe;">this</span>-&gt;layers.push_back(layer);

    <span style="color: #569cd6;">size_t</span> <span style="color: #fff;">nlayers</span> = <span style="color: #9cdcfe;">this</span>-&gt;layers.size();
    <span style="color: #9cdcfe;">if</span> (nlayers &gt; 1) {
      <span style="color: #9cdcfe;">for</span> (<span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">previous</span> : <span style="color: #9cdcfe;">this</span>-&gt;layers[nlayers-2]-&gt;neurons) {
        <span style="color: #9cdcfe;">for</span> (<span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">latest</span> : <span style="color: #9cdcfe;">this</span>-&gt;layers[nlayers-1]-&gt;neurons) {

          ((<span style="color: #569cd6;">HiddenNeuron</span> *)latest)-&gt;add_weighted_input(previous, weight);
        }
      }
    }
  } 

}; <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
There are other forms of the <code>add_layer..()</code> function which generate a random
starting weight (uniform or guassian), but the plain one here takes in a
starting weight as given.
</p>

<p>
The final layer should be an <code>OutputLayer</code>, completing the network streaming
data from Input to Output.
</p>

<h3 id="org28075a1">Gradient Descent</h3>
<p>
Gradient descent is the training process of measuring the error's rate of
change with respect to the weights/biases, and altering the weights/biases
accordingly. This starts with calculating the Error for the current set of
weights and biases. A training dataset (<i>i.e.</i> one with solutions) is passed
through the Network, and the error is calculated as the sum of the square
of the difference between the calculated output and the desired output.
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/train.cpp</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;iostream&gt;</span>

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neural_network.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"hidden_neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"output_layer.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"util.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #569cd6;">double</span> <span style="color: #569cd6;">NeuralNetwork</span>::<span style="color: #dcdcaa;">get_error</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_inputs</span>, 
                                  <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_outputs</span>)
  {

    <span style="color: #9cdcfe;">if</span> (training_inputs.size() != training_outputs.size()) {
      <span style="color: #569cd6;">std</span>::cerr &lt;&lt; <span style="color: #7cb461;">"net::get_error: training dataset inputs must match size of outputs."</span> &lt;&lt; <span style="color: #569cd6;">std</span>::endl;
    }

    <span style="color: #569cd6;">double</span> <span style="color: #fff;">total_error</span> = 0.0;
    <span style="color: #9cdcfe;">for</span> (<span style="color: #569cd6;">size_t</span> <span style="color: #fff;">set_index</span> = 0; set_index &lt; training_inputs.size(); set_index++) {
      <span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">input</span> = training_inputs[set_index];
      <span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">output</span> = training_outputs[set_index];
      <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt; <span style="color: #fff;">value</span> = <span style="color: #9cdcfe;">this</span>-&gt;get_output(input);
      total_error += <span style="color: #569cd6;">sinn</span>::<span style="color: #569cd6;">util</span>::sumsqdiff(value, output);
    }

    <span style="color: #9cdcfe;">this</span>-&gt;last_error = total_error;
    <span style="color: #9cdcfe;">return</span> total_error;
  }


} <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<p>
The error can be calculated before and after a small change (<i>perturbation</i>)
is made to <i>a</i> weight/bias: the rate of change of the error with respect to
<i>that weight or bias</i> can be approximated from:
</p>

<p>
\[ \frac{dError}{dWeight} \approx \frac{\Delta{}Error}{\Delta{}Weight} = \frac{Error_{after} - Error_{before}}{Perturbation_{Weight}} \]
</p>

<p>
Using the gradient, a required change in that weight or bias can be calculated:
</p>

<p>
\[ dWeight = -\frac{dError}{dWeight}\eta \]
</p>

<p>
Where \(\eta\) is the learning rate. This is the descent part, the rate of
change is like a steepness, and the learning rate is a step size. We want to
walk down the hill, so there's a negative sign in front.  This desired change
is stored until all the gradients have been calculated, then it is
enacted. This process should reduce the error to an acceptably low value.
</p>

<pre class="src src-C++"><span style="color: #5C6370;">// </span><span style="color: #5C6370;">src/train.cpp</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">&lt;iostream&gt;</span>

<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"neural_network.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"hidden_neuron.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"output_layer.hpp"</span>
<span style="color:  #dcdcaa;">#include</span> <span style="color: #7cb461;">"util.hpp"</span>

<span style="color: #9cdcfe;">namespace</span> <span style="color: #569cd6;">sinn</span> {

  <span style="color: #569cd6;">void</span> <span style="color: #569cd6;">NeuralNetwork</span>::<span style="color: #dcdcaa;">train</span>(<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_inputs</span>, 
                            <span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">std</span>::<span style="color: #569cd6;">vector</span>&lt;<span style="color: #569cd6;">double</span>&gt;&gt; <span style="color: #fff;">training_outputs</span>, 
                            <span style="color: #569cd6;">double</span> <span style="color: #fff;">learning_rate</span>, 
                            <span style="color: #569cd6;">double</span> <span style="color: #fff;">dWeight</span>)
  {
    <span style="color: #569cd6;">double</span> <span style="color: #fff;">initial_error</span> = <span style="color: #9cdcfe;">this</span>-&gt;get_error(training_inputs, training_outputs);
    <span style="color: #9cdcfe;">for</span> (<span style="color: #569cd6;">size_t</span> <span style="color: #fff;">layer_index</span> = 1; layer_index &lt; <span style="color: #9cdcfe;">this</span>-&gt;layers.size(); layer_index++) {
      <span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">layer</span> = <span style="color: #9cdcfe;">this</span>-&gt;layers[layer_index];

      <span style="color: #9cdcfe;">for</span> (<span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">_neuron</span> : layer-&gt;neurons) {
        <span style="color: #569cd6;">HiddenNeuron</span> *<span style="color: #fff;">neuron</span> = ((<span style="color: #569cd6;">HiddenNeuron</span> *)_neuron);

        <span style="color: #9cdcfe;">for</span> (<span style="color: #569cd6;">size_t</span> <span style="color: #fff;">weight_index</span> = 0; weight_index &lt; neuron-&gt;weights.size(); weight_index++) {

          <span style="color: #569cd6;">double</span> <span style="color: #fff;">weight_before</span> = neuron-&gt;weights[weight_index];
          neuron-&gt;weights[weight_index] += dWeight;
          <span style="color: #569cd6;">double</span> <span style="color: #fff;">dError</span> = <span style="color: #9cdcfe;">this</span>-&gt;get_error(training_inputs, training_outputs) - initial_error;
          neuron-&gt;weights[weight_index] = weight_before; <span style="color: #5C6370;">// </span><span style="color: #5C6370;">done in this way to prevent possible </span>
                                                         <span style="color: #5C6370;">// </span><span style="color: #5C6370;">floating point errors introduced by </span>
                                                         <span style="color: #5C6370;">// </span><span style="color: #5C6370;">adding and subtracting</span>

          <span style="color: #569cd6;">double</span> <span style="color: #fff;">gradient</span> = (dError == 0) ? 0 : dWeight/dError;
          <span style="color: #5C6370;">//</span><span style="color: #5C6370;">double gradient = dWeight/dError;</span>
          <span style="color: #5C6370;">//</span><span style="color: #5C6370;">std::cout &lt;&lt; dError &lt;&lt; "  " &lt;&lt; gradient  &lt;&lt; std::endl;</span>
          neuron-&gt;set_substitute_weight(weight_index, weight_before - (learning_rate * gradient));

        }

        {
          <span style="color: #569cd6;">double</span> <span style="color: #fff;">bias_before</span> = neuron-&gt;get_bias();
          neuron-&gt;set_bias(bias_before + dWeight);
          <span style="color: #569cd6;">double</span> <span style="color: #fff;">dError</span> = <span style="color: #9cdcfe;">this</span>-&gt;get_error(training_inputs, training_outputs) - initial_error;
          neuron-&gt;set_bias(bias_before);

          <span style="color: #569cd6;">double</span> <span style="color: #fff;">gradient</span> = (dError == 0.0) ? 0.0 : dWeight/dError;
          neuron-&gt;set_substitute_bias(bias_before - (learning_rate * gradient));
        }

      }
    }


    <span style="color: #9cdcfe;">for</span> (<span style="color: #569cd6;">size_t</span> <span style="color: #fff;">layer_index</span> = 1; layer_index &lt; <span style="color: #9cdcfe;">this</span>-&gt;layers.size(); layer_index++) {
      <span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">layer</span> = <span style="color: #9cdcfe;">this</span>-&gt;layers[layer_index];

      <span style="color: #9cdcfe;">for</span> (<span style="color: #9cdcfe;">auto</span> <span style="color: #fff;">_neuron</span> : layer-&gt;neurons)
        ((<span style="color: #569cd6;">HiddenNeuron</span> *)_neuron)-&gt;swap_weights_and_bias();

    }

    <span style="color: #9cdcfe;">this</span>-&gt;get_error(training_inputs, training_outputs);
    <span style="color: #5C6370;">//</span><span style="color: #5C6370;">std::cerr &lt;&lt; this-&gt;last_error &lt;&lt; std::endl;</span>
  }

}; <span style="color: #5C6370;">// </span><span style="color: #5C6370;">namespace sinn</span>
</pre>

<h2 id="org66f675e">Demonstration</h2>
<p>
In the repository I have some tests prepared for some <b>very</b> simple
use-cases. To run them, clone the repo and just <code>make</code>. It depends only on
<code>gcc</code>. The test cases are the two discussed above. Here's an underwhelming gif
of the network being built and the tests being run:
</p>

<center>
  <img src="/img/nn_tests.gif" width="60%"/><br />
</center>

<h2 id="orgca490f2">Closing remarks</h2>
<p>
In this post I've shown how simple a neural network can be, in my simple
literal implementation. There are many improvements that could be made (back
propagating learning, fewer abstractions, better testing), but sadly I lack
the time.
</p>

<h2 id="orgb36eee5">Resources</h2>
<p>
Some useful resources on Neural Networks:
</p>

<ul class="org-ul">
<li>gentle introduction to neural networks series (GINNS) - part 1 - <a href="https://towardsdatascience.com/a-gentle-introduction-to-neural-networks-series-part-1-2b90b87795bc">https://towardsdatascience.com/a-gentle-introduction-to-neural-networks-series-part-1-2b90b87795bc</a></li>
<li>GINNS2 - neural network from scratch - <a href="https://towardsdatascience.com/build-neural-network-from-scratch-part-2-673ec7cdd89f">https://towardsdatascience.com/build-neural-network-from-scratch-part-2-673ec7cdd89f</a></li>
<li>(GINNS) ends here - author didn't finish it, last post in 2017.</li>
<li>network + weights + activation function?</li>
<li>quick ml terminology - <a href="https://hackernoon.com/everything-you-need-to-know-about-neural-networks-8988c3ee4491">https://hackernoon.com/everything-you-need-to-know-about-neural-networks-8988c3ee4491</a></li>
<li>beginner's guide to activation functions - <a href="https://towardsdatascience.com/secret-sauce-behind-the-beauty-of-deep-learning-beginners-guide-to-activation-functions-a8e23a57d046">https://towardsdatascience.com/secret-sauce-behind-the-beauty-of-deep-learning-beginners-guide-to-activation-functions-a8e23a57d046</a></li>
<li>"building a silicon brain" - <a href="https://www.the-scientist.com/features/building-a-silicon-brain-65738">https://www.the-scientist.com/features/building-a-silicon-brain-65738</a></li>
<li>"Machine, Learning, 1951" (cool photograph of neuron) (what's with the odd comma placement?) - <a href="https://www.the-scientist.com/foundations/machine--learning--1951-65792">https://www.the-scientist.com/foundations/machine--learning--1951-65792</a></li>
<li>examples of keras networks - <a href="https://github.com/keras-team/keras/tree/master/examples">https://github.com/keras-team/keras/tree/master/examples</a></li>
<li>"Neural Network Design" by Hagan, DeMuth, Beale and De Jesus.</li>
<li>"Epoch vs Iterations vs Batch size" - <a href="https://towardsdatascience.com/epoch-vs-iterations-vs-batch-size-4dfb9c7ce9c9">https://towardsdatascience.com/epoch-vs-iterations-vs-batch-size-4dfb9c7ce9c9</a></li>
<li>tiny-dnn: header-only dependency-free deep learning neural network library - <a href="https://github.com/tiny-dnn/tiny-dnn">https://github.com/tiny-dnn/tiny-dnn</a></li>
</ul>
