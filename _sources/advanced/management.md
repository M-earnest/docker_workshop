# Management of software containers

### Learning objectives

- basic docker management
- docker commands
- resource management

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)
- minimal understanding of BASH, i.e. primarily the `pwd`, `ls`  and `cd` commands. (Check the _refresher section_ [link](link) to catch up!)


#### How's docker configured?

The setup and configuration of a given docker installation is rather complex and characterized by a myriad of factors and settings: storage, RAM, swap, CPU, proxy, etc. ...
    
You should be aware of how the docker installation you're using is setup and configured at any given time, as otherwise perfectly working docker containers fail to function properly
as usual, consider the readme and/or docs of a given docker container before using it

We can get a comprehensive overview of our docker setup and configuration via the docker command:

    `docker info`

Which should produce something like the followin output:

```

(base) Michaels-MBP:Desktop me$ docker info
Client:
 Version:    24.0.6
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.11.2-desktop.5
    Path:     /Users/me/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.23.0-desktop.1
    Path:     /Users/me/.docker/cli-plugins/docker-compose
  dev: Docker Dev Environments (Docker Inc.)
    Version:  v0.1.0
    Path:     /Users/me/.docker/cli-plugins/docker-dev
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.20
    Path:     /Users/me/.docker/cli-plugins/docker-extension
  init: Creates Docker-related starter files for your project (Docker Inc.)
    Version:  v0.1.0-beta.9
    Path:     /Users/me/.docker/cli-plugins/docker-init
  sbom: View the packaged-based Software Bill Of Materials (SBOM) for an image (Anchore Inc.)
    Version:  0.6.0
    Path:     /Users/me/.docker/cli-plugins/docker-sbom
  scan: Docker Scan (Docker Inc.)
    Version:  v0.26.0
    Path:     /Users/me/.docker/cli-plugins/docker-scan
  scout: Docker Scout (Docker Inc.)
    Version:  v1.0.9
    Path:     /Users/me/.docker/cli-plugins/docker-scout

Server:
 Containers: 14
  Running: 0
  Paused: 0
  Stopped: 14
 Images: 9
 Server Version: 24.0.6
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 8165feabfdfe38c65b599c4993d227328c231fca
 runc version: v1.1.8-0-g82f18fe
 init version: de40ad0
 Security Options:
  seccomp
   Profile: unconfined
  cgroupns
 Kernel Version: 6.4.16-linuxkit
 Operating System: Docker Desktop
 OSType: linux
 Architecture: aarch64
 CPUs: 10
 Total Memory: 7.661GiB
 Name: linuxkit-9a0b4d61aa6b
 ID: 601c4efb-57ee-48fc-a551-5f501a24c3cf
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 HTTP Proxy: http.docker.internal:3128
 HTTPS Proxy: http.docker.internal:3128
 No Proxy: hubproxy.docker.internal
 Experimental: false
 Insecure Registries:
  hubproxy.docker.internal:5555
  127.0.0.0/8
 Live Restore Enabled: false

WARNING: daemon is not using the default seccomp profile
```
<br>

Among this barrage of information, we can see that docker uses a default amount of RAM, CPUs, etc.

- all of these parameters can be set and configured within the docker run command and the respective flags for a specific container,
  - e.g. we can set the RAM  afforded to our previously pulled Ubuntu Container by using the following flags --memory RAM in mb or gb, e.g. --memory 4gb

      `docker run -it --rm --memory 4gb ubuntu`

- set swap using --memory-swap in mb ir gb, e.g. --memory-swap 5gb

    `docker run -it --rm --memory 4gb --memory-swap 5gb ubuntu`

- set CPUs using --cpus CPUs as int, e.g. --cpus 2

    `docker run -it --rm --memory 4gb --memory-swap 5gb --cpus 2 ubuntu`

- Configuration of your Docker installation and specific containers can also be achived via the Docker Desktop GUI
    - see under settings ->  Resources or Advanced
    - find OS specific instructions on the [Docker Website](https://docs.docker.com/desktop/settings/mac/)


#### !! Docker configuration Slide 18 !!
- have to check what Docker-machine is for this part

```


    or the command line (in every OS)

    completey reset and create new default

    docker-machine stop default
    docker-machine rm default
    docker-machine create -d virtualbox --virtualbox-memory=4096 \
    --virtualbox-cpu-count=2 --virtualbox-disk-size=50000 default

    modify existing default

    docker-machine stop default
    VBoxManage modifyvm default --memory 4096
    docker-machine start default
```

<br>

#### Resource management

To get a list of available docker containers using docker `images` use:

    `docker images``

```
(base) Michaels-MBP:Desktop me$ docker images
REPOSITORY             TAG       IMAGE ID       CREATED        SIZE
mycondaenv             latest    9b5e5d553c14   2 days ago     2.07GB
ubuntu                 latest    a50ab9f16797   5 days ago     69.2MB
repronim/neurodocker   latest    1107707d9d51   9 months ago   79.7MB
hello-world            latest    ee301c921b8a   9 months ago   9.14kB
```
<br>
<br>

The docker `ps` command comparatively lists all _running_ `containers`

    `docker ps`

This is worth checking, if you notice a drop in performance during computation, can't connect to certain ports when using jupyter notebooks, get a memory related error, etc.

To get a list of _all_ `containers` use the `-a` flag

    `docker ps -a`

```

(base) Michaels-MBP:Desktop me$ docker ps -a
CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS                    PORTS     NAMES
92ba07352f3a   ubuntu                        "echo 'hello from yo…"   42 hours ago   Exited (0) 42 hours ago             agitated_ride
eaa9ac8ecad1   ubuntu                        "/bin/bash"              42 hours ago   Exited (0) 42 hours ago             unruffled_galileo
f0e40b0a0568   mycondaenv                    "jupyter lab --ip='0…"   2 days ago     Exited (0) 2 days ago               sad_elion
bd55e08682e5   3a7473239b05                  "jupyter lab --ip='0…"   2 days ago     Exited (0) 2 days ago               ecstatic_hermann
16350378187e   repronim/neurodocker:latest   "neurodocker generat…"   4 weeks ago    Exited (1) 4 weeks ago              frosty_fermat
0228440b6b2f   repronim/neurodocker:latest   "neurodocker generat…"   4 weeks ago    Exited (1) 4 weeks ago              charming_ganguly
eba0b7f9580e   hello-world                   "/hello"                 4 weeks ago    Exited (0) 4 weeks ago              romantic_galois

```

<br>

#### Stop/Delete/Rename Containers

Docker containers can also be stopped manually using the docker `stop` command:

`docker stop image-id`



And to delete a given docker container use the `remove` command `rm` and provide a `container-id`

    `docker rm container-id`

```
(base) Michaels-MBP:Desktop me$ docker rm 92ba07352f3a
92ba07352f3a

```

As we can see the output isn't very informative, it just mirrors the provided Container ID as confirmation. So let's check if we've managed to remove the respective Ubuntu Container:

```

(base) Michaels-MBP:Desktop me$ docker ps -a

CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS                    PORTS     NAMES
eaa9ac8ecad1   ubuntu                        "/bin/bash"              42 hours ago   Exited (0) 42 hours ago             unruffled_galileo
684e37f2c347   hello-world                   "/hello"                 42 hours ago   Exited (0) 42 hours ago             jolly_villani
f0e40b0a0568   mycondaenv                    "jupyter lab --ip='0…"   2 days ago     Exited (0) 2 days ago               sad_elion
bd55e08682e5   3a7473239b05                  "jupyter lab --ip='0…"   2 days ago     Exited (0) 2 days ago               ecstatic_hermann
16350378187e   repronim/neurodocker:latest   "neurodocker generat…"   4 weeks ago    Exited (1) 4 weeks ago              frosty_fermat
0228440b6b2f   repronim/neurodocker:latest   "neurodocker generat…"   4 weeks ago    Exited (1) 4 weeks ago              charming_ganguly
eba0b7f9580e   hello-world                   "/hello"                 4 weeks ago    Exited (0) 4 weeks ago              romantic_galois

```


Using the the `--rm` flag when running a container should prevent that a container keeps running in the background after executing the relevant commands or exiting the environment however, some containers may rely on different implementations and keep running in the background.

`By now our evergreen: check the readme and/or docs of a given docker container!`

We can further use the associated tag related behavior to "rename" a given docker container in order to prevent unwanted deletions or problems with regard to version control using the tag command:

`docker tag old-container-name/container-id:tag new-container-name/container-id:tag`


```

Output

```


#### Import/Export

Besides using Docker Hub to share and download docker containers, it's also possible to export and import them locally using the docker commands save & load

    `docker save -o my_cool_image.tar`

    `docker load --input my_cool_image.tar`



#### Docker Management summary: 

Basic image commands:

```
    # Set RAM, swap and CPUs for a given *docker container*
    docker run -it --rm --memory 2gb --memory-swap 3gb --cpus 1 container-name
    # Get list of currently available *docker containers*
    docker images
    # Get list of currently running *docker containers*
    docker ps
    # Stop a given running *docker container*
    docker stop image-id
    # Rename/change tag of a given *docker container*
    docker tag old-image-name/-id new-image-name/id
    # Export/save a given *docker container*
    docker save -o path/my_cool_image.tar image-name
    # Import/load a given *docker container*
    docker load --input path/my_cool_image.tar
```

#### Docker Management 101 - exercises

   1. "rename" our Ubuntu container, changing the tag from latest to image_42

   2. export/save the newly created container as a_container_at_the_end_of_the_universe.tar to your Desktop

   3. remove the existing Ubuntu containers

   4. import/load a_container_at_the_end_of_the_universe.tar

   5. run the newly loaded container using 2GB of RAM, 3 GB of swap and 1 CPU

