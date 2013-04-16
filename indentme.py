import sublime, sublime_plugin, re

from IndentMe import IndentMe

from UnindentMe import UnindentMe


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