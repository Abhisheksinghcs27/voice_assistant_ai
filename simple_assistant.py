import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import subprocess
import datetime
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from assistant_modules import ModuleManager

class SimpleVoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Assistant state
        self.is_listening = False
        self.assistant_name = "Alexa"
        
        # Initialize module manager
        self.module_manager = ModuleManager()
        
        # Create GUI
        self.create_gui()
    
    def create_gui(self):
        """Create the graphical user interface"""
        self.root = tk.Tk()
        self.root.title(f"{self.assistant_name} - Simple Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"{self.assistant_name} Voice Assistant", 
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
        • "Open [application]" - Open applications (calculator, notes, safari, etc.)
        • "What time is it?" - Get current time
        • "What's the date?" - Get current date
        • "Create a note" - Create a text note
        • "Weather in [city]" - Get weather information
        • "Calculate [expression]" - Basic calculator
        • "Play music" - Play music
        • "Set reminder" - Set a reminder
        • "Send email" - Compose email
        • "Open wifi settings" - System settings
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
        """Process user commands using module manager"""
        if not command:
            return
        
        try:
            # Use module manager to process the command
            response = self.module_manager.process_command(command)
            self.speak(response)
                
        except Exception as e:
            self.speak(f"Sorry, I encountered an error: {str(e)}")
    
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
    
    def run(self):
        """Start the voice assistant"""
        self.speak(f"Hello! I'm {self.assistant_name}, your voice assistant. How can I help you today?")
        self.root.mainloop()

if __name__ == "__main__":
    assistant = SimpleVoiceAssistant()
    assistant.run()

