# Software containers & data


### Learning objectives

- get local data into containers
- get online data into containers
- Datalad?

### Motivation

From time to time, it might be advised or even necessary to provide some data that comes with your Docker container, e.g. for reproducible purposes, tutorials, etc.
But how do we get data into our Docker containers?

``
what else?
....
....
....

``


### Getting Data into a container

Let's say we want to put a picture of whale into our Docker container because we're such docker fans and whales are nothing but awesome, but we've learned that the state of a given container cannot be changed from the mounting part of this workshop.

We can achieve this by copying the datan(i.e. our .png file) into our Docker container during its build, hence must include respective instruction in our Dockerfile.
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

### Practical application

With that, we can include almost any kind of data of almost any size. As we not only like Docker, but also data processing using e.g., pandas and sharing our knowledge about it, let's include a small respective tutorial in the form of a `jupyter notebook`, as well as a small `sample dataset`. In this way you could also include demogrpahic data, READMEs or any additional data necessary for a processing pipeline.

To this end, we again simply copy the respective files from the examples folder to out my_first_docker folder

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


### Input/Output - administrator rights

- notes re folder structures here
- input

### Datalad?

- might be too much time investment or too confusing if kept too short, instead replace by a scientific example??


### Docker & data - discussion

- What would you like to have in your Docker containers?
- What type of data are you planning on working with?
- Let us know and we'll go through the respective steps!
