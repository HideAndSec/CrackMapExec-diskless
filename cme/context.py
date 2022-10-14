#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import configparser

class Context:

    def __init__(self, logger, args):
        self.log = logger
        self.log.debug = logging.debug
        self.localip = None

        for key, value in vars(args).items():
            setattr(self, key, value)
