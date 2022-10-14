#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib

import cme.protocols as cme_protocols


class protocol_loader:
    def get_protocols(self):
        protocols = {}
        protocols_names = [x for x in cme_protocols.__loader__.get_resource_reader("cme.protocols").contents() if not x.endswith(".py")]

        for prot_name in protocols_names:
            prot = importlib.import_module(f"cme.protocols.{prot_name}")
            protocols[prot_name] = prot

        return protocols