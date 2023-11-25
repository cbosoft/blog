---
title: "Unreliable Sorting"
layout: post
excerpt: "Solving the problem of sorting by unreliable pairwise ratings to facilitate design of quantitative descriptors."
tags: software-dev Python
---

# Literature
 - ["How do People Sort by Ratings?"](https://dl.acm.org/doi/10.1145/3290605.3300535)
 - ["Fault Tolerant Sorting Networks"](https://epubs.siam.org/doi/10.1137/0404042)

# Problem Statement

In [a previous post]({% post_url 2023-02-09-gamifying-image-annotation %}), I set up an app to crowd-source comparisons of pairs of images - comparing based on some abstract qualities such as focus, or how similar the subject is to a fox.

<center>
<img src="{{site.baseurl}}/img/constrained-sorting/imclasregan.png" style="display: inline-block; width: 40%;"/>
<p><i>Dataset is <a href="https://www.kaggle.com/competitions/dogs-vs-cats/rules">"Dogs vs Cats" from Kaggle</a></i></p>
</center>

The results are a series of pairs of items and an ordering within that pair.

 - `A < B`
 - `B < F`
 - `D < F`

How do we recover the true order of all items? Or, more realistically, how do we recover the *most likely* true order?

For the very simple situation above, we have a number of possible correct solutions:

 - `[A, B, D, F]`
 - `[A, D, B, F]`
 - `[D, A, B, F]`

This problem is under-defined: we don't have examples for every combination of pairs.

...

This task is not easily solved. If we have pairings involving every item, then we are fully constrained and the problem is fairly simple to solve... However this is complicated because we may have *conflicting constraints*. I mean, the annotators are not infallible and we could end up with circular references:

 - `A < B`
 - `B < C`
 - `C < A` 👉 Circular!

We need to find some way of dealing with these conflicts. There are also, potentially, going to be conflicts for a single pair (`A < B`, `B < A` ?!). This is expected: people aren't infallible; people have differeing opinions. How do we deal with these differing opinions? Majority voting? Monte-carlo optimisation? Bayesian optimisation?