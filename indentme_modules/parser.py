import re


class ParseMe():
  status = {}
  optionalClosures = []


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
      'startedTagIsClosure': False,
      'startedTagIsAnXHTMLClosure': False,
      'startedTagIsAValidClosure': False,
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

    self.optionalClosures = ['HTML', 'HEAD', 'BODY', 'P', 'DT', 'DD', 'LI', 'OPTION', 'THEAD', 'TH', 'TBODY', 'TR', 'TD', 'TFOOT', 'COLGROUP']
    
    self.nonClosingTags = ['IMG', 'INPUT', 'BR', 'HR', 'FRAME', 'AREA', 'BASE', 'BASEFONT', 'COL', 'ISINDEX', 'LINK', 'META', 'PARAM' ]

  
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

  def handle_start_open_style_tag(self):
    pass

  def handle_start_style_closure_tag(self):
    pass

  def handle_end_style_closure_tag(self):
    pass

  def handle_start_script_open_tag(self):
    pass

  def handle_start_script_closure_tag(self):
    pass

  def handle_end_script_closure_tag(self):
    pass

  def handle_end_iteration(self):
    pass

  def handle_start_parsing(self):
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

    if len(self.status['openTags']) > 0 and self.status['openTags'][-1] == self.status['lastProcessedTag'] and self.status['lastProcessedTag'].upper() in (OCT.upper() for OCT in self.optionalClosures):    
      
      # Remove the tag from the open tag array
      self.status['openTags'].pop()
      
    # Register last processed tag
    self.status['unfinishedTag'] = True

    if not self.status['lastProcessedTag'].upper() in (OCT.upper() for OCT in self.nonClosingTags):
      # Append tag to open tag list
      self.status['openTags'].append(self.status['lastProcessedTag'])

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
    self.status['startedTagIsAnXHTMLClosure'] = False
    self.status['startedTagIsClosure'] = False

  def hook_end_auto_closed_tag(self):

    self.status['unfinishedTag'] = False

    if not self.status['lastProcessedTag'].upper() in (OCT.upper() for OCT in self.nonClosingTags):
      self.status['openTags'].pop()
    
    self.handle_end_auto_closed_tag()

  def hook_start_closure_tag(self):

    self.status['unfinishedTag'] = True
    self.status['startedTagIsClosure'] = True

    self.status['lastProcessedTag'] = re.split(r'[\s|>]', self.status['originalFileStr'][self.status['index'] + 2 : ])[0]

    # If the closure matches the last open tag
    if len(self.status['openTags']) > 0 and self.status['openTags'][-1] == self.status['lastProcessedTag']:
      # Remove the tag from the open tag array
      self.status['openTags'].pop()
      self.status['startedTagIsAnXHTMLClosure'] = True

    elif len(self.status['openTags']) > 1 and self.status['openTags'][-2] == self.status['lastProcessedTag']:
      # Remove the last 2 tags from the open tag array
      self.status['openTags'].pop()
      self.status['openTags'].pop()
      self.status['startedTagIsAValidClosure'] = True

    self.handle_start_closure_tag()

  def hook_parse_content(self):
    self.handle_parse_content()

  def hook_start_comment_tag(self):
    self.status['commentTagOpen'] = True
    self.handle_start_comment_tag()

  def hook_end_comment_tag(self):
    self.status['commentTagOpen'] = False
    self.handle_end_comment_tag()

  def hook_start_open_style_tag(self):
    self.status['styleTagOpen'] = True
    self.handle_start_open_style_tag()

  def hook_start_style_closure_tag(self):
    self.status['styleTagOpen'] = False
    self.handle_start_style_closure_tag()

  def hook_end_style_closure_tag(self):
    self.handle_end_style_closure_tag()

  def hook_start_script_open_tag(self):
    self.status['scriptTagOpen'] = True
    self.handle_start_script_open_tag()

  def hook_start_script_closure_tag(self):
    self.status['scriptTagOpen'] = False
    self.handle_start_script_closure_tag()

  def hook_end_script_closure_tag(self):
    self.handle_end_script_closure_tag()

  def hook_end_iteration(self):
    self.handle_end_iteration()

  def hook_start_parsing(self):
    self.handle_start_parsing()

  def hook_end_parsing(self):
    self.handle_end_parsing()

  # ................................................................
  #
  # Perform parse and call required methods
  #
  # ................................................................
  def run(self):

    # Hook for when the parsing starts
    self.hook_start_parsing()

    for self.status['index'] in range(len(self.status['originalFileStr'])):

      self.status['char'] = self.status['originalFileStr'][self.status['index']]

      # If a comment tag is ending (eg. -->)
      if self.status['index'] > 2 and self.status['char'] == '>' and self.status['originalFileStr'][self.status['index'] - 2 : self.status['index'] + 1] == '-->' and self.status['attributeIsOpen'] == False and self.status['commentTagOpen'] == True:
        self.hook_end_comment_tag()

      # If a comment tag is starting (eg. <!--)
      elif self.status['index'] + 4 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 4] == '<!--' and self.status['attributeIsOpen'] == False:
        self.hook_start_comment_tag()


      # If a style closure tag is starting (eg. </style>)
      if self.status['index'] + 8 < len(self.status['originalFileStr']) and self.status['char'] == '<' and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 8] == '</style>' and self.status['attributeIsOpen'] == False and self.status['styleTagOpen'] == True:
        self.hook_start_style_closure_tag()

      # If a style opening tag is starting (eg. <style>)
      elif self.status['index'] + 6 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 6] == '<style' and self.status['attributeIsOpen'] == False:
        self.hook_start_open_style_tag()


      # If a script closure tag is starting (eg. </script>)
      if self.status['index'] + 9 < len(self.status['originalFileStr']) and self.status['char'] == '<' and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 9] == '</script>' and self.status['attributeIsOpen'] == False and self.status['scriptTagOpen'] == True:
        self.hook_start_script_closure_tag()

      # If a script opening tag is starting (eg. <script>)
      elif self.status['index'] + 7 < len(self.status['originalFileStr']) and self.status['originalFileStr'][self.status['index'] : self.status['index'] + 7] == '<script' and self.status['attributeIsOpen'] == False:
        self.hook_start_script_open_tag()


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
              # If the tag being ended is <script>
              if self.status['startedTagIsClosure'] and len(self.status['openTags']) > 0 and self.status['openTags'][-1] == 'script':
                self.hook_end_script_closure_tag()

              # If the tag being ended is <style>
              if self.status['startedTagIsClosure'] and len(self.status['openTags']) > 0 and self.status['openTags'][-1] == 'style':
                self.hook_end_style_closure_tag()

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