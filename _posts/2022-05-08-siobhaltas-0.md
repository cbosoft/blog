---
title: "Sìobhaltas 0: Pre-Planning"
excerpt: "Àite Domhainn -> Sìobhaltas. A new plan for the strategy game, a new direction and (most importantly, of course) a new name!"
layout: post
tags: games software-dev C++
comments: true
---

# A strategy game for the patient

Last year I got started on this wee strategy game with "idle hero" style elements. I liked the idea of having a game with only sporadic input on the part of the player, and I have always liked the idea of a "digital aquarium" kind of thing: I want something interesting to appear every time I open a new terminal.

With that inspiration laid out, I started development of a terminal based "No Man's Sky" -esque strategy game. This was a really cool thing to think about and research: how star systems are formed, how planets are formed, what are they formed of, what would be feasible to live in, what kind of details need to be considered, as a civilisation, before embarking on space travel, and so on. However, in the process of researching all this, I neglected to included anything resembling gameplay!

I started to think about how an idle game might include elements of strategy. Traditional idle games don't have the best game play - instead having some kind of baby's first strategy elements involving very few moving parts. I want to have something a bit more involved, something requiring a little thought, a bit of *challenge*. As a fan of the games of FROM Software, I completely buy into the thinking that challenging game play can be very rewarding.

My task became thinking of how non-trivial strategy be incorporated into an idle game.

As I was already thinking about a space civilisation simulation game - what strategy is involved in running a civilisation? Civil planning, infrastructure, defence, ... boils down to **governance**. This is usually done on a granular level in real-time strategy or turn-by-turn in games like Civilization. This could definitely be adapted for idle play by changing how the player governs. Instead of making the micromanage-y decisions, the player would set more broad-ranging policy. The civilisation would then behave as per these rules for better or for worse. In this way, the player only requires to interact occasionally with the game, while still having to make relatively involved decisions.

# Gameplay!

Okay so let's make that spiel more concise:
- Sci-fi space-faring civilisation sim
- Player sets governing policy
- Civilisations behave as per policy
- Player's actions will affect population count, happiness and so on.
- Similar to sandbox games (e.g. Minecraft, Dwarf Fortress) no explicit goal is given to the player
- Actions and milestones are tracked (to give some sense of progress)
- Exploration yields archaeological finds etc - story elements for the player to read
- As in some RTS games (e.g. Stronghold) - select stories from the population will be made available to the player

This loosely sets out the scope of the game**play**. But how will the game be interacted with? What will it look like?

# UI

I envisage the game to take the form of a terminal-based game. This will have a simple command like interface (CLI). This will allow the player to check on their civilisation:

{% highlight bash %}
> game --check
Population:    9.3B
Current mood:  elated
News:
  - New miracle material discovered decreasing interplanetary travel costs.
  - Habitable planet discovered: new target for colonisation.
  - People opt for four day work week - mood elevated while productivity unaffected.
{% endhighlight %}

This could be included in a `.bashrc`, facilitating the "digital aquarium" use of the game.

Policies will be set by the player through a purpose-designed declarative "programming" language. This could be input statement-by-statement in the CLI:

{% highlight bash %}
> game --add-policy "expand into new solar system"
{% endhighlight %}

Or could be entered in the user's editor as a whole set of policies at once.

This CLI could be used in tandem with a TUI (terminal user interface) or GUI (graphical user interface) giving more information, perhaps an interactive history or timeline.

# Implementation and technologies

## PolicyLang
The civilisation controlled by the player I expect to be defined by some nice maths. This maths is controlled by the policies set by the player. These policies are set, as mentioned previously, by the player through a simple declarative language. The syntax of this language emulates political manifestos or other similar legalese: human readable, but relatively precise in meaning.

Each policy starts with a vague yet promising statement, like all good political manifestos.

{% highlight text %}
expand territory
{% endhighlight %}

Under the hood, a default action is changed. Details can be optionally provided to give specifics.

{% highlight text %}
improve cultural impact by focusing on artistry
focus on advancement by reducing school fees
improve defences by enforcing conscription
{% endhighlight %}

The choices should be varied enough that a player doesn't feel limited by their options. Along with this, the simulation model needs to encompass all the possibilities...

## Simulation Method
I want a server-less setup, so the game binary should stand alone. When the executable is run, the simulated world should be updated according to how much time has passed since last run (using the ***Maths***). This should be fast (not timestepped, but directly calculated). This echoes event-based simulation techniques.

# Sìobhaltas? Sìobhaltas!
Ah, Sìobhaltas. I think the game needs a new name. It's been a while, the scope has changed, and the name was always a bit of a stretch. Àite Domhainn means "Deep space" but not like, really. "Àite" is Scots Gaelic for "place" and "Domhainn" is "deep", so deep place. This was born of a desire to focus on the exploration of space - the colonisation and settlement of worlds. However, the gameplay I have in mind focuses more on the *people* than the setting. I think a new name is called for. I have settled on Sìobhaltas - Gaelic for "Civilisation". (I hope that's distinct enough to keep Sid Meier off my back!) The new name is a good fit, as I see it, gelling with the focus on people and society. In some translations sìobhaltas becomes "civility" which I quite like, too. 

# Conclusions
So this post has been a bit all over the place, but I wanted to get some ideas down on paper. (Not sure the term "paper" strictly applies to a blog post? Oh well.) I've talked a bit about how the game should be played, I've talked a bit about the implementation details, and I unnecessarily explained the name change.

# Next Steps
The main part of the game I'm not 100% on is the modelling of the civilisation itself. This will take some iterations to get to a satisfying result and will likely take the most time and effort. Following from this, development of PolicyLang will likely be the next biggest time sink. This would be followed writing and developing the "copy" - writing the text of the game (histories, people, events, objects, alien races, ...). Finally followed by packaging and polish.

Listifying:
1. Develop mathematical models of civilisation
2. Develop PolicyLang
3. Write game copy
4. Package everything together and polish.