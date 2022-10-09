import io
import subprocess

num = 1000

for i in range(num):
	result = subprocess.run(["python3", "client.py", "en", "5"], stdout=subprocess.PIPE)
	correct = False
	correct_word = None
	words = []
	available = []
	for line in result.stdout.decode("utf-8").split("\n"):
		if line.startswith("Correct word was:"):
			correct_word = line.split(" ")[3]
		if line.startswith("WE GUESSED"):
			correct = True
		if line.startswith("Word chosen:"):
			words.append(line.split(" ")[2])
		if "available words" in line:
			available.append(line.split(" ")[5])

	attempts = len(words)

	while len(words) < 6:
		words.append("")
		available.append("")
	with io.open("result.csv", "a") as f:
		f.write(",".join(words))
		f.write(",")
		f.write(",".join(available))
		f.write(",")
		f.write(str(attempts))
		f.write(",")
		if correct_word is not None:
			f.write(str(correct_word))
		f.write(",")
		f.write(str(correct))
		f.write("\n")

	if i % 50 == 0:
		print(i)
