---
title: "Testing out ML Experiment Trackers"
layout: post
excerpt: "Taking a look at ways of tracking ML experiments: MLFlow, Weights and Biases, and Tensorboard."
tags: ml
---

Machine learning experiments - especially hyperparameter optimisation - generate a heap of information that is necessary to store in a searchable way. This is used to show improvements over time, to choose the best model, and so on. I've used [TensorBoard](https://www.tensorflow.org/tensorboard) in the past and I've developed a homebrew solution as well ["MLDB"](https://github.com/cbosoft/mldb). I enjoyed building my homebrew solution, but as I've learned more about infrastructuring I see how far it is from "production ready". I don't have time, unfortunately, to bring MLDB to production ready status. It's time to bite the bullet and just use an off-the-shelf solution.

I found three ML experiment tracking solutions to look at. I used TensorBoard in the past, so that's on the list. I searched around, discussed with colleagues, and found two others: [MLFlow](https://mlflow.org/) and [Weights and Biases](https://wandb.ai/site).

I'm gonna look at each solution in turn, and evaluate based on my criteria:
 - ease of installation and setup
 - ease of logging parameters, metrics, and misc data
 - ease of searching through historic results

# TensorBoard
TensorBoard is probably the most widely used of the three solutions I've tested here. Many libraries support logging to TensorBoard automatically. Many tutorials use TensorBoard. Many AI platforms support TensorBoard's UI as it's so prevalent (e.g. [Run:AI](https://www.run.ai/)).

<center class="standout">
<img src="{{site.baseurl}}/img/ml-tracker/tensorboard-website.png" style="width: 80%;">
<p>Screenshot of the <a href="https://www.tensorflow.org/tensorboard">TensorBoard website</a></p>
</center>


## Setup
Getting started from scratch isn't well explained, but it isn't hard. Nice and simple installation:
{% highlight bash %}
$ pip install tensorboard
{% endhighlight %}

Run the server:
{% highlight bash %}
$ tensorboard --logdir runs
{% endhighlight %}

This runs a server which records data to a `runs` directory, and serves a UI to `localhost`.

Then ready to start using!

## Logging
This is less simple. Well, it's hidden away. This is part of what's nice about TensorBoard, it doesn't want *you* to use it, but your ML library (tensorflow, pytorch) should use it internally. The example they give on their [getting started page](https://www.tensorflow.org/tensorboard/get_started) suggests using TensorBoard via a callback function passed to the training ("fit") function.

{% highlight python %}
import tensorflow as tf

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

...

model.fit(x=x_train, 
          y=y_train, 
          epochs=5, 
          validation_data=(x_test, y_test), 
          callbacks=[tensorboard_callback])
...
{% endhighlight %}

You can store scalars which covers metrics and other parameters (no distinction is made between them). Interestingly, it has support for viewing *embeddings* for a model, allowing exploration and interpretation of deep learning models.

## Search
Search is by keyword search based on the `log_dir` parameter passed to the TensorBoard writer object. You're free to hierarchically organise runs (stored in nested directories in the backend). This is enough to get by, but misses some features of the other solutions.

## Overall
I'm not a fan of `tensorboard`. I don't like the approach to logging, and I don't like the inflexible backend. I want some control over the logged data. In principle, logging more is more good-er. Mainly I want to know more about the provenance of the logged data. The inflexible backend becomes an issue when training on multiple machines e.g. in a kubernetes cluster. I want results to be sent to central storage to track everything. Finally, a very minor gripe, TensorBoard seems optimised for TensorFlow while I prefer PyTorch. (It does work with PyTorch, but could work nicer with TensorFlow.)

Overall: 👎

# ML Flow

<center class="standout">
<img src="{{site.baseurl}}/img/ml-tracker/mlflow-website.png" style="width: 80%;">
<p>Screenshot of the <a href="https://mlflow.org/">ML Flow website</a></p>
</center>
## Setup
Installation is simple:
{% highlight bash %}
$ pip install mlflow
{% endhighlight %}

This python package includes the command line utility `mlflow` which is used to start the tracking server (where the data is stored) and the UI. There are different backends to choose from, which is ***great***. There is also provision for storing images and models and any other data as an "artefact". These are stored outside the tracking database (e.g. in an S3 bucket).

I used PostgreSQL as the backend storage for MLDB, so I chose that as the backend for `mlflow`. I have plenty storage on my server, so will use local storage for artefacts, "proxied" via the tracking server. To keep things neat, I set up a docker image for mlflow and composed it with the DB image.

The MLFLow image is based on the `python-3.10` image:
{% highlight dockerfile %}
# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
RUN pip install --upgrade pip
RUN pip install numpy scipy scikit-learn
RUN pip install mlflow psycopg2-binary

# backend db settings
ENV MLFLOW_BACKEND_STORE_URI="postgresql+psycopg2://RUNS:PASS@db:5432/RUNS"

# UI served to any IP
ENV MLFLOW_HOST="0.0.0.0"

CMD mlflow --artefacts-destination './artefacts' --serve-artifacts
{% endhighlight %}

The docker compose file:
{% highlight yaml %}
services:
  db:
    image: postgres
    env:
      POSTGRES_USER: RUNS
      POSTGRES_PASSWORD: PASS
    expose:
      - 5432
    networks:
      dbnet:
    volumes:
      - type: bind
        source: ./data
        target: /var/lib/postgresql/data
  mlflow:
    build: ./mlflow-server
    depends-on:
      - db
    ports:
      - 5454:5000
    networks:
      dbnet:
networks:
  dbnet:
{% endhighlight %}

Then, mlflow and backend can be run with just:
{% highlight bash %}
$ docker-compose up -d
{% endhighlight %}

This stores the results of runs (config and metrics etc) in the postgres database (which is stored outside the docker containers, local to the server) and artefacts (model states, segmented images, embeddings, ...) also stored local to the server.

## Logging
Parameters and metrics are stored in a similar way, but are kept distinct which is nice.

{% highlight python %}
import mlflow

with mlflow.start_run(run_name='test-run'):
    ...
    mlflow.log_param('lr', 1e-3)
    mlflow.log_metric('rmse', 0.1, step=epoch)
{% endhighlight %}
## Search
## Overall

# Weights and Biases
Weights and Biases was suggested to me by a colleague who had tried it in the past. This proprietary and paid solution seemed too expensive - if not for their free academic tier. 100Gb of free storage isn't bad. How does it match up to the others?

<center class="standout">
<img src="{{site.baseurl}}/img/ml-tracker/wandb-website.png" style="width: 80%;">
<p>Screenshot of the <a href="https://wandb.ai/site">Weights and Biases website</a></p>
</center>

## Installation
Dead simple setup. Install the python package, get an API key, go!
## Logging
## Search
## Overall

# Summary
