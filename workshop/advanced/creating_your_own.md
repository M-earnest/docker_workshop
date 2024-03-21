# Creating your own software container

Now it's time to build your own image. 

Ideally you can already start thinking about the needs/dependencies of your existing projects and build a `proxy-Dockerfile` containing all the neccesary instructions, so that later on you'll only have to exchange the necessary file and pathnames according to your needs. 

For this you can feel free to create a new Dockerfile by hand, adapt one of our examples or use neurodocker for the heavy lifting.

Here are also a few more things you should consider (special thanks to Peer Herholz, again!)

![depiction of what to consider when creating a project, i.e. software-, os-, data-dependencies](/static/software_container_considerations.png)


