#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:26:06 2019

@author: roy
"""

import requests
from base64 import b64encode
import re

class Router(object):
    
    def __init__(self, host, username='admin', password='admin'):
        self.host = host
        self.username = username
        self.password = password

        self.user_pass_str = username + ':' + password
        self.user_pass_encode = b64encode(self.user_pass_str.encode()).decode('ascii')
        self.authentication = 'Basic ' + self.user_pass_encode
        self.cookie = 'Authorization=' + self.authentication

        self.session = requests.Session()
        self.referer = 'http://' + self.host
        self.session.headers['Cookie'] = self.cookie
        self.session.headers['Referer'] = self.referer

        self.main_referer = self.referer + '/mainFrame.htm'
        
        # Stop the requests after a specific time
        self.timeout = 1.5
        self.post_timeout = 3

    def login(self):
        response = self.session.get(self.referer, timeout = self.timeout)
        is_login_success = re.search('(?i)username or password is incorrect', response.text)
        if is_login_success == None:
            return True

    def post_data(self, referer, post_url, payload):
        self.session.headers['Referer'] = referer
        response = self.session.post(post_url, data = payload, timeout = self.post_timeout)
        return response.text

    def get_wan_details(self):
        referer = self.main_referer
        post_url = self.referer + '/cgi?1&1'
        payload = '[WAN_ETH_INTF#1,0,0,0,0,0#0,0,0,0,0,0]0,2\r\nenable\r\nX_TP_lastUsedIntf\r\n[WAN_IP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,0\r\n'
        response = self.post_data(referer, post_url, payload)

        addressingType = r'(?:addressingType=)(.*)'
        ipAddress = r'(?:externalIPAddress=)(.*)'
        subnetMask = r'(?:subnetMask=)(.*)'
        defaultGateway = r'(?:defaultGateway=)(.*)'
        dnsServers = r'(?:DNSServers=)(.*)'
        
        wan_details = [addressingType, ipAddress, subnetMask, defaultGateway, dnsServers]
        for c in range(len(wan_details)):
            search = re.search(wan_details[c], response)
            wan_details[c] = search.group(search.lastindex)
        return wan_details

    def configure_wan(self, ipAddress, subnetMask, defaultGateway, dnsServers, dnsServers2):
        referer = self.main_referer
        post_url = self.referer + '/cgi?2&2'
        payload = '[WAN_ETH_INTF#1,0,0,0,0,0#0,0,0,0,0,0]0,2\r\nX_TP_lastUsedIntf=ipoe_eth3_s\r\nX_TP_lastUsedName=ewan_ipoe_s\r\n[WAN_IP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,18\r\nexternalIPAddress={}\r\nsubnetMask={}\r\ndefaultGateway={}\r\nNATEnabled=1\r\nX_TP_FullconeNATEnabled=0\r\nX_TP_FirewallEnabled=1\r\nmaxMTUSize=1500\r\nDNSOverrideAllowed=1\r\nDNSServers={},{}\r\nX_TP_IPv4Enabled=1\r\nX_TP_IPv6Enabled=0\r\nX_TP_IPv6AddressingType=Static\r\nX_TP_ExternalIPv6Address=::\r\nX_TP_PrefixLength=64\r\nX_TP_DefaultIPv6Gateway=::\r\nX_TP_IPv6DNSOverrideAllowed=0\r\nX_TP_IPv6DNSServers=::,::\r\nenable=1\r\n'.format(ipAddress, subnetMask, defaultGateway, dnsServers, dnsServers2)

        response = self.post_data(referer, post_url, payload)
        if response == '[error]0':
            return True

    def reboot(self):
        referer = self.main_referer
        post_url = self.referer + '/cgi?7'
        payload = '[ACT_REBOOT#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n'
        response = self.post_data(referer, post_url, payload)
        if response == '[error]0':
            return True