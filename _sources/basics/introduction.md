# A super short introduction - Container & Virtualization

<br>
<br>

### Learning objectives

- Why do we use containers?
- What are the various types virtualization based solutions?
- How to use Docker?
- How to use Conda?

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)

<br>
<br>


### Container technologies

- Isolate the computing environments
- Provide a mechanism to encapsulate environments in a self-contained unit that can run anywhere

<br>

#### Motivation - Why do we need containers?

`Reproducibility!`

- Each project in a lab depends on complex software environments
    - operating system
    - drivers
    - software dependencies: Python/MATLAB/R + libraries


- We try to avoid
    - "the computer I used was shut down a year ago, can’t rerun the results from my publication..."
    - "the analysis were run by my student, have no idea where and how..." 
    - etc.


`Collaboration!`

- Sharing your code or using a repository might not be enough, i.e. because of software version or OS specific conflicts
- Data code might not adhere to the same standards or structure (e.g. [BIDS](https://bids.neuroimaging.io/))

- We try to avoid

    - "well, I forgot to mention that you have to use Clang, gcc never worked for me..."
    - "don’t see any reason why it shouldn’t work on Windows...(I actually have no idea about Windows, but won’t say it...)"
    - "it works on my computer..."
    - etc.


#### Virtual Machines and Containers

`Two main types`

- Virtual Machines:
    - Virtualbox
    - VMware
    - AWS, Google Compute Engine, ...

- Containers:
    - Docker
    - Singularity  


Share the same main idea

- Isolate the computing environment
- Allows faithful reconstruction of computing environments
- Allows for easy sharing of computing environments, between different OS and systems


#### Docker

- Docker is an open-source platform that allows for `building, deploying, and managing applications/research workflows` in self-sufficient, portable `containers`

- Recent additions to Docker include a straightforward GUI (Graphical User Interface) called [Docker Desktop](https://docs.docker.com/desktop/use-desktop/), but Docker is most powerful when making use of the Command-line aka the UNIX Shell.
    -  this is also what we'll be focussing on in this workshop

- runs on all of the most common OS (i.e. Linux, Mac OS X and Windows)

Interesting tutorials and blog posts:

- collect new ressoruces here !!!!!!


#### Docker vs Singularity

`Docker`:
- docker can escalate privileges, so you can be effectively treated as a root on the host system
    - this is usually not supported or viewed in a positive light by administrators from HPC centers


`Singularity`:

- a container solution created for scientific and application driven workloads
- supports existing and traditional HPC resources
- a user inside a Singularity container is the same user as outside the container
  - but you can use Vagrant to create a container (you have root privileges on your VM!)
- can run (and modify!) existing Docker containers


#### Virtual environment managers:

- environment keeps dependencies, i.e. specific versions of libraries/apps isolated from others or the system-wide installation
- allows one to simply summarize and share a list of required by different projects in separate places (often in the form of an  "environemnt.yml" file)
- allows one to work with specific versions of libraries or Python itself without affecting other projects

`Conda` - (Docker "alternative" for Python)

- most prominent package and environment manager for python

- minimal, quick installation via [Miniconda](https://docs.anaconda.com/free/miniconda/index.html)
- full suite of most relevant python packages and integrated development enviornments through the [Anaconda](https://www.anaconda.com/) project

- simple command-line implementation

```

  # Updating conda
  conda update conda
  # List available Python version
  conda search "^python$"
  # Creating a Python 3.6 environment
  conda create -n python3.6_test python=3.6
  # Install directly some packages while creating a new environment
  conda create -n python3.6_anaconda python=3.6 anaconda
  # Installing additional packages
  conda install -n python3.6_test scipy
  # Remove unused packages and caches
  conda clean -tipsy
  # Activating the environment
  source activate python3.6_test
  # Deactivating the environment
  source deactivate python3.6_test
  # Remove conda environment
  conda remove --name python3.6_test --all

```




