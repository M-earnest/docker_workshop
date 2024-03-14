
# Step 1: Use the newest Ubuntu version as a base image
FROM ubuntu:latest

# Step 2: Set the working directory
WORKDIR /project

# Step 3: Install Python 3.10, and some Python packages (e.g.    Pandas) via the Ubuntu package manager apt
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    pip3 install pandas

RUN mkdir /info

# Step 4: Copy our Python script into the container
COPY print_info.py /info/
COPY README.md /info/README.md

# Step 5: Specify the command to run the Python script
CMD ["cat", "/info/README.md"]
#CMD ["python3", "print_info.py"]



