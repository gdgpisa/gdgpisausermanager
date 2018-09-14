# gdgpisausermanager
Welcome to the Google Developer Group Pisa bot. This bot is written in *python* and atm is not available on herokuapp.

The bot will be available on Telegram.

Feel free to fork this repo! Contributions are really appreciated. Please have a look at the [Contributing Guidelines](.github/CONTRIBUTING.md) or at the [TODO](#contributing-) list down there. You can easily start having a look at our [Issues](https://github.com/domenicoblanco/gdgpisausemanager.github.io/issues).

**Don't know where to start?** 🤔 have a look at our [**help wanted**](https://github.com/domenicoblanco/gdgpisausermanager.github.io/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) or [**good first issue**](https://github.com/domenicoblanco/gdgpisausermanager.github.io/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) tickets.

## Getting Started 🛠

To get starting developing, we really recommend to clone the bot locally and start developing on your machine. 

### Linux
1. Install [Python 2.7](https://www.python.org/) with your package manager.
```
Debian
sudo apt install python-2.7
```

2. Install [pip](https://pip.pypa.io/en/stable/installing/)
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

3. Install [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
```
Debian
pip install python-telegram-bot --upgrade
```
Or you can install from source with
```
git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
cd python-telegram-bot
python setup.py install
```

4. Start a chat with [BotFather](https://t.me/BotFather)

5. Use the ```/newbot``` command to create a new bot. The BotFather will ask you for a name and username, then generate an authorization token for your new bot.

6. Copy the token and paste it on the variable **TOKEN** inside the [python script](https://github.com/domenicoblanco/gdgpisausermanager.github.io/gdgpisausermanager.py)

7. Run
```
python gdgpisausermanager.py
```

## Contributing 🤝

Feel free to contribute to this project! You can have a look at our [Contribution guidelines](.github/CONTRIBUTING.md) if you don't know how to proceed.

Feel free to [open a issue](https://github.com/domenicoblanco/gdgpisausermanager.github.io/issues/new) or [submit a new pull request](https://github.com/domenicoblanco/gdgpisausermanager.github.io/pulls) ❤️

Here a short TODO list:

- [ ] Update this README with better instructions and a better English.
- [ ] Writing macOS setup steps to this Readme.
- [ ] Writing Windows setup steps to this Readme.
- [ ] Fix all issues
- [ ] Complete a stress test
- [ ] Clean-up the code folder.

## License 📄

This project is licensed under the MIT License - see the [License](License) file for details
