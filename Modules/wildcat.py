# -*- coding: utf-8 -*-

# system modules
import os, sys
import time
import ctypes
import threading
from datetime import datetime
import requests

# wildcat modules
from . import inputhandler as i
from . import outputhandler as o
from . import datamanager as data
from . import color
from . import encode
from . import workerhandler as qt
from . import command as cmd


PROMPT_PRE = color.colorize('wildcat', color.WHITE)
PROMPT_POST = ' > '
PROMPT_ARGS = ""


class Main(cmd.WildcatCmd):
    prompt = PROMPT_PRE + PROMPT_POST
    ruler = '='
    lastcmd = ''
    intro = None
    doc_leader = ""
    doc_header = "Command"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"
    nohelp = "%s : Command not found\n"
    use_rawinput = 1
    close_script = "Script quitting !\n"
    keyboard_interrupt = "Aborted by user\n"

    def __init__(self):
        #stdin and stdout
        self.stdin  = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stdout

        self.PRINT = o.WildcatPrint()

        #cmd loop variables
        self.cmdqueue = []
        self.completekey = 'tab'

        #paths
        self.WC_PATH   = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.DATA_PATH = self.WC_PATH + '/DATA/'

        #utilities
        self.ENCODE = encode.Coding()

    def preloop(self):
        """Run before main loop, used for printing banner"""
        greet = [   "                                              " +color.colorize("_____",color.YELLOW),
                    " __      __."+  color.colorize("__.", color.RED)    + "__       .____________        " + color.colorize("  | |  ", color.YELLOW),
                    "/  \    /  \\"+ color.colorize("__|", color.RED)    + "  |    __| _/\_   ___ \_____"   + color.colorize(" ___| |___", color.YELLOW),
                    "\   \/\/   /" + color.colorize("  |", color.YELLOW) + "  |   / __ | /    \  \/\__  \\" + color.colorize("\\_",color.YELLOW) + color.colorize(" _|_ ", color.RED) + color.colorize("__|", color.YELLOW),
                    " \        /"  + color.colorize("|  |",color.YELLOW) + "  |__/ /_/ | \     \____/ __ \ "+ color.colorize("|", color.YELLOW)  + color.colorize(" | ", color.RED)   + color.colorize("|  ", color.YELLOW),
                    "  \__/\  / "  + color.colorize("|__|",color.YELLOW) + "____/\____ |  \_______ (____ / "+ color.colorize("|", color.YELLOW)  + color.colorize(" | ", color.RED)   + color.colorize("|  ", color.YELLOW),
                    "       \/        \/     \/     \/             " + color.colorize("|", color.YELLOW)    + color.colorize(" | ", color. RED)  + color.colorize("|", color.YELLOW),
                    "                                              " + color.colorize("|", color.YELLOW)    + color.colorize(" | ", color. RED)  + color.colorize("|", color.YELLOW),
                    "    Main Commands:                            " + color.colorize("|", color.YELLOW)    + color.colorize(" | ", color. RED)  + color.colorize("|", color.YELLOW),
                    "                                               " + color.colorize("\\", color.YELLOW)  + color.colorize("|", color.RED)     + color.colorize("/", color.YELLOW)
                ]

        self.PRINT.line('\n'.join(greet[:len(greet) - 1]))
        # then get all command names
        names = list(set([a[3:] for a in self.get_names() if a.startswith('do_')]) - set(['EOF']))
        for name in names:
            self.PRINT.newline()
            self.PRINT.line(' ' * 8 + "{:<38}".format(name) + color.colorize("|", color.YELLOW) + color.colorize(" | ", color. RED) + color.colorize("|", color.YELLOW))

        self.PRINT.newline()
        self.PRINT.line(greet[len(greet) - 1])
        self.PRINT.newline()

    def default(self, line):
        """Called when command not found, override for color printing"""
        line = line.split(' ')[0]
        self.PRINT.warning(line + ": command not found")
        self.PRINT.newline()

    def setprompt(self, state = None):
        if state:
            self.prompt = PROMPT_PRE + ' ' + state + ' ' + PROMPT_POST
        else:
            self.prompt = PROMPT_PRE + PROMPT_POST

    def get_names(self):
        """Override: avoid duplicated in self.__class__"""
        names = []
        classes = [self.__class__]
        while classes:
            aclass = classes.pop(0)
            if aclass.__bases__:
                classes = classes + list(aclass.__bases__)
            names += dir(aclass)
        return names

    def completenames(self, text, *ignored):
        dotext = 'do_' + text
        return [word[3:] for word in self.get_names() if word.startswith(dotext)]

    def check_admin(self):
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        return is_admin

    """
    CMD : help

    """

    def complete_help(self, *args):
        # commands = set(self.completenames(*args))
        # topics = set(a[5:] for a in self.get_names()
        #            if a.startswith('help_' + args[0]))
        # return list(commands | topics)
        return [a[5:] for a in sorted(self.get_names())
                if a.startswith('help_' + args[0])]

    # this is default do_help fucntion of cmd.py (+ column printed by WildCat)
    def do_help(self, arg):
        """Print out help"""
        if arg:
            try:
                help_func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.PRINT.line("%s\n"%str(doc))
                        return
                except AttributeError:
                    pass
                self.PRINT.warning(self.nohelp % arg)
                return
            help_func()
        else:
            names = sorted(self.get_names())
            cmds = {}
            for name in names:
                if name.startswith('do_'):
                    name = name[3:]
                    cmds[name] = [getattr(self, 'do_' + name).__doc__]

            help_header = [self.doc_header, 'Description']
            self.PRINT.table(help_header, cmds)

    def help_help(self):
        usage = ['help <command>',
                    'Print out help (of command)'
                ]
        self.PRINT.usage(usage)

    """
    CMD: quit, EOF

    """
    def help_quit(self):
        usage = ['quit',
                 'Quit program.'
                ]
        self.PRINT.usage(usage)
        return 0

    def do_quit(self, line):
        """Quit program"""
        if self.PRINT.yn("Quit the program ?"):
            sys.exit()
        else:
            return 0
    
    def help_EOF(self, line):
        usage = ["EOF (ctrl + D)",
                 "Quit program."
                ]
        self.PRINT.usage(usage)
    
    def do_EOF(self, line):
        """Quit program"""
        self.PRINT.newline()
        sys.exit()

    # Add your commands here
