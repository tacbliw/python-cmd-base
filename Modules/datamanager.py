# -*- coding: utf-8 -*-

"""
Include data readling and writing classes for managing WildCat's data

"""

class Ports:
    """
    A class to manage ports stored in a well-constructed text file
        One port per line
        In a line:

        line[:17]   => port name (eg. ssh)
        line[18:29] => port number (eg. 22) or
                       port number and protocol (eg. 22/tcp) or
                       port range (eg. 1234-5678)
        line[33:]   => port description (eg. SSH Remote Login Protocol)
    """

    def __init__(self, port_file):
        self.port_list = []
        self.readports(port_file)

    def readports(self, port_file):
        source = []
        with open(port_file, 'r') as f:
            source = f.readlines()
            
        preport = 'a'
        for line in source:
            line = line.strip('\n')
            name = line[:17].strip()
            port = line[18:29].strip()
            if '/' in port:
                port = port.split('/')[0]
                if port == preport:
                    continue
                else:
                    portlist = [int(port)]
                    preport = port
            elif '-' in port:
                port = port.split('-')
                if port[1] >= port[0]:
                    portlist = range(int(port[0]), int(port[1]) + 1)
                else:
                    portlist = range(int(port[1]), int(port[0]) + 1)
            else:
                portlist = int(port)

            description = line[33:].strip()

            for p in portlist:
                self.port_list.append([p, name, description])

    def get_name(self, port):
        """Return name of a given port"""
        port = int(port)
        for p in self.port_list:
            if p[0] == port:
                return p[1]
        return 'unknown'

    def get_description(self, port):
        """Return description of a given port"""
        port = int(port)
        for p in self.port_list:
            if p[0] == port:
                return p[2]
        return ' '







