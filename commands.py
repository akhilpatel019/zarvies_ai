import datetime
import pywhatkit
import wikipedia
import random
import urllib.parse
import re


# =====================================================
# HELPERS
# =====================================================

def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def google(query):
    return {
        "type": "url",
        "url": f"https://www.google.com/search?q={urllib.parse.quote(query)}",
        "reply": f"Searching Google for {query}"
    }


# =====================================================
# 🔥 FACTS (fast answers)
# =====================================================

FACTS = [
    ({"prime","minister","india"}, "Narendra Modi is the current Prime Minister of India."),
    ({"president","india"}, "Droupadi Murmu is the current President of India."),
    ({"capital","india"}, "The capital of India is New Delhi."),
]


def check_facts(words):
    for keys, ans in FACTS:
        if keys.issubset(words):
            return ans
    return None


# =====================================================
# 🔥 MATH
# =====================================================

def try_math(command):

    rep = {
        "plus":"+",
        "minus":"-",
        "times":"*",
        "multiply":"*",
        "multiply by":"*",
        "divide":"/",
        "divided by":"/"
    }

    for k,v in rep.items():
        command = command.replace(k,v)

    expr = re.sub(r'[^0-9+\-*/(). ]','',command)

    if not re.search(r'\d',expr):
        return None

    try:
        return f"The answer is {eval(expr)}"
    except:
        return None


# =====================================================
# 🔥 MOVIES / ENTERTAINMENT
# =====================================================

def handle_movies(words):

    if {"horror","movies"}.issubset(words):
        return "Try these horror movies: The Conjuring, Insidious, It, The Nun, Hereditary"

    if {"movies"} & words:
        return google("best movies list")


# =====================================================
# 🔥 EDUCATION
# =====================================================

def handle_education(words):

    if "aptitude" in words:
        return google("aptitude questions and answers pdf")

    if "interview" in words:
        return google("interview questions and answers")

    if "course" in words:
        return google("best online courses free")

    if "notes" in words or "pdf" in words:
        return google("study notes pdf")


# =====================================================
# 🔥 TECHNOLOGY
# =====================================================

def handle_tech(words):

    if "html" in words or "css" in words or "javascript" in words:
        return google("html css javascript tutorial examples")

    if "django" in words or "python" in words:
        return google("django python tutorial errors solutions")

    if "bootstrap" in words:
        return google("bootstrap components examples")

    if "github" in words:
        return google("github projects source code")


# =====================================================
# 🔥 BUSINESS / CAREER
# =====================================================

def handle_business(words):

    if "resume" in words:
        return google("resume template free download")

    if "job" in words:
        return google("latest job vacancies near me")

    if "startup" in words:
        return google("startup ideas for beginners")

    if "salary" in words:
        return google("average salary information")


# =====================================================
# 🔥 DESIGN / UI
# =====================================================

def handle_design(words):

    if "template" in words:
        return google("website templates free")

    if "color" in words or "palette" in words:
        return google("best color palette generator")

    if "icon" in words:
        return google("free svg icons")

    if "animation" in words:
        return google("css animation examples")


# =====================================================
# 🔥 SHOPPING
# =====================================================

def handle_shopping(words):

    if "price" in words or "buy" in words or "best" in words:
        return google("best price comparison shopping deals")


# =====================================================
# 🔥 DAILY LIFE
# =====================================================

def handle_daily(words):

    if "weather" in words:
        return google("today weather forecast")

    if "news" in words:
        return google("breaking news today")

    if "recipe" in words or "cook" in words:
        return google("easy recipes ideas")

    if "hotel" in words:
        return google("hotel booking near me")

    if "map" in words or "direction" in words:
        return google("google maps directions")

    if "plumber" in words or "electrician" in words:
        return google("local services near me")


# =====================================================
# 🔥 PROBLEM SOLVING
# =====================================================

def handle_problem(words):

    if "error" in words or "fix" in words or "not working" in " ".join(words):
        return google("how to fix error solution stackoverflow")


# =====================================================
# MAIN ENGINE
# =====================================================

def execute_command(command):

    words = tokenize(command)


    # 1 FACTS                                                           
    ans = check_facts(words)
    if ans: return ans


    # 2 MATH
    ans = try_math(command)
    if ans: return ans


    # 3 OPEN
    if "open" in words:
        site = command.replace("open","").strip()
        return {"type":"url","url":f"https://{site}.com","reply":f"Opening {site}"}


    # 4 PLAY
    if "play" in words:
        song = command.replace("play","").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube"


    # 5 ROUTED HANDLERS
    for handler in [
        handle_movies,
        handle_education,
        handle_tech,
        handle_business,
        handle_design,
        handle_shopping,
        handle_daily,
        handle_problem
    ]:
        ans = handler(words)
        if ans:
            return ans


    # 6 TIME
    if "time" in words:
        return datetime.datetime.now().strftime("The time is %I:%M %p")


    # 7 WIKI
    try:
        return wikipedia.summary(command,2)
    except:
        pass


    # 8 FINAL
    return google(command)
