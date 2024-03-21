# Workshop overview

As mentioned on the [Welcome page](https://m-earnest.github.io/docker_workshop/index.html), this workshop will be focused on how to utilize the `Docker` framework to produce and share reproducible, light-weight workflows to facilitate good scientific practice.

We will try to provide folks with a brief overview of why does this is important, central aspects of virtualization, how to work with and manage Docker containers and lastly what a container is made out of, as well as how these are build and published to the web or saved locally.

...

## The framework and setup

The entire workshop will be conducted via the 

The complete workshop will be provided within this [Jupyter Book](https://jupyterbook.org/intro.html) format you're currently looking at, free for everyone to check and try out, as well as utilize further. 

To fully participate in the workshop you'll need a `Bash shell`, here usually referred to as `terminal` and a working `Docker` installation, as outlined in the [Setup for the workshop](https://peerherholz.github.io/docker_workshop/setup.html) section. To help folks that don't have any experience with these resources, we compiled a set of tutorials that participants can go through within the [prerequisite section](https://m-earnest.github.io/docker_workshop/advanced/automating.html). While this won't be enough to go past basic skills, we still hope it will be useful to familiarize yourself with core aspects that will help during the workshop. 


For some sessiosn we will additionally use some files we provide, you can either get them by downloading the [workshop GitHub repository]() or by running the following code in you termina (we'll also discuss what these commands do in the introdcutory session, no worries):

`docker pull aaronreer1/get_workshop_materials:0.0.1`
`docker run -v $(pwd):/output aaronreer1/get_workshop_materials:0.0.1`


## Software containers - Basics
Within the first half of the workshop we will focus on the basics concerning working with `software containers`. In more detail, we will talk about what `software containers` are and have a look at how they `work`, `assessed` and `management`. 

![logo](https://media3.giphy.com/media/2nt2dX21yO0NAaP7BS/giphy.gif?cid=ecf05e47thh4b9tjde2kf9e84ag7i6m3rbbvo1tilt6fjpll&rid=giphy.gif&ct=g)\
<sub><sup><sub><sup>https://media3.giphy.com/media/2nt2dX21yO0NAaP7BS/giphy.gif?cid=ecf05e47thh4b9tjde2kf9e84ag7i6m3rbbvo1tilt6fjpll&rid=giphy.gif&ct=g
</sup></sub></sup></sub>

## Software containers - Advanced aspects
The second session will build upon the things learned during the first and will introduce the workshop participants to the larger `software container ecosystem` and more advanced aspects. Specifically, we will explore how software containers can be created and automated.  

![logo](https://media4.giphy.com/media/3orif0rjs49gsPWg1y/giphy.gif?cid=ecf05e47driaof19nl7irhimygzitnzv7ce6vkl6hua50hg5&rid=giphy.gif&ct=g)\
<sub><sup><sub><sup>https://media4.giphy.com/media/3orif0rjs49gsPWg1y/giphy.gif?cid=ecf05e47driaof19nl7irhimygzitnzv7ce6vkl6hua50hg5&rid=giphy.gif&ct=g
</sup></sub></sup></sub>

## The details


# Software containers in neuroscience research
  

You can checkout the respective sections:

* [An overview](overview.md)

   What's this workshop about and how is it organized?

* [Setup](https://m-earnest.github.io/docker_workshop/setup.html)

   What software do you need and how to get it!

* [General outline](https://m-earnest.github.io/docker_workshop/outline.html)

   Our rough timetable and a short orientation!

* [Prerequisites](https://m-earnest.github.io/docker_workshop/prerequisites.html)

   All things gotta start somewhere and using software containers in neuroscience research are of course no exceptions to that, especially since a certain amount of digital literacy, programming, etc. is required. 
   Here, we gathered some resources folks can check out in preparation for the course or just for fun.

* [Introdcution - Software containers and Virtualization](https://m-earnest.github.io/docker_workshop/basics/introduction.html)


* [Quickstarting your container expertise](https://m-earnest.github.io/docker_workshop/basics/quickstart.html)

* [Management of software containers](https://m-earnest.github.io/docker_workshop/advanced/management.html)

* [Creating software containers](https://m-earnest.github.io/docker_workshop/advanced/management.html)

* [Software containers & data](https://m-earnest.github.io/docker_workshop/advanced/data.html)

* [Creating your own software container](https://m-earnest.github.io/docker_workshop/advanced/creating_your_own.html)

* [Automating software containers](https://m-earnest.github.io/docker_workshop/advanced/automating.html)

* [Code of Conduct](https://m-earnest.github.io/docker_workshop/CoC.html)

   Necessities for creating an open, fair, safe and inclusive learning
   experience. Please go thorugh this before the workshop and adhere to general professional standards!