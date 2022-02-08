---
title: "Packaging apps on MacOS."
layout: post
excerpt: "I'm developing an app and need to package it so it can be shared, here's what I've learned about packaging Windows and mac apps."
tags: software-dev
---

# The App

I'm developing a `C++` application using `cmake` as my build system to facilitate cross-platform development. Cross platform? Cross platform! I need to target both MacOS and Windows. `cmake` has made development between these two platforms really easy. I use [CLion](https://www.jetbrains.com/clion/) as my IDE because its completion engine is reasonably fast, mostly unobtrusive, and often useful.

In the past, I've found Windows to be horrid to develop on due to the pains of getting libraries to find each other in development, however packaging seems to be the area in which Windows excels. I had no issue running the app by copying the .exe to another folder, along with the required .dlls, and then double-clicking.

MacOS though? There's a problem... 

# The Problem

As a unix-like OS I had thought this would be easy. Apps in MacOS are actually special directories called [Bundles](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html#//apple_ref/doc/uid/10000123i-CH101-SW13). These directories have a '.app' extension and a structure recognised by MacOS to be a runnable app. The structure of a bundle is given below:

```yaml
MyApp.app:
  - Contents:
    - Info.plist
    - MacOS:
      - <excutable>
    - Resources:
      - <images, sounds, etc required by app>
    - Frameworks:
      - <libraries required by app>
```

The structure contains a location in which libraries should be placed - grand! That's all we need to do then, right? Not so much.

Development is easy (to begin with) on linux and MacOS as they have ([official](https://wiki.archlinux.org/title/pacman) and [unofficial](https://brew.sh)) package managers that don't suck (unlike Windows - sorry [chocolatey](https://chocolatey.org)). These package managers download libraries and put them in the right place for it to be found - great! But what happens when an app is deployed to a system which lacks these libraries? Or has different versions installed? (Unix) executable binaries contain hints to the OS as to where to find the required libraries. We can see this with `otool`:

```bash
$ otool -L /usr/bin/python3
/usr/bin/python3:
	/usr/lib/libxcselect.dylib (compatibility version 1.0.0, current version 1.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1311.100.2)
```

The above output shows what `python3` links with. In this case, it links to system libraries. This is fine, copying this executable to another computer running the same version of MacOS should give no issues. However this is not always the case.

Another example (fictional app):

```bash
$ otool -L an_app
an_app:
	...
	/usr/local/lib/libGLEW.2.2.0.dylib (compatibility version 2.2.0, current version 2.2.0)
	...
	/usr/local/opt/libtorch/lib/libc10.dylib (compatibility version 0.0.0, current version 0.0.0)
	...
	@rpath/QtPrintSupport.framework/Versions/A/QtPrintSupport (compatibility version 6.0.0, current version 6.1.3)
	...
	@executable_path/../Frameworks/libopencv_core.4.5.dylib (compatibility version 4.5.0, current version 4.5.4)
```

This example shows a couple problems and a **solution**. Problems: (1) GLEW is not a system lib and neither is opencv - these may not be installed, or the wrong versions may be installed. (2) a lib was linked in a non-standard location and is specified by a run-time search path ([rpath](https://en.wikipedia.org/wiki/Rpath)). However, the last line gives us a solution...

# The Solution
Embedded libraries can be specified in a path relative to the executable! So to create a portable app, we just need to change these embedded library names to ones relative to the executable!

So that's all we need to do then, change the embedded library names from absolute, system dependent-ones, to ones relative to the executable.

Magically, there's another tool for this - `install_name_tool`:

```bash
$ install_name_tool -change OLD NEW EXE
```

*e.g.*

```bash
$ install_name_tool \
    -change "@rpath/QtPrintSupport.framework/Versions/A/QtPrintSupport" \
    "@executable_path/../Frameworks/QtPrintSupport.framework/Versions/A/QtPrintSupport" \
    an_app
```

Doing this for all of the non-system files should result in an executable that doesn't look outside its bundle for libraries - we have achieved portability!

Another useful tool is `macdeployqt` provided by Qt, which copies Qt libraries and plugins into the app bundle (however, it doesn't always do the best job in my experience). Further information on Qt deployment is in their [excellent article](https://doc.qt.io/qt-5/macos-deployment.html) on the topic.

Once the App Bundle is prepared, you might want to create a compressed "installer image" for it. There are [numerous tools](https://stackoverflow.com/questions/96882/how-do-i-create-a-nice-looking-dmg-for-mac-os-x-using-command-line-tools) for this:
- [create-dmg](https://github.com/create-dmg/create-dmg)
- [node-appdmg](https://github.com/LinusU/node-appdmg)
- [dropdmg](https://c-command.com/dropdmg/)
- [dmgbuild](https://pypi.org/project/dmgbuild/)

(I've been using `create-dmg`.)

For the most control over the installer, the dmg should probably be created manually (see [here](https://stackoverflow.com/a/97025) or [here](https://stackoverflow.com/a/20879598))