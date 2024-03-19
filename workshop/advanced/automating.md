# Automating software containers

If you have an project that is in development or you created a programm that will be maintained for the forseeable future, it can beconme tedious to constantly re-build your Docker Containers locally. Fortunately, there is a way to automate this process using GitHub, more specifically GitHub Workflows. The following is going to discuss how to setup a project repository, how to add the relevant workflow and how to update your container with a simple push.

This will not only make your life easier, but integrate Docker in reproducible, in terms of version-controlled, scientific practice. The actual goal of this workshop, no?

### Automating builds using Github

Github workflow explanation ...

1. Set up
The setup is simple and straightforward, as we just need to create a new GitHub repository in which we store our Dockerfile:

   - create a new Github repository called docker_workshop
   - set it up with your usual directory structure etc
   - upload your Dockerfile to this repository


So far, so simple, but to automate the build process we'll need to add a few things to our repository


2. Generate a DockerHub access token
    - head to DockerHub
    - click on your profile in the top right and select my account
    - under `security` click `create new acces token`
        - the name of the access token should match the name of your Github repository
        - grant read, write and delete permissions and click on generate
    - a new dialogue box will pop-up, copy the displayed access token (we'll make use of this in the next section)

[new_access_token](static/new_access_token.png)

3. Setup GitHub secrets
    - head to your Github repository
    - click on `settings` -> `secrets and variables` -> `actions`
    - next we will create two new GitHub "secrets" 
        - click on `new repository secret` and enter the name `DOCKERHUB_USERNAME`
            - under the `secret` heading add your DockerHub Username
        - click on `new repository secret` and enter the name `DOCKERHUB_TOKEN`
            - under the `secret` heading add the `DockerHub access token` we've copied in the previous step


!!! actions_secrets

[actions_secrets](static/actions_secrets.png)


4. Setup the Github workflow
    - go to your GitHub repo, create a new file called  `.GitHub/workflows/container_build_publish.yml`

    - copy and paste the following code into the file, make sure to replace the following part with your docker image name
        -       tags: |
                    yourhubusername/yourimagename:latest 


    ```

        name: Build and Publish Container

        on:
        # run it on push to the default repository branch
        push:
            branches: [main]
        # run it during pull request
        pull_request:

        jobs:
        # define job to build and publish docker image
        build-and-push-docker-image:
            name: Build Docker image and push to repositories
            # run only when code is compiling and tests are passing
            runs-on: ubuntu-latest

            # steps to perform in job
            steps:
            - name: Checkout code
                uses: actions/checkout@v3

            # setup Docker buld action
            - name: Set up Docker Buildx
                id: buildx
                uses: docker/setup-buildx-action@v2

            - name: Login to DockerHub
                uses: docker/login-action@v2
                with:
                username: ${{ secrets.DOCKERHUB_USERNAME }}
                password: ${{ secrets.DOCKERHUB_TOKEN }}

            - name: Login to Github Packages
                uses: docker/login-action@v2
                with:
                registry: ghcr.io
                username: ${{ github.actor }}
                password: ${{ secrets.GITHUB_TOKEN }}
            
            - name: Build image and push to Docker Hub and GitHub Container Registry
                uses: docker/build-push-action@v2
                with:
                # relative path to the place where source code with Dockerfile is located
                context: ./
                # Note: tags has to be all lower-case
                tags: |
                    yourhubusername/yourimagename:latest 
                # build on feature branches, push only on main branch
                push: ${{ github.ref == 'refs/heads/main' }}

            - name: Image digest
                run: echo ${{ steps.docker_build.outputs.digest }}

        ```
    

5. Check your GitHub action settings
    - in your GitHub repo, click `settings` -> `actions` -> `general`
    - make sure that 
        - under `Action permissions` you've selected `Allow all actions and reusable workflows`


[actions_permissions](static/actions_permissions.png)


        - under `Workflow permissions` you've selected `Read and write permissions` and `Allow GitHub Actions to create and approve pull requests`


[workflows_permissions](static/workflows_permissions.png)

6. Start the actions workflow

Every consecutive push or commit to this GitHub repository will now trigger a new build, hence your Docker container remains nicely up to date without any additional effort.

    - to test if your workflow works we therefore can simply commit or push a change, i.e.
        - update a file online, e.g. you could add or update the `README` file of your repo
        - push a change from your local machine to your online repo

    - Following go to the `actions` section of your GitHub repository
        - under workflow runs you should see either the current workflow still running or see the previous runs
            - a green checkmark indicated that your workflow has run successfully, a red cross that the worklfow failed
            - in either case you can click on the workflow in question to get more info (e.g. to check what went wrong)

[workflows](static/workflows.png)


    - If you check back on DockerHub, you should now see your updated Docker image



[docker_image_uploaded](static/docker_image_uploaded.png)




