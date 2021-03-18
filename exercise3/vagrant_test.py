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