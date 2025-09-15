import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import webbrowser
import subprocess
import datetime
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Set OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        self.openai_client = OpenAI(api_key=api_key) if api_key else None
        
        # Assistant state
        self.is_listening = False
        self.assistant_name = "Alexa"
        
        # Create GUI
        self.create_gui()
        
        # Task handlers
        self.task_handlers = {
            'web_search': self.web_search,
            'open_application': self.open_application,
            'get_time': self.get_time,
            'get_date': self.get_date,
            'create_note': self.create_note,
            'send_email': self.send_email,
            'weather': self.get_weather,
            'calculator': self.calculator,
            'music': self.play_music,
            'reminder': self.set_reminder
        }
    
    def create_gui(self):
        """Create the graphical user interface"""
        self.root = tk.Tk()
        self.root.title(f"{self.assistant_name} - AI Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"{self.assistant_name} AI Assistant", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Status: Ready", 
                                     font=('Arial', 12))
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.listen_button = ttk.Button(button_frame, text="🎤 Start Listening", 
                                       command=self.toggle_listening)
        self.listen_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.stop_listening, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Text input frame
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(text_frame, text="Or type your command:").pack(anchor=tk.W)
        
        self.text_input = ttk.Entry(text_frame, font=('Arial', 12))
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.bind('<Return>', self.process_text_command)
        
        # Send button
        send_button = ttk.Button(text_frame, text="Send", 
                                command=self.process_text_command)
        send_button.pack(pady=5)
        
        # Output area
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(output_frame, text="Conversation:").pack(anchor=tk.W)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, 
                                                   font=('Arial', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Help text
        help_text = """
        Available Commands:
        • "Search for [topic]" - Web search
        • "Open [application]" - Open applications
        • "What time is it?" - Get current time
        • "What's the date?" - Get current date
        • "Create a note" - Create a text note
        • "Weather in [city]" - Get weather information
        • "Calculate [expression]" - Basic calculator
        • "Play music" - Play music
        • "Set reminder" - Set a reminder
        • "Send email" - Compose email
        """
        
        help_label = ttk.Label(main_frame, text=help_text, 
                              font=('Arial', 9), foreground='gray')
        help_label.pack(pady=10)
    
    def speak(self, text):
        """Convert text to speech"""
        self.output_text.insert(tk.END, f"Assistant: {text}\n")
        self.output_text.see(tk.END)
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.output_text.insert(tk.END, "Listening...\n")
                self.output_text.see(tk.END)
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.output_text.insert(tk.END, "Processing...\n")
                self.output_text.see(tk.END)
                
                text = self.recognizer.recognize_google(audio)
                self.output_text.insert(tk.END, f"You: {text}\n")
                self.output_text.see(tk.END)
                
                return text.lower()
                
        except sr.WaitTimeoutError:
            self.output_text.insert(tk.END, "No speech detected. Please try again.\n")
            self.output_text.see(tk.END)
            return None
        except sr.UnknownValueError:
            self.output_text.insert(tk.END, "Could not understand audio. Please try again.\n")
            self.output_text.see(tk.END)
            return None
        except sr.RequestError as e:
            self.output_text.insert(tk.END, f"Error with speech recognition: {e}\n")
            self.output_text.see(tk.END)
            return None
    
    def process_command(self, command):
        """Process user commands using AI"""
        if not command:
            return
        
        try:
            if not self.openai_client:
                self.speak("OpenAI API key not set. Please add OPENAI_API_KEY to your environment.")
                return
            # Use OpenAI to understand and categorize the command
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Analyze the user's command and respond with a JSON object containing: 'action' (the type of action), 'parameters' (relevant parameters), and 'response' (a natural response to the user). Available actions: web_search, open_application, get_time, get_date, create_note, send_email, weather, calculator, music, reminder, general_chat."},
                    {"role": "user", "content": command}
                ],
                max_tokens=150
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            try:
                parsed = json.loads(ai_response)
                action = parsed.get('action', 'general_chat')
                parameters = parsed.get('parameters', {})
                ai_message = parsed.get('response', 'I understand your request.')
                
                # Execute the action
                if action in self.task_handlers:
                    result = self.task_handlers[action](parameters)
                    self.speak(f"{ai_message} {result}")
                else:
                    self.speak(ai_message)
                    
            except json.JSONDecodeError:
                self.speak("I understand your request. Let me help you with that.")
                
        except Exception as e:
            error_text = str(e)
            if "insufficient_quota" in error_text or "Error code: 429" in error_text or "You exceeded your current quota" in error_text:
                # Fallback to local intent parsing so the assistant still works
                parsed = self.parse_command_locally(command)
                action = parsed.get('action', 'general_chat')
                parameters = parsed.get('parameters', {})
                ai_message = parsed.get('response', 'I understand your request.')
                if action in self.task_handlers:
                    result = self.task_handlers[action](parameters)
                    self.speak(f"{ai_message} {result}")
                else:
                    self.speak(ai_message)
                self.output_text.insert(tk.END, "\n(Note: Using local understanding due to API quota limits.)\n")
                self.output_text.see(tk.END)
            else:
                self.speak(f"Sorry, I encountered an error: {error_text}")

    def parse_command_locally(self, command):
        """Very simple keyword-based intent parsing as a fallback when API is unavailable."""
        text = command.lower()
        # web search
        if text.startswith("search for ") or text.startswith("search "):
            query = text.replace("search for ", "").replace("search ", "").strip()
            return {"action": "web_search", "parameters": {"query": query}, "response": f"Searching the web for {query}."}
        # open application
        if text.startswith("open "):
            app = text.replace("open ", "").strip()
            return {"action": "open_application", "parameters": {"application": app}, "response": f"Opening {app}."}
        # time/date
        if "time" in text:
            return {"action": "get_time", "parameters": {}, "response": "Here is the current time."}
        if "date" in text or "today" in text:
            return {"action": "get_date", "parameters": {}, "response": "Here is today’s date."}
        # notes
        if text.startswith("create a note") or text.startswith("note "):
            content = text.split("note", 1)[-1].strip()
            return {"action": "create_note", "parameters": {"content": content}, "response": "Creating a note."}
        # weather
        if text.startswith("weather in "):
            city = text.replace("weather in ", "").strip()
            return {"action": "weather", "parameters": {"city": city}, "response": f"Checking weather for {city}."}
        # calculator
        if text.startswith("calculate "):
            expr = text.replace("calculate ", "").strip()
            return {"action": "calculator", "parameters": {"expression": expr}, "response": "Calculating."}
        # music
        if "play music" in text or text.startswith("play "):
            return {"action": "music", "parameters": {}, "response": "Playing music."}
        # reminder
        if text.startswith("remind me") or text.startswith("set reminder"):
            return {"action": "reminder", "parameters": {"text": command}, "response": "Setting a reminder."}
        # email
        if "send email" in text or text.startswith("email"):
            return {"action": "send_email", "parameters": {}, "response": "Opening your email client."}
        # default
        return {"action": "general_chat", "parameters": {}, "response": "I understand your request."}
    
    def toggle_listening(self):
        """Toggle voice listening on/off"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="🎤 Stop Listening")
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Listening...")
            
            # Start listening in a separate thread
            self.listen_thread = threading.Thread(target=self.continuous_listen)
            self.listen_thread.daemon = True
            self.listen_thread.start()
        else:
            self.stop_listening()
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.listen_button.config(text="🎤 Start Listening")
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Ready")
    
    def continuous_listen(self):
        """Continuously listen for voice commands"""
        while self.is_listening:
            command = self.listen()
            if command:
                self.process_command(command)
    
    def process_text_command(self, event=None):
        """Process text-based commands"""
        command = self.text_input.get().strip()
        if command:
            self.text_input.delete(0, tk.END)
            self.output_text.insert(tk.END, f"You: {command}\n")
            self.output_text.see(tk.END)
            self.process_command(command)
    
    # Task handlers
    def web_search(self, parameters):
        """Perform web search"""
        query = parameters.get('query', '')
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"I've searched for '{query}' on the web."
        return "What would you like me to search for?"
    
    def open_application(self, parameters):
        """Open applications"""
        app_name = parameters.get('application', '').lower()
        apps = {
            'calculator': 'Calculator',
            'notes': 'Notes',
            'safari': 'Safari',
            'chrome': 'Google Chrome',
            'spotify': 'Spotify',
            'mail': 'Mail'
        }
        
        if app_name in apps:
            try:
                subprocess.run(['open', '-a', apps[app_name]])
                return f"I've opened {apps[app_name]} for you."
            except:
                return f"Sorry, I couldn't open {apps[app_name]}."
        return "What application would you like me to open?"
    
    def get_time(self, parameters):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    def get_date(self, parameters):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}."
    
    def create_note(self, parameters):
        """Create a text note"""
        content = parameters.get('content', '')
        if content:
            filename = f"note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(content)
            return f"I've created a note with your content: {content}"
        return "What would you like me to write in the note?"
    
    def send_email(self, parameters):
        """Open email client"""
        webbrowser.open('mailto:')
        return "I've opened your email client."
    
    def get_weather(self, parameters):
        """Get weather information"""
        city = parameters.get('city', '')
        if city:
            url = f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}"
            webbrowser.open(url)
            return f"I've opened weather information for {city}."
        return "Which city's weather would you like to check?"
    
    def calculator(self, parameters):
        """Basic calculator"""
        expression = parameters.get('expression', '')
        if expression:
            try:
                result = eval(expression)
                return f"The result is {result}."
            except:
                return "I couldn't calculate that expression."
        return "What would you like me to calculate?"
    
    def play_music(self, parameters):
        """Play music"""
        webbrowser.open('https://open.spotify.com')
        return "I've opened Spotify for you."
    
    def set_reminder(self, parameters):
        """Set a reminder"""
        reminder_text = parameters.get('text', '')
        if reminder_text:
            # In a real implementation, you'd integrate with a calendar/reminder app
            return f"I've set a reminder for: {reminder_text}"
        return "What would you like me to remind you about?"
    
    def run(self):
        """Start the voice assistant"""
        self.speak(f"Hello! I'm {self.assistant_name}, your AI voice assistant. How can I help you today?")
        self.root.mainloop()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

