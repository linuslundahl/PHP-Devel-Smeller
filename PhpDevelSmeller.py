import sublime
import sublime_plugin
import os
import re


class PhpDevelSmeller(sublime_plugin.EventListener):
    def on_post_save(self, view):
        """Finds and alerts the user of smelly PHP code."""
        settings = sublime.load_settings("PhpDevelSmeller.sublime-settings")
        path = view.file_name()
        extension = os.path.splitext(path)[1]

        if extension in settings.get("extensions"):
            smells = settings.get("smells")
            code = open(path, 'r', encoding='utf-8').read()
            ignore = re.compile('\/\/\slegitimate\r')

            i = 1
            errors = []
            for line in code.split("\n"):
                for smell in smells:
                    ex = re.compile(smells[smell])
                    if ex.search(line) and not ignore.search(line):
                        errors.append("%s:%i" % (smell, i))
                i = i + 1

            if len(errors):
                errors = ', '.join(errors)
                if settings.get("use_notification_center"):
                    os.system('terminal-notifier -message "' + errors + '"')
                else:
                    sublime.error_message(errors)


class PhpDevelCleanerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Cleans the current file from smelly code."""
        settings = sublime.load_settings("PhpDevelSmeller.sublime-settings")
        path = self.view.file_name()
        extension = os.path.splitext(path)[1]

        if extension in settings.get("extensions"):
            smells = settings.get("smells")
            ignore = re.compile('\/\/\slegitimate\r')

            edit = self.view.begin_edit()
            for smell in smells:
                offset = 0
                i = 0
                arr = []
                for region in self.view.find_all("^.*(" + smells[smell] + ".*;)\\n?$"):
                    line = self.view.substr(self.view.line(region))
                    if not ignore.search(line):
                        arr.append(sublime.Region(region.begin() + offset, region.end() + offset))
                        offset -= arr[i].size()
                        i = i + 1

                for i in arr:
                    self.view.erase(edit, i)
            self.view.end_edit(edit)
