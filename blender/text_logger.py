#!/usr/bin/env python

import bpy

class Logger(object):
    def __init__(self):
        txt = bpy.ops.text.new()