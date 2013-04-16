import re


class ParseMe():
  status = {}

  def __init__(self, fileStr):
    # Initial parsing listeners status 
    
    self.status = {
      'char': '',
      'originalFileStr':  fileStr,
      'index': 0,
      'openTags': [],
      'unfinishedTag': False,
      'tagStartedOnThisIteration': False,
      'tagClosedOnThisIteration': False,
      'lastProcessedTag': '',
      'openTagIsClosure': False,
      'openTagIsAValidClosure': False,
      'lastOpenTagSettings': "default",
      'attributeIsOpen': False,
      'attrQuotes': '',
      'doIndent': True,
      'doFormat': True,
      'indentationLevel': 0,
      'indentationStr': '  ',
      'indentedFileStr': '',
      'breakAfterChar': False,
      'indentAfterChar': False,
      'commentTagOpen': False,
      'styleTagOpen': False,
      'scriptTagOpen': False
    }
      
  
  # ................................................................
  #
  # Handles (to be overriden when instance is created)
  #
  # ................................................................

  def handle_open_tag(self):
    pass

  def handle_start_attribute(self):
    pass

  def handle_end_attribute(self):
    pass
    
  def handle_end_tag(self):
    pass

  def handle_end_auto_closed_tag(self):
    pass

  def handle_start_closure_tag(self):
    pass

  def handle_parse_content(self):
    pass

  def handle_start_comment_tag(self):
    pass

  def handle_end_comment_tag(self):
    pass

  def handle_start_style_tag(self):
    pass

  def handle_end_style_tag(self):
    pass

  def handle_start_script_tag(self):
    pass

  def handle_end_script_tag(self):
    pass

  def handle_end_iteration(self):
    pass

  def handle_end_parsing(self):
    pass


  # ................................................................
  #
  # Hooks
  #
  # ................................................................

  def hook_open_tag(self):

    self.status['tagStartedOnThisIteration'] = True
    self.status['lastProcessedTag'] = re.split(r'[\s|>]', self.status['originalFileStr'][self.status['index'] + 1 : ])[0]
    

    # Register last processed tag
    self.status['unfinishedTag'] = True

    self.handle_open_tag()

  def hook_start_attribute(self):

    self.status['attributeIsOpen'] = True;
    self.status['attrQuotes'] = self.status['char']

    self.handle_start_attribute()

  def hook_end_attribute(self):
        
    self.status['attributeIsOpen'] = False;
    self.status['attrQuotes']=''

    self.handle_end_attribute()
    
  def hook_end_tag(self):

    self.status['unfinishedTag'] = False
    
    self.handle_end_tag()
  
    # Reset listeners
    self.status['openTagIsAValidClosure'] = False
    self.status['openTagIsClosure'] = False

  def hook_end_auto_closed_tag(self):

    self.status['unfinishedTag'] = False
    
    self.handle_end_auto_closed_tag()

  def hook_start_closure_tag(self):

    self.status['unfinishedTag'] = True
    self.status['openTagIsClosure'] = True

    self.status['lastProcessedTag'] = re.split(r'[\s|>]', self.status['originalFileStr'][self.status['index'] + 2 : ])[0]

    # If the closure matches the last open tag
    if len(self.status['openTags']) > 0 and self.status['openTags'][-1] == self.status['lastProcessedTag']:
      self.status['openTagIsAValidClosure'] = True

    self.handle_start_closure_tag()

  def hook_parse_content(self):
    self.handle_parse_content()

  def hook_start_comment_tag(self):
    self.status['commentTagOpen'] = True
    self.handle_start_comment_tag()

  def hook_end_comment_tag(self):
    self.status['commentTagOpen'] = False
    self.handle_end_comment_tag()

  def hook_start_style_tag(self):
    self.status['styleTagOpen'] = True
    self.handle_start_style_tag()

  def hook_end_style_tag(self):
    self.status['styleTagOpen'] = False
    self.handle_end_style_tag()

  def hook_start_script_tag(self):
    self.status['scriptTagOpen'] = True
    self.handle_start_script_tag()

  def hook_end_script_tag(self):
    self.status['scriptTagOpen'] = False
    self.handle_end_script_tag()

  def hook_end_iteration(self):
    self.handle_end_iteration()

  def hook_end_parsing(self):
    self.handle_end_parsing()

  # ................................................................
  #
  # Perform parse and call required methods
  #
  # ................................................................
  def run(self):

    for self.status['index'] in range(len(self.status['originalFileStr'])):

      self.status['char'] = self.status['originalFileStr'][self.status['index']]

      # If a comment tag is ending (eg. -->)
      if self.status['index'] > 2 and self.status['char'] == '>' and self.status['originalFileStr'][self.status['index'] - 2 : self.status['index'] + 1] == '-->' and self.status['attributeIsOpen'] == False and self.status['commentTagOpen'] == True:
        self.hook_end_comment_tag()

      # If a comment tag is starting (eg. <!--)
      elif self.status['index'] + 4 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 4] == '<!--' and self.status['attributeIsOpen'] == False:
        self.hook_start_comment_tag()


      # If a style tag is ending (eg. </style>)
      if self.status['index'] + 8 < len(self.status['originalFileStr']) == '<' and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 8] == '</style>' and self.status['attributeIsOpen'] == False and self.status['styleTagOpen'] == True:
        self.hook_end_style_tag()

      # If a style tag is starting (eg. <style>)
      elif self.status['index'] + 6 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 6] == '<style' and self.status['attributeIsOpen'] == False:
        self.hook_start_style_tag()


      # If a script tag is ending (eg. </script>)
      if self.status['index'] + 9 < len(self.status['originalFileStr']) == '<' and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 9] == '</script>' and self.status['attributeIsOpen'] == False and self.status['scriptTagOpen'] == True:
        self.hook_end_script_tag()

      # If a script tag is starting (eg. <script>)
      elif self.status['index'] + 7 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 7] == '<script' and self.status['attributeIsOpen'] == False:
        self.hook_start_script_tag()


      if self.status['commentTagOpen'] == False and self.status['styleTagOpen'] == False and self.status['scriptTagOpen'] == False:

        # If a tag is being opened
        if re.search(r'<\w', self.status['originalFileStr'][self.status['index'] : self.status['index'] + 2]) and self.status['attributeIsOpen'] == False:
          self.hook_open_tag()

        # If a closure tag is starting (eg. </div>)
        elif self.status['char'] == '<' and self.status['originalFileStr'][self.status['index'] + 1] == '/':
          self.hook_start_closure_tag()

        # If a tag is already open
        elif self.status['unfinishedTag']:

          # If there is no attribute open
          if self.status['attributeIsOpen'] == False:

            # If an attribute is being opened
            if (self.status['char'] == '"' or self.status['char'] == '\''):
              self.hook_start_attribute()

            # If a tag is being auto closed (eg. <br />)
            elif self.status['char'] == '>' and self.status['originalFileStr'][self.status['index'] - 1] == '/':
              self.hook_end_auto_closed_tag()

            # If a tag is being ended
            elif self.status['char'] == '>':
              self.hook_end_tag()

          # If an attribute is being closed
          elif self.status['char'] == self.status['attrQuotes']:
            self.hook_end_attribute()

        # Parsing content
        else:
          self.hook_parse_content()

      self.hook_end_iteration()

      if self.status['index'] + 1 == len(self.status['originalFileStr']):
        self.hook_end_parsing()
      
    return