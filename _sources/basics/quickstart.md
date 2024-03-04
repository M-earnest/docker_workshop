# Quickstarting your container expertise


### Learning objectives

- basic docker usage
- docker commands
- mounting paths

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)
- minimal understanding of BASH, i.e. primarily the `pwd`, `ls`  and `cd` commands. (Check the _refresher section_ [link](link) to catch up!)


## Outline

1. Introduction
2. Quickstart

### Where is Docker?


- either start [Docker Desktop](https://docs.docker.com/desktop/use-desktop/) GUI (Graphical User Interface)
- or simply via Command-line Interface aka the UNIX Shell.
    -  this is also what we'll be focussing on in this workshop

-- export path?

#### Getting started

- on unix based OS (e.g., Ubuntu, Mac OSX) open a terminal, type `docker` (hit enter)
- on ?windows? open docker toolbox or engine (depending on your specific OS) and type `docker` (hit enter)

    - you should be presented with the the following docker manual, providing information on common Docker commands


```
(base) Michaels-MacBook-Pro:~ me$ docker

Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
  run         Create and run a new container from an image
  exec        Execute a command in a running container
  ps          List containers
  build       Build an image from a Dockerfile
  pull        Download an image from a registry
  push        Upload an image to a registry
  images      List images
  login       Log in to a registry
  logout      Log out from a registry
  search      Search Docker Hub for images
  version     Show the Docker version information
  info        Display system-wide information

Management Commands:
  builder     Manage builds
  checkpoint  Manage checkpoints
  container   Manage containers
  context     Manage contexts
  image       Manage images
  manifest    Manage Docker image manifests and manifest lists
  network     Manage networks
  plugin      Manage plugins
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Swarm Commands:
  config      Manage Swarm configs
  node        Manage Swarm nodes
  secret      Manage Swarm secrets
  service     Manage Swarm services
  stack       Manage Swarm stacks
  swarm       Manage Swarm

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes

Invalid Plugins:
  buildx      failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-buildx: no such file or directory
  compose     failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-compose: no such file or directory
  dev         failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-dev: no such file or directory
  extension   failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-extension: no such file or directory
  init        failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-init: no such file or directory
  sbom        failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-sbom: no such file or directory
  scan        failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-scan: no such file or directory
  scout       failed to fetch metadata: fork/exec /Users/me/.docker/cli-plugins/docker-scout: no such file or directory

Global Options:
      --config string      Location of client config files (default "/Users/me/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var and default context set with "docker context use")
  -D, --debug              Enable debug mode
  -H, --host list          Daemon socket to connect to
  -l, --log-level string   Set the logging level ("debug", "info", "warn", "error", "fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/Users/me/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/Users/me/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/Users/me/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Run 'docker COMMAND --help' for more information on a command.

For more help on how to use Docker, head to https://docs.docker.com/go/guides/

```

You can test if your Docker installation was successful by running:

  `docker run hello-world`

If you get the following output you're good to go:

````
(base) Michaels-MacBook-Pro:~ me$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

````


### So what did we just do? The RUN command

the command: `docker run hello-world`

1. tells docker to run or execute the _container_ or _image_ `hello-world`
2. if the wanted container is not already on your machine, docker automatically searches for and downloads it
3. docker run then runs or executes the given container doing whatever the container is supposed to do



### Where do docker containers come from ?

In most cases, docker containers are stored online on and downloaded from [Docker Hub](https://hub.docker.com/), an extensive online repository, where On folks can upload and store as many docker containers as they want for free, only requirement: a [Docker ID](https://docs.docker.com/docker-id/)

- your Docker ID is the Username that you choose when signing up for Docker Hub, if you want to connect your local Docker to Docker Hub you can run:
  `Docker login`

  - following you will be asked to provide your username and password

```

(base) Michaels-MacBook-Pro:~ me$ docker login
Log in with your Docker ID or email address to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com/ to create one.
You can log in with your password or a Personal Access Token (PAT). Using a limited-scope PAT grants better security and is required for organizations using SSO. Learn more at https://docs.docker.com/go/access-tokens/

Username: your_username
Password: 
Login Succeeded

```

Once you're logged in your build and tagged docker images can be pushed to the docker hub via the command line:
  `docker push your-cool-image`
  
- additionally, it is possible to automatically build a container from a GitHub repository after pushing commits to a respective repo (note: both methods will be covered during the afternoon sessions)

- image????


### Docker commands 101 - in depth

Now let's further explore docker commands within a typical workflow.

At first, we want to download a certain docker container to work with, for the sake of simplicity and time we're going to use the classic Ubuntu container (also alwyas a great way to start, when designing a new container that is dependent on it's own OS).

#### Docker commands 101 - pull

Instead of automatically downloading the container via docker run, we use the respective docker command docker pull image name, hence

`docker pull ubuntu`

```
Using default tag: latest
latest: Pulling from library/ubuntu
Digest: sha256:f9d633ff6640178c2d0525017174a688e2c1aef28f0a0130b26bd5554491f0da
Status: Image is up to date for ubuntu:latest
docker.io/library/ubuntu:latest
  
```

As you can see, we downloaded all _layers_ that are needed to build the classic Ubuntu docker container, with the message Status: 

```
Downloaded newer image for ubuntu:latest showing you that everything worked
```

Super important: by default, docker pull always searches and downloads the container that is tagged with `latest`, hence if you want to have a certain version (e.g., an older release or developer) it is necessary to indicate the respective tag:

#### Docker commands 101 - run

Now if we want to work with our newly downloaded docker container, we can simply run/execute it via:

`docker run ubuntu`

Which should result in:

```

(base) Michaels-MacBook-Pro:~ me$ docker run ubuntu
(base) Michaels-MacBook-Pro:~ me$ 

```

- docker used run, nothing happend? all the fuzz for that?

Correct, as each docker container is build for reason and purpose, hence what happens when you run a given docker container depends (more or less) exclusively on its setup and definition.

The Ubuntu docker container may contain a complete Ubuntu installation, but has not no defined `magic`, that is functionality/commands that are automatically executed when running (note: more on that during the afternoon sessions). It is therefore extremely important to consult the readme or docs of a given docker container before using it.

Let's say we consulted the Ubuntu container documentation and found out that it is possible to make use of the `contained Bash Shell` by simply integrating Bash commands into our `run` command. Try the following:

  `docker run ubuntu echo "hello from your container"`

Which should give you the output message: `hello from your container`

This is neat (although redundant), but cumbersome if we want to use more complex commands. After consulting the documentation again we try the following command to give us a bit more flexibility:

We can utilizes a given docker container in an _interactive_ fashion by including the `--it` flag in the the docker run command:

`docker run -it ubuntu bash`

Here, we also tell the ubuntu docker container to start/enter the bash shell.

Now we can explore the interactive Ubuntu environment, e.g.:

```

(base) Michaels-MacBook-Pro:~ me$ docker run -it ubuntu bash
root@806c74068242:/# echo $SHELL 
/bin/bash
root@806c74068242:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@806c74068242:/# 

```

As we can see the container is in fact simulating a complete Ubuntu file system.

Inside the ubuntu docker container we can utilize the functionality from the ubuntu OS and exit the container by typing `exit`

```
root@806c74068242:/# exit
exit
(base) Michaels-MacBook-Pro:~ me$ 

```

Depending on a given container's architecture and definition, it should remove itself from running instances when exiting. 
However it's worth to ensure that and check which instance are currently running when you notice e.g., a drop in perfomance (note: more on docker management in the next session).

This can easily be done by:

`docker ps`

Or by checking under `containers` in the Docker Dekstop GUI.

In order to ensure that a given docker container is removed from running instances after exiting, the --rm flag can be included in the docker run command:

`docker run -it --rm ubuntu bash`

It's important to note that unless explicitly specified, creating, modifying and deleting files in a container reuslts in neither permanent nor saved changes, as this is against the encapsulation and reproducibility idea.

We can verify this by running the following commands in our container:

```

(base) Michaels-MacBook-Pro:~ me$ docker run -it --rm ubuntu bash
root@3efa79a80611:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@3efa79a80611:/# mkdir test
root@3efa79a80611:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  test  tmp  usr  var
root@3efa79a80611:/# exit
exit

(base) Michaels-MacBook-Pro:~ me$ docker run -it --rm ubuntu bash
root@9bc5ba4cf999:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

```

Furthermore, we cannot interact with data stored on our host or somewhere outside the docker container.

In order to address both problems, we need to `mount` paths

#### Docker commands 101 - mount

`Mounting` describes a mapping from paths outside the docker container to paths inside the docker container.

This is achieved through the `-v` flag within the `docker run` command and utilized as follows: 

`-v path/outside/container:/path/inside/container`

So to make our systems /Desktop available inside the docker container as a folder called `/data` within the ubuntu container we run:

`docker run -it --rm -v /Users/peerherholz/Desktop:/data ubuntu bash`

Which gives us:

```

(base) Michaels-MacBook-Pro:~ me$ docker run -it --rm -v /Users/me/Desktop:/data ubuntu bash
root@8f5c051b6904:/# ls
bin  boot  data  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@8f5c051b6904:/# cd data
root@8f5c051b6904:/data# ls
docker_mne  rand  sub-01  sub-02  sub-03  sub-04  sub-05
root@8f5c051b6904:/data# mkdir test_object_permanence
root@8f5c051b6904:/data# ls
docker_mne  rand  sub-01  sub-02  sub-03  sub-04  sub-05  test_object_permanence

```

And to verify that we actually created a _permanent_ folder  (let's call it `test_object_permanence`) on our system:

```
root@8f5c051b6904:/data# exit 
exit
(base) Michaels-MacBook-Pro:~ me$ cd Desktop/
(base) Michaels-MacBook-Pro:Desktop me$ ls
docker_mne		rand			sub-01			sub-02			sub-03			sub-04			sub-05			test_object_permanence

```

Great, at least we created something permanent for once!

Most of the time, it's a good idea to indicate absolute paths on the host system. In our example the directory `/data` didn't exist in the Ubunutu container before mounting it, hence it was created automatically, however this is also depends on the docker container and it's setup/definition at hand as e.g. within automated functionality a certain directory is expected.

`As per usual`: check the readme and/or docs of a given docker container!

Further, we can mount as many directories and files as you want, indicating each with a -v flag, for example we could map an input and an output directory wrt preprocessing/analyzing data:

docker run -it --rm 
-v /Users/me/Desktop:/input:ro 
-v /Users/me/Desktop/analyses:/output 
ubuntu bash

```
(base) Michaels-MacBook-Pro:Desktop me$ docker run -it --rm -v /Users/me/Desktop:/input:ro -v /Users/me/Desktop/analyses:/output ubuntu bash


root@97917588b533:/# 
root@97917588b533:/# ls
bin  boot  dev  etc  home  input  lib  media  mnt  opt  output  proc  root  run  sbin  srv  sys  tmp  usr  var
root@97917588b533:/# ls input
analyses  docker_mne  rand  sub-01  sub-02  sub-03  sub-04  sub-05  test_object_permanence

```

And again to verify:

```

root@97917588b533:/# exit
exit
(base) Michaels-MacBook-Pro:Desktop me$ ls
analyses		rand			sub-02			sub-04			test_object_permanence
docker_mne		sub-01			sub-03			sub-05

```

Again, check the readme and/or docs of the docker container at hand if some paths and/or files are expected and if the paths are generated automatically.


### Docker commands 101 - excerices

To solidfy what we've learned in this session, please try the following excercises:


- pull the neurodebian docker container in its nd-non-free version
- mount your Desktop to data and create a directory namend docker_is_fun
- within it, create a .txt named i_like_docker.txt
- exit the container
- run the container again, this time mounting the newly created docker_is_fun as read-only to /input, as well as an directory docker_is_love as output within the same host directory
- copy the i_like_docker.txt from the input to the output directory



### Summary - Docker 101

- [Docker Hub]() -- repositories to share Docker images

- basic image usage:
```

    # Download docker container 'ubuntu'
    docker pull ubuntu
    # Run installed docker container
    docker run ubuntu
    # Run installed docker container interactively
    docker run -it ubuntu
    # Run installed docker container interactively, removing it after exiting
    docker run -it --rm ubuntu
    # Run installed docker container interactively, removing it after exiting,
    # mounting paths
    docker run -it --rm -v /path/on/host:/path/within/container ubuntu
```







