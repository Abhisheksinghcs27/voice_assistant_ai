# AI Voice Assistant

A powerful Python-based voice assistant that can perform various tasks through voice commands and text input. Built with speech recognition, text-to-speech, and a modular architecture for easy extension.

## Features

### 🎤 Voice Recognition
- Real-time speech-to-text conversion
- Continuous listening mode
- Noise cancellation and ambient noise adjustment
- Support for multiple languages (via Google Speech Recognition)

### 🔊 Text-to-Speech
- Natural-sounding voice output
- Adjustable speech rate and volume
- Cross-platform compatibility

### 🤖 AI-Powered Processing
- OpenAI GPT integration for natural language understanding
- Modular command processing system
- Extensible architecture for custom commands

### 🎯 Task Capabilities
- **Web Search**: Search the internet for any topic
- **Application Control**: Open system applications
- **Time & Date**: Get current time and date information
- **Note Taking**: Create and save text notes
- **Weather**: Get weather information for any city
- **Calculator**: Perform mathematical calculations
- **Music**: Control music applications
- **Email**: Open email client
- **Reminders**: Set and manage reminders
- **System Settings**: Access system preferences

### 🖥️ User Interface
- Modern GUI built with tkinter
- Real-time conversation display
- Voice and text input options
- Status indicators and controls

## Installation

### Prerequisites
- Python 3.7 or higher
- macOS (for best compatibility with system applications)
- Microphone access
- Internet connection

### Step 1: Clone or Download
```bash
# If you have this as a repository
git clone <repository-url>
cd voice_assistant_ai

# Or navigate to the project directory
cd voice_assistant_ai
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install PyAudio (if needed)
On macOS, you might need to install PyAudio separately:
```bash
# Using Homebrew
brew install portaudio
pip install PyAudio

# Or using conda
conda install pyaudio
```

### Step 4: Set Up Environment Variables (Optional)
For enhanced AI features, create a `.env` file:
```bash
cp env_example.txt .env
```

Edit the `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage (No API Key Required)
```bash
python simple_assistant.py
```

### Advanced Usage (With OpenAI API)
```bash
python main.py
```

### Command Examples

#### Voice Commands
- "What time is it?"
- "Open calculator"
- "Search for Python programming"
- "Weather in New York"
- "Create a note"
- "Play music"
- "Send email"
- "Calculate 15 plus 27"
- "Set reminder to call mom"

#### Text Commands
You can also type commands in the text input field:
- "open safari"
- "search for machine learning"
- "what's the date today"
- "weather in London"

## Project Structure

```
voice_assistant_ai/
├── main.py                 # Full-featured assistant with OpenAI integration
├── simple_assistant.py     # Basic assistant without API requirements
├── assistant_modules.py    # Modular command processing system
├── requirements.txt        # Python dependencies
├── env_example.txt         # Environment variables template
├── README.md              # This file
└── notes/                 # Directory for saved notes (created automatically)
```

## Architecture

### Modular Design
The assistant uses a modular architecture where each capability is implemented as a separate module:

- **WebSearchModule**: Handles web search commands
- **ApplicationModule**: Manages application launching
- **TimeDateModule**: Provides time and date information
- **NoteModule**: Handles note creation and management
- **WeatherModule**: Provides weather information
- **CalculatorModule**: Performs mathematical calculations
- **MusicModule**: Controls music applications
- **EmailModule**: Handles email-related tasks
- **ReminderModule**: Manages reminders and tasks
- **SystemModule**: Controls system settings

### Adding Custom Modules
To add a new capability, create a new class that inherits from `AssistantModule`:

```python
class CustomModule(AssistantModule):
    def can_handle(self, command):
        # Return True if this module can handle the command
        return 'custom' in command.lower()
    
    def execute(self, command, parameters=None):
        # Implement the command logic
        return "Custom response"
```

Then add it to the `ModuleManager` in `assistant_modules.py`.

## Troubleshooting

### Common Issues

#### 1. PyAudio Installation
If you encounter issues installing PyAudio:
```bash
# On macOS with Homebrew
brew install portaudio
pip install PyAudio

# On Ubuntu/Debian
sudo apt-get install python3-pyaudio
```

#### 2. Microphone Access
Ensure your application has microphone permissions:
- macOS: System Preferences → Security & Privacy → Microphone
- Windows: Settings → Privacy → Microphone

#### 3. Speech Recognition Issues
- Check your internet connection (required for Google Speech Recognition)
- Ensure your microphone is working and properly configured
- Try speaking clearly and in a quiet environment

#### 4. OpenAI API Errors
- Verify your API key is correct
- Check your OpenAI account balance
- Ensure you have proper API access

### Performance Tips
- Use a good quality microphone for better speech recognition
- Speak clearly and at a moderate pace
- Minimize background noise
- Close unnecessary applications to free up system resources

## Customization

### Changing Assistant Name
Edit the `assistant_name` variable in the assistant class:
```python
self.assistant_name = "Your Custom Name"
```

### Adjusting Speech Settings
Modify speech rate and volume:
```python
self.engine.setProperty('rate', 150)    # Speed (words per minute)
self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
```

### Adding New Applications
Edit the `apps` dictionary in `ApplicationModule`:
```python
self.apps = {
    'your_app': 'Your Application Name',
    # ... existing apps
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google Speech Recognition API
- OpenAI GPT API
- PyAudio and SpeechRecognition libraries
- pyttsx3 for text-to-speech

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the project documentation
3. Open an issue on the repository
4. Contact the development team

---

**Enjoy using your AI Voice Assistant!** 🎉

