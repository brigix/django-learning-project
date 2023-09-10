from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
import requests
import json
from django.http import JsonResponse
import os
import openai

monthly_challenges = {
    "january": "Eat no meat",
    "february": "Love is in the air",
    "march": "Exercise for at least 20 min every day",
    "may": None
}

# Create your views here.


def index(request):
    list_items = ""
    months = list(monthly_challenges.keys())

    return render(request, "challenges/index.html", {
        "months": months
    })
    # for month in months:
    #     capitalized_month = month.capitalize()
    #     month_path = reverse("month_challenge", args=[month])
    #     list_items += f'<li><a href="{month_path}">{capitalized_month}</a></li>'
    # response_data = f"<ul>{list_items}</ul>"
    # return HttpResponse(response_data)


def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())
    try:
        redirect_month = months[month - 1]
        redirect_path = reverse("month_challenge", args=[redirect_month])
        return HttpResponseRedirect(redirect_path)
    except:
        return HttpResponseNotFound("Month not found")


def monthly_challenge(request, month):
    try:
        challenge_text = monthly_challenges[month]
        return render(request, "challenges/challenge.html", {
            "text": challenge_text,
            "month":  month,
        })
        #response_data = render_to_string("challenges/challenge.html")
        #return HttpResponse(response_data)
    except:
        raise Http404()

openai.api_key = ""

# List of all 36 Lenormand cards
lenormand_cards = [
        "Rider", "Clover", "Ship", "House", "Tree", "Clouds",
        "Snake", "Coffin", "Bouquet", "Scythe", "Whip", "Birds",
        "Child", "Fox", "Bear", "Stars", "Stork", "Dog",
        "Tower", "Garden", "Mountain", "Crossroad", "Mice", "Heart",
        "Ring", "Book", "Letter", "Man", "Woman", "Lily",
        "Sun", "Moon", "Key", "Fish", "Anchor", "Cross"
]
def save_lenormand_keywords(request):
    meanings = {}
    # Iterate over each card and context
    for card in lenormand_cards:
        meanings[card] = {}
        prompt = f"Give 4 key nouns, 4 key adjectives and 4 key verbs for Lenormand card {card} meaning, Convert traditional Lenormand meanings to suit modern world everyday life"
         # Make a POST request to the ChatGPT API
        response = openai.Completion.create(
                   model="text-davinci-003",
                   prompt=prompt,
                   temperature=0.3,
                   max_tokens=200,
                   top_p=1.0,
                   frequency_penalty=0.0,
                   presence_penalty=0.0,
                 )

        # Extract the generated meaning from the API response
        generated_meaning = response["choices"][0]["text"].strip()
        print(f"generated_meaning: {card}")
        # Store the meaning for the card and context
        meanings[card]['keyword'] = generated_meaning

    # Save the meanings to a JSON file
    with open("lenormand_keywords_nouns_verbs_adj.json", "w") as file:
        json.dump(meanings, file, indent=4)

    return JsonResponse({"status": "success"})

def save_lenormand_card_meanings(request):

    # List of contexts for each card
    contexts = ["general", "keywords", "nouns", "verbs", "adjectives", "health", "career", "love", "self development", "spiritual meaning"]

    meanings = {}
    # Iterate over each card and context
    for card in lenormand_cards:
        meanings[card] = {}
        for context in contexts:
            if context == "verbs" or context == "nouns" or context == "keywords" or context == "adjectives":
                prompt = f"Generate list of {context} for Lenormand card {card}"
            else:
                prompt = f"What is the meaning of Lenormand card {card} in the context of {context} ?"
            # Make a POST request to the ChatGPT API
            response = openai.Completion.create(
                   model="text-davinci-003",
                   prompt=prompt,
                   temperature=0.3,
                   max_tokens=200,
                   top_p=1.0,
                   frequency_penalty=0.0,
                   presence_penalty=0.0,
                 )

            # Extract the generated meaning from the API response
            generated_meaning = response["choices"][0]["text"].strip()
            print(f"generated_meaning: {card}, {context}")
            # Store the meaning for the card and context
            meanings[card][context] = generated_meaning

    # Save the meanings to a JSON file
    with open("lenormand_meanings.json", "w") as file:
        json.dump(meanings, file, indent=4)

    return JsonResponse({"status": "success"})

def save_lenormand_combinations(request):
    combinations = {}
    # Iterate over each card and context
    for card1 in lenormand_cards:
        combinations[card1] = {}
        for card2 in lenormand_cards:
            if card2 != card1:
                prompt = f"What is the meaning of Lenormand cards {card1} and {card2} combination?"
                response = openai.Completion.create(
                   model="text-davinci-003",
                   prompt=prompt,
                   temperature=0.3,
                   max_tokens=200,
                   top_p=1.0,
                   frequency_penalty=0.0,
                   presence_penalty=0.0,
                 )

                # Extract the generated meaning from the API response
                generated_meaning = response["choices"][0]["text"].strip()
                print(f"combination: {card1}, {card2}")
                # Store the meaning for the card and context
                combinations[card1][card2] = generated_meaning

    # Save the meanings to a JSON file
    with open("lenormand_combinations.json", "w") as file:
        json.dump(combinations, file, indent=4)

    return JsonResponse({"status": "success"})
