import sublime, sublime_plugin, urllib, json, os, re

class SyncSniptCommand(sublime_plugin.TextCommand):

    def get_username(self):
        # snipt plugin settings
        self.settings = sublime.load_settings("Snipt.sublime-settings")
        self.username = self.settings.get('snipt_username')

    def run(self, edit):
        # check for username config
        self.get_username()
        username = self.username

        if (not self.username):
            sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
        else:
            # grab all user account
            response = urllib.urlopen('http://snipt.net/api/users/%s.json' % username)
            parse = json.load(response)
            parse_me = parse['snipts']

        	# current location + repo
            cwd = os.getcwd() + '/repo/'

            # run the loop
            for item in parse_me:
                # grab the user url and parse the snipts
                response = urllib.urlopen('http://beta.snipt.net/api/public/snipt/%s/?format=json' % item)
                parse = json.load(response)
                code = parse['code']

                # cleaning the title for filename
                title = parse['title']
                rx = re.compile('\W+')
                cleantitle = rx.sub(' ', title).strip()

                # lets turn wine (snipts) into water (sublime snippets)
                buildfile = cwd + '%s.sublime-snippet' % cleantitle[0:20]
                newfile = open(buildfile,'w')
                newfile.write('<snippet><content><![CDATA[%s]]></content><tabTrigger>snipt</tabTrigger></snippet>' % code)
                newfile.close()

class CreateSniptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print 1