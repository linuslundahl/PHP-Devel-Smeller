import sublime
import sublime_plugin
import os
import re


class PhpDevelSmeller(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings("PhpDevelSmeller.sublime-settings")
        path = view.file_name()
        root, extension = os.path.splitext(path)

        if extension in settings.get("extensions"):
            smells = settings.get("smells")
            code = open(path, 'r').read()

            ignore = re.compile('\/\/\slegitimate')

            l = 1
            errors = ''
            for line in code.split("\n"):
                for smell in smells:
                    ex = re.compile(smells[smell])
                    if ex.search(line) and not ignore.search(line):
                        errors += "%s smells bad at line %i\n" % (smell, l)
                l = l + 1

            if len(errors):
                if (settings.get("use_notification_center")):
                    os.system('terminal-notifier -message "' + errors + '"')
                else:
                    sublime.error_message(errors)
