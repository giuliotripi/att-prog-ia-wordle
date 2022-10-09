from aiohttp import web
import secrets
import json
import random

routes = web.RouteTableDef()

users = {}

languages = ["it", "en"]

words = {}

for lang in languages:
    print("Loading language:", lang)
    f = open("dictionaries/" + lang + ".json")
    words[lang] = json.loads(f.readline().encode().decode("utf-8-sig"))
    f.close()


@routes.get('/start')
async def start(request):
    global users
    token = secrets.token_urlsafe(10)
    lang = request.query["lang"]
    len = request.query["len"]
    if "word" in request.query:
        word = request.query["word"]
    else:
        word = get_random_word(len, lang)
    print("Chosen word:", word)
    users[token] = {"word": word, "guess": 0}
    return web.json_response({"ok": True, "token": token})


@routes.get('/guess')
async def guess(request):
    token = request.query["token"]
    word = request.query["word"]
    original_word = users[token]["word"]
    original_word_array = list(users[token]["word"])
    if len(word) != len(original_word):
        return web.json_response({"error": "Length diff"}, status=400)

    details = {}

    correct = 0
    for i in range(len(original_word)):
        detail = "wrong"
        if word[i] == original_word[i]:
            detail = "correct"
            correct += 1
            original_word_array[i] = "*"
        details[i] = detail

    for i in range(len(original_word)):
        if details[i] != "correct" and word[i] in original_word_array:
            details[i] = "wrong position"

    users[token]["guess"] += 1

    guessed = correct == len(original_word)

    guess = users[token]["guess"]

    if guessed:
        del users[token]

    return web.json_response({"result": details, "guess": guess, "guessed": guessed})


def get_random_word(length, language):
    word_list = get_words(length, language)
    # print("Found", len(word_list), "words")
    return random.choice(word_list)


def get_words(length, language):
    return [e for e in words[language] if len(e) == int(length)]


app = web.Application()
app.add_routes(routes)
web.run_app(app)
