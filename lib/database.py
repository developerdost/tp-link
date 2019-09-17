#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:38:29 2019

@author: roy
"""
import os

class Database(object):
    
    def __init__(self):
        self.database = 'config.bin'
    
    def config(self):
        try:
            # create a configure file, if aleady exist then skip it
            if not os.path.exists(self.database):
                with open(self.database, 'w') as file:
                    file.write('Default IP : 0.0.0.0\nTarget IP : 0.0.0.0\n')
        except Exception:
            pass
    
    def read(self):
        if os.path.exists(self.database):
            # Read the content of the file
            with open(self.database) as file:
                data = file.read()
            return data
    
    def write(self, data):
        if os.path.exists(self.database):
            # Read the content of the file
            content = self.read().splitlines()
            # search default ip address then update
            if data.startswith('Default'):
                content = data + '\n' + content[1]
            # search target ip address then update
            elif data.startswith('Target'):
                content = content[0] + '\n' + data
                
            # Write data into file
            with open(self.database, 'w') as file:
                file.write(content) 
            return True
        