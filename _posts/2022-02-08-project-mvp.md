---
project: "MVP - ML Visualised using Python"
elevator_pitch: "Script to visualise structure of ML model, aiding in design."
technologies: "Python, LaTeX, NetworkX"
repo: "github.com/cbosoft/mvp"
layout: projectpage
tags: software-dev ml projects
status: Released
---

<img src="https://github.com/cbosoft/mvp/raw/master/examples/example_1.png?raw=true" />
# Motivation

The architecture of a machine learning model decides how the model "thinks". A whole bunch of research is dedicated to figuring out new and improved ways of designing networks. However, the maths gets a little complicated - there are a lot of layers and the size of each is important to consider. The smallest layer gives the reduced features considered by the model. If this restriction is too small, the model won't have enough information to act upon. If the restriction is too large, then the model will have *too much* information available and may take a long time to train, or be so complex that it doesn't learn.

Enter, MVP: a script to take a given model layout and sketch it out in a rigorous manner so that an intuitive picture of your design network can be obtained.

# Challenges

## Representing the network
This was the first challenge, and the easiest thanks to the python library [`networkx`](https://networkx.org). A node in the graph represents a piece of data flowing through the ML model. A graph edge is the operation applied to the data (convolution, pooling, activation, and so on).

## Drawing
Drawing programmatically in an aesthetically pleasing way is not too hard. I chose to output LaTeX code from my script, which can be compiled to PDF using `pdflatex` or any other LaTeX compiler. This PDF can be converted to image format if desired using e.g. imagemagick's `convert`:

```bash
convert -density 384 "{pdf_fn}" -quality 100 -alpha remove "${PDF_FILE}"
```

Each node in the graph is drawn as a rectangle in 45&deg; perspective. The height of the rectangle gives the number of features, while the width gives the channels. In this way, we have a graphical representation of the size of data we're dealing with at every stage.

Edges in the graph, representation operations on data, are represented visually just by a coloured rhombus joining the node prior to the node following. The colour indicates the type of operation, but the name is given too. 

## Traversal
A network is quite a thing to traverse in a generic manner. You could go through it in any number of ways, if we're talking about a general network. Thankfully, machine learning models tend to have an overall direction. (Although some have annoying back connections to give the network a sort-of "memory".)

To overcome this, I split up our potential structures into three groups:
- Single input, single output (SISO)
- Multiple input, single output (MISO)
- Multiple input, multiple output (MIMO)

I then developed a tree structure which is drawn from trunk to leaf. This was generic enough to cover both SISO and MIMO cases without issue. A slight complication was encountered for MIMO - solved by finding a pivot node. There is assumed to be a node common to all paths, this is taken as a pivot. Two trees are formed up- and down-stream from the pivot. They can then each be drawn, resulting in the whole MIMO network being displayed.

<img src="https://github.com/cbosoft/mvp/raw/master/examples/example_3.png?raw=true" />

(kinda looks like a person wearing really [big yellow wellies](https://www.theglasgowstory.com/image/?inum=TGSE01085))

# Conclusions

The script achieves what I set out to accomplish. The LaTeX produced drawings are clear and precise, and easily editable. The project could do with more documentation, as always. I tried to mitigate this by choosing good variable, function, and module names such that the code is fairly readable on its own.

I don't like the double-tree solution I cam up with. It works, and will work for most simple ML model structures, but I think it will fail for networks with skip connections which would fail to be represented by the tree. There must be a better way, but the code works and that's good enough for now!