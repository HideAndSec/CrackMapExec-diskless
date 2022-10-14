#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import os
import sys

import cme
from cme.context import Context
from cme.logger import CMEAdapter
import cme.modules as cme_modules


class module_loader:

    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        self.cme_path = os.path.expanduser('~/.cme')

    def module_is_sane(self, module, module_path):
        module_error = False

        if not hasattr(module, 'name'):
            self.logger.error('{} missing the name variable'.format(module_path))
            module_error = True

        elif not hasattr(module, 'description'):
            self.logger.error('{} missing the description variable'.format(module_path))
            module_error = True

        #elif not hasattr(module, 'chain_support'):
        #    self.logger.error('{} missing the chain_support variable'.format(module_path))
        #    module_error = True

        elif not hasattr(module, 'supported_protocols'):
            self.logger.error('{} missing the supported_protocols variable'.format(module_path))
            module_error = True

        elif not hasattr(module, 'opsec_safe'):
            self.logger.error('{} missing the opsec_safe variable'.format(module_path))
            module_error = True

        elif not hasattr(module, 'multiple_hosts'):
            self.logger.error('{} missing the multiple_hosts variable'.format(module_path))
            module_error = True

        elif not hasattr(module, 'options'):
            self.logger.error('{} missing the options function'.format(module_path))
            module_error = True

        elif not hasattr(module, 'on_login') and not (module, 'on_admin_login'):
            self.logger.error('{} missing the on_login/on_admin_login function(s)'.format(module_path))
            module_error = True

        if module_error: return False

        return True

    def get_modules(self):
        modules = {}

        mods_blacklist = ["example_module.py", "__init__.py"]
        mods_names = [x for x in cme_modules.__loader__.get_resource_reader("cme.modules").contents() if x not in mods_blacklist]

        for mod_name in mods_names:
            mod = importlib.import_module(f"cme.modules.{mod_name.removesuffix('.py')}").CMEModule()
            modules[mod.name] = {'description': mod.description, 'options': mod.options.__doc__} #'chain_support': m.chain_support}

        return modules

    def init_module(self, module):
        if module:
            module_logger = CMEAdapter(extra={'module': module.name.upper()})
            context = Context(self.db, module_logger, self.args)

            module_options = {}

            for option in self.args.module_options:
                key, value = option.split('=', 1)
                module_options[str(key).upper()] = value

            module.options(context, module_options)

        return module
