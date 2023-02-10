---
layout: post
title: "Digging into Multi-Factor Authentication"
tags: Python Rust
excerpt: "MFA apps use RFC-defined algorithms - let's figure out how they work and implement our own version."
comments: true
---

{% assign languages="Python, Rust" | split: ", " %}

# Authenticator App

These days it's impossible to go long without being pestered to set up MFA - Multi-Factor Authentication via something like a phone or via email. One method is using an "Authenticator" app installed on a smart phone to provide this second factor of security. This is great for security, and relatively convenient. How do these apps work?

When you're setting up MFA with a service, you are given a code (text or QR code), you scan this via your authenticator app. From then on your app generates (every thirty seconds or so) One Time Password (OTP) codes which can be used to authenticate access to the service.

The QR code contains a secret key which your app holds on to. Then, at any moment, the app can create an authentication code by doing *maths* with the key and the current time giving a code. The server does the same maths with the secret and the current time. If the codes are the same, then the authentication succeeds. This is a cryptographically secure - and convenient - authentication method.

Note: this process requires no data to pass from the service to the authentication device (apart from at set up). In fact the authentication device doesn't even need to be connected to the internet. This limits vectors for attack and offers security improvements over other methods such as email or SMS.

# Methods: HOTP or TOTP?

There are, in general, two operational modes of authenticator apps. The first being "HMAC-based One-Time-Password" (HOTP): which uses a Hash-based Message Authentication Code (HMAC) as basis for the OTP. The second mode is a modification of the first which relies on the current time: "Time-based One-Time-Password".

HOTP is not often used, TOTP is much more common (verging on ubiquitous). The primary goal of this post is then to implement a working version of this TOTP algorithm.

# Hash-based Message Authentication Code (HMAC)

The HMAC mechanism is described in [RFC2104](https://datatracker.ietf.org/doc/html/rfc2104). This method uses a hash function (e.g. SHA-1, MD5) and a secret key to (1) authenticate messages and (2) check data integrity.

A hashing algorithm works on blocks of bytes (of size B) and produces a hash of length L bytes. These sizes depend on the algorithm. SHA-1 and MD5 use block sizes of 64 bytes but SHA-1 has digest size L of 20 bytes while MD5 has L=16 bytes.

The HMAC algorithm is defined, in RFC2104, as:

{% highlight python %}
B: BlockLength
hash: HashFunction
K: SecretKey

ipad = b'\x36'*B
opad = b'\x5C'*B

def HMAC(K: SecretKey, message: str)
    return hash(K ^ opad, hash(K ^ ipad, message))
{% endhighlight %}

where the caret `^` indicates bitwise exclusive-or (XOR). There are some missing details from the above:

 - If the key is longer than the block size, then the key is itself hashed.
 - If the key is shorter than a block, then it is right-padded with zeros.

Let's go ahead and implement this. Handily, the RFC actually includes a `c` implementation using the MD5 hashing algorithm which makes writing this code really easy.

{% include tab_bar.html %}

{% include tabpython.html %}

There is actually a python module which calculates this for you (<code>hmac.HMAC(key, msg, hasher_t)</code>) but let's write it out in full regardless.

{% highlight python %}
# my_hmac.py
import hashlib


trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))


def hmac(K: bytes, message: bytes, hasher_t=hashlib.sha1):

    hasher = hasher_t()

    if len(K) > hasher.block_size:
        K = hasher_t(K).digest()

    K = K.ljust(hasher.block_size, b'\x00')
    hasher.update(K.translate(trans_36))
    hasher.update(message)
    istr = hasher.digest()

    hasher = hasher_t()
    hasher.update(K.translate(trans_5C))
    hasher.update(istr)

    return hasher.digest()
{% endhighlight %}
{% include end_tab.html %}

{% include tabrust.html %}
{% highlight rust %}
use sha1::{Sha1, Digest};

const BLOCK_SIZE: usize = 64;

fn clean_k(k: Vec<u8>) -> [u8; BLOCK_SIZE] {
    let mut k_sized: [u8; BLOCK_SIZE] = [0; BLOCK_SIZE];
    if k.len() > BLOCK_SIZE {
        let res = Sha1::digest(k);
        for i in 0..res.len() {
            k_sized[i] = res[i];
        }
    }
    else {
        for i in 0..k.len() {
            k_sized[i] = k[i];
        }
    }

    k_sized
}

fn do_xor(arr: [u8; BLOCK_SIZE], v: u8) -> [u8; BLOCK_SIZE] {
    let mut rv = [0u8; BLOCK_SIZE];
    for i in 0..BLOCK_SIZE {
        rv[i] = arr[i] ^ v;
    }
    rv
}


pub fn hmac(k_raw: Vec<u8>, m: Vec<u8>) -> Vec<u8> {
    let k = clean_k(k_raw);
    let k_i = do_xor(k, 0x36);
    let k_o = do_xor(k, 0x5c);

    let ihash = Sha1::new()
        .chain_update(k_i)
        .chain_update(m)
        .finalize();

    let ohash = Sha1::new()
        .chain_update(k_i)
        .chain_update(ihash)
        .finalize();

    ohash.to_vec()
}
{% endhighlight %}

Making use of the <code>sha1 = "0.10.0"</code> crate.
{% include end_tab.html%}




# HMAC-Based One-Time-Password (HOTP)

The HOTP algorithm is defined in [RFC4226](https://datatracker.ietf.org/doc/html/rfc4226).

```
HOTP(K, C) = Truncate(HMAC-SHA-1(K, C))
```
where `Truncate` represents the function that converts an HMAC-SHA-1 value into an HOTP value, and `C` is an 8-byte counter variable (the "moving factor").

The RFC describes the process very well: split into three steps:

1. Generate HMAC-SHA-1 value: a 20 byte string.
```
HS = HMAC-SHA-1(K, C)
```
2. Generate a 4-byte (31 bit) string through "Dynamic Truncation"
```
Sbits = DynamicTruncation(HS)
```
3. Compute HOTP value (with n digits)
```
Snum = StToNum(Sbits)
HOTP = Snum % 10^n
```

`StToNum` is a function which converts the bytes forming the string into an integer.

The "DynamicTruncation" function is where the magic happens. An offset is chosen as the four low order bits of the string, then bytes are taken from the string at position `offset` up to and not including `offset+4`. The least significant (right-most) 31 bits of this selection is the returned truncated value. The most significant bit is removed (i.e. by taking 31 instead of 32 bits) as this would be the sign bit - removing it removes any system-dependent ambiguity associated with the modulo operator.

The RFC again gives a reference implementation in Java, which makes the transliteration a breeze (although I would have preferred another C reference implementation to Java).

{% include tab_bar.html %}

{% include tabpython.html %}
{% highlight python %}
# my_hotp.py
from my_hmac import hmac


POWERS_TEN = [1_000_000, 10_000_000, 100_000_000]


def hotp(k: bytes, c: int, n: int) -> int:
    c_str = c.to_bytes(8, 'big')
    hs = hmac(k, c_str)
    offset = hs[-1] & 0xf
    snum = int.from_bytes(hs[offset:offset+4], 'big') & (2**31 - 1)
    return snum % POWERS_TEN[n - 6]
{% endhighlight %}
{% include end_tab.html %}

{% include tabrust.html %}
{% highlight rust %}
use crate::hmac::hmac;


const POWERS_TEN: [u32; 3] = [
    1_000_000, 10_000_000, 100_000_000
];


pub fn hotp(k: Vec<u8>, c_num: u64, n: usize) -> String {
    let mut c_arr = [0u8; 8];
    let mut running_c_num = c_num;
    for j in 0..8 {
        let i = 7 - j;
        c_arr[i] = (running_c_num & 255u64) as u8;
        running_c_num >>= 8;
    }

    let c_bytes = c_arr.to_vec();

    let hs = hmac(k, c_bytes);
    let offset = (hs[hs.len()-1] & 0xfu8) as usize;

    let snum = (
        (((hs[offset] & 0x7f) as u32) << 24)
        | (((hs[offset+1] & 0xff) as u32) << 16)
        | (((hs[offset+2] & 0xff) as u32) << 8)
        | ((hs[offset+3] & 0xff) as u32)
        ) % POWERS_TEN[n - 6];

    format!("{:0>n$}", snum)
}
{% endhighlight %}
{% include end_tab.html%}


# Time-Based One-Time-Password (TOTP)
HOTP is not commonly used, TOTP is much more common (verging on ubiquitous). This is perhaps owing to a lack of synchronisation issues which can arise with HOTP as the server and the client both need to maintain a counter variable or authorisation will fail. As TOTP uses the time-depended moving factor, there is a lesser burden on staying in synchronisation: there is no counter being incremented on success, only a clock which is increasing at the same rate (hopefully) on both client and server.

The TOTP algorithm is a modification of the HOTP algorithm, with a time dependent moving factor and is described in [RFC6238](https://datatracker.ietf.org/doc/html/rfc6238).

This modification is very simple. Rather than using an incrementing counter, the current time (in seconds since 1st Jan 1970: unix time) is used. This is combined with a time start `t0` value, and a time step `x` value to give the adjusted time T:

```
T = (unix_time - t0) / x
```

Just using that `T` moving factor as the counter value in the previous gives you the code we need to authenticate with all your favourite services. Common settings are `t0 = 0` and `x = 30`.

{% include tab_bar.html %}

{% include tabpython.html %}
{% highlight python %}
# my_totp.py
from time import time

from my_hotp import hotp


def topt(k: bytes, t0: int, x: int, n: int, **kwargs) -> str:
    return hotp(k, (int(time()) - t0)//x, n, **kwargs)
{% endhighlight %}
{% include end_tab.html %}

{% include tabrust.html %}
{% highlight rust %}
use std::time::SystemTime;

use crate::hotp::hotp;

pub fn totp(k: Vec<u8>, t0: u64, x: u64, n: usize)-> String {
    let unix_time = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap()
        .as_secs();

    let adjusted_t = (unix_time - t0) / x;

    hotp(k, adjusted_t, n)
}
{% endhighlight %}
{% include end_tab.html%}

However, most services are not super forthcoming with the 'secret' that you need...

# QR Codes
QR codes tend to be the main way you'll link your authentication app with a service.

<center><img src="{{ site.baseurl }}img/auth/qr_example.png" width="50%"/><p>Example QR from: <a href="https://rootprojects.org/authenticator/">rootprojects.org/authenticator</a></p></center>

These QR codes are very easy to use, but hide the data away from us. The QR code contains an `otpauth` URI of the following format:
```
otpauth://<TYPE>/<Issuer>:<Account>?secret=<Secret>&<other arguments>
```
There's the secret we want! But, not quite... Our secret is given as a string of text, but this is not the key itself. It is a base32 encoding of the key. We need to decode it and then we can use it.

{% include tab_bar.html %}

{% include tabpython.html %}
{% highlight python %}
import base64
key_from_uri = 'abcdabcdabcd'
key_bytes = base64.b32decode(key_from_uri)
{% endhighlight %}
{% include end_tab.html %}

{% include tabrust.html %}
{% highlight rust %}
use koibumi_base32 as base32;
let encoded_secret = "abcdabcdabcdabcd";
let decoded_secret = base32::decode(encoded_secret);
{% endhighlight %}
Making use of the <code>koibumi_base32 = "0.0.2"</code> crate.
{% include end_tab.html%}

## Fini! 🎉
And that's the last piece of the puzzle. Our TOTP implementation is complete!


# Conclusions

In this post I've given an overview of the - surprisingly simple - algorithm behind the common "Authenticator" apps. I was blown away by the utility of the RFC memoranda. The documentation (at least for this area) was well written and easy enough to follow. The example code and given test cases made implementation a breeze.

I've given my implementation here in both Python and Rust. This was for me to practice using Rust. It was interesting to see how easy it was to implement in Rust and how much harder working in a dynamically typed language like Python was for a relatively low-level application like this (dealing with bitwise operations).





# Resources
- [How do apps like google and microsoft authenticator work](https://www.ontimetech.com/technology-news/how-do-apps-like-google-and-microsoft-authenticator-work/)
- [Wikipedia: Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator)
- [GitHub: Google Authenticator](https://github.com/google/google-authenticator)
- [RFC2104 - HMAC](https://datatracker.ietf.org/doc/html/rfc2104)
- [RFC4226 - HOTP](https://datatracker.ietf.org/doc/html/rfc4226)
- [RFC6238 - TOTP](https://datatracker.ietf.org/doc/html/rfc6238)