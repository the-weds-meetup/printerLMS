# Printer LMS

> A IS212 Project - Do you want to build a LMS?

## Development

Run the following commands

```bash
# clone the repo
git clone https://github.com/the-weds-meetup/printerLMS.git

# create docker-compose.yml
cp docker-compose.yml.example docker-compose.yml

# replace ${MOODLE_DOCKER_WWWROOT} with the path to your code
# e.g. let  `MOODLE_DOCKER_WWWROOT=./src`, thus:
# volumes:
#   - "./src:/var/www/html"

# run the containers
docker compose up

# open localhost:3000 on your browser

# any files you change in ${MOODLE_DOCKER_WWWROOT} will be reflected in the browser
```

### Optional

> Set up a php code formatter.
>
> Make sure you have npm (or yarn) installed
>
> Credits to [prettier/plugin.php](https://github.com/prettier/plugin-php)

```bash
# use npm
npm -i # install dependencies
npm run prettier path/to/file.php --write # format your code

# use yarn
yarn install # install dependencies
yarn run prettier path/to/file.php --write # format your code

```

#### Limitations of prettier/plugin-php

### Pre-requisites

1. Docker

1. [Node.js v14](https://nodejs.org/en/download/) (Optional)
