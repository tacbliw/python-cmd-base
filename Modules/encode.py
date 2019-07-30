#-*- coding: utf-8 -*-

class Coding:
    def __init__(self):
        self.encoders_list = ['hex', 'base64', 'sha1', 'md5']

    def base64(self, string):
        """Base64 encoder"""
        import base64
        string_bytes = string.encode('ascii')
        return base64.b64encode(string_bytes).decode('ascii')

    def sha1(self, string):
        """SHA1 encoder"""
        import hashlib
        string_bytes = string.encode('ascii')
        return hashlib.sha1(string_bytes).hexdigest()

    def md5(self, string):
        """MD5 encoder"""
        import hashlib
        string_bytes = string.encode('ascii')
        return hashlib.md5(string_bytes).hexdigest()

    def hex(self, string):
        """Hex encoder"""
        return ''.join([hex(ord(c))[2:] for c in string])
