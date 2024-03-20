# Software containers & data


### Learning objectives

- get local data into containers
- get online data into containers
- learn different ways of getting data into containers (e.g. store them in container or mount them into container during runtime)

### Motivation

From time to time, it might be advised or even necessary to provide some data that comes with your Docker container, e.g. for reproducible purposes, tutorials, etc.
But how do we get data into our Docker containers? Well, there are two different ways of equipping your container with additional data:

1. One can either copy the data inside the container during its build. This way the respective data is permanently stored inside our image. As mentioned above, this functionality can come in handy if you want to provide tutorials or user-manuals to the end-user of your container or some test data to make sure the containers behaviour matches the expected behaviour. 
2. However, sometimes it is required to get data into our container in a more generic way during runtime, e.g. if we have set-up an automated analysis workflow within our container and want the user to provide their own data, such that the analysis can be run on that data inside the container. To achieve this, we can **mount** a directory from our local computer to a directory within the container. This way we can give the container access to specific directories on our local computer, e.g. to load data from our machine into the container. Since mounting is a bidirectional process we can also allow the container to write outputs to sepcific directories on our local machine.
<br>

In the following sections, we will go over both ways of getting data inside your conatiner and provide some practical examples.



### Getting Data into a container permanently

Let's say we want to put a picture of whale into our Docker container because we're such docker fans and whales are nothing but awesome, but we've learned that the state of a given container cannot be changed from the mounting part of this workshop.

We can achieve this by copying the data (i.e. our .png file) into our Docker container during its build, hence must include respective instruction in our Dockerfile.
The easiest way is to store the data you want to include in the same directory as the Dockerfile, e.g.

    ```
        mv Desktop/happy_whale.jpg Desktop/my_first_docker
    ```

Now, we add a line to our Dockerfile that indicates that this image should be copied to a specific location inside our Docker container, e.g. /home/images

    ```
        COPY ./happy_whale.jpg /home/images/happy_whale.jpg
    ```

And you guessed it: time to rebuild!

    ```
        docker build -t myfirstdocker Desktop/my_first_docker
    ```

If we now run our freshly build Docker container and check the contents of /home, we find the folder images and in it our happy_whale.jpg

```
Michaels-MBP:~ me$ docker run -it --rm myfirstdocker

- ls

```

#### Practical application

With that, we can include almost any kind of data of almost any size. As we not only like Docker, but also data processing using e.g., pandas and sharing our knowledge about it, let's include a small respective tutorial in the form of a `jupyter notebook`, as well as a small `sample dataset`. In this way you could also include demogrpahic data, READMEs or any additional data necessary for a processing pipeline.

To this end, we again simply copy the respective files from the examples folder to our my_first_docker folder

    ```
        mv Desktop/examples/* Desktop/my_first_docker
    ```

And subsequently, we again add some lines of code that do the respective copying, creating a nice structure:

    ```
        COPY ./python_pandas.ipynb /home/notebooks/
        COPY ./beers.csv /home/notebooks/data
    ```

- rebuild the container and as expected, everything is there and in place!


    ``` 
        output
    ```

### Incorporating online data

In case you don't have or don't want everything that should go into the Docker container stored locally, you can also use command line functionality to download data, e.g., using the bash command `curl`. This can be very helpful when pulling data from an online repository.

Simply add the respective command to the Dockerfile:

```
    RUN curl --output /home/images/happy_whale_2.jpg  https://cdn.pixabay.com/photo/2017/01/01/20/11/humpback-whale-1945416_960_720.jpg
```

And checking the outcome, everything worked like a charm!

```
    output
```
### Mounting data inside and outside of your container

Well, all of you should have heard about mounting before in our [quickstart](basics/quickstart.md) section. Once again, **mounting** describes a mapping from paths outside the container (e.g. your local machine or online data repositories) to paths inside the container.
<br>
Now, who remembers the flag we have to use within the `docker run` command to enable **mounting** ? ...

<br>

<details>
<summary>flag for mounting</summary>

...correct, you have to use the `-v` flag within the `docker run` command to specify the mounted directories. This flag can be untilized as follows:

```
docker run -v path/outside/container:/path/inside/container name_of_image
```

</details>

<br>

You can also restrict the rights of mounted paths, e.g. read-only in case any modification on your local system should be prevented. This ca be done by adding a `:ro`. It should look something like this: 
<br> 

```
docker run -v path/outside/container:/path/inside/container:ro name_of_image
``` 

<br>
<br>

**Note:** If you use a mounted directory to store output, produced inside your container, on your local filesystem, make sure that you have administrator rights on your own machine to access/modify the output. Since the container writes the output as a administrator, you will not be able to access/modify your data if you dont have superuser rights, e.g. when working on a compute server. One way to avoid this issue, is the user flag: `-u` which can be utilized within the `docker run` command as follows: 
```
docker run -u <userid> name_of_image
```

<br>

How do I get my `userid`?
Well, thats easy! Simply type 
```
id -u <yourusername>
``` 
into your terminal and your `userid` should appear.
<br>

![how to get user id](/static/get_user_id.png)

<br>
Add practical example here?

#### Practical application

The probabaly most common use-case for mounts in the domain of neuroscientific research is the transfer of research data into and outside of the container. 
<br>
- better option than permanetly copying data into container since neuroimaging data is often heavy
- additionally helpful to create **permanent** outputs written to your **local system** , e.g. results of analysis (remember every file thats created inside a container is removed upon shutting down the container)
  
<br>

For demonstration purposes we have created an image that can be utilized to convert the `MNE-sample-dataset`, a test dataset provided by the [MNE community](https://mne.tools/stable/index.html). MNE is a tool for MEEG data processing and visualisation.

We have stored the `MNE-sample-dataset` in the following location `~/data`. Let's check if its stored where its supposed to be:

<br>

![mounted directory before docker run](/static/mounted_directory_before_docker_run.png)

<br>

For our container to run the conversion properly, we need to mount the directory from our local system, which containing our data to the `/input` directory of the container. Further, we need to mount the directory to which we want to container to write our BIDS converted data to the `output` folder of the container:


<div style="overflow-y: scroll; height: 200px; border: 1px solid #cccccc; padding: 5px; margin-bottom: 20px;">

    ```
        # Step 1: Use the newest Ubuntu version as a base image
        <span style="color:blue"># test1</span>
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

</div>

<div style="overflow-y: scroll; height: 200px; border: 1px solid #cccccc; padding: 5px; margin-bottom: 20px;">

```
    # Output:
    <span style="color:blue"># test1 :</span>
    Opening raw data file /input/MEG/sample/sample_audvis_raw.fif...
        Read a total of 3 projection items:
            PCA-v1 (1 x 102)  idle
            PCA-v2 (1 x 102)  idle
            PCA-v3 (1 x 102)  idle
        Range : 25800 ... 192599 =     42.956 ...   320.670 secs
    Ready.
    Opening raw data file /input/MEG/sample/ernoise_raw.fif...
    Isotrak not found
        Read a total of 3 projection items:
            PCA-v1 (1 x 102)  idle
            PCA-v2 (1 x 102)  idle
            PCA-v3 (1 x 102)  idle
        Range : 19800 ... 85867 =     32.966 ...   142.965 secs
    Ready.
    Opening raw data file /input/MEG/sample/sample_audvis_raw.fif...
        Read a total of 3 projection items:
            PCA-v1 (1 x 102)  idle
            PCA-v2 (1 x 102)  idle
            PCA-v3 (1 x 102)  idle
        Range : 25800 ... 192599 =     42.956 ...   320.670 secs
    Ready.
    Opening raw data file /input/MEG/sample/ernoise_raw.fif...
    Isotrak not found
        Read a total of 3 projection items:
            PCA-v1 (1 x 102)  idle
            PCA-v2 (1 x 102)  idle
            PCA-v3 (1 x 102)  idle
        Range : 19800 ... 85867 =     32.966 ...   142.965 secs
    Ready.
    Writing '/output/MNE-sample-data-bids1/README'...
    Writing '/output/MNE-sample-data-bids1/participants.tsv'...
    Writing '/output/MNE-sample-data-bids1/participants.json'...
    Writing of electrodes.tsv is not supported for data type "meg". Skipping ...
    Writing '/output/MNE-sample-data-bids1/dataset_description.json'...
    Writing '/output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/meg/sub-emptyroom_ses-20021206_task-noise_meg.json'...
    Writing '/output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/meg/sub-emptyroom_ses-20021206_task-noise_channels.tsv'...
    Copying data files to sub-emptyroom_ses-20021206_task-noise_meg.fif
    Reserving possible split file sub-emptyroom_ses-20021206_task-noise_split-01_meg.fif
    Writing /output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/meg/sub-emptyroom_ses-20021206_task-noise_meg.fif
    Closing /output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/meg/sub-emptyroom_ses-20021206_task-noise_meg.fif
    [done]
    Writing '/output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/sub-emptyroom_ses-20021206_scans.tsv'...
    Wrote /output/MNE-sample-data-bids1/sub-emptyroom/ses-20021206/sub-emptyroom_ses-20021206_scans.tsv entry with meg/sub-emptyroom_ses-20021206_task-noise_meg.fif.
    Writing '/output/MNE-sample-data-bids1/participants.tsv'...
    Writing '/output/MNE-sample-data-bids1/participants.json'...
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_coordsystem.json'...
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_coordsystem.json'...
    Used Annotations descriptions: ['Auditory/Left', 'Auditory/Right', 'Button', 'Smiley', 'Visual/Left', 'Visual/Right']
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_events.tsv'...
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_events.json'...
    Writing '/output/MNE-sample-data-bids1/dataset_description.json'...
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_meg.json'...
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_channels.tsv'...
    Copying data files to sub-01_ses-01_task-audiovisual_run-1_meg.fif
    Reserving possible split file sub-01_ses-01_task-audiovisual_run-1_split-01_meg.fif
    Writing /output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_meg.fif
    Closing /output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_task-audiovisual_run-1_meg.fif
    [done]
    Writing '/output/MNE-sample-data-bids1/sub-01/ses-01/sub-01_ses-01_scans.tsv'...
    Wrote /output/MNE-sample-data-bids1/sub-01/ses-01/sub-01_ses-01_scans.tsv entry with meg/sub-01_ses-01_task-audiovisual_run-1_meg.fif.
    Writing fine-calibration file to /output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_acq-calibration_meg.dat
    Writing crosstalk file to /output/MNE-sample-data-bids1/sub-01/ses-01/meg/sub-01_ses-01_acq-crosstalk_meg.fif
    |MNE-sample-data-bids1/
    |--- README
    |--- dataset_description.json
    |--- participants.json
    |--- participants.tsv
    |--- sub-01/
    |------ ses-01/
    |--------- sub-01_ses-01_scans.tsv
    |--------- meg/
    |------------ sub-01_ses-01_acq-calibration_meg.dat
    |------------ sub-01_ses-01_acq-crosstalk_meg.fif
    |------------ sub-01_ses-01_coordsystem.json
    |------------ sub-01_ses-01_task-audiovisual_run-1_channels.tsv
    |------------ sub-01_ses-01_task-audiovisual_run-1_events.json
    |------------ sub-01_ses-01_task-audiovisual_run-1_events.tsv
    |------------ sub-01_ses-01_task-audiovisual_run-1_meg.fif
    |------------ sub-01_ses-01_task-audiovisual_run-1_meg.json
    |--- sub-emptyroom/
    |------ ses-20021206/
    |--------- sub-emptyroom_ses-20021206_scans.tsv
    |--------- meg/
    |------------ sub-emptyroom_ses-20021206_task-noise_channels.tsv
    |------------ sub-emptyroom_ses-20021206_task-noise_meg.fif
    |------------ sub-emptyroom_ses-20021206_task-noise_meg.json
    aaronreer@FK6P-1158240:~/data$
```

</div>

<br>

When checking our filesystem using the `ls` command we can observe that a new directory called `MNE-sample-data-bids1` has appeared.

<br>

![mounted directory after docker run](/static/mounted_directory_after_docker_run.png)

### Input/Output - administrator rights

- notes re folder structures here
- input


### Docker & data - discussion

- What would you like to have in your Docker containers?
- What type of data are you planning on working with?
- Let us know and we'll go through the respective steps!


