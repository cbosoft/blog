---
layout: post
title: "crisp - A(nother) LISP Interpreter. Part 1: Introduction and Tokenisation"
tags: software-dev C C++
excerpt: "Writing a lisp interpreter in C"
desc: "I watched a couple videos on lisp after years of not really getting it and now I sorta get it and so here I am writing an interpreter so i can better understand it."
---

### In this series...
- Part 1 (you are here)
- [Part 2]({% post_url 2019-11-27-crisp2 %})
- [Part 3]({% post_url 2019-12-03-crisp-plus-plus %}) 

## Some background
I've always been pretty interested in how computers translate source code into meaningful work, a process called compilation, or interpretation. This process, to me, has been a mystical black box of translating english words in encoded text files into a binary list of processor-understandable instructions. Then I started using GNU Emacs, and used `lisp` a little to tweak my config. Then I wanted to understand more as my superviser started impressing upon me the utility of a spartan functional procedures-are-data language like lisp, so I started searching around and found a [presentation](https://www.youtube.com/watch?v=hGY3uBHVVr4) at linux.conf.au and then I started to *get* it. The simple syntax of the language and the inherent recursive structure to lisp programs I could see how this had power.

I was lent the book "Structure and Interpretation of Computer Programs" (by Harold Abelson, Gerald Jay Sussman, and Julie Sussman), which discusses computer programming in general through the lens of lisp programming. Culminating in the design of a lisp interpreter. Inspired by the simple syntax, I thought I could put together an interpreter pretty quickly in a language I know a bit better than lisp (like `C`).


## The Code
I was originally going to annotate code and include as I went along in this post, however there is a lot of code and I keep on changing my mind about how I want to do things. So I'm only writing about highlights in these posts, about specific problems I've faced and how I tackled them. The code is available on [GitHub](https://github.com/cbosoft/lisp-interpreter).

## What is an interpreter?
According to [other](https://carld.github.io/2017/06/20/lisp-in-less-than-200-lines-of-c.html) [articles](http://leohetsch.com/create-a-minimal-lisp-like-interpreter-in-c/) I [found](https://norvig.com/lispy.html) on this topic, an interpreter takes in some string of source code, splits this string up into a list of **tokens**, then parses the token list into an **Abstract Syntax Tree** which can be **evaluated** obtaining the result. This gives the three main steps for this interpreter: tokenise, parse, evaluate.

The first step breaks up the one long string into manageable chunks of
important syntax. Whitespace is sometimes important, sometimes it doesn't
matter. For example: whitespace splits up the names of symbols, but doesn't
matter if it is included between a list opening/closing parenthesis.

```lisp
(+1 1) ;; +1 is not a valid function
(+ 1 1) ;; is fine
( + 1 1 ) ;; is fine too
```

The next step assembles the tree structure of data flow (like a UML diagram)
from the tokens, converting the list of strings into an abstract syntax tree,
which can go on to be parsed and evaluated. Lisp is very simple, and its
procedures all have a tree structure anyway (lists of lists) so we can skip a
step and go directly to an evaluable version of the AST from the list of
tokens.

The final step looks at the tree and evaluates it. Lisp has a few rules about
how to evaluate objects:

- A symbol (variable) evaluates to its value (data referred to by the name)
```lisp
(defvar pi 3.14159263)
pi ;; -> 3.14159263
```
- A non-empty list is a function call, with the first item in the list the
function, the rest the arguments and thus evaluates to the result of the
function.
```lisp
(+ 1 1) ;; -> 2
```
- An empty list evaluates to `false`:
```lisp
() ;; ->; false
```

- Anything else (`Int`, `Float`, `String`, `Bool`: atomistic types) evaluates to itself.
```lisp
3 ;; -> 3
```


## Tokenisation

```C
void tokenise(char *s, char ***tokens, int *n_tokens)
{

  // TODO

}
```

The tokenise function will take in some string of code and split up into meaningful, understandable tokens. Unnecessary whitespace, comments and so on will be stripped.

We can start by taking the input string, and scanning through character by character.


```C
#include <string.h>
void tokenise(char *input, char ***tokens, int *n_tokens)
{
  int len = strlen(input), i;
  char ch;

  for (i = 0, ch = input[0]; i &lt; s; i++, ch = input[i]) {

    // TODO

  }

}
```

As we read in characters, if they're not a newline, space, tab, or open/close parenthesis, we want to append them to a string, building up a name or keyword. We need some way to add to the token list and `c` has these wonderful macro things so we can do it easily. (Well, I guess any language can use it if the `c` pre-processor (`cpp`) is run over the code beforehand.)

```c
#include <stdlib.h>
#include <string.h>

#define ADD_TO_LIST(VALUE) \
  (*tokens) = realloc(*tokens, (++(*n_tokens))*sizeof(char*));        \
  (*tokens)[(*n_tokens)-1] = calloc(strlen(VALUE) + 1, sizeof(char)); \
  strcpy( (*tokens)[(*n_tokens)-1], VALUE);
```

Next we fill out the function, check if the character is a breaking character. If it is, add the previously read in keyword/name to the list. If it isn't, append a character to the current keyword.

```c
void tokenise(char *input, char ***tokens, int *n_tokens)
{
  int
    len = strlen(input),
    i,
    kw_or_name_len = 0;
  char
    ch,
    *kw_or_name = NULL;

  (*n_tokens) = 0;

  for (i = 0, ch = input[0]; i &lt; len; i++, ch = input[i]) {

    if ((ch == ' ') || (ch == '\n') || (ch == ')') || (ch == '(') || (ch == '\t') ) {

      if (kw_or_name != NULL) {
        kw_or_name[kw_or_name_len] = '\0'; // add null char to finish string
        ADD_TO_LIST(kw_or_name);
        kw_or_name = NULL;
        kw_or_name_len = 0;
      }

      if ((ch == '(') || (ch == ')'))
        ADD_TO_LIST(ch == '(' ? "(" : ")");

    }
    else {
      kw_or_name = realloc(kw_or_name, ((++kw_or_name_len) + 1)*sizeof(char));
      kw_or_name[kw_or_name_len-1] = ch;
    }

  }

  if (kw_or_name != NULL) {
    kw_or_name[kw_or_name_len] = '\0'; // add null char to finish string
    ADD_TO_LIST(kw_or_name);
    kw_or_name = NULL;
    kw_or_name_len = 0;
  }

}
```

And that's the tokeniser. We could do a bit more than this, like track the number of open parens keeping track of when closing a list makes sense, we could track line and column number to aid in debugging. I'm sure there's more, but all this is extra. This code as a tokeniser works.

I'll leave this post here, this is such a big topic I'm definitely going to split this up. I don't want to have to keep adding to the same post, and I don't want to leave it until I'm finished the interpreter before writing this as I kinda want this to document my progress. I'll chunk the project into manageable poast-sized steps, and go from there.

### Continue reading
- [Part 2]({% post_url 2019-11-27-crisp2 %})
- [Part 3]({% post_url 2019-12-03-crisp-plus-plus %}) 