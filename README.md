# Testinfra
With Testinfra you can write unit tests in Python to test actual state of your servers configured by management tools like Salt, Ansible, Puppet, Chef and so on.

It has the capability of using various bakends to connect to servers where the test cases are being run, i.e. local, paramiko, docker, podman, ssh, salt, ansible etc. In this repository the ansible backend will be used.

# Prerequisites
- Some Python programming knowledge
- Vagrant: https://learn.hashicorp.com/tutorials/vagrant/getting-started-install?in=vagrant/getting-started
- VirtualBox: https://www.virtualbox.org/wiki/Downloads
- Python (at least version 3.8 or higher): https://www.python.org/downloads/
- pip: https://pip.pypa.io/en/stable/installing/
- pipenv
    ```bash
    pip install pipenv --user
    ```

# Exercise 1: Setup Python virtual environment
When all the prerequisites have been installed, proceed with installing the python libraries. These are defined in the [Pipfile](./Pipfile).

Installing the libraries can be done in the terminal
```bash
pipenv install
```

# Exercise 2: Start Vagrant VM's
There are 2 vm's defined inside [Vagrantfile](./Vagrantfile) which we will use for testing. In the terminal start these 2 vm's.

```bash
vagrant up
```

# Exercise 3: Setup Ansible inventory
Testinfra can use multiple methods to connect to servers where the unit tests should run. During these excercises Ansible will be used. Similar to Ansible, we need to define our inventory with servers.
Edit [inventories/vagrant.ini](./inventories/vagrant.ini) and fill in the details about the 2 vm's defined in the [Vagrantfile](./Vagrantfile).

When the inventory is ready, test if ansible can reach them by executing an ansible ping

```bash
pipenv run ansible all -m ping -i inventories/vagrant.ini
```

This command should return a pong, like below
```json
server1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
server2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

# Exercise 4: Write a first unit test
For Vagrant we are using CentOS 7 as a base image, we will write a test case that verifies that the vm is CentOS version 7.8.

Checking system information can be done using the SystemInfo module (https://testinfra.readthedocs.io/en/latest/modules.html#systeminfo).

Create a file in [exercise/vagrant_test.py](exercise/vagrant_test.py) with the following contents:

```python
import logging
import testinfra
import pytest
import pytest_check as check
import requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

def test_os_type(host):
    """Check that we are running at minimum CentOS 7"""
    os_type = check.is_true(host.system_info.type == "linux")
    os_distro = check.is_true(host.system_info.distribution == "centos")
    os_release = check.is_true(host.system_info.release == "7")

    if os_type and os_distro and os_release:
        logger.info(f"{host} is running linux centos 7")
    else:
        logger.error(f"{host} is not running linux centos 7")
```

Now we can run the unit test by executing the following command in the root of the project.

```bash
pipenv run py.test -v --html=vagrant_test.html --self-contained-html --ansible-inventory=inventories/vagrant.ini.answer --connection=ansible exercise/vagrant_test.py --capture sys -rPs
```

The output will be similar below when all the test cases have passed

```bash
exercise/vagrant_test.py::test_os_type[ansible://server1] 
--------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------
2021-03-18 13:41:34 [    INFO] <testinfra.host.Host ansible://server1> is running linux centos 7 (vagrant_test.py:17)
PASSED                                                                                                                                                        [ 50%]
exercise/vagrant_test.py::test_os_type[ansible://server2] 
--------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------
2021-03-18 13:41:35 [    INFO] <testinfra.host.Host ansible://server2> is running linux centos 7 (vagrant_test.py:17)
PASSED                                                                                                                                                        [100%]

============================================================================== PASSES ===============================================================================
__________________________________________________________________ test_os_type[ansible://server1] __________________________________________________________________
------------------------------------------------------------------------- Captured log call -------------------------------------------------------------------------
INFO     root:vagrant_test.py:17 <testinfra.host.Host ansible://server1> is running linux centos 7
__________________________________________________________________ test_os_type[ansible://server2] __________________________________________________________________
------------------------------------------------------------------------- Captured log call -------------------------------------------------------------------------
INFO     root:vagrant_test.py:17 <testinfra.host.Host ansible://server2> is running linux centos 7
----------------------------------- generated html file: file:///home/amresh/Projects/ziggo/cdaas/testinfra-kt/vagrant_test.html ------------------------------------
========================================================================= 2 passed in 1.98s =========================================================================
```

After the tests have run, we also get an html report [vagrant_test.html](vagrant_test.html)

# Code Structure
The test in exercise 3 showed how we can run a unit test on each vagrant vm. Now we will dive into the parts of the code.

Like any Python program we can import any libraries we need. Lines 1 until 4 are needed by testinfra, this will import the libraries for logging, unit testing and testinfra.

Line 5 is not needed by testinfra, but to illustrate that we can import any library we need. For testing url's for example we can import the python requests library.

Line 7 and 8 and will set up our basic logger, we can use the logger to print out any output we need.

Line 10 is the test function in which the logic is described for our unit test. Note that every test function should start with **test_** in order to be executed as a unit test.

Lines 12 until 14 are calling the pytest_check and testinfra libraries. These will check the host information and return True or False to the variables.

In Lines 16 until 19 the information is returned back to the logger. If all of the variables are true, then the test has passed and we can return an INFO with a descriptive text. If one of the variables is false, we return an ERROR.

```python
1. import logging
2. import testinfra
3. import pytest
4. import pytest_check as check
5. import requests
6.
7. logging.basicConfig(level=logging.ERROR)
8. logger = logging.getLogger()
9.
10. def test_os_type(host):
11.     """Check that we are running at minimum CentOS 7"""
12.     os_type = check.is_true(host.system_info.type == "linux")
13.     os_distro = check.is_true(host.system_info.distribution == "centos")
14.     os_release = check.is_true(host.system_info.release == "7")
15.
16.     if os_type and os_distro and os_release:
17.         logger.info(f"{host} is running linux centos 7")
18.     else:
19.         logger.error(f"{host} is not running linux centos 7")
```

# Exercise 5: Test if openssh is installed
For this exercise we want to if the package **openssh-server** is installed on the vm's. Explore the package module of testinfra [https://testinfra.readthedocs.io/en/latest/modules.html#package](https://testinfra.readthedocs.io/en/latest/modules.html#package) and create a new test function in [exercise/vagrant_test.py](exercise/vagrant_test.py)

When the function is implemented, run the unit tests and verify that the new test has also executed.

```bash
pipenv run py.test -v --html=vagrant_test.html --self-contained-html --ansible-inventory=inventories/vagrant.ini.answer --connection=ansible exercise/vagrant_test.py --capture sys -rPs
```