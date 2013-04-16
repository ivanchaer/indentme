import sublime, sublime_plugin, re

from ParseMe import ParseMe


class UnindentMe(ParseMe):

  tagMap = {}

  def put_indented_file(self):

    output = []
    lastI = 0
    for i in sorted(self.tagMap):
      # output += '%s, %s; ' % (i, self.tagMap[i])

      area = self.status['originalFileStr'][lastI:i]

      area = re.sub(r'[\n|\r|\r\n]\s*|[\n|\r|\r\n]+', r'\n', area)
      area = re.sub(r'^[\n|\r|\r\n]|[\n|\r|\r\n]$', '', area)

      if self.tagMap[i] == 'tag':
        output += [area]

      elif self.tagMap[i] == 'content':
        output += [area]

      lastI = i



    return ''.join(output)

      
  # ................................................................
  #
  # Handles
  #
  # ................................................................

  def handle_open_tag(self):
  
    self.tagMap[self.status['index']] = 'content'
    
  def handle_end_tag(self):

    self.tagMap[self.status['index'] + 1] = 'tag'

  def handle_end_auto_closed_tag(self):

    self.tagMap[self.status['index'] + 1] = 'tag'

  def handle_start_closure_tag(self):

    self.tagMap[self.status['index']] = 'content'

  def handle_end_parsing(self):

    return self.put_indented_file()

  def handle_start_comment_tag(self):
    self.tagMap[self.status['index']] = 'content'

  def handle_end_comment_tag(self):
    self.tagMap[self.status['index'] + 1] = 'tag'

  def handle_start_open_style_tag(self):
    self.tagMap[self.status['index']] = 'content'

  def handle_start_style_closure_tag(self):
    self.tagMap[self.status['index'] + 1] = 'tag'

  def handle_start_script_open_tag(self):
    self.tagMap[self.status['index']] = 'content'

  def handle_start_script_closure_tag(self):
    self.tagMap[self.status['index'] + 1] = 'tag'

  
