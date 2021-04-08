
# gdgpisausermanager

Welcome to the Google Developer Group Pisa bot. This bot is written in *python* and atm is not available on herokuapp.

  

The bot will be available on Telegram.

  

Feel free to fork this repo! Contributions are really appreciated. Please have a look at the [Contributing Guidelines](.github/CONTRIBUTING.md) or at the [TODO](#contributing-) list down there. You can easily start having a look at our [Issues](https://github.com/gdgpisa/gdgpisausermanager/issues).

  

**Don't know where to start?** 🤔 have a look at our [**help wanted**](https://github.com/gdgpisa/gdgpisausermanager/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) or [**good first issue**](https://github.com/gdgpisa/gdgpisausermanager/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) tickets.

  

## Getting Started 🛠

  

To get starting developing, we really recommend to clone the bot locally and start developing on your machine.

  

1. Install [Python 3.9](https://www.python.org/) with your package manager.

- Debian: `sudo apt install python-3.9`

- Ubuntu: `sudo apt-get install python-3.9`

- Windows: [download from website](https://www.python.org/downloads/)

- macOS: [Install Brew](https://brew.sh) and launch `brew install python@3.9`

  

2. Install [pip](https://pip.pypa.io/en/stable/installing/)

- Debian/Ubuntu/MacOS: `curl https://bootstrap.pypa.io/get-pip.py | sudo python -` (you may need to use `python3` instead of `python`)

- Windows: python comes already with pip installed, just update it with `python -m pip install --upgrade pip`

  

3. Install [gdg-pisa-user-manager](https://github.com/gdgpisa/gdgpisausermanager)

```

python -m pip install git+https://github.com/gdgpisa/gdgpisausermanager --upgrade

# If the command above fails, try with

python -m pip install https://github.com/gdgpisa/gdgpisausermanager/archive/master.zip --upgrade

```

(you may need to use `python3` instead of `python`)

  

4. Start a chat with [BotFather](https://t.me/BotFather)

  

5. Use the ```/newbot``` command to create a new bot. The BotFather will ask you for a name and username, then generate an authorization token for your new bot.

  

6. Copy the token into `.telegram.token` file or set an environment variable called `TELEGRAM_TOKEN`. The content will be read by [`Config.TOKEN`](https://github.com/gdgpisa/gdgpisausermanager/blob/master/config.py#L7)

  

7. Run

```

gdg-pisa-user-manager

```

  

## Docker

For whom who prefers to use a Docker container, there's a Dockerfile based on Python 3.9 and Alpine. In order to start this container we need to install Docker and Docker Compose.

  

1. Install Docker

- Debian: Follow [Docker's official guide](https://docs.docker.com/engine/install/debian/)

- Ubuntu: Follow [Docker's official guide](https://docs.docker.com/engine/install/ubuntu/)

- macOS: [Install Brew](https://brew.sh) and launch `brew install docker`

  

2. Install Docker Compose

- Debian/Ubuntu: `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

- macOS: `brew install docker-compose`

  

3. Clone or download this repository

  

4. Preparing Docker Compose

In the same path as the precedent step, create or append to `docker-compose.yml`

```

gdgpisausermanager:

image: gdgpisausermanager

build: ./gdgpisausermanager

container_name: gdgpisausermanager

environment:

- TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

restart: unless-stopped

```

⚠️ Be sure to replace `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` with your actual token, this is just an example from [Telegram](https://core.telegram.org/bots/api#authorizing-your-bot).

If you're not sure about how to obtain your token, please refer to step 4 of [Getting started](https://github.com/gdgpisa/gdgpisausermanager#getting-started-)

  

5. Launch container 🎉

`docker-compose up -d`

  

### ⚠️ Modifying `gdgpisausermanager` folder

If you made some changes to `gdgpisausermanager` you need to completely remove the container, use `docker-compose up --build --force-recreate --no-deps gdgpisausermanager`.

After this, it's **strongly** suggested to also cleanup the environment with `docker system prune`.

  

## Contributing 🤝

  

Feel free to contribute to this project! You can have a look at our [Contribution guidelines](.github/CONTRIBUTING.md) if you don't know how to proceed.

  

Feel free to [open a issue](https://github.com/gdgpisa/gdgpisausermanager/issues/new) or [submit a new pull request](https://github.com/gdgpisa/gdgpisausermanager/pulls) ❤️

  

Here a short TODO list:

  

- [ ] Update this README with better instructions and a better English.

-  [x] Writing macOS setup steps to this Readme.

-  [x] Writing Windows setup steps to this Readme.

- [ ] Fix all issues

- [ ] Complete a stress test

- [ ] Clean-up the code

  

## License 📄

  

This project is licensed under the MIT License - see the [License](https://github.com/gdgpisa/gdgpisausermanager/blob/master/LICENSE) file for details