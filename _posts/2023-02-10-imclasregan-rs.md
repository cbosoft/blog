---
project: "ImClasRegAn"
elevator_pitch: "Image classification and regression annotation tool."
repo: "github.com/cbosoft/imclasregan"
layout: projectpage
tags: software-dev projects Rust
status: Alpha
---

# Motivation
As laid out in [another post]({% post_url 2023-02-09-gamifying-image-annotation %}), I'm interesting in making the task of annotating images easier. This led me to develop a [small tool](https://github.com/cbosoft/trusty_patches) which started out as a web app, but through some iffy choices ended up as a desktop app. A web app would enable sharing to a wider audience and thus allow crowd sourcing annotation. I redesigned the tool as a [web app (python backend)](https://github.com/cbosoft/imclasregan/tree/python-backend) and all was well. Until it wasn't. I hadn't designed the backend well and ended up facing locking very frequently. I can't imagine what it would end up like if even ten people tried to use it concurrently. Seeking performance, I re-wrote it in rust. This resulted in the project as presented here.

# Specification
The web app should:
 - Allow users to quickly assign labels to images
 - Operate with a minimum of user interaction
 - Scale to many concurrent users (on the order of 100)

# Swapping from Python 🐍 to Rust 🦀
## Web Framework
In Python, I used the `http` module's server implementation, subclassing `SimpleHTTPRequestHandler` and implementing the methods I require (just the `do_POST` method, really). In Rust, a quick google search returned a recommendation for [`Rocket`](https://rocket.rs), a web framework promising speed and security without comprimising flexibility. Sounds good. [Let's take a look (v0.5)](https://rocket.rs/v0.5-rc/guide/getting-started/):

{% highlight rust %}
#[macro_use] extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index])
}
{% endhighlight %}

And that's all it takes to get started? Cool! This app returns "hello, world!" no matter the request, not the most useful. The way rocket works, you register handler functionss which match request types and paths (see the `get` macro in the above). To match the Python `http.SimpleHTTPRequestHandler`, the app needs to serve files its asked for. Turns out, this is pretty [easy](https://rocket.rs/v0.5-rc/guide/requests/):

{% highlight rust %}
#[macro_use] extern crate rocket;

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", FileServer::from("/"))
}
{% endhighlight %}

Adding in handlers for the various commands sent from the front end can be done like so:

{% highlight rust %}
#[macro_use] extern crate rocket;

use rocket::serde::Deserialize;
use rocket::serde::json::Json;

#[derive(Deserialize)]
#[serde(crate = "rocket::serde")]
struct Foo {
    bar: i64
}

#[post("/", data="<foo>")]
fn cmd_handler(foo: Json<Foo>) -> String {
    format!("got {:?}", foo)
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", FileServer::from("/"))
        .mount("/", routes![cmd_handler])
}
{% endhighlight %}

## Database Interop
I ended up going with SQLite for choice of database. Python comes with the `sqlite3` module. In Rust, there are options: [`SQLx`](https://crates.io/crates/sqlx), [`Diesel`](https://crates.io/crates/diesel), [`sqlite`](https://crates.io/crates/sqlite). My use case is pretty simple, I don't need the query checking of `SQLx` or an ORM like `Diesel`. The simplicity of `sqlite` suits me for this use case.

## Frontend
The frontend is unchanged coming from the python version. The HTML is pretty minimal, just some `div`s and a a `canvas`. Some javascript is used to request images from the server and show them to the user. In particular, we need to take an image (sent by server via `json`) and display it on the `canvas`.

Simple HTML page:
{% highlight html %}
<!-- classification.html (simplified) -->
<html>
  <head>
    <script type="text/javascript" src="classification.js"> </script>
  </head>
  <body onload="init()">
    <center>
      <canvas id="image"></canvas>
    </center>
  </body>
</html>
{% endhighlight %}

And the corresponding javascript:
{% highlight js %}
// classification.js (simplified)

function init() {
    get_image();
}

function send_data(o) {
    return fetch('/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(o)
    });
}

function get_image() {
    var canvas = document.getElementById("image");
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    state.iid = null;
    send_data({ command: "GetImage" })
        .then(response => response.json())
        .then(set_image_on_doc);
}

function set_image_on_doc(data) {
    var imagedata = new ImageData(new Uint8ClampedArray(data.data), data.width, data.height);
    state.iid = data.iid;
    state.start_time = Date.now();
    var aspect_ratio = data.width / data.height;
    var big_height = 300.0;
    var big_width = big_height * aspect_ratio;
    var options = {
        resizeWidth: big_width,
        resizeHeight: big_height,
        resizeQuality: "high"
    };
    createImageBitmap(imagedata, options).then(bitmap => {
        var canvas = document.getElementById("image");
        var ctx = canvas.getContext('2d');
        canvas.width = bitmap.width;
        canvas.height = bitmap.height;
        ctx.drawImage(bitmap, 0, 0);
    });
}
{% endhighlight %}

When the page loads, a POST request is made of the server asking for an image. When the server replies, the image data is processed to form an `ImageBitmap` (via `ImageData` and `Uint8ClampedArray`). The `ImageBitmap` is resized from the original to fit the height of the canvas (300px). The resized bitmap is display on the canvas.

# Conclusion
I was initially hesitant to learn a new framework to develop this web app - so I started in Python. However, this was *very* easy. There was a small learning curve, and the troubleshooting was mostly finalised in the python prototype. The fact that the web app architecture allows the front- and backends to be completely separate definitely made the transition easier. I don't normally write web apps, I tend to stick with desktop apps. This experience may have changed my mind! 

# Future Directions
The database backend, SQLite, is not [particularly scaleable](https://stackoverflow.com/questions/54998/how-scalable-is-sqlite). When a user visits the site, they're served an image (no insert) and when they perform a classification, the result is added to the server (insert). An insert for SQLite entails locking the database. The insert itself should take very little time, the data being added are only a couple `int`s and a `str`. However, if the app grows larger, then a more scaleable database backend should be used. I've had good success with `PostgreSQL` in previous projects.

# Spec Check
Does the app:
 - [x] Allow users to quickly assign labels to images
 - [x] Operate with a minimum of user interaction
 - [x] Scale to many concurrent users **(on the order of 100)**

See note above about scaling for larger user counts.