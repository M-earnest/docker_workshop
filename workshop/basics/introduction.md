# A super short introduction - Container & Virtualization

<br>
<br>

### Learning objectives

- Why do we use containers?
- What are the various types of virtualization based solutions?
- How to use Docker (maybe call it benefits of using Docker)?

<br>

*formulate objectives as questions or statements, e.g. motivation for virtualization?

### Requirements
- a working version of [Docker](https://docs.docker.com/get-docker/)
- access to a [Unix terminal/shell](https://en.wikipedia.org/wiki/Unix_shell)

<br>
<br>



<br>

#### Motivation - Why do we need containers?

*To motivate why the benefits of using containerization (or any kind of virtualization techniques for that matter) let's imagine the following scenario:*
<br>
<br>
**Your PI tasks you to do a couple of analyses for a new project. Lucky enough, you learn that one of your colleagues did run comparable analyses in the past and is so nice to share it with you. Even better: everything is assembled in one handy script called fancy_analyzes.py.
Your colleague tells you to run the script via navigating to the respective folder and type:**
<br>
<br> 
`fancy_analysis.py` 
<br>
<br>
Amazing, you can relax and let the script do the work as it will just run on your data and computational environment …
<br>
<br>
maybe add image here?
<br>
<br>
...Well, unfortunately the script immediately produces errors or does not work on your data/ in your computational environment, such that you are not able to reproduce anything. 
<br>
<br>
Why does this happen?! 

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

![it works on my machine](/static/It_works_on_my_machine.png)

#### Virtual Machines and Containers (maybe call this virtualization techniques and include virtual environments here?)

`Two main types`

- Virtual Machines:
    - Virtualbox
    - VMware
    - AWS, Google Compute Engine, ...
        - emulate whole computer system (software+hardware)
        - run on top of a physical machine using a hypervisor
        - hypervisor shares and manages hardware of the host and executes the guest operating system
        - guest machines are completely isolated and have dedicated resources
    

- Containers:
    - Docker
    - Singularity 
        - share the host system’s kernel with other containers
            → kernel level virtualization
        - each container gets its own isolated user space
        - only bins and libs are created from scratch
        - containers are very lightweight and fast to start up

![Virtual machines vs. Container](/static/VM_vs_Container.png)
        

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

![example workflow using containerization](/static/Container_workflow.png)



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

<details>
<summary>Conda options</summary>

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
</details>



`python venv` - (python module for the creation of virtual environments)

<details>
<summary>python venv options</summary>
![python venv manual](/static/python_venv.png)
</details>


### Container technologies

- Isolate the computing environments from the host system
- Provide a mechanism to encapsulate environments in a self-contained unit that can run anywhere





