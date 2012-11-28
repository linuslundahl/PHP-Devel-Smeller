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
            errors = []
            for line in code.split("\n"):
                for smell in smells:
                    ex = re.compile(smells[smell])
                    if ex.search(line) and not ignore.search(line):
                        errors.append("%s:%i" % (smell, l))
                l = l + 1

            if len(errors):
                errors = ', '.join(errors)
                if (settings.get("use_notification_center")):
                    os.system('terminal-notifier -message "' + errors + '"')
                else:
                    sublime.error_message(errors)


class PhpDevelCleanerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("PhpDevelSmeller.sublime-settings")
        path = self.view.file_name()
        root, extension = os.path.splitext(path)

        if extension in settings.get("extensions"):
            smells = settings.get("smells")
            ignore = re.compile('\/\/\slegitimate')

            edit = self.view.begin_edit()
            for smell in smells:
                offset = 0
                i = 0
                r = []
                for region in self.view.find_all("^.*(" + smells[smell] + ".*;)\\n?$"):
                    line = self.view.substr(self.view.line(region))
                    if not ignore.search(line):
                        r.append(sublime.Region(region.begin() + offset, region.end() + offset))
                        offset -= r[i].size()
                        i = i + 1

                for i in r:
                    self.view.erase(edit, i)
            self.view.end_edit(edit)
