---
title: "Paging Dr. Docker: HTTP communication between containers"
layout: post
excerpt: "Want to containerise your tests? Watch out!"
tags: software-dev how-i-fixed
---

# I'm building a web app.
As many people do.

The app is structured across two containers: a database and server. The server both works as site server and as API for running analysis of *stuff*. The web app takes input from the user via the site and runs analysis via the API. (I feel like the analysis APIt should be carved off into its own container separate from the website, but I'm keeping it simple here.) I've got a mock up of the frontend done. I've started the put together the backend, but I want to follow some good ole Test Driven Development (TDD).

I added a container of tests to my app and... encountered a problem.

# The problem
Whenever I tried to make a server request from the test container, the connection failed.

```
test-container # curl http://server:8080
...
curl: (7) Failed to connect to server port 8080 after 5 ms: Couldn't connect to server
```

Odd! Maybe there's something up with my docker network setup?

```
test-container # ping server
PING server (172.28.0.3): 56 data bytes
64 bytes from 172.28.0.3: seq=0 ttl=64 time=0.161 ms
...
```

Nah, no worries there. The server name is resolved to its docker IP fine, and I get a reply pong from my ping. So the server is findable, but something goes wrong when I try to make a request on port 8080.

To get more information, I checked out the connection to the other container, `db`, my PostgreSQL database.

```
test-container # ping server
PING server (172.28.0.2): 56 data bytes
64 bytes from 172.28.0.2: seq=0 ttl=64 time=0.131 ms
...
```

As expected, no issues pinging it. Then GET on the database app port?

```
test-container # curl http://db:5432
curl: (52) Empty reply from server
```

No issues using `curl` to run a GET request. This gave me some ideas. So the `db` container is responsive on its port, but `server` is not. **There's something specific about the set up of the server container that's causing the issue.**

### What's different about the configuration of the two containers?

`db` is the docker provided PostgreSQL image, on port 5432. `server` is my custom image, based on alpine, running off port 8080 and bound to host at 8080.

Only difference I can see with regards to networking is the port binding. Is that causing issues?

I can't see any mention of potential issues on the [docker-compose docs](https://docs.docker.com/compose/compose-file/06-networks/), or the [docker networking docs](https://docs.docker.com/network/), or in a [general web search](https://www.google.com/search?q=docker+access+bound+port+from+another+container). Should this be a problem? Maybe there's something fundamental I'm not getting about port binding. I'd imagined it worked like port forwarding, so requests to localhost:8080 would be passed on to server:8080 within the docker network. It seems more in depth than that!

Running curl from the host machine answers my question though.
```
host-machine # curl localhost:8080
<!DOCTYPE html>
<html>
  ...
</html>
```
Making requests of the server from the host works perfectly fine. The server is running and was set up ok, it just couldn't see any requests from the test container.

# The solutions
So if I can't access my server on the bound port from within the docker network, I could
  1. move my test image onto the host network,
  2. move my tests out from the container,  or
  3. don't bind the server port during testing.

I opted for #2.

There wasn't any real need for my tests to be containerised, so not unhappy about this. In fact, moving my tests outside of a container makes them easier to run (can just run the tests, don't need to build the image, start the container, and attach to the relevant network). If I do change my mind in future, if it seems like containerisation would be a real advantage for testing, I'll go back to option 1.

Bright side: one fewer Dockerfile to worry about!
