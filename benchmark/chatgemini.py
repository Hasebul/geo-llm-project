import google.generativeai as genai
from google.ai.generativelanguage import Part, Content
import json
from datetime import datetime
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

with open('benchmark.json') as f:
    data = json.load(f)
    for i in range(len(data)):
        context = data[i]['context']
        context['timestamp'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        chat = model.start_chat(history=[
            Content(
                parts=[
                    Part(
                        text=json.dumps(context)),
                    Part(
                        text="Remember this context. I will ask you MCQ questions about this. You just need to answer numerically (e.g., 1/2/...). No explanation needed."),
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

        for j in range(len(data[i]['questions'])):
            total_questions += 1
            question = data[i]['questions'][j]['statement']
            prompt = question + "\n"
            for k in range(len(data[i]['questions'][j]['options'])):
                prompt = prompt + "Option" + \
                    str(k+1) + ": " + \
                    data[i]['questions'][j]['options'][k] + ", "

            response = chat.send_message(prompt)

            if data[i]['questions'][j]['answer'] == int(response.text):
                correct_answers += 1

            # print("> " + prompt)
            # print(data[i]['questions'][j]['answer'], response.text)
accuracy = correct_answers * 100 / total_questions

# print 2 digit after decimal point
accuracy = "{:.2f}".format(accuracy)
print(f"Accuracy: {accuracy}%")
