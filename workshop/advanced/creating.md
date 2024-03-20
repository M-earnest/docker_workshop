# Creating software containers

### Learning objectives

- basic docker management
- docker commands
- resource management

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- a Docker Hub and GitHub account
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)
- minimal understanding of BASH, i.e. primarily the `pwd`, `ls`  and `cd` commands. (Check the _refresher section_ [link](link) to catch up!)



### Docker - there and back again


So far, we (hopefully) got to know how docker works, how containers can be downloaded, used and managed. Next, we'll learn how to create docker containers for our own work, including all the necessary dependencies to make your workflow truly reproducible. As a heads-up, most of the infos here are distilled from the [dockerfile reference page](https://docs.docker.com/reference/dockerfile/), which is great resource if you're looking for more in-depth explanations for the following lesson.


### Docker containers - the creation

When it comes to creating docker containers, two essential parts are relevant:

- a Dockerfile
- the `docker build` command

### Dockerfiles

At the beginning there was a Dockerfile...

A Dockerfile is, in essence, a machine-readable instruction on how to build a docker iamge. It can be considered as the "source code" of a docker container.

The Dockerfile usually includes a mixture of `bash` commands, that you would also normally use on your machine to e.g. setup a [Conda enviornment]() or to install specific software, and docker specific commands (called instructions). Below you'll find a list of acceptable Docker instructions are, if the terminology is condusing or you want to dive deeper into what the different commands are and how they are used check out the [Docker build documentation](https://docs.docker.com/engine/reference/builder/). We'll only make use of a few relevant commands for this tutorial that we will explain in detail below.

```
Instruction

ADD - Add local or remote files and directories.
ARG - Use build-time variables.
CMD - Specify default commands.
COPY - Copy files and directories.
ENTRYPOINT - Specify default executable.
ENV - Set environment variables.
EXPOSE - Describe which ports your application is listening on, i.e. for interactions with the users filesystem.
FROM - Create a new build stage from a base image.
HEALTHCHECK - Check a containers health on startup.
LABEL - Add metadata to an image.
MAINTAINER - Specify the author of an image.
ONBUILD - Specify instructions for when the image is used in a build.
RUN - Execute build commands.
USER	Set user and group ID.
VOLUME	Create volume mounts.
WORKDIR	Change working directory.
```

### Building a Dockerfile

The following will be a step-by-step guide on how to create a Dockerfile and how to populate our file with the necessary instructions to build a Docker container. Each separate instruction is called a "layer". Layers are executed consecutively from to to bottom, when using the build command to compose an Docker Image.

We will be relying on the `command line` and `bash` from here on out, if this seems like gibberish to you, please go through the [course prerequisites - Introduction to the (unix) command line: bash](https://m-earnest.github.io/docker_workshop/prerequisites/intro_to_shell.html).

Here are the relevant layers we're going to build, i.e how our Dockerfile is going to look like:

```
    FROM ubuntu:latest
    WORKDIR /project
    RUN apt-get update && \
        apt-get install -y python3.10 python3-pip && \
        pip3 install pandas

    RUN mkdir /info

    COPY print_info.py /info/
    COPY README.md /info/README.md

    CMD ["cat", "/info/README.md"]
```

So, let's explain this step-by-step and bring it all together with a practical example.

### 1. FROM - Baseimage

`FROM ubuntu:latest`

The "From" command defines the OS architecture that your image is supposed to use, e.g. Ubuntu 20.04. This will be referred to as the "base" or "baseimage" of a container. At times we will also use the 'From' command to call specific packages or environment managers, such as Conda. In this, case a specific OS  will be defined in the respective image that the 'from' command points to, e.g when calling 'FROM continuumio/miniconda3', the minconda3 image will have a specific OS defined.

It is also possible to use the 'From' command to chain multiple Docker images or more complex building steps together, for our purposes this is rarely necessary. You can find more info on Multi-stage builds [here](https://docs.docker.com/build/building/multi-stage/). 

### 2. WORKDIR - working directory

`WORKDIR /project`

The WORKDIR instruction sets the working directory for any of the other instructions that follow it in the Dockerfile (e.g. RUN, CMD, ENTRYPOINT, COPY, etc.)

- it further is the directory you will likely mount from your host system for input/output operations, facilitating data exchange between your container and host (If the specified directory does not exist on your system, Docker will create it automatically)
    - the only argument we provide is a concise, descriptive name for the folder/folder structure, e.g.

        `/project`

**note** Be cautious if you mount a directory from your local machine onto the WORKDIR the originally contained files cannot be accessed anymore as they will be replaced with the contents of your local directory. To circumvent this you can set the WORKDIR multiple times in a script or e.g. simply create a folder strcuture where you'll store you scripts and use the WORKDIR as the input/output directory for your data.

### 3. RUN - install software, execute commands

```
    RUN apt-get update && \
        apt-get install -y python3.10 python3-pip && \
        pip3 install pandas

    RUN mkdir /info
```

In the installation instructions, we want to provide information on what software/packages we want to install to run our workflow. Using the Ubuntu baseimage we can make use of the standard package managers 'pip' and 'apt-get' in the same way we would use them in our bash shell.

For this we'll make use of the `RUN` instruction, which will execute any specified command to create a new layer.

So to install e.g. Python using the Ubuntu baseimage and apt package manager we would write:

```
    RUN apt-get update && apt-get install -y python3.10
```

**note** You should always combine RUN apt-get update with apt-get install in the same statement, as otherwise you may run into cache issues (more info [here](https://docs.docker.com/develop/develop-images/instructions/#apt-get))

### 4. COPY - add files to image

```
    COPY print_info.py /info/
    COPY README.md /info/README.md
```

Using the COPY instruction we can permanently add files from our local system to our Docker Image.
- simply provide the path to the files you want to copy and the directory were they are supposed to be stored in the image
- e.g. if i want to add a script "print_info.py" from the curent working directory into the project folder of the image:

    `COPY print_info.py /project/`

### 5. Entrypoint and CMD - make the image exectuable

`CMD ["cat", "/info/README.md"]`

To make a docker image executable you'll need to include either an 'ENTRYPOINT', an 'CMD' or a mixture of both instructions. These specify what should happen when a container starts, and what arguments can be passed to modify the behaviour of the container. 

The ENTRYPOINT specifies a command that will always be executed when the container starts (i.e. this should be the "main" command), while CMD defines the default arguments of the container, e.g.

`ENTRYPOINT ["echo", "Hello, World!"]`

    or 

`CMD ["echo", "Hello, World!"]`

Given no further arguments when the container is run (after we've build it, of course), both of these will simply print "Hello World!", but the behavior of the 'CMD' command can be overriden when the container is run with specific instruction, e.g. 'docker run myimage Hello, Docker!' prints "Hello, Docker!" instead of "Hello World!". 

A practical use case can be to combine bothe instructions, so that the entrypoint provides a command that is always exectued, while CMD provides arguments that the user might want to exchange, e.g. if we want our container to execute a python script, we simply provide command line argument "python" as our ENTRYPOINT and use CMD to specify a default name of the script.

'''
    FROM python:3.10
    ENTRYPOINT ["python"]
    CMD ["script.py"]
'''

If we now simply run this conatiner using 'docker run myimage' it will try to locate and execute "script.py", if the user instead wants to run his python script called "my_script.py", he can simply add this info to the run instruction, i.e. 'docker run myimage "my_script.py"'.

If you have more complex commands that should initally be run you can further provide bash scripts as your ENTRYPOINT like so:

```
    COPY ./docker-entrypoint.sh /
    ENTRYPOINT ["/docker-entrypoint.sh"]
```


### Practical example

Let's try this all together! The following docker image will simply print some info about the files in the image if using the deafult parameters but can additionaly function as a computing environment (Ubuntu, Python3.10) when our deafult commands are replaced.


1. Let's create a new directory on our desktops called my_first_docker and in it an empty textfile called Dockerfile. Open your shell, type the following and hit enter 

`mkdir ~/Desktop/my_first_docker && touch ~/Desktop/my_first_docker/Dockerfile`

2. Download the course materials and copy the print_info.py script from the resources folder into `my_first_docker folder`

`cp /resources/README.md /Users/me/Desktop/my_first_docker`


3. Open your Dockerfile with a text-editor of your choice (again VScode is recommended) and copy-paste the following into the file and save it

```
    # Step 1: Use the newest Ubuntu version as a base image
    FROM ubuntu:latest

    # Step 2: Set the working directory
    WORKDIR /project

    # Step 3: Install Python 3.10, and some Python packages (Scipy, Pandas) via the Ubuntu package manager apt
    RUN apt-get update && \
        apt-get install -y python3.10 python3-pip && \
        pip3 install pandas

    # let's also create  a folder to store our info file in
    RUN mkdir /info

    # Step 4: Copy our Python script and README into the info folder of the image
    COPY print_info.py /info/
    COPY README.md /info/README.md

    # Step 5: Specify the default command when the image is run, e.g. to print the contents of the readme file 
    CMD ["cat", "/info/README.md"]
```

**4. Docker build**

Now that we've composed our Dockerfile, we can build our image via the 'docker build' command in the terminal. 

For this we provide a name for our image via the `-t flag` and specify the path to our Dockerfile, resulting in e.g (given we're in the my_first_docker folder).:

    `docker build -t myfirstdocker .`

<div style="overflow-y: scroll; height: 200px; border: 1px solid #cccccc; padding: 5px; margin-bottom: 20px;">
  <p>

    (base) Michaels-MacBook-Pro:my_first_docker me$ sudo docker build -t my_first_docker .
    [+] Building 1484.8s (9/9) FINISHED                  docker:desktop-linux  
    => [internal] load .dockerignore		                                                                  0.0s 
    => => transferring context: 2B 				                                                           	  0.0s 
    => [internal] load build definition from Dockerfile		 	                                              0.0s
    => => transferring dockerfile: 597B 				 	                                                  0.0s
    => [internal] load metadata for docker.io/library/ubuntu:latest 	                                      0.0s
    => [1/4] FROM docker.io/library/ubuntu:latest 			                                                  0.0s
    => [internal] load build context 					                                                      0.0s
    => => transferring context: 138B					                                                      0.0s
    => CACHED [2/4] WORKDIR /project  				                                                          0.0s
    => [3/4] RUN apt-get update &&     apt-get install -y python3.10 python3-pip && pip3 install pandas    1483.5s
    => [4/4] COPY print_info.py  /project/ 			                                                          0.0s
    => [4/6] RUN mkdir /info                                                                                  0.1s
    => [5/6] COPY print_info.py /info/                                                                        0.0s
    => [6/6] COPY README.md /info/README.md                                                                   0.0s
    => exporting to image						                                                              1.2s
    => => exporting layers						                                                              1.2s
    => => writing image sha256:c1891eb763de4c8432eae0d7239f7acd2f0d02782a5a4d87ec3f558f5c033ad6 	          0.0s 
    => => naming to docker.io/library/my_first_docker			                                              0.0s 
                                                                                                                
    What's Next?
    View a summary of image vulnerabilities and recommendations → docker scout quickview

  </p>
</div>

As you can see from the output, the steps we defined in our Dockerfile are executed step by step, comparable to docker pull. And we can check if our image was actually created successfully by using the `docker images` command:

```
    (base) Michaels-MacBook-Pro:my_first_docker me$ docker images
    REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
    my_first_docker        latest    c1891eb763de   23 minutes ago   614MB
```

**5. Docker run**

The most basic way to run a container from the terminal is simply `docker run imagename`, e.g. in :

`docker run my_first_docker`

This will result in our defined default behaviour (CMD ["cat", "/info/README.md"]). The output looks like this:

```
    (base) Michaels-MBP:my_first_docker me$ docker run my_first_docker
    # EEG Demographics Dataset

    ## Author
    - Name: M. Ernst
    - Date: 2024-03-09
    - Location: Frankfurt am Main, Germany

    ## Experiment Description
    This dataset is part of a study investigating …

    ## Dataset Contents
    The `demographics.csv` file contains demographic information of the EEG study participants, including:
    - `SubjectID`: Unique identifier for each participant.
    - `Age`: Age of the participant.
    - `Handedness`: “L” for left-, ”R” for righthanded

    ## Usage Instructions
    …

    ## Citing This Work
    If you use this dataset in your research, please cite it as follows:
    Ernst, M. (2024). Study Title. Frankfurt am Main, Germany. ORCID-ID

```

If Instead we want to run the python script in our containers `info folder` we replace the default command, by including instructions in `docker run ...`, like so: 

`docker run my_first_docker python3 /info/print_info.py`

```
    Date: 2024-03-13
    Welcome to the Docker image for Your Study Title Here. Youll find all relevant information in the README file located in this folder.
```

No if we would want our container to work as a computing enviornment (i.e. to run python scripts) we simply modify the `docker run` command by providing a `mount path`, i.e. a pointer for which directories of the host system should be made accessible to the container. Again, we do this by providing a `v -flag` (volume), a local file path and the working directory in our container, separated by `:`. If we want to mount our current working directory (`pwd` in bash) to the `/projects` folder in our container and run a local python script we can do:

`docker run -v $(pwd):/project my_first_docker python3 print_info_copy.py`

    where:   
        $(pwd) = local machine :
        /project = docker container  
        my_first_docker = imagename 
        python3 = executable 
        print_info_copy.py = filename

Resulting in:

```
    (base) Michaels-MBP:my_first_docker me$ docker run -v $(pwd):/project my_first_docker python3 print_info_copy.py
    Date: 2024-03-13
    Welcome to the Docker image for Your Study Title Here (Imported script via CMD). Youll find all relevant information in the README file located in this folder.

```

### Virtualizing a workflow

- More complex example of a docker container
- e.g. create eviornment via conda with specific packages, provide input and output path, do a simple task (e.g. mne report, create BIDS folder structure etc.)


### Neurodocker?

You might wonder: Isn't there a sufficient, faster and easier way of composing Dockerfiles?
Well, say no more and meet `Neurodocker`, a Docker container that targets the creation of Docker containers - Dockerception.

Even though Neurodocker was designed for (you might've guessed it already) Docker containers to utilize in the realm of neuroscience, it's also a very handy tool for any other research field, as especially the basic setup is done very quickly and hassle-free.

So, let's see how we can create our Dockerfiles using `Neurodocker`. At first we have to get the Neurodocker image using the `docker pull command`


![pull Neurodocker image](/static/Neurodocker_pull_image.png)

```
aaronreer@FK6P-1158240:~$ docker pull repronim/neurodocker:0.9.5
0.9.5: Pulling from repronim/neurodocker
8a49fdb3b6a5: Already exists
0357922e53aa: Already exists
9a0b2b81bdd7: Already exists
1bed10bb162b: Already exists
61479f8dd1a7: Already exists
5fca58cb4537: Already exists
76b5b227fa86: Already exists
Digest: sha256:3d4ae0b3e6f0767ad2ea3dc401b4a011c354a682eb9db4a9c18bcee2cbd7cddb
Status: Downloaded newer image for repronim/neurodocker:0.9.5
docker.io/repronim/neurodocker:0.9.5
```


All we have to do now is run Neurodocker, providing the necessay input arguments beginning with stating that we want to create a Docker container and that we want to use `neurodebian:bullseye` as a base and apt as package manager:


![Neurodocker: select base-image and package manager](/static/Neurodocker_generate_docker_base.png)

```
aaronreer@FK6P-1158240:~$ docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \

```



Next, we specify all the Linux packages that we want to have installed in our image:


![Neurodocker: Linux installations ](/static/Neurodocker_generate_docker_linux_installations.png)


```
aaronreer@FK6P-1158240:~$ docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \

```

Now, we are only missing the python part...



![Neurodocker: setting up python](/static/Neurodocker_generate_docker_python.png)

```
aaronreer@FK6P-1158240:~$ docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \
--miniconda version=latest env_name=myenvironmentname \
conda_install="python=3.11 numpy pandas" \
pip_install="mne"
```

Great! We have all the information that we need. Hence, let's run the `Neurodocker` container parsing the output to a file called 'Dockerfile'. We can do so using the `>-operator` :


![Neurodocker: run container and parse output to Dockerfile](/static/Neurodocker_generate_docker_python_toDockerfile.png)

```
aaronreer@FK6P-1158240:~/data$ docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \
--miniconda version=latest env_name=myenvironmentname \
conda_install="python=3.11 numpy pandas" \
pip_install="mne" > Dockerfile
```




So using Neurodocker can save you a lot of time and stress. It's especially great to set up the basics of your Docker container, so one approach to create a Docker container for your workflow may be to do the basics with Neurodocker and fine-tune to your needs manually.


### Docker push

Now this is where we could stop if we just want to make a quick reproducible solution for our basic workflows. But we, of course, want to additionally enable open and community-driven science, by getting our containerized workflows out there, but how do we do that?

In general, we can simply share our Dockerfile or created image (use the export/import functionality - Docker save/load) via e.g. USB or email.
But our preferred solution should be to make use of this thing called "internet" and share our Docker container on Docker Hub, making it available to everyone. Just make sure that nothing sensitive is contained in your container.

This is again rather straightforward and can be achieved in a few simple steps. 

1. Create and login to your Docker Hub account

Before you can push an image, you need to log in to Docker Hub. Simply create an account online, run  `docker login` from your command line and enter your Docker Hub username and password.

2. Tag your image

After building our image, we need to `tag` it, in order to make it identifiable online. Tags can be anything, but should be meaningful file and version names (1.0 etc. or "latest" are common). The general form of the tag command is e.g.

```
    docker tag image-id username/repository:tag
```
Where `image-id` is the name provided when building your image, `username` is your Docker Hub username, `repository` is the repository or folder on your Docker Hub where your container is supposed to be stored and `tag` is of course the specific version name. So this could look like

```
    docker tag myworkflowimage mernst/workflow:latest
```

3. Docker push
Next we simply use the `docker push` command to send our freshly tagged Docker container to Docker Hub, e.g.

```
    docker push yourhubusername/container:tag
```



### Docker containers - creating and pushing - a recap

- Creating and sharing Docker containers is achieved through three parts: a `Dockerfile`, the `build` and the `push` command.
- Dockerfiles can either be created completely manually or supported by neurodocker
- using docker build, the Docker container is created following the information in the Dockerfile
    
```
docker build -t myfirstdocker path/to/directory/containing/Dockerfile
```

- once build, the Docker container should be tagged and subsequently pushed to Docker Hub

```

docker tag image-id yourhubusername/container:tag
docker push yourhubusername/container:tag

```

- the build and push process can be automatized using a combination of Docker Hub and GitHub


### Excercise

- ???
- as this is an interactive session might not be necessary, but for the general audience we could have them go to the whole process for a simple python project?

