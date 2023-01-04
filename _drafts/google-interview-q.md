---
title: "A Google interview question"
excerpt: "foo"
layout: post
tags: software-dev
has_diagrams: true
---

A mate of mine passed on an interview task they'd been asked during an interview for Google as a brain teaser. I thought it was quite an interesting question, with some interesting possible solutions...

# The Question

> Q: Given an M x N array, give the number of elements in the largest rectangle or square where all elements sum to 0. Give your answer in 45 minnutes.

So given an array, we need to find a large rectangle where elements sum to 0 and count the elements in that rectangle. I followed the 45 minute time limit while thinking of these ideas, but I spent some time after the limit was over in implementing and testing these ideas

# Solution 1: Brute Force (BF)

A brute force solution: try every possible rectangle, in descending order of size, and stop once you find one that sums to zero.

I initially discounted

# Solution 2: Monte Carlo 1

<div class="mermaid" id="centre">
graph TD 
S[Generate random rect] --> Q{Sums to zero?} -->|Yes| D[Done!]
Q-->|No| R[Try again] --> S
</div>

Solution in ??

# Solution 3: Sudoku Solver-esque Brancing Method

1. Start with the largest rectangle
2. Does it sum to zero? (if so, you're done!)
3. Create sub matrices for each possible shrinking direction (left, right, up, or down)
4. For each sub-matrix, GOTO 2.

I thought I was really clever coming up with this recursive alorithm until I realised (1) it doesn't work (2) I was really thinking of the same method as the brute force search (or breadth first search).