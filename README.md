## Welcome to the MyMoney App
‘MyMoney’ is a platform that lets investors track their consolidated portfolio value across equity, debt, and gold.

## Installation and usage

### Installation

If you are on a Mac or Linux machine, you most likely already have Python3.x installed. Windows users can follow [this excellent tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10). There are more advanced configuration instructions at the [official Python website](https://docs.python.org/3/using/index.html).

We first need to make sure that we install `pip` and `virtualenv` for the correct version of Python (3.7 or later) on your computer. Open a terminal and run the following command:
```shell
$ python3 --version
```

`pip` is included in Python 3.4+ installations, so just install `virtualenv` with:
```shell
$ python3 -m pip install virtualenv
```

Create mymoney workspace directory:
```shell
$ mkdir mymoney_workspace && cd mymoney_workspace
```

Create a virtual environment:
```shell
$ python3 -m venv ./venv
```

Now activate the virtual environment:
```shell
$ source venv/bin/activate
```
> NOTE: You will need to activate your environment before every session of testing the app.

Download the mymoney zip file and unzip it:

To unzip on Mac run: 
```shell
$ unzip mymoney.zip
```

When you are done, you should be able to see two directories under `money_workspace' like the one below.
```shell
EXAMPLE:

$ tree -L 1                                                                                                                 
.
├── mymoney
├── mymoney.zip
└── venv

2 directories, 0 files
```

### Building and running the solution

 `geektrust.py`. This is the file that will contain your main method.

This file receive in the command line argument and parse the file passed in. Once the file is parsed and the application processes the commands, it will only print the output.

We build and run the solution by using the following commands

```
cd mymoney
python3 -m pip install -r requirements.txt
python3 -m geektrust sample_inputs/not_rebalaceable.txt
python3 -m geektrust sample_inputs/rebalaceable.txt

```

# Unit tests

For Python we currently support only the inbuilt [unittest](https://docs.python.org/3/library/unittest.html) framework. For test coverage we use [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/) framework. 

The unit tests are checked by the command -

```
python3 -m unittest discover tests
```

The unit test coverage is found by the command -

```
coverage run -m unittest discover tests
```
