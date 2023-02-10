---
title: "GAMIFY YOUR ANNOTATION"
layout: post
excerpt: "Annotating images is time consuming and boring. Maybe there's a better way..."
tags: software-dev Python ml Rust
---

# Intro
### Image classification tasks are easy.

Which of the below images is of a cat, and which is of a dog?

<center>
<img src="{{site.baseurl}}/img/gamifying-image-annotation/cat.jpg" style="display: inline-block; width: 40%;" />
<img src="{{site.baseurl}}/img/gamifying-image-annotation/dog.jpg" style="display: inline-block; width: 40%;" />
<br/>
<a href="https://en.wikipedia.org/wiki/Cat#/media/File:Cat_yawn_with_exposed_teeth_and_claws.jpg">(left)</a> <a href="https://en.wikipedia.org/wiki/Dog#/media/File:Big_and_little_dog.jpg">(right)</a>
</center>

See? Easy!

Okay I'm not arguing in good faith. It's easy for us, and especially so for clean cut examples like the above. It's also not particularly scalable to ask people to classify images manually. People get bored. It's also not "objective" - different people have different opinions, the same person on *different days* can have different opinions of an image!

To get around this, let's train a machine learning model to perform the classification. Let the machines do the work!

Many architectures are available for classification and it is a relatively simple task. (Simpler than, say, segmentation.)

Some example models we could use:
 - [Random forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
 - [Logistic regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
 - ANN (fully connected)
 - CNN

We're using images: we will want to pass a feature detector over the image to reduce the dimensionality in the classification model. If we pass the raw image, we're in-effect asking the model to classify based on WxH datapoints - potentially *millions*. Dimensionality reduction through feature extraction is really essential for image analysis. Luckily, there are a bunch of models already trained. [Orange datamining](https://orangedatamining.com) has several built in to their image plugin.

As always with data-driven models, our task is not "how do we model this" (difficult, *interesting*) but is concerned mainly with building a dataset (easy, **boring**). Building an image classification dataset like this is easy enough, our eyes are good at spotting features in images and we're very capable at recognising patterns in these features. It's just tedious to manually form a dataset large enough. There are also the opinion-related issues I mentioned earlier. To get around this, **let's crowd source a dataset**.

# Gamifying
The idea here is to make manual classification as easy and fast as possible - with a little superficial encouragement thrown in for good measure. This way the classification task can be handed out to a large set of people. The ease of use is important to ensure engagement. Gamifying it a little (e.g. storing high scores, providing written encouragement) will further increase engagement and get more classifications. Finally, using a wide group of people will drill down through opinion and arrive at the truth of the situation - at least I hope!

# Time for Crab? 🦀
Starting off this project I wanted to write it in [Rust](/blog/tag/Rust/). My vision was a nearly-pure client-side app compiled to WASM. This client would call out to a postgresql server running elsewhere to get images and to store results. This seemed perfectly reasonable and doable in Rust. To build the project I made use of some packages:

 - UI - [eframe/egui](https://crates.io/crates/eframe)
 - Database - [tokio-postgres](https://crates.io/crates/tokio-postgres)

The immediate-mode GUI framework `eframe`/`egui` made building this project really easy and quite fun. I started with the [wasm-compatible template from eframe](https://github.com/emilk/eframe_template). I had to learn a bit about async to use `tokio`, required by my choice of database driver. As the `tokio` runtime needs to run in a loop (it would normally be the `fn main() {...}` of a given program), it had to be shifted to another thread and communication facilitated by channels (another thing I had to learn).

In the end, I had a functional classification "game" running locally. The next step would be to compile to WASM and then chuck on a server: job done!

<center>
<img src="{{site.baseurl}}/img/gamifying-image-annotation/trusty_patches.png" style="display: inline-block; width: 40%;"/>
<p><i>Dataset is <a href="https://www.kaggle.com/competitions/dogs-vs-cats/rules">"Dogs vs Cats" from Kaggle</a></i></p>
</center>

This is where I hit a roadblock. `tokio` is not compatible with WASM. `postgres` doesn't have a pure-rust implementation not relying on `tokio`. I looked into other database formats like `SQLite` and different libraries like `sqlx`, but couldn't find a solution that satisfied my desired requirements of both WASM-compatible and client-side. Oh well.

I ended up switching to `SQLite` anyway. The project expects three tables in the database (schema in pseudocode):

 - `IMAGES(ID: int, NAME: text, DATA: blob, WIDTH: int, HEIGHT: int)`
 - `CLASSIFICATIONRESULTS(SESSION_ID: int, IMAGE_ID: int, CLASS_ID: int, TIME_TAKEN: real)`
 - `CLASSIFICATIONS(ID: int, NAME: text, DESCRIPTION: text)`

`IMAGES` contains the binary image, as well as an identifier and a name. `CLASSIFICATIONS` describes the classes you want to put the images in to. E.g. for the example shown above, there are two: `CAT` and `DOG`. Finally, classification results shows the results, pairs of images and classes. Also included in the results is some meta data - how long the user took to perform the classification and a session ID. The session ID is a UUIDv4 generated when the page loads. It is an anonymous identifier used only for analysing how many images are annotated in a single sitting.

This project is on GitHub [here](https://github.com/cbosoft/trusty_patches). The name comes from my typical use case of classifying instances of objects detected on an image using [Mask R-CNN](https://arxiv.org/abs/1703.06870) - so I tend to classify parts of an image or *patches*. I want to get good, *trustable*, classifications using this tool - hence the name.

# Starting again

Okay okay so first server-less attempt didn't go so well. Let's rethink that and add a server into the mix. `Rust` would be a good choice for this still, but by the time I got to this stage it was pretty late. I wanted to get a working version up and running by the end of the night. I fell back to [`Python`](/blog/tag/Python/) to prototype out the server quickly.

I came up with a very, very, simple server innheriting from the `SimpleHTTPServerHandler` in the `http` standard library. This server would listen for post requests containing commands. These commands boil down to "get me some stuff from the database" and "here's some stuff, put it in the database". I have some simple javascript which forms these commands and recieves the replies from the server.

This was very quick to set up and I had a functional version finished in under an hour. Rust may be application performant, but Python is certainly development performant.

<center>
<img src="{{site.baseurl}}/img/gamifying-image-annotation/imclasregan.png" style="display: inline-block; width: 40%;"/>
<p><i>Dataset is <a href="https://www.kaggle.com/competitions/dogs-vs-cats/rules">"Dogs vs Cats" from Kaggle</a></i></p>
</center>

In addition to performing classification, I added the functionality to aid in the development of regression or rating tasks. The user is asked to choose which of two randomly selected images is more `$something` where `$something` is a quality of the image: like "in focus". This is useful for helping to design quantifiers of the specified quality. This could be useful for developing a dataset for regressing an indicator of that quality, however further processing would be required. 

This project is also on [GitHub](https://github.com/cbosoft/imclasregan/tree/python-backend). The name this time is a portmanteau (mash up) of image classification and regression annotation.

# Quality Regression

Using the ["Dogs vs. Cats"](https://www.kaggle.com/competitions/dogs-vs-cats/rules) dataset, I annotated XXXX pairs images - marking which of each was more or less *foxy*. Foxy, of course, meaning fox-like, vulpine, having the attributes of a fox. This is a somewhat arbitrary qualitative measure. It primarily came down to the ears - pricked attentive ears where definitely a prime indicator for foxiness as I was annotating.

The results are a series of pairs of items and an ordering within that pair.

 - `A < B`
 - `B < F`
 - `D < F`

How do we recover the true order of all items? Or, more realistically, how do we recover the *most likely* true order?

This task is not easily solved. If we have pairings involving every item, then we are fully constrained and the problem is fairly simple to solve... However this is complicated because we may have *conflicting constraints*. I mean, the annotators are not infallible and we could end up with circular references:

 - `A < B`
 - `B < C`
 - `C < A` 👉 Circular!

We need to find some way of dealing with these conflicts. There are also, potentially, going to be conflicts for a single pair (`A < B`, `B < A` ?!). This is expected: people aren't infallible; people have differeing opinions. How do we deal with these differing opinions? Majority voting? Monte-carlo optimisation? Bayesian optimisation?

**To be continued...**