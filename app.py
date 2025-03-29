import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os

# Configure the Gemini API
genai.configure(api_key="AIzaSyCAN2xDwxrgwItp6bxnUIkfmwAeazBqWGI")

class VoiceAssistant:
    def __init__(self): 
        # Fixed constructor method
        # initialize the voice assistant:
        # Set up speech recognition.
        # Configure text-to-speech engine.
        # Set up the AI model and the Vision API client.

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.configure_voice()
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def configure_voice(self):
        #Configure the voice settings:
        #Adjust the speaking rate of the assistant.
        # Select a specific voice if multiple voices are available.
        #"""

        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)

    def speak(self, text):
        #Convert text into speech:
        #Uses the text-to-speech engine to speak the provided text.
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        #Listen to the user's voice input:
        #Uses the microphone to capture audio input.
        #Processes the audio and converts it into text using Google's Speech
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.energy_threshold = 8000  # Adjusted for noisy environments
            
            try:
                audio = self.recognizer.listen(source, timeout=20)
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
                return ""
            except sr.RequestError as e:
                print(f"Request error from Google Speech Recognition: {e}")
                return ""
            except Exception as e:
                print(f"Unexpected error: {e}")
                return ""

    def get_ai_response(self, prompt):
         #Get a response from the generative AI model:
         #Send a prompt to the AI model and return its response.
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def run(self):
        self.speak("Hello saptadeep! I'm your voice assistant")
        
        while True:
            user_input = self.listen()
            if not user_input:
                continue
                
            if "I want to exit now" in user_input.lower():
                self.speak("Goodbye!")
                break
                
            response = self.get_ai_response(user_input)
            print(f"AI: {response}")
            self.speak(response)

if __name__ == "__main__":  # Fixed the main block
    assistant = VoiceAssistant()
    assistant.run()