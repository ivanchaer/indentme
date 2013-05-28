import sublime, sublime_plugin, re

from indentme_modules.parser import ParseMe

# Load Settings

settings = sublime.load_settings('indentme.sublime-settings')
def get_setting(name, default=None):
   v = settings.get(name)
   if v == None:
      try:
         return sublime.active_window().active_view().settings().get(name, default)
      except AttributeError:
         # No view defined.
         return default
   else:
      return v
    

class IndentMe(ParseMe):
  modifications = {}

  def put_indented_file(self):
    
    output = ''

    for i in range(len(self.status['originalFileStr'])):

      output += (self.status['originalFileStr'][i])

      if (i, 'br') in self.modifications:
        if self.modifications[(i, 'br')]:
          output += '\n'

      if (i, 'indent') in self.modifications:
        if self.modifications[(i, 'indent')] > 0:
          output += (self.status['indentationStr'] * self.modifications[(i, 'indent')])

      if (i, 'message') in self.modifications:
        output += self.modifications[(i, 'message')]

    return output

      
  # ................................................................
  #
  # Methods to get tag settings from settings file
  #
  # ................................................................

  def get_tag_settings_id(self,tag):
    # Check if tag is on libraries
    tagOnLibrary = [i for i in get_setting("tag-libraries")["html-tags"] if tag == i]
  
    # Otherwise, use default settings
    if len(tagOnLibrary) == 0: tagOnLibrary = [i for i in get_setting("tag-libraries")["html-tags"] if "default" == i]

    return tagOnLibrary


  def break_after_tag(self, tag):
    return get_setting("tag-libraries")["html-tags"][tag]["line-break"]["after"] == True

  def break_before_tag(self, tag):
    return get_setting("tag-libraries")["html-tags"][tag]["line-break"]["before"] == True

  def break_inside_tag(self, tag):
    return get_setting("tag-libraries")["html-tags"][tag]["line-break"]["inside"] == True

  def indent_tag_contents(self, tag):
    return get_setting("tag-libraries")["html-tags"][tag]["contents"]["indented"] == True

  def format_tag_contents(self, tag):
    return get_setting("tag-libraries")["html-tags"][tag]["contents"]["formatted"] == True


  # ................................................................
  #
  # Handles
  #
  # ................................................................

  def handle_open_tag(self):
    self.status['lastOpenTagSettings'] = self.get_tag_settings_id(self.status['lastProcessedTag'])

    if self.break_before_tag(self.status['lastOpenTagSettings'][0]): 
      self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags']) - 1
      self.modifications[(self.status['index'] - 1, 'br')] = True

  def handle_end_tag(self):

    lastProcessedTagSettings = self.get_tag_settings_id(self.status['lastProcessedTag'])
    lastOpenTagSettings = self.get_tag_settings_id(self.status['lastOpenTagSettings'][0])

    if self.break_inside_tag(lastProcessedTagSettings[0]): 
      self.status['breakAfterChar'] = True
      self.status['indentAfterChar'] = True

  def handle_end_auto_closed_tag(self):

    # if the tag specifies this setting, insert break after tag closes
    if self.break_after_tag(self.status['lastOpenTagSettings'][0]): 
      self.status['breakAfterChar'] = True
      self.status['indentAfterChar'] = True

  def handle_start_closure_tag(self):

    processedTagSettings = self.get_tag_settings_id(self.status['lastProcessedTag'])

    # If the closure matches the last open tag
    if self.status['startedTagIsAnXHTMLClosure']:
      
      if self.break_inside_tag(processedTagSettings[0]): 
        # self.modifications[(self.status['index'] - 1, 'message')] = str(processedTagSettings)
        self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags'])
        self.modifications[(self.status['index'] - 1, 'br')] = True

    elif self.status['startedTagIsAValidClosure']:

      if self.break_inside_tag(processedTagSettings[0]): 
        
        self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags']) - 1
        self.modifications[(self.status['index'] - 1, 'br')] = True

      

  def handle_start_comment_tag(self):
    self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags'])
    self.modifications[(self.status['index'] - 1, 'br')] = True

  def handle_end_comment_tag(self):
    self.status['breakAfterChar'] = True
    self.status['indentAfterChar'] = True

  def handle_start_open_style_tag(self):
    self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags'])
    self.modifications[(self.status['index'] - 1, 'br')] = True
  def handle_end_style_closure_tag(self):
    self.status['breakAfterChar'] = True
    self.status['indentAfterChar'] = True

  def handle_start_script_open_tag(self):
    self.modifications[(self.status['index'] - 1, 'indent')] = len(self.status['openTags'])
    self.modifications[(self.status['index'] - 1, 'br')] = True
  def handle_end_script_closure_tag(self):
    self.modifications['']
    #self.status[(self.status['index'], 'message')] = '!!!'
    self.status['indentAfterChar'] = True



  def handle_parse_content(self):
    if re.search(r'[\n|\r|\r\n]', self.status['char']):
      self.status['indentAfterChar'] = True

  def handle_end_iteration(self):
    """
    Create dictionary of modifications to make
    """

    # Set the indentation level to correspond to the number of tags open
    self.status['indentationLevel'] = len(self.status['openTags'])

    # Add line break after char when needed
    if self.status['doFormat'] and self.status['breakAfterChar']:
      self.modifications[(self.status['index'],'br')] = True 

    # Add indentation after char when needed
    if self.status['doIndent'] and self.status['indentAfterChar']:
      self.modifications[(self.status['index'], 'indent')] = self.status['indentationLevel']


    # Reset listeners
    self.status['breakAfterChar'] = False
    self.status['indentAfterChar'] = False
    
  def handle_start_parsing(self):
    self.modifications = {}

  def handle_end_parsing(self):
    return self.put_indented_file()