import sublime, sublime_plugin, urllib2, json, os, re

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
            # grab the user data
            try:
                response = urllib2.urlopen('http://snipt.net/api/users/%s.json' % username)
            except urllib2.URLError, (err):
                sublime.error_message("Connection refused. Try again later. Snipt step: 1")
                return
            
            # grab all user snipt #'s
            parse = json.load(response)
            parse_me = parse['snipts']

        	# current location + repo
            cwd = os.getcwd() + '/repo/'

            # run the loop
            for item in parse_me:
                
                # grab the user url and parse the snipts
                try:
                    response = urllib2.urlopen('http://beta.snipt.net/api/public/snipt/%s/?format=json' % item)
                except urllib2.URLError, (err):
                    sublime.error_message("Connection refused. Try again later. Snipt step: 2")
                    return

                # parse the response for code snipt 
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

# This is coming soon. Ability to send text to snipt.net and create a sublime snippet.
# class CreateSniptCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         print 1