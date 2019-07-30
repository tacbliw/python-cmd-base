# -*- coding: utf-8 -*-

#system modules
import sys

#my modules
from . import color

#globals
markers = { 
            'ques'  : color.colorize('[?] '  , color.BLUE   ),
            'feed'  : color.colorize('[*] '  , color.CYAN   ),
            'pos'   : color.colorize('[+] '  , color.GREEN  ),
            'neg'   : color.colorize('[-] '  , color.RED    ),
            'warn'  : color.colorize('[!] '  , color.YELLOW ),
            'error' : color.colorize('[Err] ', color.MAGENTA)
          }

table_positions = [15, 20, 50]

class WildcatPrint:
    """
    Notifications and prompts printing

    """
    def newline(self):
        sys.stdout.write('\n')

    def line(self, text):
        sys.stdout.write(text)

    def question(self, prompt, paramValue="", necessary=False):
        """Prompt user for an input string"""
        retVal = input(markers['ques'] + prompt + " [" + str(paramValue) + "]: ")
        if not retVal:
            if paramValue:
                return paramValue
            else:
                if necessary:
                    return self.question(prompt, necessary=True)

                else:
                    return ''

        return retVal

    def feed(self, feed):
        """Print out a feed"""
        self.line(markers['feed'] + feed)

    def positive(self, text, paramValue=None):
        """Print positive msg"""
        if paramValue:
            self.line(markers['pos'] + "Set " + text + " => " + str(paramValue))
        else:
            self.line(markers['pos'] + text)

    def negative(self, text, paramValue=None):
        """Print negative msg"""
        if paramValue:
            self.line(markers['neg'] + "Set " + text + " => " + str(paramValue))
        else:
            self.line(markers['neg'] + text)


    def warning(self, text, warn=""):
        """Print warning msg"""
        if warn:
            self.line(markers['warn'] + warn + " : " + text)
        else:
            self.line(markers['warn'] + text)

    def yn(self, text):
        """Prompt for yes/no question"""
        self.line(markers['ques'])
        ans = input(text + " (y/n): ")
        if ans in ['yes', 'y', '']:
            return True
        elif ans in ['no', 'n']:
            return False
        else:
            return self.yn(text)

    def error(self, error='', text=''):
        """Print error msg"""
        self.line(markers['error'])
        if text:
            self.line(color.colorize(error + ' : ', color.WHITE) + text)
        else:
            self.line(color.colorize(error, color.WHITE))

    """
    Printing for 'help' command

    """
    def usage(self, usage=[], header=[], param={}):
        """Print usage description"""
        self.line("{0:>{pos}}{1}\n".format("Usage: ", usage[0], pos = table_positions[0]))
        self.line('\t' + '\n\t'.join(usage[1:]))
        self.newline()

        if param != {}:
            self.table(header, param)
            self.newline()
            self.newline()

    def header(self, header):
        """Print header for table function"""
        [header.append('') for i in range(2)] # make sure header have at least 3 elements

        line = "  {hdr[0]:<{pos[0]}}{hdr[1]:<{pos[1]}}{hdr[2]:<{pos[2]}}".format(hdr=header, pos=table_positions)
        self.line(line)
        self.newline()

        self.line('  ' + '-' * 60 + '\n')
        self.newline()

    def table(self, header, param):
        """Print variables table"""
        self.newline()
        if header:
            self.header(header)

        for key in param: # append to make sure param have 2 elements
            param[key].append('')
            param[key].append('')

        for key in param:
            line = "  {key:<{pos[0]}}{hdr[0]:<{pos[1]}}{hdr[1]:<{pos[2]}}".format(key=key, hdr=param[key], pos=table_positions)
            self.line(line)
            self.newline()
        self.newline()
