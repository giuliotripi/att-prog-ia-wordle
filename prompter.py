import requests
import sys
import json
import string
import re
import random

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print("Usage:", sys.argv[0], "lang length")
	sys.exit(1)


alphabet = list(string.ascii_lowercase)

lang = sys.argv[1]
length = int(sys.argv[2])

correct_characters = {}
already_used_characters = set()


def chars_in_str(chars, string):
	for char in chars:
		if char not in string:
			return False

	return True


def choose_word(wordlist):
	return max(wordlist, key=word_point)


def word_point(_word):
	return len(set(_word) - already_used_characters) + sum([char_frequency[c] for c in _word])


for i in range(length):
	# qui stare attenti a copiare per valore
	correct_characters[i] = list(alphabet)

f = open("dictionaries/" + lang + ".json")
words = json.loads(f.readline().encode().decode("utf-8-sig"))
f.close()

words = [e for e in words if len(e) == int(length)]

all_words = [e for e in words if len(e) == int(length)]


total_characters = len(words) * length

char_frequency = {}

for c in alphabet:
	char_frequency[c] = 0

for word in words:
	for c in word:
		try:  # For special chars like italian à
			char_frequency[c] += 1
		except KeyError:
			alphabet += c
			char_frequency[c] = 1

for c in alphabet:
	char_frequency[c] /= total_characters
	print(c, char_frequency[c])

must_be_characters = []

for i in range(1, 7):

	while True:
	
		print("Guess", i, ", available words:", len(words))

		word = choose_word(words)

		print("Word chosen:", word, "with points:", word_point(word))

		already_used_characters |= set(word)

		result = {"result": {}}
		
		guessed = input("Guessed [y/n/w]?").lower()
		
		if guessed in ["y", "n"]:
			break
		elif guessed == "w":
			words.remove(word)
	
	result["guessed"] = guessed == "y"
	
	if result["guessed"]:
		print("Correct word was:", word)
		print("WE GUESSED IN", i, "ATTEMPTS!")
		sys.exit(0)
		
	
	for pos in range(0, length):
		if len(correct_characters[pos]) == 1:
			result["result"][pos] = "correct"
		else:
			outcome = input("Character '{}' is correct [Yes/No/Wrong position]?".format(word[pos])).lower()
			result["result"][pos] = "correct" if outcome == "y" else ("wrong" if outcome == "n" else "wrong position")


	for key in result["result"]:
		int_key = int(key)
		if result["result"][key] == "correct":
			correct_characters[int_key] = list(word[int_key])
		elif result["result"][key] == "wrong position":
			must_be_characters.append(word[int_key])
			# if word[int_key] in correct_characters[int_key]:
			# print("---- Removed", word[int_key], "in wrong position", int_key)
			correct_characters[int_key].remove(word[int_key])
		elif result["result"][key] == "wrong":
			for j in range(length):
				if word[int_key] in correct_characters[j] and len(correct_characters[j]) != 1:
					# print("+++++ Removed", word[int_key], "from position", key, "ALL")
					correct_characters[j].remove(word[int_key])

	str_regex = ""
	for key in correct_characters:
		str_regex += "[" + "".join(correct_characters[key]) + "]"

	print("New regex:", str_regex)
	print("Must be:", must_be_characters)

	regex = re.compile(str_regex)

	words = [e for e in words if regex.match(e) and (i <= 2 or chars_in_str(must_be_characters, e))]


sys.exit(100)
