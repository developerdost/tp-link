#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:26:06 2019

@author: roy
"""
import time
import sys
import os
import requests

from lib.router import Router
from lib.database import Database


def wan_configure():
    ip = input('\n{}IP Address :: {}'.format(color_input, color_default))
    subnet = input('{}Subnet Mask :: {}'.format(color_input, color_default))
    gateway = input('{}Default Gateway :: {}'.format(color_input, color_default))
    dns = input('{}Primary DNS :: {}'.format(color_input, color_default))
    dns2 = input('{}Secondary DNS :: {}'.format(color_input, color_default))
    return (ip, subnet, gateway, dns, dns2)

def wan_details():
    wan_details = router.get_wan_details()
    wan_ = '[+] Address Type : ' + wan_details[0]
    wan_ += '\n[+] IP Address : ' + wan_details[1]
    wan_ += '\n[+] Subnet Mask : ' + wan_details[2]
    wan_ += '\n[+] Default Gateway : ' + wan_details[3]
    wan_ += '\n[+] DNS Server : ' + wan_details[4]
    return wan_

def execute_task(task = None):
    # Read configuration file
    lines = database.read().splitlines()
    
    if task == None:
        ip = lines[1].replace('Target IP : ', '')
    elif task == 'reset':
        ip = lines[0].replace('Default IP : ', '')
        
    if not ip == '0.0.0.0':
        # Get wan details
        wan_details = router.get_wan_details()
        subnet = wan_details[2]
        gateway = wan_details[3]
        dns_server = wan_details[4].split(',')
        dns = dns_server[0]
        dns2 = dns_server[1]
        
        output = router.configure_wan(ip, subnet, gateway, dns, dns2)
        return (output,ip)
    else:
        return ('error','error')

def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.08)

if __name__ == "__main__":
    color_error = '\033[1;31m'
    color_success = '\033[1;32m'
    color_options = '\033[1;33m'
    color_input = '\033[1;34m'
    color_heading = '\033[1;36m'
    color_default = '\033[1;37m'

    menu = """{}
**************************************************
        TP-Link Wireless N Router WR841N
             Model No. TL-WR841N
**************************************************
{}
1. Execute Task             2. Reset Connection
3. Default IP Address       4. Target IP Address
5. Read Configuration       6. Reboot Router
7. Configure WAN            8. WAN Details
0. Exit/Logout
    """.format(color_heading, color_options)

    # Create an object of database module
    database = Database()
    # Create an object of router module
    router = Router('192.168.0.1', 'Esu','roy_007')
    
    try:
        if router.login(): # login success
            # Create an database file that store device credentials
            database.config()
        
            check = False
            output = ''
            
            # create a continuous loop
            while True:
                # clear the screen
                os.system('clear')
                # print the result
                if not output == '':
                    print('\n' + output)
                
                if check:
                    # print the menu screen
                    delay_print(menu)
                    check = False
                    color_input = '\n\r' + color_input
                else:
                    # print the menu screen
                    print(menu)
                    color_input = color_input.replace('\n\r', '')
                
                # checking the user input, if it is number then ok otherwise give an exception
                try:
                    option = int(input('{}:: {}'.format(color_input, color_default)))
                    
                    if option == 0:
                        print('\n{}[x] Thank you for using it.\n{}'.format(color_success, color_default))
                        sys.exit()    
                    elif option == 1:
                        output, ip = execute_task()
                        if not output == 'error':
                            output = '{}[+] You are now connected with {}'.format(color_success, ip)
                        else:
                            output = '{}[-] Please enter a valid ip address'.format(color_error)        
                    elif option == 2:
                        output, ip = execute_task('reset')
                        if not output == 'error':
                            output = '{}[+] You are now connected with {}'.format(color_success, ip)
                        else:
                            output = '{}[-] Please enter a valid ip address'.format(color_error)    
                    elif option == 3:
                        default_ip = input('{}\nDefault IP Address :: {}'.format(color_input, color_default))
                        data = 'Default IP : ' + default_ip
                        if database.write(data):
                            output = '{}[+] {}'.format(color_success, data)
                    elif option == 4:
                        target_ip = input('{}\nTarget IP Address :: {}'.format(color_input, color_default))
                        data = 'Target IP : ' + target_ip
                        if database.write(data):
                            output = '{}[+] {}'.format(color_success, data)
                    elif option == 5:
                        data = database.read().splitlines()
                        data = '[+] ' + data[0] + '\n' + '[+] ' + data[1]
                        if data:
                            output = '{}{}'.format(color_success, data)
                    elif option == 6:
                        if router.reboot():
                            output = '{}[+] Router going to reboot, please wait'.format(color_success)        
                    elif option == 7:
                        (ip, subnet, gateway, dns, dns2) = wan_configure()
                        if router.configure_wan(ip, subnet, gateway, dns, dns2):
                            output = '{}[+] WAN Configured Successfully'.format(color_success)        
                    elif option == 8:
                        output = '{}{}'.format(color_success, wan_details())    
                    else:
                        output = '{}[-] Invalid option, please try again'.format(color_error)
                except ValueError:
                    output = '{}[-] Please enter only digit'.format(color_error)
                    continue
                except Exception:
                    output = '{}[-] Network is unreachable'.format(color_error)
                    continue
        else: # login failed
            print('\n{}[-] Login failed, please try again{}'.format(color_error, color_default))
    except requests.exceptions.ConnectionError: # Network is unreachable.
        print('\n{}[-] Network is unreachable'.format(color_error))
    except KeyboardInterrupt:
        print('\n{}[-] User press CTRL + C{}'.format(color_error, color_default))