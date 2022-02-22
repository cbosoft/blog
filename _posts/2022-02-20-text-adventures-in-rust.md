---
project: "FeOTAE - a Rusty Text Adventure Engine"
elevator_pitch: "A simple text adventure game engine."
repo: "github.com/cbosoft/feotae"
layout: projectpage
tags: Rust
status: Released
has_diagrams: true
---

# Motivation
A couple [weeks ago]({% post_url 2022-02-03-rust-lang %}) I started getting in to learning about rust. I have a habit of writing simple text adventure games when I learn a new language. I started this in high school when I was learning `C#` with a text-adventre version of Counter Strike - inspired by an [XKCD comic](https://xkcd.com/91/). I actually got really far with that, to the point where I had network based multiplayer kinda working, but then I abandoned the project as school and university took over.

So I started a new text adventure to get into the swing of things with `Rust`. This went really well I think, I quite quickly arrived at a usable game engine. This was mostly facilitated by the rust package (sorry, crate) `serde` - a fantastic (de)serialisation library.


# Challenges
## Getting used to `Rust`!
The main challenge I faced in this project was getting to grips with `Rust`, and especially how it handles *references*. Before I get to references, I had to learn how to create functions, and classes/objects. `Rust` doesn't have things explicitly called classes, but has structs which are the same thing. `C++` has structs and classes and the two have a lot of crossover - `Rust` eliminates that crossover by smushing the two together.

```rust
struct Foo {
    a: i32,
    b: i32
}

impl Foo {
    pub fn new(a: i32, b: i32) {
        Foo{a, b}
    }

    pub fn total(&self) -> i32 {
        self.a + self.b
    }
}
```

The above creates a simple (pointless) object with two *private* properties, and a constructor *associated function*. The "constructor" creates a new `Foo` object and initialises its values of `a` and `b`. The new object is returned by being the last value in scope - I don't need to explicitly `return` it. This is quite a big change for me and it seems to encourage a more functional style of writing code: smaller and more functions, fewer side-effects. This is also encouraged by the borrow-checker I touched on in the previous paragraph, which I initially found a bit confusing. Luckily, `Rust` has extensive [documentation ("The Book")](https://doc.rust-lang.org/book/) and a fantastic [examples library](https://doc.rust-lang.org/rust-by-example/) that makes it easier to get into the swing of things.

In addition to getting used to memory management, moving-by-default, references etc in `Rust`, I had to get into module structure and package manaagement. Oh and the different kinds of structs (unit, tuple, and struct) and destructuring `let (x, y, z) = point;` and `Result`s and so on. All of this made easier by the documentation and fantastic compiler. The rust compiler has the ***best*** compiler output I have ever seen.


## Challenge 2: Game loop
I wanted to keep this game relatively simple, as I don't have a huge amount of spare time to devote to these projects anymore. I decided therefore to keep the game loop to a very barebones: (1) display current location, (2) get and act on user input, (3) goto 1. Of course, preceding the loop some set up is required

<div id="centre" class="mermaid">
graph TD
A[0. Read game data] --> B[1. Display state] --> C[2. Get+process input] --> B
</div>

No menus, no networking, just simple text adventuring. The majority of the logic is contained in a main `Game` struct, while things like stage/location information is in a `Stage` struct. Navigation between stages is facilitated by `Path`s, which can be hidden or visible. A `Trigger` is activated by performing certain actions like `use lever` or just by entering a stage (`on enter`). These triggers set or unset `flags` in the main game, and can be used to hide/show `Path`s or `Item`s.


## Challenge 3:
The game setup also needs to be handled - which I initially used TOML for, but quickly found that TOML is not great for structured data serialisation due to its overly verbose syntax and I ended up switching to YAML as previously mentioned. YAML makes nesting objects really simple and readable as compared to TOML, as can be seen below:

### TOML
```toml
name = "walk through the woods"

[stages]
[stages.1]
name = "the woods"

[stages.1.items]
[stages.1.items.axe]
name = "axe"

[stages.1.paths]
[stages.1.paths.north]
destination = 2

[stages.2]
name = "more woods"

[stages.2.paths]
[stages.2.paths.south]
destination = 1
```

### and the equivalent YAML
```yaml
name: "walk through the woods"
stages:
  - name: the woods
    items:
      axe:
        name: axe
    paths:
      north:
        destination: 2
  - name: more woods
    paths:
      south:
        destination: 1
```

Now, serialisation could have been a pain. Switching between serialisation backends *could* have been infeasible or impractical. However, `Rust` has a great library `serde` which ***automatically*** creates serialisation and deserialisation functions for your objects, using the `#[derive(...)]` annotation.


```rust
use serde::{Serialize, Deserialize}

#[derive(Serialize, Deserialize)]
struct Foo {
    // ...
}

// ...

fn main() {
    match read_file_contents("foo.yaml") {
        Ok(contents) => {
            match serde_yaml::from_str(&contents) {
                Ok(_foo) => println!("deserialised foo!"),
                Err(msg) => println!(msg)
            }
        },
        Err(msg) => println!(msg)
    }
}

```

When changing from TOML to YAML, all I had to do was change out `toml::from_str` to `serde_yaml::from_str`, *and that was it!*


# Conclusions
The project has served its purpose, and I have gotten a bit more used to `Rust` now. `Rust` has some great features. I especially like `match ... {}` syntax for making decisions based on return value - especially when paired with the `Result` type for error checking. The borrow checker has been the source of some annoyance - but only because I'm not yet used to it.


## Appendix: the name

FeO is the chemical symbol for iron oxide AKA rust, then the rest is just "Text Adventure Engine" abbreviated to give FeOTAE.


I'm happy enough with my simple game engine and now that I've done the interesting bit, I haven't the heart to actually create a game in it!