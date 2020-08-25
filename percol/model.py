# -*- coding: utf-8 -*-

import six
from percol import display, debug

class SelectorModel(object):
	def __init__(self,
				 percol, collection, finder,
				 query = None, caret = None, index = None):
				 # query = None, caret = None, index = None, recent = True):
		self.original_finder_class = finder
		self.percol = percol
		self.finder = finder(collection)
		self.setup_results(query)
		self.setup_caret(caret)
		self.setup_index(index)
		# self.recent = recent
		self.stack = []
		self.query_mode = True

	# ============================================================ #
	# Pager attributes
	# ============================================================ #

	@property
	def absolute_index(self):
		return self.index

	@property
	def results_count(self):
		return len(self.results)

	# ============================================================ #
	# Initializer
	# ============================================================ #

	
	def setup_results(self, query):
	# def setup_results(self, query, recent=False):
		self.query   = self.old_query = query or u""
		self.results = self.finder.get_results(self.query)
	
		self.marks   = {}

	def setup_caret(self, caret):
		if isinstance(caret, six.string_types):
			try:
				caret = int(caret)
			except ValueError:
				caret = None
		if caret is None or caret < 0 or caret > display.screen_len(self.query):
			caret = display.screen_len(self.query)
		self.caret = caret

	def setup_index(self, index):
		self.index = 0
		if index is None or index == "first":
			self.select_top()
		elif index == "last":
			self.select_bottom()
		else:
			self.select_index(int(index))

	# ============================================================ #
	# Result handling
	# ============================================================ #

	search_forced = False
	def force_search(self):
		self.search_forced = True

	def should_search_again(self):
		return self.query != self.old_query or self.search_forced

	old_query = u""
	def do_search(self, query):
		with self.percol.global_lock:
			self.index = 0
			self.results = self.finder.get_results(query)
			self.marks   = {}
			# search finished
			self.search_forced = False
			self.old_query = query

	def get_result(self, index):
		try:
			return self.results[index][0]
		except IndexError:
			return None

	def get_selected_result(self):
		return self.get_result(self.index)

	def get_selected_results_with_index(self):
		results = self.get_marked_results_with_index()
		if not results:
			try:
				index = self.index
				result = self.results[index] # EAFP (results may be a zero-length list)
				results.append((result[0], index, result[2]))
			except Exception as e:
				debug.log(f"model.py 102, get_selected_results_with_index, {self.finder.host}", e)
		# debug.log(results)
		return results


	def quote_path(self,path): # put quotes around paths with spaces
		withquotes = path
		if path.find(' '):
			withquotes = "\""+path+"\""
		return withquotes

	# Replacement for get_selected_results_with_index to select command or path, separated by sep
	def get_selected_results_with_index_f(self,sep,field=None):
		results = self.get_marked_results_with_index()
		# debug.log(f'model.py 116, sep:{sep}, r:{results}')
		
		if not results:
			try:
				index = self.index
				result = self.results[index] # EAFP (results may be a zero-length list)
				results.append((result[0], index, result[2]))
				# debug.log(f'model.py 123, {results}')
			except Exception as e:
				debug.log("model.py 124, get_selected_results_with_index_f", e)
		
		if field is not None:
			# debug.log(f'model.py 127, {results}')			
			if field == 1: # put quotes around directories
				newresults = []
				for r in results:					
					path = self.quote_path(r[0].split(sep)[1])
					newresults.append((path,r[1],r[2]))
					# debug.log("model.py, Modified path %s"%path)
				results = newresults
			elif field == -1: #chdir and run command
				newresults = []
				for r in results:
					path = self.quote_path(r[0].split(sep)[1])
					command = r[0].split(sep)[2]
					newresults.append((path+'; '+command,r[1],r[2]))
					# debug.log("model.py, Modified path %s"%path)
				results = newresults
			else:
				results = [(r[0].split(sep)[field],r[1],r[2]) for r in results]
				# debug.log(f'model.py 145, r:{results}')				
		
		return results


	def stack_selected_results_with_index_f(self,field=1,sep='║'):
		results = self.get_marked_results_with_index()
		if not results:
			try:
				index = self.index
				result = self.results[index] # EAFP (results may be a zero-length list)
				results.append((result[0], index, result[2]))
			except Exception as e:
				debug.log("model.py, stack_selected_results_with_index_f", e)
		if field is not None:
			results = [r[0].split(sep)[2] for r in results]
		self.stack += results

	def pop_stack(self):
		if len(self.stack) > 0:
			self.stack.pop()

	# ------------------------------------------------------------ #
	#  Selections
	# ------------------------------------------------------------ #

	def select_index(self, idx):
		try:
			# For lazy results, correct "results_count" by getting
			# items (if available)
			self.results[idx]
			self.index = idx
		except:
			pass
		if self.results_count > 0:
			self.index = idx % self.results_count

	def select_top(self):
		self.select_index(0)

	def select_bottom(self):
		self.select_index(-1)

	# ------------------------------------------------------------ #
	# Mark
	# ------------------------------------------------------------ #

	def get_marked_results_with_index(self):
		if self.marks:
			# debug.log([self.results[index][0] for index in self.marks if self.get_is_marked(index)])
			return [(self.results[index][0], index, self.results[index][2])
					for index in self.marks if self.get_is_marked(index)]
		else:        
			return []

	def set_is_marked(self, marked, index = None):
		if index is None:
			index = self.index          # use current index
		self.marks[index] = marked

	def get_is_marked(self, index = None):
		if index is None:
			index = self.index          # use current index
		return self.marks.get(index, False)

	# ------------------------------------------------------------ #
	# Caret position
	# ------------------------------------------------------------ #

	def set_caret(self, caret):
		q_len = len(self.query)
		self.caret = max(min(caret, q_len), 0)

	# ------------------------------------------------------------ #
	# Text
	# ------------------------------------------------------------ #

	def __decode_char(self, ch):
		if six.PY2:
			return chr(ch).decode(self.percol.encoding)
		else:
			return str(bytearray([ch]), encoding=self.percol.encoding)

	def append_char_to_query(self, ch):
		self.query += self.__decode_char(ch)
		self.forward_char()

	def insert_char(self, ch):
		q = self.query
		c = self.caret
		self.query = q[:c] + self.__decode_char(ch) + q[c:]
		self.set_caret(c + 1)

	def insert_string(self, string):
		caret_pos  = self.caret + len(string)
		self.query = self.query[:self.caret] + string + self.query[self.caret:]
		self.caret = caret_pos

	# ------------------------------------------------------------ #
	# Finder
	# ------------------------------------------------------------ #

	def remake_finder(self, new_finder_class):
		self.finder = self.finder.clone_as(new_finder_class)
