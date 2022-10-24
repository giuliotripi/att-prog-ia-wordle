import sys
from base import *

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print("Usage:", sys.argv[0], "lang length")
	sys.exit(1)


lang = sys.argv[1]
length = int(sys.argv[2])

utils = WordleUtils(lang, length)

must_be_characters = []

for i in range(1, 7):

	while True:
	
		print("Guess", i, ", available words:", len(utils.words))

		if len(utils.words) < 20 and utils.are_word_similar() and i < 6:
			print(utils.words)
			word = utils.choose_word_delete_similar()
		else:
			word = utils.choose_word(utils.words)

		print("Word chosen:", word, "with points:", utils.word_point(word))

		utils.already_used_characters |= set(word)

		result = {"result": {}}
		
		guessed = input("Guessed [y/n/w]?").lower()
		
		if guessed in ["y", "n"]:
			break
		elif guessed == "w":
			utils.words.remove(word)
	
	result["guessed"] = guessed == "y"
	
	if result["guessed"]:
		print("Correct word was:", word)
		print("WE GUESSED IN", i, "ATTEMPTS!")
		sys.exit(0)

	for pos in range(0, length):
		if len(utils.correct_characters[pos]) == 1 and utils.correct_characters[pos][0] == word[pos]:
			result["result"][pos] = "correct"
		else:
			outcome = input("Character '{}' is correct [Yes/No/Wrong position]?".format(word[pos])).lower()
			result["result"][pos] = "correct" if outcome == "y" else ("wrong" if outcome == "n" else "wrong position")

	must_be_characters = utils.load_info_from_result(result["result"], word, must_be_characters)

	regex = utils.make_regex()

	print("Must be:", must_be_characters)

	utils.words = [e for e in utils.words if regex.match(e) and (i <= 2 or chars_in_str(must_be_characters, e))]


sys.exit(100)
