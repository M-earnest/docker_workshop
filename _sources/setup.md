# Setup for the workshop

ToDo:
- dumb it down, remove extra dependencies


Most of the materials for this workshop you can find on this website, if you'd like to give input, leave comments or highlight relevant parts (publicly or privately) we encourage you to make use of the [`hypothes.is`](https://web.hypothes.is/) plugin via the anotation sidebar on the right side of the page. If you'd rather download all of the materials as a zip file, you can do so throug the associated [Github repo]() via this [link](). You can open the respective lessons (.md files) via an IDE (e.g. VScode, Atom) or via Jupyter Notebooks/Lab.

The only software you will necessarily have to install will be [Docker](). We'll come to the actual setup for this shortly, but there are a few other requirements that will need to be satisfied. 

## Required software

- A command-line shell: Bash
- An IDE or text editor: e.g. VSCode (recommended)
- A modern browser

Mac and Linux distributions automatically provide a command line shell, simply search for `terminal` and you should be good to go. Windows users will have to complete a few additional steps, see the OS-specific installation instructions down below.


## General things

There are a few computing requirements for the course that are absolutely necessary:

1. You must have administrator access to your computer (i.e., you must be able to install things yourself without requesting IT approval).
2. You must have at least `20 GB` of free disk space on your computer (but we would recommend more, to be safe).
3. If you are using Windows you must be using Windows 10/11; Windows 7 and 8 will not be sufficient for this course.
4. Some parts of this course will make use of GitHub, so creating a GitHub account is recommended
5. For easier communication we've created a Discord Server for this programm, if you're interested install Discord and follow this [link](https://discord.gg/BEX7XRb8)

If you foresee any of these being a problem please reach out to one of the instructors too see what steps you can take to ensure you are ready for the course start.

## Some quick general notes on instructions

- If you have some of these things installed on your computer already that should (theoretically) be okay.
  However, you need to make sure that you are able to complete the steps described in `checking your install` (not there yet) section below without issue.
  - This is mainly to see if your Docker installation is actually working!

## OS-specific installation instructions

Select the tab that corresponds to your operating system and follow the instructions therein.

````{tab-set}
```{tab-item} Windows
**Bash shell - Windows Subsystem for Linux (WSL)**

Windows doesn't come with a preinstalled bash shell. To remedy this we will rely on [WSL (Windows subystems for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install), which will provide a Unix command-line based on the latest Ubuntu distribution.

1. Search for `Windows Powershell` in your applications; right click and select `Run as administrator`.
   Select `Yes` on the prompt that appears asking if you want to allow the app to make changes to your device.
2. Type the following into the Powershell and then press `Enter`:

       wsl --install

3. Press `Enter` again when prompted to reboot your computer.
4. You'll find a new apllication named "Ubuntu", this is your new command line tool. Right-click and run this app as administrator.
   - the first launch of the new Linux distribution may take some time as files need to be decompressed and stored
4. Upon opening the apllication you will be prompted to set up your Linux username and password
   - to make use of the command line you'll have to bascially create an deafult user account, which gives you the ability to run sudo (Super User Do) administrative commands
   - the account name should be simple and contain no extra characters or spaces, e.g. your initials or first name will usually do
   - `Note: When entering your password nothing will appear on the screen (blind typing), but you're input will still be registeres. Simply type a password and hit enter.
5. Make sure that Ubuntu is up-to-date by entering the following and hitting enter: `sudo apt update && sudo apt upgrade`
   - here you'll be asked for the password you set in the previous step

From this point on whenever the instructions specify to "open a terminal" please assume you are supposed to open the Ubuntu application.

! This will create a virtual Ubuntu application on your system. The terminal will alwyays start in your Ubuntu home directory, to access your windows file system you'll have to use the following path `/mnt/c/Users/yourusername`

**VSCode**

1. Go to https://code.visualstudio.com/ and click the download button, then run the `.exe` file.
2. Leave all the defaults during the installation with the following exception:
      - Please make sure the box labelled "Register Code as an editor for supported file types" is selected
3. When working with Linux under Windows using WSL you will have two different filesystems/drives since WSL will create a distinct filestystem for every Linux distribution you have installed. VSCode automatically detects WSL distributions and you can connect to them via the remote connection button (Blue button at the bottom left corner of your VSCode window). This is what it should look like:

!add screenshots here

**Docker**

Unfortunately, getting Docker to work on Windows is a tad more complicated. 

   1. Download the installer using the download button at the top of the page, or from the release notes. 
   2. Double-click Docker Desktop Installer.exe to run the installer. By default, Docker Desktop is installed at C:\Program Files\Docker\Docker. 
   3. When prompted, ensure that "Use WSL 2" instead of Hyper-V option on the Configuration page is selected. 
   4. If your system only supports one of the two options, you will not be able to select which backend to use. 
   5. Follow the instructions on the installation wizard to authorize the installer and proceed with the install. 
   6. When the installation is successful, select Close to complete the installation process. 
   7. Open Docker Dektop, agree to the the terms of service and login using your Dockerhub user credentials. Now, the Docker engine should start (if starting of the Docker engine takes more than 5 minutes, restart your computer).

`If your admin account is different to your user account, you must add the user to the docker-users group:`
   1. Run Computer Management as an administrator. 
   2. Navigate to Local Users and Groups > Groups > docker-users. 
   3. Right-click to add the user to the group. 
   4. Sign out and sign back in for the changes to take effect.
```

```{tab-item} Linux
**Bash shell**

You already have it!
Depending on which version of Linux you’re running you may need to type `bash` inside the terminal to access it (and hit enter).
To check whether this is necessary, follow these steps:

1. Open a terminal and type `echo $SHELL`.
   If it reads `/bin/bash` then you are all set!
   If not, whenever the instructions read "open a terminal," please assume you are to open a terminal, type `bash`, and the proceed with the instructions as specified.


**VSCode**

1. Go to https://code.visualstudio.com/ and click the download button for either the .deb (Ubuntu, Debian) or the .rpm (Fedora, CentOS) file.
1. Double-click the downloaded file to install VSCode.
   (You may be prompted to type your administrator password during the install).

-- explanation on how to acess wsl

**Docker**

1. You will be following different instructions depending on your distro ([Ubuntu](https://docs.docker.com/engine/install/ubuntu/), [Debian](https://docs.docker.com/engine/install/debian/), [Fedora](https://docs.docker.com/engine/install/fedora/), [CentOS](https://docs.docker.com/engine/install/centos/)).
   Make sure to follow the “Install using the repository” method!
1. Once you’ve installed Docker make sure to follow the [post-install instructions](https://docs.docker.com/engine/install/linux-postinstall/) as well.
   You only need to do the “Manage Docker as a non-root user” and “Configure Docker to start on boot” steps.
1. Open a new terminal and type `docker run hello-world`.
   A brief introductory message should be printed to the screen.
```

```{tab-item} MacOs
**Bash shell**

You already have it!
Newer versions of Mac OS will rely on a differnt standard, i.e. `zsh`, so we might need a few extra steps to setup your system.

1. To check which shell you're using open a terminal and type `echo $SHELL`.
   - If it reads `/bin/bash` then you are all set!
   - If it read `/bin/zsh we will need to make the following adjustments
2. Type `cat /etc/shells` and hit enter
   - under the list of accaeptable shells you should find `/bin/bash`, note down this path (in most cases it should just read /bin/bash)
3. Type `chsh -s /bin/bash` and hit enter (Note. `chsh` stands simply for "change shell", this process is harmless and reversible, no worries. For more info see the official [documentation](https://linux.die.net/man/1/chsh)))
4. Close and reopen your terminal
5. Verify that you're now using the bash shell via `echo $SHELL`

**VSCode**

1. Go to https://code.visualstudio.com/ and click the download button.
1. Unzip the downloaded file (e.g., `VSCode-darwin-stable.zip`) and moving the resulting `Visual Studio Code` file to your Applications directory.


**Docker**

1. Go to https://hub.docker.com/editions/community/docker-ce-desktop-mac/ and press “Get Docker”.
1. Open the “Docker.dmg” file that is downloaded and drag and drop the icon to the Applications folder
1. Open the Docker application and enter your password.
   An icon will appear in the status bar in the top-left of the screen.
   Wait until it reads “Docker Desktop is now up and running!”
1. Open a new terminal and type `docker run hello-world`.
   A brief introductory message should be printed to the screen.

(The above step-by-step Docker instructions are distilled from [here](https://docs.docker.com/docker-for-mac/install/).
If you have questions during the installation procedure please check that link for potential answers!)
```
````

**Note**: If the instructions aren't working and you have spent more than 15-20 minutes troubleshooting on your own, reach out on the #help-installation channel on the Discord channel with the exact problems you're having.
One of the instructors will try and get back to you quickly to help resolve the situation.
If they're unable to help via Discord, you may be directed to attend one of the installation office hours.


## GitHub account

Go to https://github.com/join/ and follow the on-screen instructions to create an account.
It is a good idea to associate this with your university e-mail (if you have one) as this will entitle you to sign up for the [GitHub Student Developer Pack](https://education.github.com/pack) or [GitHub for teachers](https://education.github.com/teachers) which come with some nice free bonuses.

## Discord

Go to https://discord.com/ and download and install Discord. Please note, that you can also use Discord through your browser if you don't want to download it.
You will be invited to the course channel via e-mail.

## Modern web browser

Install Firefox or Chrome.
(Safari will also work.)
Microsoft Edge is not modern, despite what Microsoft might try and otherwise tell you.



### Getting the workshop content

Now that you have installed the required software (or not) to follow the workshop, it's time to gather the respective
materials. Please use the `tab` matching your setup.

```{tabbed} Conda
<img src="https://upload.wikimedia.org/wikipedia/commons/e/ea/Conda_logo.svg" alt="conda logo" width="300"/>\
<sub><sup><sub><sup>https://upload.wikimedia.org/wikipedia/commons/e/ea/Conda_logo.svg</sup></sub></sup></sub>

By installing `Python` on your system (i.e. specifically `Conda`) and setting up the appropriate environment, you will be able to open all the `Jupyter Notebooks` and go through the whole content of the course locally. 

To get things up and running, please follow these steps:

1. Download the [`environment.yml`](https://raw.githubusercontent.com/peerherholz/docker_workshop/master/environment.yml) file (e.g. with right mouse click -> Save As). Make sure that the file ends with `.yml` and not `.txt`.
2. Open up a conda terminal (or any other terminal), and create a new conda environment with the following command: `conda env create -f /path/to/file/environment.yml` - For example ``conda env create -f ~/Downloads/environment.yml`
3. Download the notebooks in this repository via [this link](https://github.com/peerherholz/docker_workshop/archive/master.zip)) and unzip them to your preferred location, e.g. `Desktop/Python_for_Psychologists_Winter2021`.
4. Next, open up a `conda terminal` (or any other `terminal`), activate the `conda environment` with `conda activate pfp_2021` (or on older `conda environment` with `source activate pfp_2021` for `mac` and `linux` and `activate pfp_2021` for `windows`).
5. Finally, via the `terminal`, move to the folder where you've put all the unzipped content of this workshop, e.g. with the command `cd ~/Desktop/docker_workshop` and run the command `jupyter notebook`. If the `notebook server` isn't automatically opened in a new browser window, please copy-paste either the `http://127.0.0.1:8888/...` or the `http://localhost:8888/...` path into a new browser window and press `Enter`. You should now see the `jupyter notebook server` (looking like a file browser and displaying the content of the directory). 
```

```{tabbed} Jupyter NBViewer
<img src="https://nbviewer.jupyter.org/static/img/nav_logo.svg" alt="conda logo" width="300"/>\
<sub><sup><sub><sup>https://nbviewer.jupyter.org/static/img/nav_logo.svg</sup></sub></sup></sub>


If you want to go through the content of this workshop without installing anything on your machine, you should chose this approach. To see all the notebooks and slides from this workshop, please use this [Jupyter NBviewer link](https://nbviewer.jupyter.org/github/peerherholz/workshop_weizmann/blob/main/workshop/workshop_weizmann_overview.ipynb).
```

### Enter the matrix

Once you reached this point, you should be ready the enter the matrix and follow the workshop in your preferred way. Congrats, fantastic work!

![logo](https://media1.tenor.com/images/e5c21d98f56c4af119b4e14b6a9df893/tenor.gif?itemid=4011236)\
<sub><sup><sub><sup>https://media1.tenor.com/images/e5c21d98f56c4af119b4e14b6a9df893/tenor.gif?itemid=4011236</sup></sub></sup></sub>

