# Configure Gemini API
import os
import google.generativeai as genai

KEY = "AIzaSyAPKSXFO-ULXo45ULDkXs5aoeT5Gb0eYAo"
genai.configure(api_key=KEY)

def remove_asterick(text):
    text = text.replace('*', '')
    return text


model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """You are a seasoned and well experienced Stroke Doctor for MedicPredic AI, you are the best in the world. 
            Here is always the record of the Patient, Have it in mind, when chating, Make diagnosis for the Patients andn render help
            if they want to reach out to out Medipredict Team, send "medipredictai@gmail.com"
            Attend to thier Needs. Your response from now on is with the Patient. Make it short"""
            
def chatbot_response(text_): # Generate content
    try:
        chat = model.start_chat()

        response = chat.send_message(f"Having This {prompt}, patient:{str(text_)}")
        print(text_)
        return response.text
    except Exception as e:
        print(e)
        return 'Medipredict AI is Down'

        

# print(chatbot_response("hi"))