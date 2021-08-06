---
title: "Pytorch Tensors"
layout: post
excerpt: "Pytorch is a powerful tensor library - but what are tensors? How do we use them? What are they used for in machine learning? (spoiler: everything)"
tags: ml software-dev
---

# PyTorch

PyTorch, at its core, is a powerful tensor library and automatic differentiation tool. This is packaged up as a machine learning library - a tensor is used to store the weights and biases for the neural network and the automatic differentiation (autograd) tool is used to form the optimizer for training the network.

# Tensors

A tensor is an n-dimensional array. This can be built up by first considering a vector - a one dimensional array or list of numbers. In physics a vector is usually size 3 (so its a list of three numbers) and these three values correspond to x, y, z spatial dimensions. However, here we mean a vector of arbitrary size. A vector can be thought of like a line of numbers. A matrix is a **2 dimensional** (or *order 2*) array. This looks like a table of values, with rows and columns. Matrices can be used to describe surfaces or transformations, and can be thought of like a square or rectangle. A 3D array is a collection of matrices, and can be thought of line a cube. Now is where we get a bit abrstract: a 4D array is a collection of collections of matrices and is sort-of a hypercube. Rarely do we deal with tensors of higher *order* than 4.

# What are they for?

Pretty much **everything**.

Weights and biases ("parameters") are stored as a tensor, within PyTorch, and everything else is too: enabling fast mathematic operations and automatic gradient calculation (differentiation). So when using any value calculated by PyTorch, you'll probably be using a tensor.

Tensors are stored on a `device` (CPU or a GPU). This is useful for accelerating calculations on the GPU. A tensor can be moved between devices:

{% highlight python %}
a = torch.rand(3, 3)
a.cpu() # or a.to('cpu')
a.to('cuda:0')
{% endhighlight %}

The *shape* of a tensor describes its dimensions; how many there are and how big they are. A tensor of order 1 with length 3 is the same as a vector of size three: a list of three numbers. The shape descriptor is a `tuple`[^1] of sizes. The first size gives the size of the first dimension, the second size is for the second dimension and so on. 

[^1]: yet another word for collection of stuff - this one can't be modified.

Tensor shape is important for figuring out if two tensors can be *broadcasted* together - if they are inter-compatible to do maths with. For example: two 2D tensors of the same size, like a pair of 3x3 matrices, are compatible for element-wise operations.