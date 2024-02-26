![Python](https://img.shields.io/badge/python-v3.9.12-brightgreen.svg)
![Python](https://img.shields.io/badge/python-v3.7.6-yellow.svg)
![Static Badge](https://img.shields.io/badge/socket.io-client-orange)
![GitHub file size in bytes](https://img.shields.io/github/size/pete1328/Othello/client.py?color=pink)
![Lines of code](https://tokei.rs/b1/github/pete1328/Othello?color=purple&style=flat)
[![pylint](https://img.shields.io/badge/PyLint-8.80-brightgreen?logo=python&logoColor=white)
[![GitHub Workflow Status](https://github.com/pete1328/Othello/actions/workflows/python-client.yml/badge.svg)](https://github.com/pete1328/Othello/actions/workflows/python-client.yml)
![GitHub watchers](https://img.shields.io/github/watchers/pete1328/Othello)


# Othello Remote Client for JAR Game Board
Starter code developed with Python 3.7.0, tested with Python 2.7.10. Current files developed/tested with Python 3.9.12 and 3.7.6. All of the above should work but I primarily run in a Python 3.9.12 environment.

## Instructions
This client is compatable with a JAR Othello game board (file not attached). So, if you have access to said game board, start it up and...

To run the client, make sure the board server is started and run: `python client.py [optional port] [optional hostname]`

To run all unit tests, run `python -m unittest`
To run all tests in "test.py" tests, run `python -m unittest test`
To run the TestGetMove class in "test.py", run `python -m unittest test.TestGetMove`
To run the test_get_move_returns_a_valid_move test case in the TestGetMove class in "test.py", run `python -m unittest test.TestGetMove.test_get_move_returns_a_valid_move`

To run the test file that initiaties and tracks the results of 100 games, make sure the board server is started and run `python testOdds.py`

## Information
Client file developed by a 22 year old computer science graduate as part of a job application process. This main client program simulates a basic player that analyzes and chooses it's next move based on the current Othello game board. As of now, it is at an average win rate of 70.5 % (out of 400 games, with a mix of competing as player 1 or 2 against a random strategied opponent).

## Recommended Software
* Python 3.7 or 3.9
  * Included modules used: **sys**, **json**, and **socket**
* [Pyenv](https://github.com/pyenv/pyenv)
