import sublime
import sublime_plugin
import os
import re


class PhpSyntaxChecker(sublime_plugin.EventListener):
    TARGET_SUFFIXES = [".php", ".module", ".inc"]

    def on_post_save(self, view):
        settings = sublime.load_settings("PhpSyntaxChecker.sublime-settings").get("smelly")
        path = view.file_name()
        root, extension = os.path.splitext(path)

        if extension in self.TARGET_SUFFIXES:
            code = open(path, 'r').read()

            ignore = re.compile('\/\/\slegitimate')

            l = 1
            errors = ''
            for line in code.split("\n"):
                for smell in settings:
                    ex = re.compile(settings[smell])
                    if ex.search(line) and not ignore.search(line):
                        errors += "%s smells bad at line %i\n" % (smell, l)
                l = l + 1

            if len(errors):
                # sublime.error_message(errors)
                os.system('terminal-notifier -message "' + errors + '"')
