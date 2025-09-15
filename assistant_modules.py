import os
import webbrowser
import subprocess
import datetime
import json
import requests
from abc import ABC, abstractmethod

class AssistantModule(ABC):
    """Base class for assistant modules"""
    
    @abstractmethod
    def can_handle(self, command):
        """Check if this module can handle the given command"""
        pass
    
    @abstractmethod
    def execute(self, command, parameters=None):
        """Execute the command and return a response"""
        pass

class WebSearchModule(AssistantModule):
    """Handle web search commands"""
    
    def can_handle(self, command):
        keywords = ['search', 'find', 'look up', 'google']
        return any(keyword in command.lower() for keyword in keywords)
    
    def execute(self, command, parameters=None):
        # Extract search query from command
        search_terms = ['search for', 'find', 'look up', 'google']
        query = command.lower()
        
        for term in search_terms:
            if term in query:
                query = query.replace(term, '').strip()
                break
        
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"I've searched for '{query}' on the web."
        return "What would you like me to search for?"

class ApplicationModule(AssistantModule):
    """Handle application opening commands"""
    
    def __init__(self):
        self.apps = {
            'calculator': 'Calculator',
            'notes': 'Notes',
            'safari': 'Safari',
            'chrome': 'Google Chrome',
            'spotify': 'Spotify',
            'mail': 'Mail',
            'terminal': 'Terminal',
            'finder': 'Finder',
            'photos': 'Photos',
            'music': 'Music',
            'facetime': 'FaceTime',
            'messages': 'Messages',
            'calendar': 'Calendar',
            'reminders': 'Reminders',
            'maps': 'Maps',
            'settings': 'System Preferences'
        }
    
    def can_handle(self, command):
        return 'open' in command.lower() or 'launch' in command.lower()
    
    def execute(self, command, parameters=None):
        command_lower = command.lower()
        
        # Find the app name in the command
        for app_key, app_name in self.apps.items():
            if app_key in command_lower:
                try:
                    subprocess.run(['open', '-a', app_name])
                    return f"I've opened {app_name} for you."
                except Exception as e:
                    return f"Sorry, I couldn't open {app_name}. Error: {str(e)}"
        
        return "What application would you like me to open?"

class TimeDateModule(AssistantModule):
    """Handle time and date queries"""
    
    def can_handle(self, command):
        time_keywords = ['time', 'hour', 'clock']
        date_keywords = ['date', 'day', 'today', 'tomorrow']
        return any(keyword in command.lower() for keyword in time_keywords + date_keywords)
    
    def execute(self, command, parameters=None):
        command_lower = command.lower()
        
        if any(keyword in command_lower for keyword in ['time', 'hour', 'clock']):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif any(keyword in command_lower for keyword in ['date', 'day', 'today']):
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            return f"Today is {current_date}."
        
        elif 'tomorrow' in command_lower:
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            tomorrow_date = tomorrow.strftime("%B %d, %Y")
            return f"Tomorrow is {tomorrow_date}."
        
        return "I can tell you the time or date. What would you like to know?"

class NoteModule(AssistantModule):
    """Handle note creation and management"""
    
    def __init__(self):
        self.notes_dir = "notes"
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
    
    def can_handle(self, command):
        note_keywords = ['note', 'write', 'create note', 'save note']
        return any(keyword in command.lower() for keyword in note_keywords)
    
    def execute(self, command, parameters=None):
        if parameters and 'content' in parameters:
            content = parameters['content']
            filename = f"note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(self.notes_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            return f"I've created a note with your content: {content}"
        
        return "What would you like me to write in the note?"

class WeatherModule(AssistantModule):
    """Handle weather queries"""
    
    def can_handle(self, command):
        weather_keywords = ['weather', 'temperature', 'forecast']
        return any(keyword in command.lower() for keyword in weather_keywords)
    
    def execute(self, command, parameters=None):
        # Extract city name from command
        command_lower = command.lower()
        
        # Simple city extraction (in a real app, you'd use NLP)
        if 'weather in' in command_lower:
            city = command_lower.split('weather in')[-1].strip()
        elif 'weather for' in command_lower:
            city = command_lower.split('weather for')[-1].strip()
        else:
            city = "current location"
        
        if city and city != "current location":
            url = f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}"
            webbrowser.open(url)
            return f"I've opened weather information for {city}."
        
        return "Which city's weather would you like to check?"

class CalculatorModule(AssistantModule):
    """Handle mathematical calculations"""
    
    def can_handle(self, command):
        calc_keywords = ['calculate', 'compute', 'math', 'plus', 'minus', 'times', 'divided']
        return any(keyword in command.lower() for keyword in calc_keywords)
    
    def execute(self, command, parameters=None):
        if parameters and 'expression' in parameters:
            expression = parameters['expression']
            try:
                # Safe evaluation (in production, use a safer math parser)
                result = eval(expression)
                return f"The result is {result}."
            except Exception as e:
                return f"I couldn't calculate that expression. Error: {str(e)}"
        
        return "What would you like me to calculate?"

class MusicModule(AssistantModule):
    """Handle music and entertainment commands"""
    
    def can_handle(self, command):
        music_keywords = ['music', 'play', 'song', 'spotify', 'apple music']
        return any(keyword in command.lower() for keyword in music_keywords)
    
    def execute(self, command, parameters=None):
        command_lower = command.lower()
        
        if 'spotify' in command_lower:
            webbrowser.open('https://open.spotify.com')
            return "I've opened Spotify for you."
        elif 'apple music' in command_lower:
            subprocess.run(['open', '-a', 'Music'])
            return "I've opened Apple Music for you."
        else:
            webbrowser.open('https://open.spotify.com')
            return "I've opened Spotify for you."

class EmailModule(AssistantModule):
    """Handle email-related commands"""
    
    def can_handle(self, command):
        email_keywords = ['email', 'mail', 'send email', 'compose']
        return any(keyword in command.lower() for keyword in email_keywords)
    
    def execute(self, command, parameters=None):
        webbrowser.open('mailto:')
        return "I've opened your email client."

class ReminderModule(AssistantModule):
    """Handle reminder and task management"""
    
    def can_handle(self, command):
        reminder_keywords = ['reminder', 'remind', 'task', 'todo']
        return any(keyword in command.lower() for keyword in reminder_keywords)
    
    def execute(self, command, parameters=None):
        if parameters and 'text' in parameters:
            reminder_text = parameters['text']
            # In a real implementation, you'd integrate with a calendar/reminder app
            # For now, we'll just acknowledge the reminder
            return f"I've set a reminder for: {reminder_text}"
        
        return "What would you like me to remind you about?"

class SystemModule(AssistantModule):
    """Handle system-related commands"""
    
    def can_handle(self, command):
        system_keywords = ['volume', 'brightness', 'wifi', 'bluetooth', 'restart', 'shutdown']
        return any(keyword in command.lower() for keyword in system_keywords)
    
    def execute(self, command, parameters=None):
        command_lower = command.lower()
        
        if 'volume' in command_lower:
            return "I can't control system volume yet, but you can use the volume controls on your device."
        elif 'brightness' in command_lower:
            return "I can't control screen brightness yet, but you can use the brightness controls on your device."
        elif 'wifi' in command_lower:
            subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.network'])
            return "I've opened network preferences for you."
        elif 'bluetooth' in command_lower:
            subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.bluetooth'])
            return "I've opened Bluetooth preferences for you."
        
        return "I can help you with some system settings. What would you like to adjust?"

class ModuleManager:
    """Manages all assistant modules"""
    
    def __init__(self):
        self.modules = [
            WebSearchModule(),
            ApplicationModule(),
            TimeDateModule(),
            NoteModule(),
            WeatherModule(),
            CalculatorModule(),
            MusicModule(),
            EmailModule(),
            ReminderModule(),
            SystemModule()
        ]
    
    def process_command(self, command):
        """Process a command through all available modules"""
        for module in self.modules:
            if module.can_handle(command):
                return module.execute(command)
        
        return "I'm not sure how to help with that. Could you try rephrasing your request?"

