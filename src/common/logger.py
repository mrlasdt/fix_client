#!/usr/bin/python
# -*- coding: utf8 -*-
import logging


def setup_logger(name, path, verbose):
    lz = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(path, mode='w')
    fileHandler.setFormatter(formatter)
    lz.addHandler(fileHandler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    lz.addHandler(streamHandler)
    level = logging.NOTSET if not verbose else logging.INFO
    lz.setLevel(level)
