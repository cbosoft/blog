---
title: "Assembly is WILD"
layout: post
excerpt: "The power afforded by assembly is astounding; the skill required to wield it properly moreso. This is a tale of GameBoys, CPU emulation, and learning assembly."
tags: software-dev C Python
---

Two weeks ago I was working on a project. I was building containerised apps using Docker to create a scalable system I could unleash on my work's fancy new cluster. I was attacking the project and making good progress when I was compelled by the [dark wizard](https://www.youtube.com/watch?v=HLRdruqQfRk) to emulate the Intel 8080-descendent that is the GameBoy CPU. Abruptly stopping work on the containerised app, I started consulting the opcode tables and technical specifications of the GameBoy.

In high school I first learned about logic gates, digital circuits and the like. I had an excellent teacher who inspired me. A younger version of the dark wizard compelled me to design an 8bit processor from *discrete components*. I drew up circuit diagrams for the sRAM, the logic circuits and the ALU, I sketched out the instruction set, and then popped off to university and the project got dropped.

My recent foray into CPU emulation echoed my earlier shallow investigation into CPU design. I've remembered a lot, and I've learned even more. Including some surprising (horrifying?) things.

# Sharp LR35902
The Sharp LR35902 CPU is an 8bit CPU used in the GameBoy within the SoC. This CPU features a mind-blowing 65,535 bytes of memory (16bit). The CPU runs at a *blazingly fast* 4MHz. Emulating this wee processor requires fleshing out the 512 or so instructions given in the Intel 8080-derived table with the extended bit-operations table. (There is so much information available online on the GameBoy, the tables are given [here](https://meganesu.github.io/generate-gb-opcodes/) while a wealth of technical reference is collected [here](https://github.com/Gekkio/gb-ctr).)

Building the emulator for this CPU opened my eyes to assembly: assembly code has no concept of an object or a struct, it has no concept of a for loop or anything. It has `LD` (load). It has `JP` (jump). It has things like `ADD`, `SUB`, and `OR`. Each command is timed in terms of *cycles*. For a 1MHz CPU, this is feels really quite incredible: you can perform four million additions per second! (Albeit 8bit additions...) When writing programs normally, it feels like there is some overhead to be overcome. Performing anything at a rate commensurate with the clock rate seems nuts. On a modern processor this would be on the order of billions of operations! Of course, the processor *is* performing instructions at that rate, and there *is* overhead associated with our fancy modern objects and moving them about and so on.

Thinking about assembly got the dark wizard interested; now I must look into writing assembly.

# Fizz Buzz
Children's game and now coding interview question: fizz buzz is a number game. In turn say integers increasing from one, unless the number is divisible by three (in which case say 'fizz') or five (say 'buzz') or fifteen (say 'fizzbuzz'). A simple pseudocode implementation is given below:

{% highlight python %}
function fizzbuzz(i):
    if i mod 15 == 0:
        return 'fizzbuzz'
    elif i mod 5 == 0:
        return 'buzz'
    elif i mid 3 == 0:
        return 'fizz'
    else:
        return i
{% endhighlight %}

Why am I talking about fizzbuzz? I'm going to go through examples of FizzBuzz implementations in different languages, analysing the performance and then comparing with an amateur hand-crafted implementation in x86 Assmebly.

## Aside: performance testing

To measure runtime performance of the fizzbuzz implementations, I wrote a small `c` program:
{% highlight c %}
#include "stdlib.h"
#include "time.h"
#include "stdio.h"

 double perf_test(const char* prog, int n) {
    double tot = 0.0;
    struct timespec start = {0, 0}, end = {0, 0};
    for (int i = 0; i < n; i++) {
        clock_gettime(CLOCK_MONOTONIC, &start);
        system(prog);
        clock_gettime(CLOCK_MONOTONIC, &end);

        tot += (double)(end.tv_sec - start.tv_sec) + 1e-9*((double)(end.tv_nsec - start.tv_nsec));
    }

    return tot / ((double)n);
}

int main(int argc, const char** argv) {

    if (argc < 2) {
        printf("usage: perf PROG [N]\n");
        return -1;
    }

    int n = 100;
    if (argc > 2) n = atoi(argv[2]);

    double result = perf_test(argv[1], n);
    printf("average time after %d repeats = %es\n", n, result);
}
{% endhighlight %}

The program takes two arguments, a program and optionally a number of repetitions (defaults to 100). The program runs the specified program/script the specified number of times and reports the average time taken to run. Example:

{% highlight bash %}
~ ./perf prog 1000
...
average time after 1000 repeats = 1e-3s
{% endhighlight %}

## `Python`
Ah cpython. Interpreted langauge, performance takes a hit in favour of flexibility. I have the most experience with python, so I started with this. Rather than return, we'll get the function to print the value to stdout. This will make testing easier.

{% highlight python %}
#!/usr/bin/env python

def fizzbuzz(i):
    if i % 15 == 0:
        print('fizzbuzz')
    elif i % 5 == 0:
        print('buzz')
    elif i % 3 == 0:
        print('fizz')
    else:
        print(i)

for i in range(1, 11):
    fizzbuzz(i)
{% endhighlight %}

Running this on integers 1 up to 10 gives us the expected result: `1 2 fizz 4 buzz fizz 7 8 fizz buzz`. Good stuff. Performance? Running the script through the perf program gives:

{% highlight bash %}
~ ./perf ./fizzbuzz.py
...
average time after 100 repeats = 1.382310e-01s
{% endhighlight %}

There's the baseline then, 0.1s to run fizzbuzz on ten integers. Even though `cpython` is `c` at heart, it definitely doesn't have its speed.

## `C`
Okay, so let's try `c`!

Same algorithm, but in `c` this time.

{% highlight c %}
#include "stdio.h"

void fizzbuzz(int i) {
    if (i % 15 == 0) {
        printf("fizzbuzz\n");
    }
    else if (i % 5 == 0) {
        printf("buzz\n");
    }
    else if (i % 3 == 0) {
        printf("fizz\n");
    }
    else {
        printf("%d\n", i);
    }
}

int main() {
    for (int i = 1; i <= 20; i++) fizzbuzz(i);
    return 0;
}
{% endhighlight %}

Compiling with `clang -Wall -Werror fizzbuzz.c -o fizzbuzz_c` and running `perf` gives much better results this time:
{% highlight bash %}
~ ./perf ./fizzbuzz_c 100
...
average time after 100 repeats = 9.426610e-03s
{% endhighlight %}

Ah, more than a factor of ten increase in speed. That's pretty good. I actually expected it to do better. 9.4ms on a ~2GHz processor is about 18.8k cycles. There's some fat to trim here. Never thought I'd call `C` bloated!

## What does the `C` assembly look like?

For the `C` program above, we can look at the generated assembly. Using clang:

{% highlight bash %}
~ clang -S -mllvm --x86-asm-syntax=intel fizzbuzz.c
{% endhighlight %}

This results in 120 or so lines of non-optimised assembly. Let's see what's going on in `main`, [Call Frame Information (CFI)](https://stackoverflow.com/questions/24462106/what-do-the-cfi-directives-mean-and-some-more-questions) removed:
{% highlight armasm linenos %}
_main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	dword ptr [rbp - 4], 0
	mov	dword ptr [rbp - 8], 1
LBB1_1:
	cmp	dword ptr [rbp - 8], 10
	jg	LBB1_4
	mov	edi, dword ptr [rbp - 8]
	call	_fizzbuzz
	mov	eax, dword ptr [rbp - 8]
	add	eax, 1
	mov	dword ptr [rbp - 8], eax
	jmp	LBB1_1
LBB1_4:
	xor	eax, eax
	add	rsp, 16
	pop	rbp
	ret
{% endhighlight %}

First of all, the program sets up the `rbp` with space enough to hold variables for the program. It sets up two 32 bit ("`dword`") values. One (at `rbp-4`) has value 0 and the other (at `rbp-8`) has value 1. A label `LBB1_1` is created. After the label, it checks to see if the value at `rbp-8` is equal to 10, if so it jumps to the end (line 16, label `LBB1_4`). **This is the exit condition of the `for`-loop in the `C` code.** Then, on line 10, the value at `rbp-8` is put in the `edi` register and `_fizzbuzz` is called. So that `mov` on line 10 is setting up the arguments to the function `call`'d on line 11.

When `_fizzbuzz` returns, flow continues from line 12, where `rbp-8` is incremented in a rather roundabout way: move `rbp-8` to register, `add` 1 to reg value, move reg value back to `rbp-8`. Then the loop is repeated, we `jmp` to label `LBB1_1` on line 7.

Exit condition where `rbp-8` is equal to 10 and the program jumps to line 16. This simply zeros out register `eax` by `xor` with itself, clears the stack and returns `0`.

Already I can see areas ripe for optimisation. This comes down to my choices when writing the `C` program, and not producing an optimised binary.

What about `_fizzbuzz`? Assembly included below, I've added comments on the role of each section.

{% highlight armasm linenos %}
_fizzbuzz:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	dword ptr [rbp - 4], edi
	mov	eax, dword ptr [rbp - 4]
	mov	ecx, 15
	cdq
	idiv	ecx        # divide i by 15, store remainder in edx
	cmp	edx, 0     # if remainder is NOT zero... 
	jne	LBB0_2     # ... jump to 2, else print "fizzbuzz" !
	lea	rdi, [rip + L_.str]
	mov	al, 0
	call	_printf  # print 'fizzbuzz'!
	jmp	LBB0_9
LBB0_2:  # not fizzbuzz... is buzz?
	mov	eax, dword ptr [rbp - 4]
	mov	ecx, 5
	cdq
	idiv	ecx
	cmp	edx, 0  # i%5 == 0?
	jne	LBB0_4  # no? jump to 4. yes? print 'buzz'
	lea	rdi, [rip + L_.str.1]
	mov	al, 0
	call	_printf
	jmp	LBB0_8
LBB0_4: # not fizzbuzz, not buzz ... is fizz?
	mov	eax, dword ptr [rbp - 4]
	mov	ecx, 3
	cdq
	idiv	ecx
	cmp	edx, 0  # i%3 == 0?
	jne	LBB0_6  # no? jump to 6. yes? print `fizz`
	lea	rdi, [rip + L_.str.2]
	mov	al, 0
	call	_printf
	jmp	LBB0_7
LBB0_6:
	mov	esi, dword ptr [rbp - 4]  # put i in as format operand
	lea	rdi, [rip + L_.str.3]     # put "%d\n" in as string
	mov	al, 0
	call	_printf  # print "%d" !
LBB0_7:
	jmp	LBB0_8
LBB0_8:
	jmp	LBB0_9
LBB0_9:
	add	rsp, 16
	pop	rbp
	ret
{% endhighlight %}

I can see less room for improvement here, but there are optimisations for sure. For example, it copies `i` (`rbp-4`) four times into `eax`. As far as I can see, this is completely unnecessary. The copy of `i` from the register `edi` onto the stack at `rbp-4`, then  *back into* the registers *again* at `eax` feels unnecessary. Could just go straight from `edi` into `eax`?

The layout of the conditions are pretty well optimised. We are getting the remainder of the division of `i` by `{15, 5, 3}`, and then checking if the remainder doesn't equal `zero`. There is no modulo instruction, we get this via `div` and getting the remainder.

Main potential improvements can be gained by pulling back from using full `int` types, and using smaller ones. This has been enlightening to say the least! If I'm every stuck for performance gains again, I'll check out the assembly for tuning!

Let's justify that title...

# What's wild about (x86) Assembly?
Oh let me count the ways...
 1. Execution time is counted in cycles.
 2. Directly¹ moving things around in memory.
 3. Can overwrite *itself* in memory!
 4. *Exceptions are first class*
 5. Writing to stdout is *writing to area of memory*

¹ Direct...ish. The OS has some hands in here, and so does the CPU microcode, but more direct that in any other programming language!

This was mind blowing to me. I don't know what I expected to be honest. We have all this complexity of OS and user application running atop layers and layers of multifaceted abstract over something so insanely simple. If we didn't have all the abstraction, what kind of performance could we achieved? I suppose this abstraction is the price we pay for both user- and developer-friendliness.
