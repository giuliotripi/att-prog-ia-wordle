import string
import json
import re


def chars_in_str(chars, _string):
	for char in chars:
		if char not in _string:
			return False

	return True

def letters_in_word(word, letters):
	num = 0
	for letter in letters:
		if letter in word:
			num += 1

	return num


class WordleUtils:
	def __init__(self, lang, length):
		self.all_words = None
		self.words = None
		self.length = length
		self.char_frequency = {}
		self.correct_characters = {}
		self.already_used_characters = set()
		self.wrong_characters = set()
		self.alphabet = list(string.ascii_lowercase)

		for i in range(length):
			# qui stare attenti a copiare per valore
			self.correct_characters[i] = list(self.alphabet)

		self.load_words(lang, length)

		self.calculate_frequency()

	def choose_word(self, wordlist):
		return max(wordlist, key=self.word_point)

	def word_point(self, _word):
		return len(set(_word) - self.already_used_characters) + sum([self.char_frequency[c] for c in _word])

	def load_words(self, lang, length):
		f = open("dictionaries/" + lang + ".json")
		words = json.loads(f.readline().encode().decode("utf-8-sig"))
		f.close()

		self.words = [e for e in words if len(e) == int(length)]

		self.all_words = [e for e in words if len(e) == int(length)]

	def calculate_frequency(self):
		total_characters = len(self.words) * self.length

		for c in self.alphabet:
			self.char_frequency[c] = 0

		for word in self.words:
			for c in word:
				try:  # For special chars like italian à
					self.char_frequency[c] += 1
				except KeyError:
					self.alphabet += c
					self.char_frequency[c] = 1

		for c in self.alphabet:
			self.char_frequency[c] /= total_characters
			print(c, self.char_frequency[c])

	def load_info_from_result(self, result, word, must_be_characters):
		for key in result:
			int_key = int(key)
			if result[key] == "correct":
				self.correct_characters[int_key] = list(word[int_key])
			elif result[key] == "wrong position":
				must_be_characters.append(word[int_key])
				# if word[int_key] in correct_characters[int_key]:
				# print("---- Removed", word[int_key], "in wrong position", int_key)
				try:
					self.correct_characters[int_key].remove(word[int_key])
				except ValueError:
					print(word[int_key], "no longer in correct_characters pos", int_key, "containing", self.correct_characters[int_key])
			elif result[key] == "wrong":
				try:
					self.wrong_characters.add(word[int_key])
				except ValueError:
					print(word[int_key], "no longer in wrong_characters pos", int_key, "containing", self.wrong_characters[int_key])
				for j in range(self.length):
					if word[int_key] in self.correct_characters[j] and len(self.correct_characters[j]) != 1:
						# print("+++++ Removed", word[int_key], "from position", key, "ALL")
						self.correct_characters[j].remove(word[int_key])

		return must_be_characters

	def make_regex(self):
		str_regex = ""
		for key in self.correct_characters:
			str_regex += "[" + "".join(self.correct_characters[key]) + "]"

		print("New regex:", str_regex)

		regex = re.compile(str_regex)

		return regex

	def are_word_similar(self):
		similar = len(self.words) > 1
		for word in self.words:
			for word2 in self.words:
				if len(set(word) - set(word2)) > 1:
					similar = False
		return similar

	def choose_word_delete_similar(self):
		letters = set()
		for word in self.words:
			for word2 in self.words:
				if len(set(word) - set(word2)) == 1:
					letters |= set(word) - set(word2)

		return max(self.all_words, key=lambda _word: letters_in_word(_word, letters))
