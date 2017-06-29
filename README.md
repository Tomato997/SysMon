# SysMon

System Monitor v1.0 Script for Python 2 using psutil
Copyright(C) 2017 by Felix Knobl.

https://twitter.com/felix_knobl

----------------------------------------------------------------------------------------

Used Twitter library:
Need to download and extract to the project directory
https://pypi.python.org/packages/ea/1e/ffb8dafa9539c68bd0994d98c1cf55760b2efe0e29189cd486bf4f23907d/twitter-1.17.1-py2.py3-none-any.whl#md5=ca1aa70131eb3b5a71d3ad76c7f030f5

or use included file: twitter-1.17.1-py2.py3-none-any.whl

----------------------------------------------------------------------------------------

Used psutil version 5.2.2

Need to be installed manually.

If installation has failed, try the following commands (under fedora):

sudo dnf install redhat-rpm-config

sudo dnf install python-devel

sudo pip install psutil

----------------------------------------------------------------------------------------

User defined configuration:

Use your own API keys ;)

How many times the current values should be posted before an average post is posted

LONG_POST_INTERVAL = 10

Timeout betweet current values posts

SHORT_POST_TIMEOUT = 60
