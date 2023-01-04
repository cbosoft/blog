---
title: "Minautomata 1: Cellular Automata"
layout: post
excerpt: "Falling sand games, how do they work?"
tags: software-dev Rust
---


# In this series
- Part 0. - [Rusty WASM]({% post_url 2022-02-22-minautomata-0 %})
- Part 1. - Cellular Automata (you are here)


# Falling Sand
Last time we got to a point where a grain of... something fell from the top of the box to the bottom. This was implemented use a simple rule:

```
IF CELL IS WHITE:
    IF CELL BELOW IS BLACK:
        MOVE CELL BELOW
```

To give a kind of gravity acting on the particle. This rule, and the grid of cells it acts on, makes up a sort of "machine" - a [Cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton).


# Cellular Automata





# References
- [Cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton)
- [Lattice gas (cellular) automaton](https://en.wikipedia.org/wiki/Lattice_gas_automaton)
- [BIO-LGCA](https://en.wikipedia.org/wiki/BIO-LGCA)
- [Epidemiology LGCA](https://ieeexplore.ieee.org/abstract/document/849664?casa_token=n2ct_SgwPNoAAAAA:E74E4Bq0ibiIuBDT9NWkhiAg7vALixw1tMRFOh9F7qIDul6-N9AwTKHvHhRh9XngBn17gZc)
- [Cellular migration BIO-LGCA](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009066)


# In this series
- Part 0. - [Rusty WASM]({% post_url 2022-02-22-minautomata-0 %})
- Part 1. - Cellular Automata (you are here)