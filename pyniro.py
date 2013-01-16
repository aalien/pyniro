# -*- coding: utf-8 -*-

import re
import urllib
import appuifw
import globalui
import telephone
import e32

class NameFetcher:
    def __init__(self):
        self.re = re.compile('<div class="header">(?P<name>[^<]*)<\/div>')
        self.query = 'http://wap.eniro.fi/query?login_name=%s' + \
                     '&login_password=%s&what=moball&search_word=%s'

    def fetch_name(self, number, user, passwd):
        try:
            conn = urllib.urlopen(self.query %(user, passwd, number))
            data = conn.read()
        except IOError:
            return None
        match = self.re.search(data)
        name = match.groupdict()['name']
        name = ' '.join(map(lambda s: s.capitalize(), name.split(' ')))
        return name

class Main:
    def __init__(self):
        self.lock = e32.Ao_lock()
        self.fetcher = NameFetcher()
        self.user = ''
        self.passwd = ''
    
    def run(self):
        appuifw.app.exit_key_handler = self.quit
        self.user = str(appuifw.query(u'Käyttäjänimi:', 'number'))
        self.passwd = str(appuifw.query(u'Salasana:', 'number'))
        telephone.call_state(self.call_state_changed)
        self.lock.wait()

    def call_state_changed(self, call):
        (state, number) = call
        if state == telephone.EStatusRinging:
            name = self.fetcher.fetch_name(number, self.user, self.passwd)
            text = u'Numeron %s omistaa %s' %(number, name)
            print text
            globalui.global_note(text, 'text')

    def quit(self):
        self.lock.signal()

if __name__ == '__main__':
    pyniro = Main()
    pyniro.run()
