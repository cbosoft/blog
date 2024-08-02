---
project: "ShakeMyLeg - a State Machine Language"
elevator_pitch: "A simple state machine definition language to elevate laboratory experiment control."
repo: "github.com/cbosoft/sml"
layout: projectpage
tags: software-dev projects Rust
status: Release
has_diagrams: false
---

# Motivation
I am developing a control software for one of our instruments. The provided software does the job but is quite limited. As a research institute it is helpful to be as flexible as possible and what's more flexible than custom software? (Well, custom hardware but that's out of scope.)

The experiments performed by the equipment, in the default software, follow a series of steps involving different control actions. These steps are fixed for a given experiment and do not react to changing measurements. For example, it's quite common to wait for a given event to occur but as we have no idea when this event will occur, the corresponding experiment step must be sufficiently long to *hopefully* contain this event. Apologies for the vagueries, I'm trying to not get fired here.

Instead of waiting ages and hoping the event is captured, we can react to changing measurements and stop the step only when the event has occurred. This removes guess work and potentially decreases average experiment time (no need to wait as long as possible).

In order to facilitate this tantalising efficiency gain I started writing a replacement software. For the most part, writing the software has been a really fun challenge. This involved reading packet streams to figure out APIs, implementing different network protocols in `Rust`, as well as getting up to speed with async in `Rust`. (Turns out, `tokio` is awesome.)

The surrounding software was coming along nicely and I had a brainwave about how to achieve flexible and efficient control: control functions could simply be written in some interpreted language and run in an embedded interpreter! One quick google search later and `mlua` was found. An hour and some coding later, and I had control implemented. Easy, nice. However, I remembered that we're a research institute and no-one knows lua (aside from a few infamous individuals).

The embedded interpreted language needed to be simpler (literally, just smaller in scope) as well as tailored to the task at hand. This is starting to sound a bit like a domain specific language...

The controller for the instrument can be modelled sufficiently as a state machine. Each 'step' mentioned above is like a state, we can move between states either by waiting for the step to complete or by reacting to measurements. What if we had a simple language to define these state machines?

This is how I came to `ShakeMyLeg`: a state machine definition language.

# Specification
SML should:
- be interpreted
- describe a state machine as a series of states
- take input on every step through the machine
- return output on every step through the machine
- allow the machine to be configurable by variables prior to running
- allow moving between states based on changing inputs

# Development Challenges
# Language design
As a data scientist and ML person, day-to-day I probably write more Python than any other language. I also make liberal use of YAML for config files. As a result, colons and indentation feel natural as a means of defining blocks:

{% highlight yaml %}
block:
  body
{% endhighlight %}

As we're defining a set of states independently from each other, we can use a top level item to define the state and give it a name:
{% highlight yaml %}
state A:
  body A

state B:
  body B
{% endhighlight %}

What happens in a state though? Well, it's really a series of conditions describing `when` you get to `changeto` another state:
{% highlight yaml %}
# flip_flop.sml
state A:
  when true:
    changeto B

state B:
  when true:
    changeto A
{% endhighlight %}

Aha! Now we have enough language to describe a very simple machine: a binary astable. Not very useful yet... How do we get data in? Well, let's say there's some object called `inputs` available to the machine. We can do something similar for `outputs`, and for other variables (`globals`).

{% highlight yaml %}
state A:
  when inputs.foo > 15:
    outputs.foo = inputs.foo + 1
    outputs.bar = globals.a
    changeto B

state B:
  when inputs.foo < 5:
    outputs.foo = inputs.foo - 1
    outputs.bar = globals.b
    changeto A
{% endhighlight %}

It would probably be handy if there was a way to execute expressions before the conditions are checked. Following anatomy, above the body is the `head`:
{% highlight yaml %}
state A:
  head:
    outputs.foo = inputs.foo + 1
    outputs.bar = globals.a
  when inputs.foo > 15:
    changeto B

...
{% endhighlight %}

As well as changing state, there's the implied default action of "do nothing" (or `stay` in the current state). Additionally, we need some way to `end` the machine. It would be good if we could refer to the final condition in some nice way (instead of `when true`), like to indicate what will happen `otherwise`.
{% highlight yaml %}
state A:
  when inputs.foo < 3:
    outputs.foo = inputs.foo + 1
    stay
  otherwise:
    end
{% endhighlight %}

Think we're getting there... If `head` is common to a bunch of states, then we can define a `default head` top level. As well as otherwise, it would be nice to name the branch that `always` runs:

{% highlight yaml %}
default head:
  outputs.ver = globals.ver

state DECR:
  when inputs.foo > 0:
    outputs.foo = inputs.foo - 1
  otherwise:
    changeto INCR

state INCR:
  always:
    outputs.foo = inputs.foo + 1
{% endhighlight %}

Last thing to really think about are the data types and expressions. I want it to be relatively intuitive for a non-programmer, so worrying about floats vs ints is out. Like Javascript, let's just have a `Number`. We'll also need a `String` type and of course `Bool`. Standard c-style ops would make sense, though I would like a power operator (like python's `**`).

{% highlight yaml %}
default head:
  outputs.number = (1.0 + 3) * (5 - 2) / (5.5^0.5)
  outputs.string = "this is a string"
  outputs.bool = true && (1.0 == 1)
  outputs.combined = outputs.bool && (outputs.string || outputs.number)
{% endhighlight %}

## Implementing the interpreter
This interpreter needs to be embedded into the control software I'm working on, so it must be implemented in (or compatible with) `Rust`. I chose `Rust` for that project because of the memory safety guarantees, strong typing, and the performance of a compiled language. For the same reasons, I'll use `Rust` for this, too.

The structure of the language (states and branchs) was relatively easy to implement an interpreter for: just match on keywords and check indentation. I actually used a state machine for this part of the interpreter.

The part which I found harder to think about was writing the expression parser. I have written interpreters before, but only for Lisp. In lisp, everything is enclosed in brackets so it is very easy to write an interpreter for. I've never written an interpreter which deals with infix notation. After some searching, I found a [page from Northern Illinois University](https://faculty.cs.niu.edu/~hutchins/csci241/eval.htm) which details converting from infix to postfix expressions, as well as how to evaluate the resulting postfix. Wonderful. Just need to break up an expression into tokens...

Tokenisation is another annoying step, chiefly because of operators with two or more characters. If all operators were only one character, then tokenisation would be as simple as splitting on whitespace and around operator-characters. However, `==`, `<=`, and friends proclude that simplicity. I've been somewhat lazy here and not dealt with this: all operators must have whitespace around them. This has the nice side effect that the resulting code is more readible (in my opinion). With that implemented, we're good to go!

## `Rust` hates raw pointers
If you use raw pointers in `Rust` it shames you for it by forcing you to declare your code horrible and unsafe. Instead you are encouraged to use smart pointers like the `Box` type. With this in mind... I wanted to have an `Expression` enum, which can be an identifier, a value, or an operation on another pair of `Expression`s... so an `Expression` contains within itself another `Expression` - the object has infinite size and that's not feasible. In `Python`, everything is a reference anyway and I wouldn't need to think about this. In `Rust`, we use `Box`es.

{% highlight rust %}
pub enum Expression {
    Value(Value),
    Identifier(Identifier),
    Unary(UnaryOperation, Box<Expression>),
    Binary(BinaryOperation, Box<Expression>, Box<Expression>),
}
{% endhighlight %}

`Box`iness aside, I adore the enum of struct thing `Rust` has going on. What a great way to sort-of do polymorphism.

## Fighting the borrow checker with (`A`)`Rc`s
In order to access a reference to a struct attr, as well as a mutable reference to another attr, we need to circumvent the borrow checker at compile time by getting us some interior mutability - we need to wrap the object in something which will do the borrow checking at runtime. `Rc` is one of these. It uses reference counting to decide if you're allowed to mutate something. (If there's more than one copy of the `Rc`'d object, the answer is no.) This is how I got the expression evaluation to work: we have two attrs of `StateMachine` to consider while evaluating an `Expression` (specifically, an `Expression::Identifier`). We have three "stores" for variables: `globals`, `inputs`, and `outputs`. The first is an attribute of the `StateMachine` which needs to be mutable. The second attr to consider... is the `State` which is being run. This is where the `Expression`s are stored in the first place. This does not need to be mutated.

So to evaluate an expression, I start from the `State` in an `Rc` which is owned by the `StateMachine`, and clone it so I have an `Rc<State>` not owned by the machine. I get a mutable reference to the `StateMachine` when I mutably borrow the `globals` store, and the expression can evaluate as desired. This also has the advantage of allowing me to cheaply move the pointer `Rc<State>` so I keep a reference to the current `State` as `StateMachine{ ... current_state: Rc<State> }`.

However, I encountered a problem... In my use-case for this interpreter, I need the `StateMAchine` to be threadsafe (i.e., I need it to be `Send+Sync`) and `Rc` is **not** thread safe. Damn. But `Arc` is! So just move to `Arc`? Yup, that works! Though, if you really want to use `Rc` instead, I locked the `Arc` usage behind a `thread_safe` feature flag.

# Conclusion
This was a really satisfying wee project! SML is now live in use in my instrumentation software, pending rigorous testing. `Rust` and `cargo` really make developing a breeze. Need a a package? `cargo install`. Need a test suite ran? `cargo test`. Need to publish to package repository? `cargo publish`. The strong typing, borrow checker, and `Result` system really put me at ease that if this compiles, there's unlikely to be a runtime panic.

# Final Spec Check
SML should:
- [X] be interpreted
- [X] describe a state machine as a series of states
- [X] take input on every step through the machine
- [X] return output on every step through the machine
- [X] allow the machine to be configurable by variables prior to running
- [X] allow moving between states based on changing inputs

# Links
Check out the source on [github.com/cbosoft/sml](https://github.com/cbosoft/sml).

Start using the library on [crates.io/crates/shakemyleg](https://crates.io/crates/shakemyleg).

Check out the docs and examples on [docs.rs/shakemyleg/2.4.0/shakemyleg/](https://docs.rs/shakemyleg/2.4.0/shakemyleg).
