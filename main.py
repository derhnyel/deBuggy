import sys
from psutil import Process,NoSuchProcess
import os
import pyfiglet
import threading
#import multiprocessing
import requests
#import urwid
#import webbrowser
#from urwid.widget import (BOX, FLOW, FIXED)
from bs4 import BeautifulSoup as bs4 
import re
from fake_useragent import UserAgent
import curses
from curses.textpad import rectangle
from curses import wrapper
#import argparse
#import asyncio
#import pickle
#import time
#
#from collections import deque

#from termcolor import colored, cprint
#import time
# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# Scrollbar positions
SCROLLBAR_LEFT = "left"
SCROLLBAR_RIGHT = "right"


bold='\033[01m'
underline='\033[04m'
reverse='\033[07m'
black='\033[30m'
red='\033[31m'
green='\033[32m'
orange='\033[33m'
blue='\033[34m'
purple='\033[35m'
cyan='\033[36m'
lightgrey='\033[37m'
darkgrey='\033[90m'
lightred='\033[91m'
lightgreen='\033[92m'
yellow='\033[93m'
lightblue='\033[94m'
pink='\033[95m'
lightcyan='\033[96m'
#end = '\033[0m'
end =''


# def LoadAnimation(LoadString):
  
#     # String to be displayed when the application is loading
    
#     StringLength = len(LoadString)
  
  
#     # String for creating the rotating line
#     animation = "|/-\\"
#     AniCount = 0
      
#     # used to keep the track of
#     # the duration of animation
#     CountTime = 0        
      
#     # pointer for travelling the loading string
#     pointer = 0                     
  
#     while (CountTime != 100):  
#         # used to change the animation speed
#         # smaller the value, faster will be the animation
#         time.sleep(0.01)                          
#         # converting the string to list
#         # as string is immutable
#         ListString = list(LoadString) 
#         # ascii->obtaining the ASCII code
#         ascii = ord(ListString[pointer])
#         # cache->for storing altered ASCII code
#         cache = 0                             
#         # if the character is "." or " ", keep it unaltered
#         # switch uppercase to lowercase and vice-versa 
#         if ascii != 32 and ascii != 46:             
#             if ascii>90:
#                 cache = ascii-32
#             else:
#                 cache = ascii + 32
#             ListString[pointer]= chr(cache)
#         # for storing the resulting string
#         ResultString =''             
#         for index in range(StringLength):
#             ResultString = ResultString + ListString[index]      
#         # displaying the resulting string
#         sys.stdout.write("\r"+ResultString + animation[AniCount])
#         sys.stdout.flush()
#         # Assigning loading string
#         # to the resulting string
#         LoadString= ResultString
#         AniCount = (AniCount + 1)% 4
#         pointer =(pointer + 1)% StringLength
#         CountTime = CountTime + 1
#    os.system('cls' if OsName=='nt' else 'clear')

def StylizeCode(Text):
    """Identifies and stylizes code in a question or answer."""
    # TODO: Handle blockquotes and markdown
    StylizedText = []
    CodeBlocks = [block.get_text() for block in Text.find_all("code")]
    BlockQuotes = [block.get_text() for block in Text.find_all("blockquote")]
    newline = False

    for child in Text.recursiveChildGenerator():
        name = getattr(child, "name", None)

        if name is None: # Leaf (terminal) node
            if child in CodeBlocks:
                if newline: # Code block
                    #if code_blocks.index(child) == len(code_blocks) - 1: # Last code block
                        #child = child[:-1]
                    StylizedText.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    StylizedText.append(("code", u"%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')
                StylizedText.append(u"%s" % str(child))

    if type(StylizedText[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if StylizedText[-2][1].endswith('\n'):
            StylizedText[-2] = ("code", StylizedText[-2][1][:-1])

    return StylizedText


def GSearch(Error):
  url = 'https://google.com/search?q=' 
  site = ' site:stackoverflow.com'
  souper=ParseUrl(url+Error+site)
  def has_href_but_no_class(tag):
      return tag.has_attr('href') and not tag.has_attr('class')

  TitlesInTags =souper.select('div h3') 
  titles=[TitlesInTags[title].text for title in range(len(TitlesInTags))]

  LinksInTags=souper.find_all(has_href_but_no_class)

  format=re.compile(r'/(.*)?q=(.*)') 

  links=[]
  for link_href in LinksInTags:
      link = link_href['href']
      regex = format.search(link)
      try:
          if regex.group(1) in 'url?' and '.google.com/' not in regex.group(2):
              links.append(regex.group(2))
      except:
          pass
  #results=[]
  # for index in range(len(titles)):
  #     SearchDict ={}
  #     SearchDict['title']=titles[index]
  #     SearchDict['link']=links[index]
  #     results.append(SearchDict)
      #SearchDict['description']=descriptions[index]
  
  return (titles,links)    

# def GSearch(Error):
#     Error+=' site:stackoverflow.com'
#     from search_engine_parser.core.engines.google import Search as GoogleSearch
#     #search_results=[]
#     gs = GoogleSearch()
    
#     SearchArgs=(Error,1)
#     #try:
#     SearchDict=gs.search(*SearchArgs)
#     # for result in SearchDict:
#     # #   #if 'stackoverflow' in result["link"]:
#     # #     print(
#     # #     result["link"])/URL
#     # #     print(result["title"])/Title
#     # #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     # #     print(result["description"])/Awnsers
#     # #     print('#####################################################################################')  
#     # #     print('------------------------------------------------------------------------------------')
#     #         search_results.append({
#     #         "Title": result["title"],
#     #         #"Body": result.find_all("div", class_="excerpt")[0].text,
#     #         #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
#     #         "Answers": result["description"],
#     #         "URL": result["link"]})
#     return SearchDict#list(SearchDict)

def SoF (url):
  HtmlText= ParseUrl(url)
  QTitle = HtmlText.find_all('a', class_="question-hyperlink")[0].get_text()
  QStatus = HtmlText.find("div", attrs={"itemprop": "upvoteCount"}).get_text() # Vote count
  QStatus += " Votes | Asked " + HtmlText.find("time", attrs={"itemprop": "dateCreated"}).get_text() # Date created
  QDescription = StylizeCode(HtmlText.find_all("div", class_="s-prose js-post-body")[0]) # TODO: Handle duplicates

  answers = [StylizeCode(answer) for answer in HtmlText.find_all("div", class_="s-prose js-post-body")][1:]
  if len(answers) == 0:
      answers.append(("no answers", u"\nNo answers for this question."))

  return QTitle,QDescription,QStatus, answers




def ParseUrl(url):
    """Turns a given URL into a BeautifulSoup object."""
    try:
        Response = requests.get(url, headers={"User-Agent": UAgent.random})
    except requests.exceptions.RequestException:
        sys.stdout.write("\n%s%s%s" % (red, "Rebound was unable to fetch Stack Overflow results. "
                                            "Please check that you are connected to the internet.\n", end))
        sys.exit(1)
    if "\.com/nocaptcha" in Response.url: # URL is a captcha page
        return None
    else:
        return bs4(Response.text, "html.parser")  












    # except Exception as e:
    #   print(e)

      




def UserConfirm(question):
      ValidInputs = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
      prompt = "[Y/n] "
      while True:
        print(reverse+cyan+bold+question+prompt+end,file=sys.stdout)
        UserChoice= input().lower()
        #for inputs in sys.stdin:
        #  UserChoice = input
        #  break
        #UserChoice=sys.stdin.read()
        if UserChoice in ValidInputs:
          return ValidInputs[UserChoice]
        #PrintColor = lambda x,y,z:cprint(x,y,z) 
        #text = colored("Please respond with 'yes' or 'no' (or 'y' or 'n').\n",'blue',attrs=['reverse','blink'])  
        #print(text)
        print(reverse+blue+"Please respond with 'yes' or 'no' (or 'y' or 'n').\n",file=sys.stdout)


def CheckErrorMessage(ErrorMessage):
    """Filters the ErrorMessage and returns valid."""
    if ErrorMessage=='':
        return False
    else:
        if any(error in ErrorMessage for error in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            return False
        else:
            return True  
def execute():
  try:      
      while True:
          RunningProcess = Process(ProcessId)
  except NoSuchProcess as e:
        return False
  
def MonitorProcess():
  global ProcessState,ErrorMessage,ValidError
  ProcessState = execute()
  #clear terminal  
  with open('log.err','r') as log:
    ErrMessage = log.read()
    ValidError=print(red+bold+ErrMessage,file=sys.stdout) if CheckErrorMessage(ErrMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
    ErrorMessage = ErrMessage.split('\n')
  if ValidError:
    print(red+bold+ErrMessage,file=sys.stdout)
    DisplayResult = UserConfirm('DeBuggy Wants to Display Search Results?: ')
    if DisplayResult:
        ErrorMessage = ErrMessage.split('\n')
        #[print(i) for i in ErrorMessage]
        
        #return ErrorMessage 
    else:
      sys.exit(1)    
  else:
    sys.exit(1)
          

          #pickle_off=  open('cache','rb')    
          #emp=pickle.load(pickle_off) 

    


#if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            #return None
  #async def Parser(self):
   #   res = await self.MonitorProcess() 
    #stackoverflow
    #stackexchange
    #gitcommunity

    #check if error message has been geerated
def CleanError():
      #RootNode code from traceback =2
       #Root Module imported and method =3
       #base for raise Exceptions =-2 error type
       #base for error and cause = -1
  #ErrorType = RawErrorMessage[-2].split(" ").remove('raise')
  #ErrorType=' '.join(ErrorType)
  error = ErrorMessage[-2]#.split(':')
  ErrorLineno = int(ErrorMessage[1].split(',')[1].strip(' line'))
  error = error
  return (ErrorLineno,error)
  #get module name

## Main ##


# class Scrollable(urwid.WidgetDecoration):
#     # TODO: Fix scrolling behavior (works with up/down keys, not with cursor)

#     def sizing(self):
#         return frozenset([BOX,])


#     def selectable(self):
#         return True


#     def __init__(self, widget):
#         """Box widget (wrapper) that makes a fixed or flow widget vertically scrollable."""
#         self._trim_top = 0
#         self._scroll_action = None
#         self._forward_keypress = None
#         self._old_cursor_coords = None
#         self._rows_max_cached = 0
#         self._rows_max_displayable = 0
#         self.__super.__init__(widget)


#     def render(self, size, focus=False):
#         maxcol, maxrow = size

#         # Render complete original widget
#         ow = self._original_widget
#         ow_size = self._get_original_widget_size(size)
#         canv = urwid.CompositeCanvas(ow.render(ow_size, focus))
#         canv_cols, canv_rows = canv.cols(), canv.rows()

#         if canv_cols <= maxcol:
#             pad_width = maxcol - canv_cols
#             if pad_width > 0: # Canvas is narrower than available horizontal space
#                 canv.pad_trim_left_right(0, pad_width)

#         if canv_rows <= maxrow:
#             fill_height = maxrow - canv_rows
#             if fill_height > 0: # Canvas is lower than available vertical space
#                 canv.pad_trim_top_bottom(0, fill_height)
#         self._rows_max_displayable = maxrow
#         if canv_cols <= maxcol and canv_rows <= maxrow: # Canvas is small enough to fit without trimming
#             return canv

#         self._adjust_trim_top(canv, size)

#         # Trim canvas if necessary
#         trim_top = self._trim_top
#         trim_end = canv_rows - maxrow - trim_top
#         trim_right = canv_cols - maxcol
#         if trim_top > 0:
#             canv.trim(trim_top)
#         if trim_end > 0:
#             canv.trim_end(trim_end)
#         if trim_right > 0:
#             canv.pad_trim_left_right(0, -trim_right)

#         # Disable cursor display if cursor is outside of visible canvas parts
#         if canv.cursor is not None:
#             curscol, cursrow = canv.cursor
#             if cursrow >= maxrow or cursrow < 0:
#                 canv.cursor = None

#         # Let keypress() know if original_widget should get keys
#         self._forward_keypress = bool(canv.cursor)

#         return canv


#     def keypress(self, size, key):
#         if self._forward_keypress:
#             ow = self._original_widget
#             ow_size = self._get_original_widget_size(size)

#             # Remember previous cursor position if possible
#             if hasattr(ow, "get_cursor_coords"):
#                 self._old_cursor_coords = ow.get_cursor_coords(ow_size)

#             key = ow.keypress(ow_size, key)
#             if key is None:
#                 return None

#         # Handle up/down, page up/down, etc
#         command_map = self._command_map
#         if command_map[key] == urwid.CURSOR_UP:
#             self._scroll_action = SCROLL_LINE_UP
#         elif command_map[key] == urwid.CURSOR_DOWN:
#             self._scroll_action = SCROLL_LINE_DOWN
#         elif command_map[key] == urwid.CURSOR_PAGE_UP:
#             self._scroll_action = SCROLL_PAGE_UP
#         elif command_map[key] == urwid.CURSOR_PAGE_DOWN:
#             self._scroll_action = SCROLL_PAGE_DOWN
#         elif command_map[key] == urwid.CURSOR_MAX_LEFT: # "home"
#             self._scroll_action = SCROLL_TO_TOP
#         elif command_map[key] == urwid.CURSOR_MAX_RIGHT: # "end"
#             self._scroll_action = SCROLL_TO_END
#         else:
#             return key

#         self._invalidate()


#     def mouse_event(self, size, event, button, col, row, focus):
#         ow = self._original_widget
#         if hasattr(ow, "mouse_event"):
#             ow_size = self._get_original_widget_size(size)
#             row += self._trim_top
#             return ow.mouse_event(ow_size, event, button, col, row, focus)
#         else:
#             return False


#     def _adjust_trim_top(self, canv, size):
#         """Adjust self._trim_top according to self._scroll_action"""
#         action = self._scroll_action
#         self._scroll_action = None

#         maxcol, maxrow = size
#         trim_top = self._trim_top
#         canv_rows = canv.rows()

#         if trim_top < 0:
#             # Negative trim_top values use bottom of canvas as reference
#             trim_top = canv_rows - maxrow + trim_top + 1

#         if canv_rows <= maxrow:
#             self._trim_top = 0  # Reset scroll position
#             return

#         def ensure_bounds(new_trim_top):
#             return max(0, min(canv_rows - maxrow, new_trim_top))

#         if action == SCROLL_LINE_UP:
#             self._trim_top = ensure_bounds(trim_top - 1)
#         elif action == SCROLL_LINE_DOWN:
#             self._trim_top = ensure_bounds(trim_top + 1)
#         elif action == SCROLL_PAGE_UP:
#             self._trim_top = ensure_bounds(trim_top - maxrow+1)
#         elif action == SCROLL_PAGE_DOWN:
#             self._trim_top = ensure_bounds(trim_top + maxrow-1)
#         elif action == SCROLL_TO_TOP:
#             self._trim_top = 0
#         elif action == SCROLL_TO_END:
#             self._trim_top = canv_rows - maxrow
#         else:
#             self._trim_top = ensure_bounds(trim_top)

#         if self._old_cursor_coords is not None and self._old_cursor_coords != canv.cursor:
#             self._old_cursor_coords = None
#             curscol, cursrow = canv.cursor
#             if cursrow < self._trim_top:
#                 self._trim_top = cursrow
#             elif cursrow >= self._trim_top + maxrow:
#                 self._trim_top = max(0, cursrow - maxrow + 1)


#     def _get_original_widget_size(self, size):
#         ow = self._original_widget
#         sizing = ow.sizing()
#         if FIXED in sizing:
#             return ()
#         elif FLOW in sizing:
#             return (size[0],)


#     def get_scrollpos(self, size=None, focus=False):
#         return self._trim_top


#     def set_scrollpos(self, position):
#         self._trim_top = int(position)
#         self._invalidate()


#     def rows_max(self, size=None, focus=False):
#         if size is not None:
#             ow = self._original_widget
#             ow_size = self._get_original_widget_size(size)
#             sizing = ow.sizing()
#             if FIXED in sizing:
#                 self._rows_max_cached = ow.pack(ow_size, focus)[1]
#             elif FLOW in sizing:
#                 self._rows_max_cached = ow.rows(ow_size, focus)
#             else:
#                 raise RuntimeError("Not a flow/box widget: %r" % self._original_widget)
#         return self._rows_max_cached

#     @property
#     def scroll_ratio(self):
#         return self._rows_max_cached / self._rows_max_displayable

# class ScrollBar(urwid.WidgetDecoration):
#     # TODO: Change scrollbar size and color(?)

#     def sizing(self):
#         return frozenset((BOX,))


#     def selectable(self):
#         return True


#     def __init__(self, widget, thumb_char=u'\u2588', trough_char=' ',
#                  side=SCROLLBAR_RIGHT, width=1):
#         """Box widget that adds a scrollbar to `widget`."""
#         self.__super.__init__(widget)
#         self._thumb_char = thumb_char
#         self._trough_char = trough_char
#         self.scrollbar_side = side
#         self.scrollbar_width = max(1, width)
#         self._original_widget_size = (0, 0)
#         self._dragging = False


#     def render(self, size, focus=False):
#         maxcol, maxrow = size

#         ow = self._original_widget
#         ow_base = self.scrolling_base_widget
#         ow_rows_max = ow_base.rows_max(size, focus)
#         if ow_rows_max <= maxrow: # Canvas fits without scrolling - no scrollbar needed
#             self._original_widget_size = size
#             return ow.render(size, focus)

#         sb_width = self._scrollbar_width
#         self._original_widget_size = ow_size = (maxcol-sb_width, maxrow)
#         ow_canv = ow.render(ow_size, focus)

#         pos = ow_base.get_scrollpos(ow_size, focus)
#         posmax = ow_rows_max - maxrow

#         # Thumb shrinks/grows according to the ratio of
#         # <number of visible lines> / <number of total lines>
#         thumb_weight = min(1, maxrow / max(1, ow_rows_max))
#         thumb_height = max(1, round(thumb_weight * maxrow))

#         # Thumb may only touch top/bottom if the first/last row is visible
#         top_weight = float(pos) / max(1, posmax)
#         top_height = int((maxrow-thumb_height) * top_weight)
#         if top_height == 0 and top_weight > 0:
#             top_height = 1

#         # Bottom part is remaining space
#         bottom_height = maxrow - thumb_height - top_height
#         assert thumb_height + top_height + bottom_height == maxrow

#         # Create scrollbar canvas
#         top = urwid.SolidCanvas(self._trough_char, sb_width, top_height)
#         thumb = urwid.SolidCanvas(self._thumb_char, sb_width, thumb_height)
#         bottom = urwid.SolidCanvas(self._trough_char, sb_width, bottom_height)
#         sb_canv = urwid.CanvasCombine([
#             (top, None, False),
#             (thumb, None, False),
#             (bottom, None, False),
#         ])

#         combinelist = [(ow_canv, None, True, ow_size[0]), (sb_canv, None, False, sb_width)]
#         if self._scrollbar_side != SCROLLBAR_LEFT:
#             return urwid.CanvasJoin(combinelist)
#         else:
#             return urwid.CanvasJoin(reversed(combinelist))


#     @property
#     def scrollbar_width(self):
#         return max(1, self._scrollbar_width)


#     @scrollbar_width.setter
#     def scrollbar_width(self, width):
#         self._scrollbar_width = max(1, int(width))
#         self._invalidate()


#     @property
#     def scrollbar_side(self):
#         return self._scrollbar_side


#     @scrollbar_side.setter
#     def scrollbar_side(self, side):
#         if side not in (SCROLLBAR_LEFT, SCROLLBAR_RIGHT):
#             raise ValueError("scrollbar_side must be 'left' or 'right', not %r" % side)
#         self._scrollbar_side = side
#         self._invalidate()


#     @property
#     def scrolling_base_widget(self):
#         """Nearest `base_widget` that is compatible with the scrolling API."""
#         def orig_iter(w):
#             while hasattr(w, "original_widget"):
#                 w = w.original_widget
#                 yield w
#             yield w

#         def is_scrolling_widget(w):
#             return hasattr(w, "get_scrollpos") and hasattr(w, "rows_max")

#         for w in orig_iter(self):
#             if is_scrolling_widget(w):
#                 return w

#     @property
#     def scrollbar_column(self):
#         if self.scrollbar_side == SCROLLBAR_LEFT:
#             return 0
#         if self.scrollbar_side == SCROLLBAR_RIGHT:
#             return self._original_widget_size[0]

#     def keypress(self, size, key):
#         return self._original_widget.keypress(self._original_widget_size, key)


#     def mouse_event(self, size, event, button, col, row, focus):
#         ow = self._original_widget
#         ow_size = self._original_widget_size
#         handled = False
#         if hasattr(ow, "mouse_event"):
#             handled = ow.mouse_event(ow_size, event, button, col, row, focus)

#         if not handled and hasattr(ow, "set_scrollpos"):
#             if button == 4: # Scroll wheel up
#                 pos = ow.get_scrollpos(ow_size)
#                 if pos > 0:
#                     ow.set_scrollpos(pos - 1)
#                     return True
#             elif button == 5: # Scroll wheel down
#                 pos = ow.get_scrollpos(ow_size)
#                 ow.set_scrollpos(pos + 1)
#                 return True
#             elif col == self.scrollbar_column:
#                 ow.set_scrollpos(int(row*ow.scroll_ratio))
#                 if event == "mouse press":
#                     self._dragging = True
#                 elif event == "mouse release":
#                     self._dragging = False
#             elif self._dragging:
#                 ow.set_scrollpos(int(row*ow.scroll_ratio))
#                 if event == "mouse release":
#                     self._dragging = False



#         return False


# class SelectableText(urwid.Text):
#     def selectable(self):
#         return True


#     def keypress(self, size, key):
#         return key


# ## Helper Functions ##


# def interleave(a, b):
#     result = []
#     while a and b:
#         result.append(a.pop(0))
#         result.append(b.pop(0))

#     result.extend(a)
#     result.extend(b)

#     return result

# class App(object):
#     def __init__(self, search_results):
#         self.search_results, self.viewing_answers = search_results, False
#         self.palette = [
#             ("title", "light cyan,bold", "default", "standout"),
#             ("stats", "light green", "default", "standout"),
#             ("menu", "black", "light cyan", "standout"),
#             ("reveal focus", "black", "light cyan", "standout"),
#             ("reveal viewed focus", "yellow, bold", "light cyan", "standout"),
#             ("no answers", "light red", "default", "standout"),
#             ("code", "brown", "default", "standout"),
#             ("viewed", "yellow", "default", "standout")
#         ]
#         self.menu = urwid.Text([
#             u'\n',
#             ("menu", u" ENTER "), ("light gray", u" View answers "),
#             ("menu", u" B "), ("light gray", u" Open browser "),
#             ("menu", u" Q "), ("light gray", u" Quit"),
#         ])

#         results = list(map(lambda result: urwid.AttrMap(SelectableText(self._stylize_title(result)), None, "reveal focus"), self.search_results)) # TODO: Add a wrap='clip' attribute
#         self.content = urwid.SimpleListWalker(results)
#         self.content_container = urwid.ListBox(self.content)
#         layout = urwid.Frame(body=self.content_container, footer=self.menu)

#         self.main_loop = urwid.MainLoop(layout, self.palette, unhandled_input=self._handle_input)
#         self.original_widget = self.main_loop.widget

#         self.main_loop.run()


#     def _handle_input(self, input):
#         if input == "enter" or (input[0]=='meta mouse press' and input[1]==1): # View answers   Either press Enter or "ALT + Left Click"
#             url = self._get_selected_link()

#             if url != None:
#                 self.viewing_answers = True
#                 question_title, question_desc, question_stats, answers = SoF(url)

#                 pile = urwid.Pile(self._stylize_question(question_title, question_desc, question_stats) + [urwid.Divider('*')] +
#                 interleave(answers, [urwid.Divider('-')] * (len(answers) - 1)))
#                 padding = ScrollBar(Scrollable(urwid.Padding(pile, left=2, right=2)))
#                 #filler = urwid.Filler(padding, valign="top")
#                 linebox = urwid.LineBox(padding)

#                 menu = urwid.Text([
#                     u'\n',
#                     ("menu", u" ESC "), ("light gray", u" Go back "),
#                     ("menu", u" B "), ("light gray", u" Open browser "),
#                     ("menu", u" Q "), ("light gray", u" Quit"),
#                 ])

#                 # highlight the selected answer
#                 _, idx = self.content_container.get_focus()
#                 txt = self.content[idx].original_widget.text
#                 self.content[idx] = urwid.AttrMap(SelectableText(txt), 'viewed', 'reveal viewed focus')

#                 self.main_loop.widget = urwid.Frame(body=urwid.Overlay(linebox, self.content_container, "center", ("relative", 60), "middle", 23), footer=menu)
#         elif input in ('b', 'B') or (input[0]=='ctrl mouse press' and input[1]==1): # Open link     Either press (B or b) or "CTRL + Left Click"
#             url = self._get_selected_link()

#             if url != None:
#                 webbrowser.open(url)
#         elif input == "esc": # Close window
#             if self.viewing_answers:
#                 self.main_loop.widget = self.original_widget
#                 self.viewing_answers = False
#             else:
#                 raise urwid.ExitMainLoop()
#         elif input in ('q', 'Q'): # Quit
#             raise urwid.ExitMainLoop()


#     def _get_selected_link(self):
#         focus_widget, idx = self.content_container.get_focus() # Gets selected item
#         title = focus_widget.base_widget.text

#         for result in self.search_results:
#             if title == self._stylize_title(result): # Found selected title's search_result dict
#                 if 'stackoverflow.com' in result["link"]:
#                     return result["link"]
#                 else:
#                   print("OPENING BROWSER")
#                   #TODO: #redirect to browser


#     def _stylize_title(self, search_result):
#         if search_result["description"] == 1:
#             return "%s (1 Description)" % search_result["title"]
#         else:
#             return "%s (%s Description)" % (search_result["title"], search_result["description"])


#     def _stylize_question(self, title, desc, stats):
#         new_title = urwid.Text(("title", u"%s" % title))
#         new_stats = urwid.Text(("stats", u"%s\n" % stats))

#         return [new_title, desc, new_stats]

def print_menu(stdscr,rw_idx,menu):
    stdscr.clear()
    #h,w = stdscr.getmaxyx()
    for idx,row in enumerate(menu):
        x = 10
        y = 0 + len(menu) + idx
        if idx == rw_idx:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(2))
        else:    
            stdscr.addstr(y,x,row)
    stdscr.refresh()

def FetchResult():#stdscr):
  global trigger,links,titles
  while True:
    if not ProcessState and ValidError:
      ErrorLineNumber,ErrMessage= CleanError()
      titles,links = GSearch(ErrMessage)
      if len(titles)==len(links):
        trigger=True
        break

def App(stdscr):
      #print(SResult)
      menu = titles
      y,x = stdscr.getmaxyx()
    # for result in links:
    #   QTitle,QDescription,QStatus, answers=SoF(result)
    #   #   menu.append(result["title"])
    #color pair init with i d,foreground,backgroud 
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_YELLOW)
      curses.init_pair(4,curses.COLOR_RED,curses.COLOR_YELLOW)
      
      ResultWindow = curses.newwin(y//2,x//2,10,10)
      curses.curs_set(False)

      current_row = 0

      print_menu(stdscr,current_row,menu)
      while True: 
          key = stdscr.getch()
          stdscr.clear()

          if key == curses.KEY_UP:
              print_menu(stdscr,current_row-1 if current_row-1 is not -1 else current_row,menu)
              if current_row-1 is not -1:
                  current_row-=1
          elif key == curses.KEY_DOWN:
              print_menu(stdscr,current_row+1 if current_row+1 is not len(menu) else current_row,menu)
              if current_row+1 is not len(menu):
                  current_row+=1
          elif key == curses.KEY_ENTER or key in [10,13]:
              stdscr.addstr(0,0,menu[current_row])
              stdscr.refresh()      
              stdscr.getch()
              if current_row==len(menu)-1:
                  break
  
          print_menu(stdscr,current_row,menu)
          stdscr.refresh()            
                    
    
      #stdscr.addstr(y,x,'home')

if __name__=='__main__':
  #queue = deque()
  OsName=os.name
  UAgent = UserAgent()
  #LoadAnimation("starting your console application...")
  os.system('cls' if OsName=='nt' else 'clear')
  DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
  print(cyan+DebuggyAnimation,file=sys.stdout)
  print(green+bold+"Checking Running Script for Errors...",file=sys.stdout)
  ProcessId = int(sys.argv[1])
  ProcessState,ValidError,trigger  = (True,False,False)
  links,titles,ErrorMessage =(None,None,None)
  # p1 = multiprocessing.Process(target=main, args=())
  # p1.start()
  FetchResultThread = threading.Thread(target=FetchResult,args=())
  FetchResultThread.daemon = True
  FetchResultThread.start()
  
  while True:
    if not ProcessState:
      if trigger:
        wrapper(App)
        break
    else:
      MonitorProcess()
  
  #main()
  
  









       


#parser = argparse.ArgumentParser (prog='deBuggy',description='Used For Error Parsing')
#parser.add_argument()
# parser.add_argument("pid", type=str, help='Process Id of Current Running Python Process')
# parser.add_argument('-m','--mtr', help='monitor current process',action='store_true')
# args = parser.parse_args()
# bugZy = Debuggy(int(args.pid))
# if args.mtr:
#   print('monitor: %s' % args.pid)
#   bugZy.MonitorProcess()



# syntax_error= """\nForgetting to put a : at the end of an if, elif, else, for, while, class, or def statement. (Causes “SyntaxError: invalid syntax”)
# # \nThis error happens with code like this:
# # \nif spam == 42 
# #                ^      
# #     print('Hello!')"""

#import os
#import time
#       #filename.close()
#   finally:
#       sys.stdout = sys_out
#sys.exit() 
#filename = open('dump.txt','w')
#sys_out = sys.stdout
#sys.stdout = filename
# k  = sys.path
# p = sys.platform
# error = None

