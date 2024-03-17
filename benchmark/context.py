# read single.json file
from datetime import datetime
from google.ai.generativelanguage import Part, Content
import google.generativeai as genai
import json
import os
# Open the file in read mode
with open('single.json', 'r') as file:
    single = json.load(file)
context
# need to convert the "context" atttribute
print(single)
context = single["context"]
text = ""
# check if context has current_time attribute
# Iterate all the keys in the context
for key in context.keys():
    # If the key is "current_time"
    if key == "mapping":
        continue
    elif key == "current_time":
        text += f"Current time is {context[key]}.\n"
    elif key == "current_day":
        text += f"Today is {context[key]}.\n"
    elif key == "current_date":
        text += f"Today's date is {context[key]}.\n"
    elif key == "distances":
        with open('distance_matrix.json', 'r') as file:
            distance_matrix = json.load(file)
        for route in context[key]:
            text += f"From {context['mapping'][route['origin']]} to {context['mapping'][route['destination']]}: {distance_matrix[route['origin']][route['destination']]}.\n"
    elif key == "current_location":
        if context[key] == "home":
            with open(f"places/home.json", 'r') as file:
                place = json.load(file)
                # Then, replace the unique_name with place_id
        else:
            flag = False
            # First search in which type the place is. So, go through each folder in the places directory
            for folder in os.listdir("places"):
                # Check if folder is folder or not
                if not os.path.isdir(f"places/{folder}"):
                    continue
                elif f"{context[key]}.json" in os.listdir(f"places/{folder}"):
                    # Then, open the json file and get the place_id
                    with open(f"places/{folder}/{context[key]}.json", 'r') as file:
                        place = json.load(file)
                        # Then, replace the unique_name with place_id
                        text += f"I am currently at {place['name']}.\n"
                    flag = True
                    break
        text += f"I am currently at {context['mapping'][context[key]]}.\n"
    else:

        if key == "home":
            with open(f"places/home.json", 'r') as file:
                place = json.load(file)
        else:
            flag = False
            # First search in which type the place is. So, go through each folder in the places directory
            for folder in os.listdir("places"):
                # Check if folder is folder or not
                if not os.path.isdir(f"places/{folder}"):
                    continue
                elif f"{key}.json" in os.listdir(f"places/{folder}"):
                    # Then, open the json file and get the place_id
                    with open(f"places/{folder}/{key}.json", 'r') as file:
                        place = json.load(file)
                    flag = True
                    break
        # for each attribute in the context[key], add the attribute name and value to the text

        # print(context['mapping'], key)
        for attribute in context[key]:
            text += f"{attribute.replace('_', ' ').title()} of {context['mapping'][key]}: {json.dumps(place[attribute],indent=2)}\n"

# snake_case_string.replace("_", " ").title()

genai.configure(api_key='AIzaSyAqKc8aMNGyU-H2-e4R871CSpdUsxIovBU')

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}

model = genai.GenerativeModel(
    'gemini-pro', generation_config=generation_config, safety_settings=safety_settings)

total_questions = 0
correct_answers = 0

context = text
chat = model.start_chat(history=[
    Content(
                        parts=[
                            Part(
                                text=json.dumps(context)),
                            Part(
                                text="Remember this context. I will ask you questions about this. Your main priority should be the informations in the question. If you need extra information, you can use the context. For example If time or date is not mentioned in the question, you can use the current time and date. But if the time or date is mentioned in the question, you have to use the mentioned time and date. Question's priority is higher than the context."),
                        ],
                        role="user",
                        ),
    Content(
        parts=[
            Part(text="Okay. Got it. Ask any question."),
        ],
        role="model",
    ),
])

response = chat.send_message(single['question'])
print(text)
print("# Question: ", single["question"])
print("\n========= GEMINI PRO ==========")
print(response.text)
print("=================================\n")
# print(model.count_tokens(json.dumps(context)))
