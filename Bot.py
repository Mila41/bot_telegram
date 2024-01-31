import re  # Regular Expressions
import nltk  # Natural Language Toolkit (расстояние левенштейна)
import random
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

def filter_text(text):
    text = text.lower()  # lower - к ниженму регистру
    text = text.strip()  # strip - вырезать пробелы с начала и конца строки
    pattern = r"[^\w\s]"  # Всё что не слово и не пробел
    text = re.sub(pattern, "", text)  # Из переменной text вырезаем "Всё что не слово и не пробел"
    text = re.sub(r"\s+", " ", text)  # Из переменной text вырезаем ВСЕ пробелы
    return text


# True, если тексты похожи (user_text пользовательский тект, example - контрольная фраза)
# False, если не похожи
def text_match(user_text, example):
    user_text = filter_text(user_text)  # Отфильтруем лишнее из первой строки
    example = filter_text(example)  # Отфильтруем лишнее из второй строки
    if user_text == example:  # Если тексты точно совпадают
        return True
    if user_text.find(example) != -1:  # Если фраза входит в пользовательский текст
        return True

    distance = nltk.edit_distance(user_text, example)
# Отношение количества ошибок к длине слова, 1.0 - слово целиком другое, 0 - слова полностью совпадают
    ratio = distance / len(example)
    if ratio < 0.40:
        return True
    return False

# Определение "намерения" пользователя
INTENTS = {
    "hello": {
        "examples": ["Привет", "Здравствуйте", "Добрый день"],
        "responses": ["Йоу", "Здарова", "Приветствую тебя, человек."],
    },
    "bye": {
        "examples": ["Пока", "До свидания", "Всего хорошего"],
        "responses": ["Давайдосвиданья", "И вам приятного денечка"],
    },
    "how_are_you": {
        "examples": ["Как дела"],
        "responses": ["Функционирую нормально"],
    },
    "buy_some_foods": {
        "examples": ["Голоден", "Хочу есть", "Продукты"],
        "responses": ["А вот фиг тебе"],
    },
}
def get_intent(user_text):
    for intent in INTENTS:
        examples = INTENTS[intent]["examples"]
        for example in examples:
            if text_match(user_text, example):
                return intent
    return None
def get_random_response(intent):
    return random.choice(INTENTS[intent]["responses"])
f = open('big_bot_config.json', 'r')
data = json.load(f)
INTENTS = data["intents"]
print("Интентов загружено из файла:", len(INTENTS))

x = []
y = []
for intent in INTENTS:
    examples = INTENTS[intent]["examples"]
    for example in examples:
        example = filter_text(example)
        if len(example) < 3:
            continue
        x.append(example)
        y.append(intent)
vectorizer = CountVectorizer()
vectorizer.fit(x)
vecX = vectorizer.transform(x)
model = RandomForestClassifier()
model.fit(vecX, y)
y_pred = model.predict(vecX)
print("accurasy_score", accuracy_score(y, y_pred))
print("f1_score", f1_score(y, y_pred, average="macro"))
def get_intent_ml(user_text):
    user_text = filter_text(user_text)
    vec_text = vectorizer.transform([user_text])
    intent = model.predict(vec_text)[0]
    return intent
proba = model.predict_proba(vectorizer.transform(["Приветики"]))
pd.DataFrame(columns=model.classes_, data=[proba[0]]).T.sort_values(by=0, ascending=False)
def bot(user_text):
    intent = get_intent(user_text)
    if intent:
        return get_random_response(intent)
    intent = get_intent_ml(user_text)
    return get_random_response(intent)
nest_asyncio.apply()
TOKEN=""  # Вставить свой токен
app = ApplicationBuilder().token(TOKEN).build()
async def telegram_reply(upd: Update, ctx):
    name = upd.message.from_user.full_name
    user_text = upd.message.text
    print(f"{name}: {user_text}")
    reply = bot(user_text)
    print(f"BOT: {reply}")
    await upd.message.reply_text(reply)
handler = MessageHandler(filters.TEXT, telegram_reply)
app.add_handler(handler)
app.run_polling()