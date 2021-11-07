# Printer LMS

> A IS212 Project - Do you want to build a LMS?

## Development

### Pre-requisites

1. Docker

1. [Node.js v14](https://nodejs.org/en/download/)

1. [Vue CLI](https://cli.vuejs.org/guide/installation.html)

### Instructions

#### Main

Run the following commands

```bash
# clone the repo
git clone https://github.com/the-weds-meetup/printerLMS.git

# create docker-compose.yml
cp docker-compose.yml.example docker-compose.yml

# run the containers
docker compose up

# open localhost:5000 on your browser to access the backend server

# remove containers and images
docker compose down --rmi all
```

### Testing

Run the following command

```bash
# enter the backend dir
cd ./backend

# ensure you installed all the modules within Requirements.txt
pip install -r requirements.txt
# pip3 install -r requirements.txt

# Run integration_test.py
python -m unittest integration_test
```
