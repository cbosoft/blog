---
project: "GreyGoo 🤖"
elevator_pitch: "A strategy game for the patient about mad science, armageddon, and robots."
repo: "github.com/cbosoft/greygoo"
layout: projectpage
tags: software-dev projects Rust
status: Alpha
has_diagrams: true
---

# Motivation

In the pre-pandemic times I got a little obsessed with the idea of a "strategy game for the patient" - creating a grand-strategy project exploring the idea called "Sìobhaltas" (née "Aìte Domhainn"). However I got lost along the way, got sidetracked with other ideas, but the main stumbling block was figuring out how to do epic timescale simulation and shrink it down to real-world scale. I toyed with the idea on-and-off until coming up with a much tighter idea: how long would it take for a grey-goo scenario to unfold? What steps would be taken to get there? Aha! this sounds like an opportunity for another "strategy game for the patient"!

# Specification
The game should be:

## Cross Platform
I like the idea of the game being available to anyone on any platform - à la the flash games of yore. The easiest way to do this: make it a web-app. However, the game may not be limited to a web app and could feasibly be an executable using, e.g. QT for UI (cross platform targeting MacOS, Windows, and Linux). The game could also be extended to mobile apps either using their native tools (Android Studio, Xcode) or using a cross platform development solution like Unity.

## Rust!
I have so far really enjoyed the performance and memory safety of Rust. I still fight with the borrow checker and I am only slowly slowly getting to grips with the language. Because it is new and fascinating to me, I want to do as much of this project as I can in Rust. Also, there is a wasm target for Rust compilation which would make the creation of a web-app easier. However, it would be less easy to use Rust for mobile development (although not impossible?)

## a Strategy Game
The player should have to make decisions which have an impact and may inspire counter-plays by the computer and thus forward planning (i.e. strategy) is required on the part of the player.

## Decentralised
I do not want the player to be beholden to a server: the game should run locally only.

## Specification Summary
- [ ] Cross platform
- [ ] Web App
- [ ] Rust-lang
- [ ] Strategy
- [ ] Client-only architecture

# Development Challenges
## Organising a game "for the patient"

## Fusing rust backend with webpage frontend

## Testing, testing, testing!

# Conclusion

# Spec Check
The application must
- [ ] 


Here is one mermaid diagram:
<div class="mermaid" id="centre">
graph TD 
A[Client] --> B[Load Balancer] 
B --> C[Server1]
B --> D[Server2]
</div>