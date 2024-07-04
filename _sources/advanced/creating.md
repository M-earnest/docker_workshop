# Creating software containers

### Learning objectives

- learn the architecture of a docker image
- learn what a dockerfile and a build context are
- learn how to build, run and share a docker container
- learn how to make your (professional life easier) by using [Neurodocker](https://www.repronim.org/neurodocker/user_guide/examples.html)

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- a Docker Hub and GitHub account
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)
- minimal understanding of BASH, i.e. primarily the `pwd`, `ls`  and `cd` commands. (Check the [refresher section](lhttps://m-earnest.github.io/docker_workshop/prerequisites.html) to catch up!)



### Docker - there and back again

So far, we (hopefully) got to know how docker works, how containers can be downloaded, used and managed. Next, we'll learn how to create docker containers for our own work, including all the necessary dependencies to make your workflow truly reproducible. As a heads-up, most of the infos here are distilled from the [dockerfile reference page](https://docs.docker.com/reference/dockerfile/), which is a great resource if you're looking for more in-depth explanations for the following session.

We will still be relying on the `command line` and `bash` from here on out, if this seems like gibberish to you, please go through the [course prerequisites - Introduction to the (unix) command line: bash](https://m-earnest.github.io/docker_workshop/prerequisites/intro_to_shell.html).


### Docker containers - the creation

When it comes to creating docker containers, two essential parts are relevant:

- a Dockerfile
- the `docker build` command

### Dockerfiles

At the beginning there was a Dockerfile...

A Dockerfile is, in essence, a machine-readable instruction on how to build a docker iamge. It can be considered as the "source code" of a docker container.

The Dockerfile usually includes a mixture of `bash commands`, that you would also normally use on your machine to e.g. to setup a [Conda enviornment]() or to install software, and docker specific commands, called `instructions`. Below you'll find a list of acceptable Docker instructions. 

If the terminology is confusing or you want to dive deeper into what the different commands are and how they are used check out the [Docker build documentation](https://docs.docker.com/engine/reference/builder/). We'll only make use of a few relevant instructions for this tutorial that we will explain in detail further below.

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

The following will be a step-by-step guide on how to create a Dockerfile and how to populate our file with the necessary instructions to build a Docker image. Each separate instruction is called a `layer`. Layers are executed consecutively from top to bottom, when using the build command to compose an Docker Image.

Here are the relevant _layers_ we're going to build, i.e. how our Dockerfile is going to look like:

```
    # Step 1: Use the newest Ubuntu version as a base image
    FROM ubuntu:latest

    # Step 2: Set the working directory
    WORKDIR /project

    # Step 3: Install Python 3.10, and some Python packages (Pandas) via the Ubuntu package manager apt
    RUN apt-get update && \
        apt-get install -y python3.10 python3-pip && \
        pip3 install pandas

    # let's also create a folder to store our files in
    RUN mkdir /info

    # Step 4: Copy our Python script and README into the info folder of the image
    COPY print_info_container.py /info/
    COPY README.md /info/README.md

    # Step 5: Specify the default command when the image is run, e.g. to print the contents of the readme file 
    CMD ["cat", "/info/README.md"]
```

So, let's explain this step-by-step and bring it all together with a practical example.

### 1. FROM - Baseimage

`FROM ubuntu:latest`

The `FROM` instruction defines the OS architecture that your image is supposed to use, e.g. Ubuntu 20.04. This will be referred to as the "base" or "baseimage" of a container. At times we will also use `FROM` to call specific packages or environment managers, such as Conda. In this case a specific OS  will already be defined in the respective image that the `FROM` instruction points to, e.g when calling `FROM continuumio/miniconda3`, the minconda3 image will have a specific OS defined.

It is also possible to use `From` to chain multiple Docker images or more complex building steps together, for our purposes this is rarely necessary. You can find more info on Multi-stage builds [here](https://docs.docker.com/build/building/multi-stage/). 

### 2. WORKDIR - working directory

`WORKDIR /project`

The WORKDIR instruction sets the working directory for any of the other instructions that follow it in the Dockerfile (e.g. RUN, CMD, ENTRYPOINT, COPY, etc.)

- it further is the directory you will likely mount from your host system for input/output operations, facilitating data exchange between your container and host
    - the only argument we provide is a concise, descriptive name for the folder/folder structure, e.g.

        `/project`

**Note:** Be cautious if you mount a directory from your local machine onto the WORKDIR. The originally contained files cannot be accessed anymore as they will be replaced with the contents of your local directory. To circumvent this you can set the WORKDIR multiple times in a script or e.g. simply create a folder strcuture where you'll store you scripts and use the WORKDIR as the input/output directory for your data.

### 3. RUN - install software, execute commands

```
    RUN apt-get update && \
        apt-get install -y python3.10 python3-pip && \
        pip3 install pandas

    RUN mkdir /info
```

In the installation instructions, we want to provide information on what software/packages we want to install to run our workflow. Using the Ubuntu baseimage we can make use of the standard package managers 'pip' and 'apt-get' in the same way we would use them in our bash shell.

For this we'll make use of the `RUN` instruction, which will execute any specified command to create a new layer.

So to install e.g. Python using the Ubuntu baseimage and apt package manager we write:

```
    RUN apt-get update && apt-get install -y python3.10
```

**Important**: RUN is a build command, if you want to execute certain scripts/code when a container is run refere to point 5.

**Note**: You should always combine RUN apt-get update with apt-get install in the same statement, as otherwise you may run into cache issues (more info [here](https://docs.docker.com/develop/develop-images/instructions/#apt-get))

### 4. COPY - add files to image

```
    COPY print_info_container.py /info/
    COPY README.md /info/README.md
```

Using the COPY instruction we can permanently add files from our local system to our Docker Image.
- simply provide the path to the files you want to copy and the directory were they are supposed to be stored in the image
- e.g. if i want to add a script "print_info_container.py" from the curent working directory of the host machine into the project folder of the image:

    `COPY print_info_container.py /project/`

### 5. Entrypoint and CMD - make the image exectuable

`CMD ["cat", "/info/README.md"]`

To make a docker image executable you'll need to include either an `ENTRYPOINT`, an `CMD` or a mixture of both instructions. These specify what should happen when a container starts, and what arguments can be passed to modify the behaviour of the container. 

The `ENTRYPOINT` specifies a command that will always be executed when the container starts (i.e. this should be the "main" command), while `CMD` defines the default arguments of the container, e.g.

`ENTRYPOINT ["echo", "Hello World!"]`

    or 

`CMD ["echo", "Hello World!"]`

Given no further arguments when the container is run (after we've build it, of course), both of these will simply print "Hello World!", but the behavior of the `CMD` instruction can be overwritten when the container is run with specific commands, e.g. `docker run myimage Hello, Docker!` prints "Hello, Docker!" instead of "Hello World!". 

A practical use-case can be to combine both instructions, so that `ENTRYPOINT` provides a command that is always exectued, while `CMD` provides arguments that the user might want to exchange, e.g. if we want our container to execute a python script, we simply provide the command line argument "python" as our ENTRYPOINT and use CMD to specify a default name of a script.

```
    FROM python:3.10
    ENTRYPOINT ["python"]
    CMD ["script.py"]
```

If we would now run this container using `docker run myimage` it will try to locate and execute "script.py", if the user instead wants to run a different python script called "my_script.py", they can simply add this info to the run command, i.e. `docker run myimage python3 my_script.py`.

If you have more complex commands that should initally be run, you can further provide bash scripts as your ENTRYPOINT like so:

```
    COPY ./docker-entrypoint.sh /
    ENTRYPOINT ["/docker-entrypoint.sh"]
```


### Practical example

Let's try this all together! The following docker image will simply print some info about the files in the image if using the deafult parameters, but can additionaly function as a computing environment (Ubuntu, Python3.10) when our deafult commands are replaced.


**1. Create the build context**

Let's create a new directory on our desktops called `my_first_docker` and in it an empty textfile called `Dockerfile`. Open your shell, type the following and hit enter 

`mkdir ~/Desktop/my_first_docker && touch ~/Desktop/my_first_docker/Dockerfile`

**2. Add files to the build context**

Download the course materials and copy all files from the examples folder into `my_first_docker folder` (README.md, print_info_container.py, print_info_local_system.py). 
Otherwise you'll find the necessary files under `/docker_workshop_oldenburg/build_example/`, if you've pulled and ran the `get_workshop_materials:0.0.3` container from the [quickstart session](https://m-earnest.github.io/docker_workshop/basics/quickstart.html).

E.g. using bash:

`cp /build_example/README.md /Users/username/Desktop/my_first_docker`

**Note:** Replace /Users/username/Desktop/my_first_docker with the path to the Desktop on your machine, you can find this path using the following commands in your terminal `pwd` (get the name of the current working directory), `ls` (list files and directories) and `cd` (change directory). The path structure may differ depending on your operating system, i.e on Linux based systems: `/home/username/Desktop`; on Windows using WSL: `/mnt/c/Users/<username>/Desktop`.

**3. Populate the Dockerfile**

Open your Dockerfile with a text-editor of your choice (VScode is recommended), copy-paste the following into the file and save it

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
    COPY print_info_container.py /info/
    COPY README.md /info/README.md

    # Step 5: Specify the default command when the image is run, e.g. to print the contents of the readme file 
    CMD ["cat", "/info/README.md"]
```

**4. Docker build**

Now that we've composed our Dockerfile, we can build our image via the `docker build` command in the terminal. 

For this we provide a name for our image via the `-t flag` and specify the path to our Dockerfile, resulting in e.g (given we're in the my_first_docker folder).:

    `docker build -t my_first_docker .`

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
    => [4/4] COPY print_info_container.py  /project/ 			                                                          0.0s
    => [4/6] RUN mkdir /info                                                                                  0.1s
    => [5/6] COPY print_info_container.py /info/                                                                        0.0s
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

This will result in our defined default behaviour (CMD ["cat", "/info/README.md"]). As printing an informative READEME is always a great starting point for a reproducible pipeline, we're doing exactly this here. 

The output looks like this:

```
    (base) Michaels-MBP:my_first_docker me$ docker run my_first_docker
    # EEG Demographics Dataset

    ## Author
    - Name: Author
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
    Lastname, F. (2024). Study Title. Frankfurt am Main, Germany. ORCID-ID

```

If Instead we want to run the python script in our containers `/info folder` we replace the default command, by including instructions in `docker run ...` substituting the first default argument of our CMD with `python3` as our executable, like so: 

`docker run my_first_docker python3 /info/print_info_container.py`

```
    Date: 2024-03-13
    Welcome to the Docker image for Your Study Title Here. Youll find all relevant information in the README file located in this folder.
```

No if we would want our container to work as a computing enviornment (i.e. to run python scripts) we simply modify the `docker run` command by providing a `mount path`, i.e. a pointer for which directories of the host system should be made accessible to the container. Again, we do this by providing a `v -flag` (volume), a local file path and the working directory in our container, separated by `:`. If we want to mount our current working directory (`pwd` in bash) to the `/projects` folder in our container and run a local python script we can do:

`docker run -v $(pwd):/project my_first_docker python3 print_info_local_system.py`

    where:   
        $(pwd) = local machine :
        /project = docker container  
        my_first_docker = imagename 
        python3 = executable 
        print_info_.py = filename

Resulting in:

```
    (base) Michaels-MBP:my_first_docker me$ docker run -v $(pwd):/project my_first_docker python3 print_info_local_system.py
    Date: 2024-03-13
    Welcome to the Docker image for Your Study Title Here (Imported script via CMD). Youll find all relevant information in the README file located in this folder.

```

### Virtualizing a workflow

Of course most workflows will necessarily be more complex, so let's look at another example.

- live demonstration

<div style="overflow-y: scroll; height: 200px; border: 1px solid #cccccc; padding: 5px; margin-bottom: 20px;">

```
# Generated by Neurodocker and Reproenv.

FROM neurodebian:latest
RUN apt-get update -qq \
           && apt-get install -y -q --no-install-recommends \
                  git \
                  nano \
           && rm -rf /var/lib/apt/lists/*
ENV CONDA_DIR="/opt/miniconda-latest" \
    PATH="/opt/miniconda-latest/bin:$PATH"
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           bzip2 \
           ca-certificates \
           curl \
    && rm -rf /var/lib/apt/lists/* \
    # Install dependencies.
    && export PATH="/opt/miniconda-latest/bin:$PATH" \
    && echo "Downloading Miniconda installer ..." \
    && conda_installer="/tmp/miniconda.sh" \
    && curl -fsSL -o "$conda_installer" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash "$conda_installer" -b -p /opt/miniconda-latest \
    && rm -f "$conda_installer" \
    && conda update -yq -nbase conda \
    # Prefer packages in conda-forge
    && conda config --system --prepend channels conda-forge \
    # Packages in lower-priority channels not considered if a package with the same
    # name exists in a higher priority channel. Can dramatically speed up installations.
    # Conda recommends this as a default
    # https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html
    && conda config --set channel_priority strict \
    && conda config --system --set auto_update_conda false \
    && conda config --system --set show_channel_urls true \
    # Enable `conda activate`
    && conda init bash \
    && conda create -y  --name ancp \
    && conda install -y  --name ancp \
           "python=3.11" \
           "pandas" \
           "numpy" \
           "scipy" \
           "plotly" \
           #"mne-base" \ 
    && bash -c "source activate ancp \
    &&   python -m pip install --no-cache-dir  \
             "ancpbids==0.2.1" \
             "mne" \ 
             "mne-bids" \ 
             "meg-qc"" \
    # Clean up
    && sync && conda clean --all --yes && sync \
    && rm -rf ~/.cache/pip/*
#ENTRYPOINT [ "mkdir","test1" ]
# Save specification to JSON.
RUN printf '{ \
  "pkg_manager": "apt", \
  "existing_users": [ \
    "root" \
  ], \
  "instructions": [ \
    { \
      "name": "from_", \
      "kwds": { \
        "base_image": "neurodebian:bullseye" \
      } \
    }, \
    { \
      "name": "install", \
      "kwds": { \
        "pkgs": [ \
          "git", \
          "nano" \
        ], \
        "opts": null \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "apt-get update -qq \\\\\\n    && apt-get install -y -q --no-install-recommends \\\\\\n           git \\\\\\n           nano \\\\\\n    && rm -rf /var/lib/apt/lists/*" \
      } \
    }, \
    { \
      "name": "env", \
      "kwds": { \
        "CONDA_DIR": "/opt/miniconda-latest", \
        "PATH": "/opt/miniconda-latest/bin:$PATH" \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "apt-get update -qq\\napt-get install -y -q --no-install-recommends \\\\\\n    bzip2 \\\\\\n    ca-certificates \\\\\\n    curl\\nrm -rf /var/lib/apt/lists/*\\n# Install dependencies.\\nexport PATH=\\"/opt/miniconda-latest/bin:$PATH\\"\\necho \\"Downloading Miniconda installer ...\\"\\nconda_installer=\\"/tmp/miniconda.sh\\"\\ncurl -fsSL -o \\"$conda_installer\\" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh\\nbash \\"$conda_installer\\" -b -p /opt/miniconda-latest\\nrm -f \\"$conda_installer\\"\\nconda update -yq -nbase conda\\n# Prefer packages in conda-forge\\nconda config --system --prepend channels conda-forge\\n# Packages in lower-priority channels not considered if a package with the same\\n# name exists in a higher priority channel. Can dramatically speed up installations.\\n# Conda recommends this as a default\\n# https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html\\nconda config --set channel_priority strict\\nconda config --system --set auto_update_conda false\\nconda config --system --set show_channel_urls true\\n# Enable `conda activate`\\nconda init bash\\nconda create -y  --name ancp\\nconda install -y  --name ancp \\\\\\n    \\"python=3.10\\" \\\\\\n    \\"pandas\\" \\\\\\n    \\"numpy\\" \\\\\\n    \\"scipy\\" \\\\\\n    \\"plotly\\"\\nbash -c \\"source activate ancp\\n  python -m pip install --no-cache-dir  \\\\\\n      \\"ancpbids\\" \\\\\\n      \\"meg-qc\\" \\\\\\n      \\"mne\\"\\"\\n# Clean up\\nsync && conda clean --all --yes && sync\\nrm -rf ~/.cache/pip/*" \
      } \
    } \
  ] \
}' > /.reproenv.json
# End saving to specification to JSON.
# Copy data (script) into image

COPY ./mne_test.py /home/scripts/
COPY ./mne_test.sh /home/scripts/
# Run the script that produces the reports within the container.
# Reports are written to the /output directory 
CMD [ "bash", "/home/scripts/mne_test.sh" ]
```

</div>


### Neurodocker

You might wonder: Isn't there a sufficient, faster and easier way of composing Dockerfiles?
Well, say no more and meet [Neurodocker](https://www.repronim.org/neurodocker/user_guide/installation.html), a Docker container that targets the creation of Docker containers - Dockerception.

Even though Neurodocker was designed for (you might've guessed it already) Docker containers to utilize in the realm of neuroscience, it's also a very handy tool for any other research field, as especially the basic setup is done very quickly and hassle-free.

So, let's see how we can create our Dockerfiles using `Neurodocker`. At first we have to get the Neurodocker image using the `docker pull command`



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


All we have to do now is run Neurodocker, providing the necessay input arguments beginning with stating that we want to create a Docker container and that we want to use `ubuntu:latest` as a base and apt as package manager:


```
aaronreer@FK6P-1158240:~$ docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \

```


Next, we specify all the Linux packages that we want to have installed in our image:


```
docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \

```

Now, we are only missing the python part...



```
docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \
--miniconda version=latest env_name=myenvironmentname env_exists=false \
conda_install="python=3.11 numpy pandas" \
pip_install="mne"
```

Great! We have all the information that we need. Hence, let's run the `Neurodocker` container parsing the output to a file called 'Dockerfile'. We can do so using the `>` operator :



```
docker run repronim/neurodocker:0.9.5 generate docker \
--base-image ubuntu:latest \
--pkg-manager apt \
--install git nano \
--miniconda version=latest env_name=myenvironmentname \
conda_install="python=3.11 numpy pandas" \
pip_install="mne" > Dockerfile
```

So using Neurodocker can save you a lot of time and stress. It's especially great to set up the basics of your Docker container, so one approach to create a Docker container for your workflow may be to do the basics with Neurodocker and fine-tune to your needs manually.

**NOTE!** When building Dockerfiles created with Neurodocker on an M1 or M2 Mac you might run into issues. These can usually be resolved by providing an architecture flag to your build command, e.g. `--platform linux/x86_64`. Searching for the specific warning should provide the necessary infos for specific cases.

### Neurodocker - Going further beyond

Check out the examples on the [Neurodocker site](https://www.repronim.org/neurodocker/user_guide/examples.html), to see how to incorporate most neuroscience relevant packages into a Docker container. 

Additionally, you should check out their [command-line-interface section](https://www.repronim.org/neurodocker/user_guide/cli.html) to see how to best make use of Neurodocker. 

**Note** If your server system doesn't support docker, Neurodocker also allows for the creation of singularity images using mostly the same syntax as above!

### Docker push

Now this is where we could stop if we just want to make a quick reproducible solution for our basic workflows. But we, of course, want to additionally enable open and community-driven science, by getting our containerized workflows out there, but how do we do that?

In general, we can simply share our Dockerfile or created image (use the export/import functionality - Docker save/load) via e.g. USB or email.
But our preferred solution should be to make use of this thing called "internet" and share our Docker container on Docker Hub, making it available to everyone. Just make sure that nothing sensitive is contained in your container.

This is again rather straightforward and can be achieved in a few simple steps. 

1. Create and login to your DockerHub account

Before you can push an image, you need to login to DockerHub. Simply create an account online, run  `docker login` from your command line and enter your Docker Hub username and password.

2. Tag your image

After building our image, we need to `tag` it, in order to make it identifiable online. Tags can be anything, but should be meaningful file and version names (1.0 etc. or "latest" are common). The general form of the tag command is e.g.

```
    docker tag image-id username/repository:tag
```
Where `image-id` is the name provided when building your image, `username` is your Docker Hub username, `repository` is the repository or folder on your Docker Hub where your container is supposed to be stored and `tag` is of course the specific version name. So this could look like

```
    docker tag 36207dff9e03 mearnst/myworkflowimage:latest
```

3. Docker push
Next we simply use the `docker push` command to send our freshly tagged Docker image to DockerHub, e.g.

```
    docker push yourhubusername/container_name:tag
```


### Docker containers - creating and pushing - a recap

- Creating and sharing Docker containers is achieved through three parts: a `Dockerfile`, the `build` and the `push` command.
- Dockerfiles can either be created completely manually or supported by neurodocker
- using docker build, the Docker container is created following the information in the Dockerfile
    
```
docker build -t my_first_docker path/to/directory/containing/Dockerfile
```

- once build, the Docker container should be tagged and subsequently pushed to Docker Hub

```

docker tag image-id yourhubusername/container:tag
docker push yourhubusername/container:tag

```

- the build and push process can be automatized using a combination of Docker Hub and GitHub. More info in the [Automating software containers](https://m-earnest.github.io/docker_workshop/advanced/automating.html) session.

