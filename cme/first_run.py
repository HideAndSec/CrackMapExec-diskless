#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import errno
import sqlite3
import shutil
import cme
import configparser
from configparser import ConfigParser, NoSectionError, NoOptionError
from cme.loaders.protocol_loader import protocol_loader
from subprocess import check_output, PIPE
import sys

CME_PATH = os.path.expanduser('~/.cme')
TMP_PATH = os.path.join('/tmp', 'cme_hosted')
if os.name == 'nt':
    TMP_PATH = os.getenv('LOCALAPPDATA') + '\\Temp\\cme_hosted'
if hasattr(sys, 'getandroidapilevel'):
    TMP_PATH = os.path.join('/data','data', 'com.termux', 'files', 'usr', 'tmp', 'cme_hosted')
WS_PATH = os.path.join(CME_PATH, 'workspaces')
CERT_PATH = os.path.join(CME_PATH, 'cme.pem')
CONFIG_PATH = os.path.join(CME_PATH, 'cme.conf')


def first_run_setup(logger):
    if not os.path.exists(CERT_PATH):
        logger.info('Generating SSL certificate')
        try:
            check_output(['openssl', 'help'], stderr=PIPE)
            if os.name != 'nt':
                os.system('openssl req -new -x509 -keyout {path} -out {path} -days 365 -nodes -subj "/C=US" > /dev/null 2>&1'.format(path=CERT_PATH))
            else:
                os.system('openssl req -new -x509 -keyout {path} -out {path} -days 365 -nodes -subj "/C=US"'.format(path=CERT_PATH))
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error('OpenSSL command line utility is not installed, could not generate certificate, using default certificate')
                default_path = os.path.join(os.path.dirname(cme.__file__), 'data', 'default.pem')
                shutil.copy(default_path, CERT_PATH)                
            else:
                logger.error('Error while generating SSL certificate: {}'.format(e))
                sys.exit(1)
