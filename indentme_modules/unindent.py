import sublime, sublime_plugin, re

from indentme_modules.parser import ParseMe


class UnindentMe(ParseMe):

  tagMap = {}

  def put_indented_file(self):
    
    output = []
    lastI = 0
    for i in sorted(self.tagMap):
      # output += '%s, %s; ' % (i, self.tagMap[i])

      area = self.status['originalFileStr'][lastI:i]

      # output += ['%s - %s (%s) [%s];\n' % (lastI, i, area, self.tagMap[i])]

      if self.tagMap[i] != 'script' and self.tagMap[i] != 'style' and self.tagMap[i] != 'comment':
        area = re.sub(r'[\n|\r|\r\n]\s*|[\n|\r|\r\n]+', r'\n', area)
        area = re.sub(r'^[\n|\r|\r\n]|[\n|\r|\r\n]$', '', area)

      output += ['%s' % area]

      lastI = i

    output = ''.join(output)

    # output = ''

    # for i in range(len(self.status['originalFileStr'])):

    #   if i in self.tagMap:
    #     output += '(' + self.tagMap[i] + ')'

    #   output += (self.status['originalFileStr'][i])


    return output

      
  # ................................................................
  #
  # Handles
  #
  # ................................................................

  

  def handle_start_parsing(self):
    self.tagMap = {}
    self.tagMap[0] = 'startfile'

  def handle_end_parsing(self):
    self.tagMap[len(self.status['originalFileStr'])] = 'endfile'
    return self.put_indented_file()



  def handle_open_tag(self):
    lastOpenTag = self.tagMap[max(self.tagMap.keys())]

    self.tagMap[self.status['index']] = lastOpenTag

  def handle_start_closure_tag(self):

    lastOpenTag = self.tagMap[max(self.tagMap.keys())]

    self.tagMap[self.status['index']] = lastOpenTag
    
  def handle_end_tag(self):
    
    tagBeingClosed = self.status['lastProcessedTag']

    self.tagMap[self.status['index'] + 1] = 'tag'

    if tagBeingClosed == 'script':
      self.tagMap[self.status['index'] + 1] = 'script'
    elif tagBeingClosed == 'style':
      self.tagMap[self.status['index'] + 1] = 'style'

  def handle_parse_content(self):
    lastOpenTag = self.tagMap[max(self.tagMap.keys())]
    
    if lastOpenTag == 'content':
      del self.tagMap[max(self.tagMap.keys())]

    if lastOpenTag == 'comment':
      self.tagMap[self.status['index'] + 1] = 'comment'
    else:
      self.tagMap[self.status['index'] + 1] = 'content'
    
  def handle_end_auto_closed_tag(self):

    self.tagMap[self.status['index'] + 1] = 'tag'

  def handle_end_comment_tag(self):
    self.tagMap[self.status['index'] + 1] = 'comment'

  def handle_start_style_closure_tag(self):
    self.tagMap[self.status['index']] = 'style'

  def handle_start_script_closure_tag(self):
    self.tagMap[self.status['index']] = 'script'

  
