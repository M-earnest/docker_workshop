### Dump for old content

- Sharing your code or using a repository might not be enough, i.e. because of software version or OS specific conflicts
- Data code might not adhere to the same standards or structure (e.g. [BIDS](https://bids.neuroimaging.io/))


`Collaboration!`
`Reproducibility!`

Share the same main idea

- Isolate the computing environment
- Allows faithful reconstruction of computing environments
- Allows for easy sharing of computing environments, between different OS and systems

 - each container gets its own isolated user space
        - only bins and libs are created from scratch
        - containers are very lightweight and fast to start up


#### Virtual environment managers:

- environment keeps dependencies, i.e. specific versions of libraries/apps isolated from others or the system-wide installation
- allows one to simply summarize and share a list of required by different projects in separate places (often in the form of an  "environemnt.yml" file)
- allows one to work with specific versions of libraries or Python itself without affecting other projects
- limited to isolate libs and bins but not the OS itself

`Conda` - (Docker "alternative" for Python)

- most prominent package and environment manager for python

- minimal, quick installation via [Miniconda](https://docs.anaconda.com/free/miniconda/index.html)
- full suite of most relevant python packages and integrated development enviornments through the [Anaconda](https://www.anaconda.com/) project

- simple command-line implementation




`python venv` - (python module for the creation of virtual environments)



### Container technologies

- Isolate the computing environments from the host system
- Provide a mechanism to encapsulate environments and virtualized OS in a self-contained unit that can run anywhere

