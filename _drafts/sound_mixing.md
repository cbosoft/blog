---
title: Synthesising and mixing sound in C++ and port audio
layout: post
excerpt: Developing a sound engine
tags: games software-dev
---

As part of developing [BounceEngine]({% post_url 2021-04-27-bounce1 %}), I
need a way of playing sound. How can we do this in `C++`?

# Digital Audio

Digital audio is an approximation of audio by splitting the wave into discrete
segments. These discrete segments are called samples. Samples are organised into
*frames*, which are samples for each of the output lines (one sample for mono,
left and right for stereio, etc). Frames are then built up into *buffers*.
Buffers are passed to the audio driver which passes it to the hardware, sample
by sample, which is played as audio to the user.

At the OS level, this is managed by the audio driver. However, sound systems are
**complicated**. Every computer can have many different possible sound systems:
headphone out, line out, integrated speakers, external audio card, internal
(motherboard) audio card, internal (PCIe) audio card... This stuff can be
abstracted away by an audio library.

# PortAudio

[PortAudio](http://www.portaudio.com/) "is a free, cross-platform, open-source,
audio I/O library" (from their website). It is a `c` library, and is compatible
with `C++`, but could do with some light wrapping. I chose this library for its
cross-platform nature and, oddly, lack of features. I want to build up the
engine from minimal components: so a sound library with minimal built in
features is what I want.

They have a very [barebones
tutorial](http://files.portaudio.com/docs/v19-doxydocs/tutorial_start.html) on
their website, which guides you through putting together a minimal example
sufficient for playing **samples**.

The basic concept boils down to three things:
- setting up the audio library
- storing information about the sound being played
- creating a callback function which feeds a buffer of samples of sound into the audio
  driver

Sound is driven by its own thread, which calls the callback function every so
often. The callback function's job is to fetch a buffer (composed of a bunch of
frames) of sound data which is to be played. This function needs to be as
low-latency as possible as it is called on the sound thread - all expensive
calls must be made elsewhere. `malloc`, `calloc`, and `new` calls should be
avoided in this function.

As multiple sounds need to be mixed together, and spatial audio could get
quite (computationally) expensive, it would perhaps make sense to store a
pre-calculated list of samples ready to be passed to the sound engine. In this
way minimising the effort required of the callback. For now, lets play a simple
single tone.

Start with including the PortAudio header and we'll also need some maths:

{% highlight c++ %}
#include <cmath>
#include <portaudio.h>
{% endhighlight %}

We need somewhere to store state information about the sound we are playing. For
our simple "Hello, World" style use case of playing a uniform tone (a sine
wave), we only need to store the time (or sample number).

{% highlight c++ %}
typedef struct {
  float time;
} SoundData;
{% endhighlight %}

Then we define a callback to pass the frame of samples on:

{% highlight c++ %}
static int sound_callback(
        const void *input_buffer, void *output_buffer,
        unsigned long frames_per_buffer,
        const PaStreamCallbackTimeInfo *time_info,
        PaStreamCallbackFlags status_flags,
        void *user_data)
{
    auto *data = (SoundData *)user_data;
    auto *out = (float *)output_buffer;
    for (int i = 0; i < frames_per_buffer; i++) {
        const float v = std::sin(data->time);
        (*out++) = v; // set value and move to next
        (*out++) = v;
        data->time += .1f;
    }
    return 0;
}
{% endhighlight %}

Only thing left to do is to is set up the audio library and play the tone!

{% highlight c++ %}
#include <stdexcept>
#include <iostream>

#define SAMPLE_RATE 44100

int main()
{
    // Initialise the engine
    SoundData data = { 0.f };
    PaError err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << Pa_GetErrorText(err) << std::endl;
        throw std::runtime_error("init");
    }

    // Initialise a stream
    PaStream *stream;
    err = Pa_OpenDefaultStream(
        &stream,
        0, /* input channels */
        2, /* output channels */
        paFloat32, /* data type */
        SAMPLE_RATE,
        256, /* buffer size, number of frames */
        sound_callback,
        &data /* pointer to data*/);
    if (err != paNoError) {
        std::cerr << Pa_GetErrorText(err) << std::endl;
        throw std::runtime_error("open stream");
    }

    // Start stream
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << Pa_GetErrorText(err) << std::endl;
        throw std::runtime_error("start stream");
    }

    // Wait a wee bit
    Pa_Sleep(10*1000);

    // Stop stream
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << Pa_GetErrorText(err) << std::endl;
        throw std::runtime_error("start stream");
    }

    // Tidy up
    err = Pa_Terminate();
    if (err != paNoError) {
        std::cerr << Pa_GetErrorText(err) << std::endl;
        throw std::runtime_error("terminate");
    }
}
{% endhighlight %}

There we go, we have a toy synthesizer. This is really simple, but pretty
powerful. We can change up the data object and callback function to change the
noise we get. We can change the volume by multiplying/dividing the output of the
sine function by some factor. (Keeping in mind our ears interpret sound
logarithmically so multiplying by 10 gets you double the volume, loosely
speaking).

# Wrapping PortAudio

I mentioned this could do with some light wrapping, and you can see why. The
set-up and tear-down part, the error handling calls, this kinda stuff could be
tidied up into a class. We also have to worry about mixing; we've got a tone
generated here but what about other sounds getting added in?

A header for the class might look like:

{% highlight C++ %}
class AudioManager {
public:
    AudioManager();
    ~AudioManager();

    void play_sound(int sound_id);
};
{% endhighlight %}
