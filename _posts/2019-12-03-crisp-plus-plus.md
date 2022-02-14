---
layout: post
title: "crisp - A(nother) LISP Interpreter. Part 3: C++, objects, polymorphism, and exceptions"
tags: software-dev C C++
excerpt: Taking a wee meta-tangent by looking at the language we're using for this.
---

### In this series...
- [Part 1]({% post_url 2019-11-21-lisp-interpreter %})
- [Part 2]({% post_url 2019-11-27-crisp2 %})
- Part 3 (you are here)


## Why?


The `c` language is beautiful and stark. It is powerful, but lacks tools. If you want to do a lot in `c`, you need to write a lot. In addition, there are no `c` dev jobs going round where I am, so I'm moving to `C++`. `C++` has a lot of nice things built in, classes are great, templates could make writing the LispObject stuff easier and there are things like `std::shared_ptr` which could negate the need for a separate garbage collector.


## So.. `C++`?


Yeah, `C++`! Hello `std::forward_list` instead of DIY linked list,
`std::stack` instead of dynamic array. `std::string` and
`std::stringstream` over `char *` and `snprintf` and soooo many streams!

`C++` has classes; definable structures with methods, constructors, and (importantly) destructors. This replaces the plain structs I used for everything in `c`: for the objects, lists, atoms and so on. What's even better, is that classes can be derived from one another, using *polymorphs*. So an object's purpose could be fulfilled by different objects of slightly different type. We can have an object of atomic integer type, or of list type, both fit into an element of a list. We could use a polymorphic class to do this.


## Next steps

I have started re-writing the interpreter in `C++` from the ground
up. I'll keep to the same lisp-y syntax and the program will do the
same jobs, but under the hood everything will be represented by an
object. I'll start with the tokeniser and parser, where I will need
to implement `LispObject`, `LispAtom`, `LispList`, and
`LispEnvironment` then build up the evaluator and flesh out the
standard library.

As of this post, the interpreter is pretty much at the state where I
left it in `c`, minus a lot of the standard library.





## Tokenising a string

I converted the tokenise function over to `C++`, making small
changes, but nothing major:


```C++
#define IS_WHITESPACE(C) ((C == '\n') || (C == ' ') || (C == '\t'))
#define ADD_TO_TOKENS(KW) \
  new_token = new LispToken(KW);\
  if (rv == NULL) {\
    rv = new_token;\
  }\
  else {\
    current_token-&gt;next = new_token;\
  }\
  current_token = new_token;



LispToken *tokenise(std::string input)
{

  char ch, nch;
  unsigned long i = 0;

  std::stringstream kw_or_name_builder;
  bool in_quote = 0, add_close_parens_on_break = 0, add_close_parens_on_parens = 0;
  int parens_level = 0;

  LispToken *rv = NULL, *current_token = NULL, *new_token = NULL;

  for (i = 0, ch = input[0], nch=input[1]; i &lt; input.length(); ch = input[++i], nch=input[i+1]) {

    if (input[i] == ';') {
      for (;input[i] != '\n' &amp;&amp; i &lt; input.length(); i++);
      continue;
    }

    // if breaking char: space, newline, or parens
    if (( IS_WHITESPACE(ch) || (ch == ')') || (ch == '(') || (ch == '\'')) &amp;&amp; !in_quote) {

      // finish reading keyword or name
      if (kw_or_name_builder.str().length()) {
        ADD_TO_TOKENS(kw_or_name_builder.str());
        kw_or_name_builder.str("");

        if (add_close_parens_on_break) {
          add_close_parens_on_break = 0;
          ADD_TO_TOKENS(")");
        }
      }

      // TODO switch-case
      // action needed on breaking char?
      if (ch == '(') {
        ADD_TO_TOKENS("(");
        parens_level++;
      }
      if (ch == ')') {
        ADD_TO_TOKENS(")");
        parens_level--;

        if (add_close_parens_on_parens) {
          add_close_parens_on_parens = 0;
          ADD_TO_TOKENS(")");
        }
      }
      else if (ch == '\'') {

        ADD_TO_TOKENS("(");
        ADD_TO_TOKENS("quote");

        if (nch == '('){
          //debug_message("NEXT CHAR IS '('; quote list\n");
          add_close_parens_on_parens = 1;
        }
        else if (IS_WHITESPACE(nch)) {
          //error
          //debug_message("NEXT CHAR IS WHITE SPACE! ERROR");
          //Exception_raise("SyntaxError", "tokenise", NULL, "single quote should be before a list or other object.");
        }
        else {
          add_close_parens_on_break = 1;
          //debug_message("NEXT CHAR IS '('; quote kw\n");
        }
      }

    }
    else {

      if (ch == '"')
        in_quote = !in_quote;

      kw_or_name_builder &lt;&lt; ch;

    }

  }

  if (kw_or_name_builder.str().length()) {
    ADD_TO_TOKENS(kw_or_name_builder.str());
    kw_or_name_builder.str();

    if (add_close_parens_on_break) {
      add_close_parens_on_break = 0;
      ADD_TO_TOKENS(")");
    }
  }

  return rv;
}
```

Main difference is the use of `std::string` and `std::stringstream`
to builder up strings. This means that there's none of the
accoutning of string length or memory size needed in the `c`
implementation.


### Started at the end? You might be interested in reading the first two entries.
- [Part 1]({% post_url 2019-11-21-lisp-interpreter %})
- [Part 2]({% post_url 2019-11-27-crisp2 %})
