---
title: "🤗 & LLMs"
layout: post
excerpt: "Large Language Models (LLMs) are all the rage right now. They show great promise for solving many problems involving natural language, or problems which can be reformulated in natural language. In this post I play about with a couple different popular LLMs and fine-tune them on new data, all using huggingface's <code>transformer</code> library."
tags: Python ml
---

# LLMs
Large Language Models (LLMs) took the internet by storm with the release of OpenAI's ChatGPT in November 2022. GPT-2 had also been a revolution when released, but a much quieter one. The user-friendliness of ChatGPT brought the power of LLMs and AI text generation to the common muggle.

These models have been used to generate ideas for youtube videos ([Tom Scott](https://www.youtube.com/watch?v=TfVYxnhuEdU)), write code automatically ([GitHub co-pilot](https://github.com/features/copilot)), and even to create entire video games in mere minutes ([report by the Independent](https://www.independent.co.uk/tech/chatgpt-gpt-4-ai-video-games-b2301358.html)).

# Hugging Face 🤗
Switching gears a sec, [Hugging Face](https://huggingface.co/) is a company, an online community, furthering the field of AI and democratising it. It's not too dissimilar to [Kaggle](kaggle.com), right down to the silly name.

Hugging Face have a fantastic python library for using transformers. It makes it seriously easy to set up and train a model, and is fully compatible with both PyTorch and Tensorflow. (I'll be using the PyTorch version for now.)

The library is split across several generically named modules. Key ones include:
- `transformers`: for using models (with transformer architecture)
- `datasets`: for using/creating/splitting datasets
- `evaluate`: for evaluation

The modules are available on PyPI:
{% highlight bash %}
# Required backend
pip install torch

pip install transformers'[torch]' datasets evaluate
{% endhighlight %}

# GPT-2
There's a great breakdown of the GPT models in [this Medium article](https://medium.com/walmartglobaltech/the-journey-of-open-ai-gpt-models-32d95b7b7fb2). Introduced by OpenAI, GPT-2 is the second version of their Generative Pre-trained Transformer NLP model. We can apply this model to the task of generating text. Doing this using Hugging Face is pretty easy:

{% highlight python %}
from transformers import pipeline

generator = pipeline(model='gpt2')

prompt = 'I would like '
result = generator(prompt)[0]['generated_text']

print(f'"{prompt}" -> "{result}"')
# $ "I would like"  -> "I would like ________ to be available
#   to the general public to download this file. These files
#   have been requested by the FBI, DEA, FBI, US Marshal Service,
#   and other entities seeking information regarding the
#   investigation of a suspected methamphetamine, or any other"
{% endhighlight %}

Interesting, but it just spouts vaguely convincing nonesense. This is just GPT-2, we can use larger models very easily. Check out the available models on Hugging Face [here](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending).

## Fine tuning
What's more useful would be to fine-tune an LLM on a custom dataset. As a researcher and teacher it would be very useful to have an LLM trained solely on a body of work. It could then be used to summarise the work.

We can't use the `pipeline` to train, we need to do a bit of work to get training. An LLM is built of two components: a tokeniser which transforms the text into tensors, and the model itself.

{% highlight python %}
from transformers import AutoTokenizer, AutoModelForCausalLM

tokeniser = AutoTokenizer.from_pretrained('gpt2')
tokeniser.pad_token = tokeniser.eos_token
model = AutoModelForCausalLM.from_pretrained(model_path)
{% endhighlight %}

We need a dataset on which to train! As I'm not imaginative, let's use a typography staple: [lorem-ipsum](https://www.lipsum.com/). I generated 5 paragraphs of lorem, and dumped it in a text document.

{% highlight text %}
dataset.txt
---
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Vivamus tempus faucibus turpis id imperdiet. Morbi rhoncus
laoreet enim. Morbi ullamcorper massa id ultricies bibendum.
Morbi velit ex, commodo eu massa a, pretium laoreet felis.
Fusce viverra nunc sed rutrum luctus. Proin in purus
ullamcorper, tempus est vel, tristique diam. Nam maximus sem
non ullamcorper hendrerit. Proin faucibus a quam at suscipit.
Etiam feugiat dolor et nibh tincidunt, eget semper urna
fringilla.
...
{% endhighlight %}

Loading the dataset is done as follows:

{% highlight python %}
from datasets import Dataset

with open('dataset.txt') as f:
    dataset = Dataset.from_dict({
        'text': [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]
    })


def tokenize_function(examples):
    return tokeniser(examples["text"], padding='max_length', truncation=True, max_length=100)


dataset = dataset.map(tokenize_function, batched=True)
dataset = dataset.add_column('labels', dataset['input_ids'])
dataset = dataset.train_test_split(0.2)
{% endhighlight %}

The last part there runs the tokeniser over the dataset, and then splits it up into test and train subsets. A new column is added as well, we want the model to aim to continue the text, so the "label" we're aiming to output is the text id itself (the output from tokenisation).

Training is done via a `Trainer` object, to which we pass information about how to train the model, the model itself, and the data.

{% highlight python %}
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="test_trainer",
    overwrite_output_dir=True,
    num_train_epochs=5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],
)
{% endhighlight %}

Finally, the model is trained simply by calling `trainer.train()`. The model will train for a specified number of epochs, and then done. We can save the model using the trainer, too.

{% highlight python %}
trainer.train()
trainer.save_model('path/to/save')
{% endhighlight %}

Loading the model later is done using the model class:

{% highlight python %}
path = 'path/to/save'
tokeniser = AutoTokenizer.from_pretrained(path)
tokeniser.pad_token = tokeniser.eos_token
model = AutoModelForCausalLM.from_pretrained(path)
{% endhighlight %}

After GPT-2 is fine-tuned on our silly Lorem ipsum, we have our own Lorem generator!

<script type="text/javascript">
var i = 0;

const LOREM_PRECALC = [
    "foo",
    "bar",
];

function pseudo_generate_lorem() {
    if (i < LOREM_PRECALC.length) {
        const e = document.getElementById('lorem-space');
        e.innerHTML += LOREM_PRECALC[i] + ' ';
        i += 1;
    }
}
</script>
<p class="standout" style="width: 100%;" id="lorem-space"></p>
<a onclick="pseudo_generate_lorem();">Generate!</a>
<small><i>Note: we're not really generating on-the-fly, it's just a simulation.</i></small>

# Walden in bloom
BLOOM is a GPT-3-like model, trained on a bunch of text across many languages and programming languages. The model comes in a couple different sizes, representing different abilities and model sizes (half a billion parameters, up to 3 billion parameters).

Walden is a book written by Henry David Thoreau about his time spent among nature at Walden Pond. He reflects on life and needs. There's something about protest, but I latched onto the minimalism and naturalist messages most. The book is great, and is available on the wonderful [Project Gutenberg](https://www.gutenberg.org/files/205/205-h/205-h.htm).

Let's see what `bloom` can do when trained (well, fine-tuned) on this book.

