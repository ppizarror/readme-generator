# coding=utf-8
"""
README GENERATOR
Generate a README.md file from a configuration file

Autor: Pablo Pizarro R. @ ppizarror.com
Licencia:
    The MIT License (MIT)
    Copyright 2017 Pablo Pizarro R.
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the Software
    is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function
# noinspection PyCompatibility
from Tkinter import *
# noinspection PyCompatibility,PyUnresolvedReferences
import tkFont
# noinspection PyUnresolvedReferences,PyCompatibility
import tkMessageBox
# noinspection PyCompatibility
from tkFileDialog import askopenfilename

# Library imports
from PIL import ImageTk
from resources.content import *
from resources.utils import *
from resources.vframe import VerticalScrolledFrame
import json
import time
import traceback
import winsound

# Constants
VERSION = '0.6.0'


# noinspection PyUnusedLocal,PyBroadException
class App(object):
    """
    Main Application
    """

    def __init__(self):
        """
        Constructor.
        """

        def _about():
            """
            Print about on console.

            :return:
            """
            self._print(self._lang['ABOUT_APPTITLE'].format(VERSION))
            self._print(self._lang['ABOUT_AUTHOR'] + '\n')

        def _kill():
            """
            Destroy the application.

            :return:
            """
            self._root.destroy()
            exit()

        def _scroll_console(event):
            """
            Función que atrapa el evento del scrolling y mueve los comandos.

            :param event: Evento
            :return: None
            """
            if 0 < event.x < 420 and 38 < event.y < 150:
                if is_windows():
                    if -1 * (event.delta / 100) < 0:
                        move = -1
                    else:
                        move = 2
                elif is_osx():
                    if -1 * event.delta < 0:
                        move = -2
                    else:
                        move = 2
                else:
                    if -1 * (event.delta / 100) < 0:
                        move = -1
                    else:
                        move = 2
                if len(self._console) < 5 and move < 0:
                    return
                self._info_slider.canv.yview_scroll(move, 'units')

        self._root = Tk()
        self._root.protocol('WM_DELETE_WINDOW', _kill)
        self._root.tk.call('tk', 'scaling', 1.35)

        # Load configuration
        with open('resources/config.json') as json_data:
            d = json.load(json_data)
            self._config = d
        self._config['ROOT'] = str(os.path.abspath(os.path.dirname(__file__))).replace(
            '\\', '/') + '/'
        with open(self._config['LANG']) as json_data:
            d = json.load(json_data)
            self._lang = d

        # Window properties
        size = [self._config['APP']['WIDTH'], self._config['APP']['HEIGHT']]
        self._root.minsize(width=size[0], height=size[1])
        self._root.geometry('%dx%d+%d+%d' % (
            size[0], size[1], (self._root.winfo_screenwidth() - size[0]) / 2,
            (self._root.winfo_screenheight() - size[1]) / 2))
        self._root.resizable(width=False, height=False)
        self._root.focus_force()

        # Window style
        self._root.title(self._config['APP']['TITLE'])
        self._root.iconbitmap(self._config['APP']['ICON']['TITLE'])
        fonts = [tkFont.Font(family='Courier', size=8),
                 tkFont.Font(family='Verdana', size=6),
                 tkFont.Font(family='Times', size=10),
                 tkFont.Font(family='Times', size=10, weight=tkFont.BOLD),
                 tkFont.Font(family='Verdana', size=6, weight=tkFont.BOLD),
                 tkFont.Font(family='Verdana', size=10),
                 tkFont.Font(family='Verdana', size=7)]

        f1 = Frame(self._root, border=5)
        f1.pack(fill=X)
        f2 = Frame(self._root)
        f2.pack(fill=BOTH)

        # Load file
        self._startbutton = Button(f1, text=self._lang['LOAD_FILE_BUTTON'],
                                   state='normal', relief=GROOVE,
                                   command=self.load_file)
        self._startbutton.pack(side=LEFT, padx=5, anchor=W)

        # Label that shows loaded configuration name
        self._mainlabelstr = StringVar()
        Label(f1, textvariable=self._mainlabelstr, foreground='#666').pack(side=LEFT, padx=0)

        # Uploads
        upimg = ImageTk.PhotoImage(
            file=self._config['APP']['ICON']['UPLOADBUTTON'])
        self._uploadbutton = Button(f1, image=upimg, relief=GROOVE, height=20,
                                    width=20, border=0, state='disabled')
        self._uploadbutton.image = upimg
        self._uploadbutton.pack(side=RIGHT, padx=2, anchor=E)

        # Start process
        self._startbutton = Button(f1, text=self._lang['START_PROCESS'],
                                   state='disabled', relief=GROOVE,
                                   command=self.start_process)
        self._startbutton.pack(side=RIGHT, padx=5, anchor=E)

        # Console
        self._info_slider = VerticalScrolledFrame(f2)
        self._info_slider.canv.config(bg='#000000')
        self._info_slider.pack(pady=2, anchor=NE, fill=BOTH, padx=1)
        self._info = Label(self._info_slider.interior, text='', justify=LEFT, anchor=NW,
                           bg='black', fg='white',
                           wraplength=self._config['APP']['WIDTH'],
                           font=fonts[0], relief=FLAT, border=2,
                           cursor='arrow')
        self._info.pack(anchor=NW, fill=BOTH)
        self._info_slider.scroller.pack_forget()
        self._console = []
        self._cnextnl = False
        _about()

        # Other variables
        self._lastfolder = self._config['ROOT']
        self._loadedfile = {}

        # Events
        self._root.bind('<MouseWheel>', _scroll_console)

    def _clearstatus(self):
        """
        Clear a loaded status.

        :return: None
        """
        self._uploadbutton.configure(state='disabled')
        self._startbutton.configure(state='disabled')
        self._mainlabelstr.set('')
        self._loadedfile = {}

    def _clearconsole(self, scrolldir=1):
        """
        Clear the console.

        :param scrolldir: Scroll direction
        :return:
        """

        # noinspection PyShadowingNames,PyUnusedLocal
        def _slide(*args):
            """
            Mueve el scroll.

            :return: None
            """
            self._info_slider.canv.yview_scroll(1000 * scrolldir, 'units')

        self._console = []
        self._info.config(text='')
        self._root.after(10, _slide)

    def _errorsound(self):
        """
        Create a error sound.

        :return: None
        """
        if self._config['APP']['SOUNDS']:
            winsound.MessageBeep(1)

    def load_file(self):
        """
        Load a file to create README.md.

        :return: None
        """
        self._print(self._lang['LOAD_WAITING_USER'], end='', hour=True)
        if self._config['REMEMBER_LAST_FOLDER']:
            filename = askopenfilename(
                title=self._lang['LOAD_FILE_PICKWINDOW_TITLE'],
                filetypes=[(self._lang['LOAD_FILE_JSON'], '.json')],
                initialdir=self._lastfolder)
        else:
            filename = askopenfilename(
                title=self._lang['LOAD_FILE_PICKWINDOW_TITLE'],
                filetypes=[(self._lang['LOAD_FILE_JSON'], '.json')])

        # Check if filename is not empty
        if filename == '':
            self._print(self._lang['LOAD_CANCELLED'])
            self._clearstatus()
            return
        else:
            self._print(self._lang['PROCESS_OK'])

        # Store last folder
        filepath = os.path.split(filename)
        self._lastfolder = filepath[0]

        # Validate file
        self._print(self._lang['START_LOADING'].format(filename), hour=True, end='')
        if self.validate(filename):
            self._print(self._lang['LOAD_OK'])
            self._uploadbutton.configure(state='disabled')
            self._startbutton.configure(state='normal')
            self._mainlabelstr.set(self._loadedfile['PROJECT']['NAME'])
        else:
            self._clearstatus()
            self._print(self._lang['LOAD_FAILED'].format(filename))
            self.validate(filename, showerrors=True)

    def _print(self, msg, hour=False, end=None, scrolldir=1):
        """
        Print a message on console.

        :param msg: Message
        :param hour: Hour
        :param scrolldir: Scroll direction
        :return: None
        """

        def _consoled(c):
            """
            Generates string with hour of message.

            :param c: Lista
            :return: Texto
            """
            text = ''
            for i in c:
                text = text + i + '\n'
            return text

        def _get_hour():
            """
            Return system hour.

            :return: String
            """
            return time.ctime(time.time())[11:19]

        def _slide(*args):
            """
            Scroll the console.

            :return: None
            """
            self._info_slider.canv.yview_scroll(2000 * scrolldir, 'units')

        try:
            msg = str(msg)
            if hour:
                msg = self._config['CONSOLE']['MSG_FORMAT'].format(_get_hour(), msg)
            if len(self._console) == 0 or self._console[len(self._console) - 1] != msg:
                if self._cnextnl:
                    self._console[len(self._console) - 1] += msg
                else:
                    self._console.append(msg)
                if end == '':
                    self._cnextnl = True
                else:
                    self._cnextnl = False

            if len(self._console) > self._config['CONSOLE']['LIMIT_MESSAGES_CONSOLE']:
                self._console.pop()

            self._info.config(text=_consoled(self._console))
            self._root.after(50, _slide)
        except:
            self._clearconsole()

    def start_process(self):
        """
        Start generation process.

        :return:
        """
        self._print(self._lang['PROCESS_STARTED'], end='', hour=True)
        try:
            fl = open(self._lastfolder + '/README.md', 'w')

            # Data variables
            project = self._loadedfile['PROJECT']
            icon = self._loadedfile['PROJECT']['ICON']
            description = self._loadedfile['DESCRIPTION']
            badges = self._loadedfile['BADGES']
            badgelist = ''
            badgelistcfg = self._loadedfile['BADGES'].keys()
            badgelistcfg.sort()
            for b in badgelistcfg:
                badgelist += CONTENT_BADGE_ITEM.format(badges[b]['HREF'], badges[b]['ALT'], badges[b]['IMAGE'])
            author = self._loadedfile['AUTHOR']
            author_section = author['SECTION']
            contentreadme = open(self._loadedfile['CONTENT'])

            # Write elements on README
            if icon['IMAGE'] != '':
                if self._loadedfile['PROJECT']['URL'] != '':
                    fl.write(CONTENT_HEADER_URL_IMAGE.format(project['URL'], project['URL_TITLE'], icon['ALT'],
                                                             icon['IMAGE'], project['NAME'], icon['WIDTH'],
                                                             icon['HEIGHT']))
                else:
                    fl.write(CONTENT_HEADER_NO_URL_IMAGE.format(icon['ALT'], icon['IMAGE'], project['NAME'],
                                                                icon['WIDTH'], icon['HEIGHT']))
            else:
                if self._loadedfile['PROJECT']['URL'] != '':
                    fl.write(CONTENT_HEADER_URL_NO_IMAGE.format(project['URL'], project['URL_TITLE'], project['NAME']))
                else:
                    fl.write(CONTENT_HEADER_NO_URL_IMAGE.format(project['NAME']))
            if description != '':
                fl.write(CONTENT_DESCRIPTION.format(description))
            if badgelist != '':
                fl.write(CONTENT_BADGES.format(badgelist))
            fl.write('\n')
            for line in contentreadme:
                fl.write(line)
            if author_section['SHOW']:
                if author['DATE'] != '':
                    if author['URL'] != '':
                        fl.write(CONTENT_AUTHOR_SECTION_URL_DATE.format(author_section['TITLE'], author['URL'],
                                                                        author['ALT'], author['NAME'], author['DATE']))
                    else:
                        fl.write(CONTENT_AUTHOR_SECTION_URL_DATE.format(author['NAME'], author['DATE']))
                else:
                    if author['URL'] != '':
                        fl.write(CONTENT_AUTHOR_SECTION_URL_NO_DATE.format(author_section['TITLE'], author['URL'],
                                                                           author['ALT'], author['NAME']))
                    else:
                        fl.write(CONTENT_AUTHOR_SECTION_NO_URL_NO_DATE.format(author['NAME']))

            # Process finished
            contentreadme.close()
            fl.close()
            self._print(self._lang['PROCESS_OK'])
            self._startbutton.configure(state='disabled')
            self._uploadbutton.configure(state='normal')
        except Exception as e:
            self._errorsound()
            self._print(self._lang['PROCESS_ERROR'])
            self._print(str(e))
            self._print(traceback.format_exc())

    def run(self):
        """
        Run the app.

        :return: None
        """
        self._root.mainloop()

    def validate(self, configfile, showerrors=False):
        """
        Validates a configfile.

        :param showerrors: Show errors on console
        :param configfile: Configuration file
        :return:
        """

        def print_error(error_id, formatstr=None):
            """
            Print error on console.

            :param formatstr: List to format
            :param error_id: Error ID
            :return: None
            """
            if showerrors:
                if formatstr is not None:
                    if type(formatstr) is list:
                        self._print('[CONFIG] ' + self._lang['FILE_ERRORS'][error_id].format(*formatstr))
                    else:
                        self._print('[CONFIG] ' + self._lang['FILE_ERRORS'][error_id].format(formatstr))
                else:
                    self._print('[CONFIG] ' + self._lang['FILE_ERRORS'][error_id])
            self._errorsound()

        try:
            with open(configfile) as json_data:
                cfg = json.load(json_data)
            for c in ['PROJECT', 'AUTHOR', 'DESCRIPTION', 'BADGES', 'CONTENT']:
                if c not in cfg.keys():
                    print_error('ELEMENT_NOT_FOUND', c)
                    if not showerrors:
                        return False
            for c in ['NAME', 'ICON', 'URL', 'URL_TITLE']:
                if c not in cfg['PROJECT'].keys():
                    print_error('PROJECT_ENTRY', c)
                    if not showerrors:
                        return False
            for c in ['IMAGE', 'ALT', 'WIDTH', 'HEIGHT']:
                if c not in cfg['PROJECT']['ICON'].keys():
                    print_error('PROJECT_ICON_ENTRY', c)
                    if not showerrors:
                        return False
            if cfg['PROJECT']['ICON']['IMAGE'] != '':
                if not str(cfg['PROJECT']['ICON']['WIDTH']).isdigit():
                    print_error('PROJECT_ICON_WIDTH', cfg['PROJECT']['ICON']['WIDTH'])
                    if not showerrors:
                        return False
                if not str(cfg['PROJECT']['ICON']['HEIGHT']).isdigit():
                    print_error('PROJECT_ICON_HEIGHT', cfg['PROJECT']['ICON']['HEIGHT'])
                    if not showerrors:
                        return False
            if cfg['PROJECT']['NAME'] == '':
                print_error('PROJECT_EMPTY_NAME')
                if not showerrors:
                    return False
            for c in ['NAME', 'URL', 'ALT', 'DATE', 'SECTION']:
                if c not in cfg['AUTHOR'].keys():
                    print_error('AUTHOR_ENTRY', c)
                    if not showerrors:
                        return False
            for c in ['TITLE', 'SHOW']:
                if c not in cfg['AUTHOR']['SECTION'].keys():
                    print_error('AUTHOR_SECTION_ENTRY', c)
                    if not showerrors:
                        return False
            if cfg['AUTHOR']['SECTION']['SHOW']:
                if cfg['AUTHOR']['SECTION']['TITLE'] == '':
                    print_error('AUTHOR_SECTION_EMPTY_IF_ENABLED')
                    if not showerrors:
                        return False
            badges = cfg['BADGES']
            for k in badges.keys():
                for c in ['IMAGE', 'HREF', 'ALT']:
                    if c not in badges[k]:
                        print_error('BADGE_ENTRY', [c, k])
                        if not showerrors:
                            return False
                    if badges[k]['IMAGE'] == '':
                        print_error('BADGE_IMAGE_EMPTY', k)
                        if not showerrors:
                            return False
                if not k.isdigit():
                    print_error('BADGE_TAG_NUMERIC', k)
                    if not showerrors:
                        return False
            if cfg['CONTENT'] == '':
                print_error('CONTENT_EMPTY')
                if not showerrors:
                    return False
            else:
                filepath = os.path.split(configfile)
                contentpath = filepath[0] + '/' + cfg['CONTENT']
                if not os.path.isfile(contentpath):
                    print_error('CONTENT_FILE_NOT_EXIST', contentpath)
                    if not showerrors:
                        return False
            self._loadedfile = cfg
            return True
        except Exception as e:
            self._errorsound()
            self._print(self._lang['PROCESS_ERROR'])
            self._print(str(e))
            self._print(traceback.format_exc())
            return False


if __name__ == '__main__':
    App().run()
