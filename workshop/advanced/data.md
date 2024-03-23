# Software containers & data


### Learning objectives

- get local data into containers
- get online data into containers
- bind mount input/output directories to a container during runtime

### Motivation

From time to time, it might be advised or even necessary to provide some data that comes with your Docker container, e.g. for reproducible purposes, tutorials, etc.
But how do we get data into our Docker containers? Well, there are two different ways of equipping your container with additional data:

1. One can either copy the data inside the container during its build. This way the respective data is permanently stored inside our image. As mentioned above, this functionality can come in handy if you want to provide tutorials or user-manuals to the end-user of your container or some test data to make sure the containers behaviour matches the expected behaviour.

2. However, sometimes it is required to get data into our container during runtime, e.g. if we have set-up an automated analysis workflow within our container and want the user to provide their own data, such that the analysis can be run on that data inside the container. To achieve this, we can **mount** a directory from our local computer to a directory within the container. This way we can give the container access to specific directories on our local computer, e.g. to load data from our machine into the container. Since mounting is a bidirectional process we can also allow the container to write outputs to sepcific directories on our local machine.
<br>

In the following sections, we will go over both ways of getting data inside your conatiner and provide some practical examples.


### Getting Data into a container permanently

Let's say we want to add a picture of a whale into our Docker container, because we're such docker fans and whales are nothing but awesome, buuut we've learned that the state of a given container cannot be permanently changed from the mounting part of this workshop.

So as we've already seen we can use the `COPY instruction` to add the data (i.e. our .png file) into our Docker container during its build.

So let's first build  a new build context + Dockerfile:

```
 mkdir docker_data_container
 touch docker_data_container/Dockerfile

```

Open the file with `VScode` and add the following line:

```
    FROM ubuntu:latest
```

Now we add the relevant file to our `build context`, i.e. we move the data you want to include in the same directory as the Dockerfile, e.g.

```
mv Desktop/happy_whale.jpg Desktop/docker_data_container
```

Now, we add a line to our Dockerfile that indicates that this image should be copied to a specific location inside our Docker container, e.g. /home/images

```
COPY ./happy_whale.jpg /home/images/happy_whale.jpg
```

And you guessed it: time to build!

```
docker build -t whale_container Desktop/docker_data_container
```

If we now `run` our freshly build Docker container and check the contents of /home, we find the folder images and in it our happy_whale.jpg

```
(base) Michaels-MacBook-Pro:Desktop me$ docker run -it --rm whale_container bash
root@8e2a056bed3a:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@8e2a056bed3a:/# cd home/
root@8e2a056bed3a:/home# ls
images
root@8e2a056bed3a:/home# cd images/
root@8e2a056bed3a:/home/images# ls
'happy_whale.jpg'
```

If this seems tedious or you have to copy a lot of files you can also directly add a number of files, i.e. from the current working directory where the `docker build` command is run, replace the above code with:

```
    COPY . /home/images
```

### Incorporating online data

In case you don't have or don't want everything that should go into the Docker container stored locally, you can also use command line functionality to download data, e.g., using the bash command `curl`. This can be very helpful when pulling data from an online repository.

Simply add the respective lines to the Dockerfile:

```
    RUN apt-get update && apt-get install curl -y
    RUN curl --output /home/images/happy_whale_2.jpg  https://cdn.pixabay.com/photo/2023/09/25/06/48/whale-8274342_1280.jpg

```

Rebuild and checking the outcome, everything worked like a charm!

```
    (base) Michaels-MacBook-Pro:Desktop me$ docker run -it --rm whale_container bash
    root@b41d20e42fbb:/# ls
    bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
    root@b41d20e42fbb:/# cd home/
    root@b41d20e42fbb:/home# cd images/
    root@b41d20e42fbb:/home/images# ls
    happy_whale.jpg  happy_whale_2.jpg
```

### Mounting data inside and outside of your container

Well, all of you should have heard plenty about mounting in our [quickstart](basics/quickstart.md) section. Once again, **mounting** describes a mapping from paths outside the container (e.g. your local machine or online data repositories) to paths inside the container.

<br>
Now, who remembers the flag we have to use within the `docker run` command to enable **mounting** ? ...

<br>

<details>
<summary>Solution</summary>

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

**Note on server system usage:** If you use a mounted directory to store output, produced inside your container, on your local filesystem, make sure that you have administrator rights on your own machine to access/modify the output. Since the container writes the output as a administrator, you will not be able to access/modify your data if you dont have superuser rights, e.g. when working on a compute server. One way to avoid this issue, is the user flag: `-u` which can be utilized within the `docker run` command as follows: 
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


#### Practical application

The probably most common use-case for mounts in the domain of neuroscientific research is the transfer of research data into and outside of the container. 

<br>

- better option than permanetly copying data into container since neuroimaging data is often lagre
- additionally helpful to create **permanent** outputs written to your **local system** , e.g. results of analysis (remember every file thats created inside a container is removed upon shutting down the container)
  
<br>

For demonstration purposes we have created an image that can be utilized to convert the `MNE-sample-dataset`, a test dataset provided by the [MNE community](https://mne.tools/stable/index.html), into the [BIDS](https://bids.neuroimaging.io/) format, a standardized way of organizing your neuroimaging data. MNE is an open-source tool for MEEG data processing and visualisation.

You can find the dataset in the `~/docker_workshop_oldenburg` directory on your local machine. Let's check if its stored where its supposed to be:

<br>

![mounted directory before docker run](/static/mounted_directory_before_docker_run.png)

```
aaronreer@FK6P-1158240:~/docker_workshop_oldenburg$ ls
MNE-sample-data
```

<br>

For our container to run the conversion properly, we need to mount the directory from our local system, containing our data to the `/input` directory of the container. Further, we need to mount the directory to which we want to container to write our BIDS converted data to the `output` folder of the container:

```
docker run \
-v /home/aaronreer/docker_workshop_oldenburg/MNE-sample-data/:/input/ \
-v /home/aaronreer/docker_workshop_oldenburg/:/output aaronreer1/ \
mne_conversion:firsttry
```


<details>
<summary>Output</summary>

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

</details>

<br>

When checking our filesystem using the `ls` command we can observe that a new directory called `MNE-sample-data-bids1` has appeared.

<br>

![mounted directory after docker run](/static/mounted_directory_after_docker_run.png)




### Docker & data - discussion

- What would you like to have in your Docker containers?
- What type of data are you planning on working with?
- Let us know and we'll go through the respective steps!


