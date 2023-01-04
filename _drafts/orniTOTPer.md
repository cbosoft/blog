---
project: "Ornithopter 🪶"
elevator_pitch: "A low-security MacOS implementation of the TOTP protocol for MFA with laziness and ease of use in mind."
technologies: "Rust"
repo: "github.com/cbosoft/ornitotper"
layout: projectpage
tags: software-dev projects
status: Alpha
has_diagrams: true
---

<div class="colourbox"><i class="fa fa-info-circle"></i> <b>This project is an unsecure toy and should not be used by <i>anyone</i>.</b></div>

# Motivation
Multi-Factor Authentication (MFA) seems like a great idea, but in instances where you need to input a OTP code frequently then unlocking your phone, opening the Authenticator app, and copying the code (perhaps manually, perhaps via shared clipboard) can be exceedingly tedious.

A desktop MFA Authentication app is a terrible, *terrible*, ***terrible*** idea from a security perspective. It turns what is a relatively ok second factor into a really quite poor second factor. (I'm not even sure if it still counts as a second factor - it's on the same device!) It is for this reason I have the disclaimer/banner at the top.

All that said, I thought this could be useful for accounts for which security is not a concern but for whatever reason MFA is required.

# Specification
The resulting application from this project is an implementation of the TOTP protocol ([RFC6238](https://datatracker.ietf.org/doc/html/rfc6238)) for the desktop.

The application must:
- be exceedingly easy to use (i.e. one-click to obtain OTP),
- preferably have OTP delivered straight to clipboard,
- (optionally) be able to work with multiple accounts, and
- (optionally) have a secure method of storing application data (e.g. secret keys for MFA accounts)

# Development Challenges
## TOTP Algorithm
The first real challenge was finding out about and then implementing the MFA algorithm itself. This turned out to be a relatively easy and fun task - I wrote about it [here]({% post_url 2022-06-07-impl-mfa-auth %}).

## Serialisation
- serde json

## MacOS Clipboard interop
- https://github.com/aweinstock314/rust-clipboard

## Structuring the bundle for dual CLI and GUI operation?
- https://developer.apple.com/documentation/appkit/nsapplicationdelegate/1428564-applicationdockmenu
- https://stackoverflow.com/questions/33681565/how-can-i-add-a-menu-to-the-application-in-the-dock
- https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/LoadingResources/CocoaNibs/CocoaNibs.html#//apple_ref/doc/uid/10000051i-CH4
- https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html#//apple_ref/doc/uid/10000123i-CH101-SW1

## Secure storage of secret
- https://github.com/hwchen/keyring-rs

# Conclusion

# Spec Check
The application must
- [ ] be exceedingly easy to use (i.e. one-click to obtain OTP)
- [ ] preferably have OTP delivered straight to clipboard,
- [ ] (optionally) be able to work with multiple accounts, and
- [ ] (optionally) have a secure method of storing application data (e.g. secret keys for MFA accounts)


Here is one mermaid diagram:
<div class="mermaid" id="centre">
graph TD 
A[Client] --> B[Load Balancer] 
B --> C[Server1]
B --> D[Server2]
</div>