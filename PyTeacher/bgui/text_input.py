
"""

This module defines the following constants:

*InputText options*
	* BGUI_INPUT_NONE = 0
	* BGUI_INPUT_SELECT_ALL = 1

	* BGUI_INPUT_DEFAULT = BGUI_INPUT_NONE
"""

from .widget import Widget, WeakMethod, BGUI_DEFAULT, BGUI_CENTERY, \
	BGUI_NO_FOCUS, BGUI_MOUSE_ACTIVE, BGUI_MOUSE_CLICK, BGUI_MOUSE_RELEASE, \
	BGUI_NO_NORMALIZE
from .key_defs import *
from .label import Label
from .frame import Frame

import time
import re

# InputText options
BGUI_INPUT_NONE = 0
BGUI_INPUT_SELECT_ALL = 1

BGUI_INPUT_DEFAULT = BGUI_INPUT_NONE


class TextInput(Widget):
	"""Widget for getting text input"""
	theme_section = 'TextInput'
	theme_options = {
				'TextColor': (1, 1, 1, 1),
				'FrameColor': (0, 0, 0, 0),
				'BorderSize': 0,
				'BorderColor': (0, 0, 0, 0),
				'HighlightColor': (0.6, 0.6, 0.6, 0.5),
				'InactiveTextColor': (1, 1, 1, 1),
				'InactiveFrameColor': (0, 0, 0, 0),
				'InactiveBorderSize': 0,
				'InactiveBorderColor': (0, 0, 0, 0),
				'InactiveHighlightColor': (0.6, 0.6, 0.6, 0.5),
				'LabelSubTheme': '',
				}

	def __init__(self, parent, name=None, text="", prefix="", font=None, pt_size=None, color=None,
					aspect=None, size=[1, 1], pos=[0, 0], sub_theme='', input_options=BGUI_INPUT_DEFAULT, options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param text: the text to display (this can be changed later via the text property)
		:param prefix: prefix text displayed before user input, cannot be edited by user (this can be changed later via the prefix property)
		:param font: the font to use
		:param pt_size: the point size of the text to draw
		:param color: color of the font for this widget
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""

		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)

		self.text_prefix = prefix
		self.pos = len(text)
		self.input_options = input_options
		self.colors = {}
		self.pt_size=pt_size

		#create widgets
		self.frame = Frame(self, size=[1, 1], options=BGUI_NO_FOCUS | BGUI_DEFAULT)
		self.highlight = Frame(self, size=self.frame.size, border=0, options=BGUI_NO_FOCUS | BGUI_NO_NORMALIZE)
		self.cursor = Frame(self, size=[1, 1], border=0, options=BGUI_NO_FOCUS | BGUI_NO_NORMALIZE)
		self.label = Label(self, text=text, font=font, pt_size=pt_size, sub_theme=self.theme['LabelSubTheme'], options=BGUI_NO_FOCUS | BGUI_DEFAULT)

		#Color and setting initialization
		self.colormode = 0

		theme = self.theme

		self.colors["text"] = [None, None]
		self.colors["text"][0] = theme['InactiveTextColor']
		self.colors["text"][1] = theme['TextColor']

		self.colors["frame"] = [None, None]
		self.colors["frame"][0] = theme['InactiveFrameColor']
		self.colors["frame"][1] = theme['FrameColor']

		self.colors["border"] = [None, None]
		self.colors["border"][0] = theme['InactiveBorderColor']
		self.colors["border"][1] = theme['BorderColor']

		self.colors["highlight"] = [None, None]
		self.colors["highlight"][0] = theme['HighlightColor']
		self.colors["highlight"][1] = theme['HighlightColor']

		self.border_size = [None, None]
		self.border_size[0] = theme['InactiveBorderSize']
		self.border_size[1] = theme['BorderSize']

		self.swapcolors(0)

		#gauge height of the drawn font
		fd = self.system.textlib.dimensions(self.label.fontid, "Egj/}|^,")
		self.height=fd[1]
		py = 1 - (fd[1] / self.size[1])
		px = fd[1] / self.size[0] - fd[1] / 1.5 / self.size[0]
		self.label.position = [px, py]
		self.fd = self.system.textlib.dimensions(self.label.fontid, self.text_prefix)[0] + fd[1] / 3.2

		self.frame.size = [1, 1]
		self.frame.position = [0, 0]

		self.slice = [len(text), len(text)]
		self.slice_direction = 0
		self.mouse_slice_start = 0
		self.mouse_slice_end = 0
		#create the char width list
		self._update_char_widths()

		#initial call to update_selection
		self.selection_refresh = 1
		self.just_activated = 0
		self._active = 0  # internal active state to avoid confusion from parent active chain

		#blinking cursor
		self.time = time.time()

		#double/triple click functionality
		self.click_counter = 0
		self.single_click_time = 0.0
		self.double_click_time = 0.0

		# On Enter callback
		self._on_enter_key = None

		#line number
		self.lineNumber = 0

		self.lineHeight = 0

	@property
	def text(self):
		return self.label.text

	@property
	def prefix(self):
		return self.text_prefix

	@prefix.setter
	def prefix(self, value):
		self.fd = self.system.textlib.dimensions(self.label.fontid, value)[0] + fd[0] / 3.2
		self.text_prefix = value

	@property
	def on_enter_key(self):
		"""A callback for when the enter key is pressed while the TextInput has focus"""
		return self._on_enter_key

	@on_enter_key.setter
	def on_enter_key(self, value):
		self._on_enter_key = WeakMethod(value)

	#utility functions
	def _update_char_widths(self):
		self.char_widths = []
		for char in self.text:
			self.char_widths.append(self.system.textlib.dimensions(self.label.fontid, char * 20)[0] / 20)

	def select_all(self):
		"""Change the selection to include all of the text"""
		self.slice = [0, len(self.text)]
		self.update_selection()

	def select_none(self):
		"""Change the selection to include none of the text"""
		self.slice = [0, 0]
		self.update_selection()

	#Activation Code
	def activate(self):
		if self.frozen:
			return
		self.system.focused_widget = self
		self.swapcolors(1)
		self.colormode = 1
		if self.input_options & BGUI_INPUT_SELECT_ALL:
			self.slice = [0, len(self.text)]
			self.slice_direction = -1
		self.just_activated = 1
		self._active = 1

	def deactivate(self):
		self.system.focused_widget = self.system
		self.swapcolors(0)
		self.colormode = 0
		self.just_activated = 0
		self._active = 0

	def swapcolors(self, state=0):  # 0 inactive 1 active

		self.frame.colors = [self.colors["frame"][state]] * 4
		self.frame.border = self.border_size[state]
		self.frame.border_color = self.colors["border"][state]
		self.highlight.colors = [self.colors["highlight"][state]] * 4
		self.label.color = self.colors["text"][state]

	#Selection Code
	def update_selection(self):
		# generate a list of all the lines
		newlines = [ (i.start(), i.end()) for i in re.finditer('\n', self.text)]
		newlines.insert(0,(0,0))
		newlines.append((len(self.text), len(self.text)))
		# find left and right cursor position in the relevant line
		left = self.fd + self.system.textlib.dimensions(self.label.fontid, self.text[newlines[self.lineNumber][1]:self.slice[0]])[0]
		right = self.fd + self.system.textlib.dimensions(self.label.fontid, self.text[newlines[self.lineNumber][1]:self.slice[1]])[0]
		# if text is highlited set find the position of the text ( 34.425 is the number of lines in the window)
		self.highlight.position = [left, (self.size[1] - (self.lineNumber + 1) * self.size[1]/34.425)]
		# the height of the highlite is the same as text height, the width is calculated using the selected positions
		self.highlight.size = [right - left, self.label._pt_size]
		# set the direction of the highlite, whether it is running from right to left or left to right
		if self.slice_direction in [0, 1]:
			self.cursor.position = [left, (self.size[1] - (self.lineNumber + 1) * self.size[1]/34.425)]
		else:
			self.cursor.position = [right, (self.size[1] - (self.lineNumber + 1) * self.size[1]/34.425)]
		self.cursor.size = [1, self.label._pt_size ]

	def find_mouse_slice(self, pos):
		# generate a list of all the lines
		newlines = [(i.start(), i.end()) for i in re.finditer('\n', self.text)]
		newlines.insert(0,(0,0))
		newlines.append((len(self.text), len(self.text)))
		#find the line number clicked by the mouse
		self.lineNumber = (int)(34.425 - ((34.425/self.size[1])*(pos[1]-30)))
		# ensure the cursor is not below the last line
		if self.lineNumber > len(newlines)-2:
			self.lineNumber = len(newlines)-2
		cmc = self.calc_mouse_cursor(pos)
		mss = self.mouse_slice_start
		self.mouse_slice_end = cmc
		# determine whether the mouse has just been clicked or beeing dragged to the left or to the right
		if cmc < mss:
			self.slice_direction = -1
			self.slice = [self.mouse_slice_end+newlines[self.lineNumber][1], self.mouse_slice_start+newlines[self.lineNumber][1]]
		elif cmc > mss:
			self.slice_direction = 1
			self.slice = [self.mouse_slice_start+newlines[self.lineNumber][1], self.mouse_slice_end+newlines[self.lineNumber][1]]
		else:
			self.slice_direction = 0
			self.slice = [self.mouse_slice_start+newlines[self.lineNumber][1], self.mouse_slice_end+newlines[self.lineNumber][1]]
		self.selection_refresh = 1

	#calculate the position relative to the text for highliting
	def calc_mouse_cursor(self, pos):
		newlines = [ (i.start(), i.end()) for i in re.finditer('\n', self.text)]
		newlines.insert(0,(0,0))
		newlines.append((len(self.text), len(self.text)))
		adj_pos = pos[0] - (self.position[0] + self.fd)
		find_slice = 0
		i = 0
		self._update_char_widths()
		for entry in self.char_widths[newlines[self.lineNumber][1]:newlines[self.lineNumber+1][0]]:
			if find_slice + entry > adj_pos:
				if abs((find_slice + entry) - adj_pos) >= abs(adj_pos - find_slice):
					return i
				else:
					return i
			else:
				find_slice += entry
			i += 1

		self.time = time.time() - 0.501

		return i

	#Method for calulating whether the mouse was clicked or dragged
	def _handle_mouse(self, pos, event):
		"""Extend function's behaviour by providing focus to unfrozen inactive TextInput,
		swapping out colors.
		"""
		if self.frozen:
			return
		if event == BGUI_MOUSE_CLICK:
			newlines = [ (i.start(), i.end()) for i in re.finditer('\n', self.text)]
			newlines.insert(0,(0,0))
			newlines.append((len(self.text), len(self.text)))
			self.mouse_slice_start = self.calc_mouse_cursor(pos)
			if not self._active:
				self.activate()
			if not self.input_options & BGUI_INPUT_SELECT_ALL:
				self.find_mouse_slice(pos)
		elif event == BGUI_MOUSE_ACTIVE:
			if not self.just_activated or self.just_activated and not self.input_options & BGUI_INPUT_SELECT_ALL:
				self.find_mouse_slice(pos)
		if event == BGUI_MOUSE_RELEASE:
			self.selection_refresh = 1
			if self.slice[0] == self.slice[1]:
				self.slice_direction = 0
			self.just_activated = 0
			self.time = time.time()

		Widget._handle_mouse(self, pos, event)

	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		newlines = [ (i.start(), i.end()) for i in re.finditer('\n', self.text)]
		newlines.insert(0,(0,0))
		newlines.append((len(self.text), len(self.text)))
		if self != self.system.focused_widget:
			return

		# Try char to int conversion for alphanumeric keys... kinda hacky though
		try:
			key = ord(key)
		except:
			pass

		if is_shifted:
			sh = 0  #used for slicing
		else:
			sh = 1
		slice_len = abs(self.slice[0] - self.slice[1])
		x, y = 0, 0

		if key == BACKSPACEKEY:
			if slice_len != 0:
				self.label.text = self.text[:self.slice[0]] + self.text[self.slice[1]:]
				self.char_widths = self.char_widths[:self.slice[0]] + self.char_widths[self.slice[1]:]
				self.slice = [self.slice[0], self.slice[0]]
				#handle char length list
			elif self.slice[0] > 0:
				self.label.text = self.text[:self.slice[0] - 1] + self.text[self.slice[1]:]
				self.slice = [self.slice[0] - 1, self.slice[1] - 1]
				if (self.slice[0] < newlines[self.lineNumber][1]):
					self.lineNumber = self.lineNumber-1
		elif key == DELKEY:
			if slice_len != 0:
				self.label.text = self.text[:self.slice[0]] + self.text[self.slice[1]:]
				self.char_widths = self.char_widths[:self.slice[0]] + self.char_widths[self.slice[1]:]
				self.slice = [self.slice[0], self.slice[0]]
			elif self.slice[1] < len(self.text):
				self.label.text = self.text[:self.slice[0]] + self.text[self.slice[1] + 1:]

		elif key == LEFTARROWKEY:
			slice_len = abs(self.slice[0] - self.slice[1])
			if (self.slice_direction in [-1, 0]):
				if is_shifted and self.slice[0] > 0:
					self.slice = [self.slice[0] - 1, self.slice[1]]
					self.slice_direction = -1
				elif is_shifted:
					pass
				else:
					if slice_len > 0:
						self.slice = [self.slice[0], self.slice[0]]
					elif self.slice[0] > 0:
						if (self.slice[1] == newlines[self.lineNumber][1]):
							self.lineNumber = self.lineNumber - 1
							self.slice = [self.slice[0] - 1, self.slice[0] - 1]
						else:
							self.slice = [self.slice[0] - 1, self.slice[0] - 1]
					self.slice_direction = 0

			elif self.slice_direction == 1:
				if is_shifted:
					self.slice = [self.slice[0], self.slice[1] - 1]
				else:
					self.slice = [self.slice[0], self.slice[0]]
				if self.slice[0] - self.slice[1] == 0:
					self.slice_direction = 0

		elif key == RIGHTARROWKEY:
			slice_len = abs(self.slice[0] - self.slice[1])
			if (self.slice_direction in [1, 0]):
				if is_shifted  and self.slice[1] < len(self.text):
					self.slice = [self.slice[0], self.slice[1] + 1]
					self.slice_direction = 1
				elif is_shifted:
					pass
				else:
					if slice_len > 0:
						self.slice = [self.slice[1], self.slice[1]]
					elif self.slice[1] < len(self.text):
						if (self.slice[1] == newlines[self.lineNumber+1][0]):
							self.lineNumber = self.lineNumber + 1
							self.slice = [self.slice[1] + 1, self.slice[1] + 1]
						else:
							self.slice = [self.slice[1] + 1, self.slice[1] + 1]
					self.slice_direction = 0
			elif self.slice_direction == -1:
				if is_shifted:
					self.slice = [self.slice[0] + 1, self.slice[1]]
				else:
					self.slice = [self.slice[1], self.slice[1]]
				if self.slice[0] - self.slice[1] == 0:
					self.slice_direction = 0
		elif key == DOWNARROWKEY:
			if self.lineNumber < len(newlines) - 2:
				self.lineNumber = self.lineNumber+1
				self.slice = [min((self.slice[0]-newlines[self.lineNumber-1][1])+newlines[self.lineNumber][1], newlines[self.lineNumber+1][0]),
							  min((self.slice[1]-newlines[self.lineNumber-1][1])+newlines[self.lineNumber][1], newlines[self.lineNumber+1][0])]
			#print (self.slice)
		elif key == UPARROWKEY:
			if (self.lineNumber > 0):
				self.lineNumber = self.lineNumber-1
				self.slice = [min((self.slice[0]-newlines[self.lineNumber+1][1]) + newlines[self.lineNumber][1], newlines[self.lineNumber+1][0]),
							  min((self.slice[1]-newlines[self.lineNumber+1][1]) + newlines[self.lineNumber][1], newlines[self.lineNumber+1][0])]
		else:
			char = None
			if ord(AKEY) <= key <= ord(ZKEY):
				if is_shifted: char = chr(key - 32)
				else: char = chr(key)

			elif ord(ZEROKEY) <= key <= ord(NINEKEY):
				if not is_shifted: char = chr(key)
				else:
					key = chr(key)
					if key == ZEROKEY: char = ")"
					elif key == ONEKEY: char = "!"
					elif key == TWOKEY: char = "@"
					elif key == THREEKEY: char = "#"
					elif key == FOURKEY: char = "$"
					elif key == FIVEKEY: char = "%"
					elif key == SIXKEY: char = "^"
					elif key == SEVENKEY: char = "&"
					elif key == EIGHTKEY: char = "*"
					elif key == NINEKEY: char = "("

			elif PAD0 <= key <= PAD9:
				char = str(key - PAD0)
			elif key == PADPERIOD: char = "."
			elif key == PADSLASHKEY: char = "/"
			elif key == PADASTERKEY: char = "*"
			elif key == PADMINUS: char = "-"
			elif key == PADPLUSKEY: char = "+"
			elif key == SPACEKEY: char = " "
			elif key == TABKEY: char = "\t"
			elif key == ENTERKEY :
				char = "\n"
				self.lineNumber = self.lineNumber + 1
			elif not is_shifted:
				if key == ACCENTGRAVEKEY: char = "`"
				elif key == MINUSKEY: char = "-"
				elif key == EQUALKEY: char = "="
				elif key == LEFTBRACKETKEY: char = "["
				elif key == RIGHTBRACKETKEY: char = "]"
				elif key == BACKSLASHKEY: char = "\\"
				elif key == SEMICOLONKEY: char = ";"
				elif key == QUOTEKEY: char = "'"
				elif key == COMMAKEY: char = ","
				elif key == PERIODKEY: char = "."
				elif key == SLASHKEY: char = "/"
			else:
				if key == ACCENTGRAVEKEY: char = "~"
				elif key == MINUSKEY: char = "_"
				elif key == EQUALKEY: char = "+"
				elif key == LEFTBRACKETKEY: char = "{"
				elif key == RIGHTBRACKETKEY: char = "}"
				elif key == BACKSLASHKEY: char = "|"
				elif key == SEMICOLONKEY: char = ":"
				elif key == QUOTEKEY: char = '"'
				elif key == COMMAKEY: char = "<"
				elif key == PERIODKEY: char = ">"
				elif key == SLASHKEY: char = "?"

			if char:
			    #need option to limit text to length of box
				#need to replace all selected text with new char
				#need copy place somewhere
				# as the tab character does not work, 4 spaces are used instead
				if (char == "\t"):
					self.label.text = self.text[:self.slice[0]] + " " + self.text[self.slice[1]:]
					self.label.text = self.text[:self.slice[0]] + " " + self.text[self.slice[1]:]
					self.label.text = self.text[:self.slice[0]] + " " + self.text[self.slice[1]:]
					self.label.text = self.text[:self.slice[0]] + " " + self.text[self.slice[1]:]
					self.slice[0] = self.slice[0] + 3
					self.slice[1] = self.slice[1] + 3
				else:
					self.label.text = self.text[:self.slice[0]] + char + self.text[self.slice[1]:]
				
				#update the slice
				self.slice = [self.slice[0] + 1, self.slice[0] + 1]
				self.slice_direction = 0

		#update selection widgets after next draw call
		self.selection_refresh = 1

		#ensure cursor is not hidden
		self.time = time.time()

	def _draw(self):
		temp = self.text
		self.label.text = self.text_prefix + temp

		if self == self.system.focused_widget and self._active == 0:
			self.activate()

		# Now draw the children
		Widget._draw(self)

		self.label.text = temp

		if self.colormode == 1 and self.system.focused_widget != self:
			self._active = 0
			self.swapcolors(0)
			self.virgin = 1
			self.colormode = 0

		#selection code needs to be called after draw, which is tracked internally to TextInput
		if self.selection_refresh == 1:
			self.update_selection()
			self.selection_refresh = 0

		#handle blinking cursor
		if self.slice[0] - self.slice[1] == 0 and self._active:
			if time.time() - self.time > 1.0:
				self.time = time.time()

			elif time.time() - self.time > 0.5:
				self.cursor.colors = [[0.0, 0.0, 0.0, 0.0]] * 4
			else:
				self.cursor.colors = [self.colors["text"][1]] * 4
		else:
			self.cursor.colors = [[0.0, 0.0, 0.0, 0.0]] * 4
