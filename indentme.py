import sublime, sublime_plugin, re, sys, imp, os

sys.path.append(os.path.join(os.path.dirname(__file__), "indentme_modules"))

# Make sure all dependencies are reloaded on upgrade
if 'indentme_modules.reloader' in sys.modules:
    imp.reload(sys.modules['indentme_modules.reloader'])
import indentme_modules.reloader


from indentme_modules.indent import IndentMe

from indentme_modules.unindent import UnindentMe

from indentme_modules.parser import ParseMe



class indentmeCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    fileStr = self.view.substr(sublime.Region(0, self.view.size()))

    # Remove current formatting and indenting
    indentator = UnindentMe(fileStr)
    indentator.run()

    # Apply new indentation
    indentator = IndentMe(indentator.handle_end_parsing())
    indentator.run()



    reg = sublime.Region(0, self.view.size())
    self.view.replace(edit, reg, indentator.handle_end_parsing())