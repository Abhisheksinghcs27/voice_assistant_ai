#!/usr/bin/env python3
"""
Quick Start Script for AI Voice Assistant
This script checks dependencies and launches the appropriate assistant version.
"""

import sys
import subprocess
import importlib.util

def check_dependency(module_name):
    """Check if a module is available"""
    return importlib.util.find_spec(module_name) is not None

def install_dependency(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🎤 AI Voice Assistant - Quick Start")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Required dependencies
    required_deps = [
        'speech_recognition',
        'pyttsx3',
        'requests',
        'numpy'
    ]
    
    # Optional dependencies
    optional_deps = [
        'openai',
        'python_dotenv'
    ]
    
    print("\n📦 Checking dependencies...")
    
    # Check required dependencies
    missing_required = []
    for dep in required_deps:
        if check_dependency(dep):
            print(f"✅ {dep}")
        else:
            print(f"❌ {dep} - Missing")
            missing_required.append(dep)
    
    # Check optional dependencies
    missing_optional = []
    for dep in optional_deps:
        if check_dependency(dep):
            print(f"✅ {dep} (optional)")
        else:
            print(f"⚠️  {dep} - Missing (optional)")
            missing_optional.append(dep)
    
    # Install missing required dependencies
    if missing_required:
        print(f"\n🔧 Installing missing required dependencies: {', '.join(missing_required)}")
        for dep in missing_required:
            print(f"Installing {dep}...")
            if install_dependency(dep):
                print(f"✅ Successfully installed {dep}")
            else:
                print(f"❌ Failed to install {dep}")
                return
    
    # Try to install PyAudio (special handling)
    if not check_dependency('pyaudio'):
        print("\n🔧 Installing PyAudio...")
        print("Note: PyAudio might require system dependencies.")
        print("On macOS, you may need to run: brew install portaudio")
        
        if install_dependency('PyAudio'):
            print("✅ Successfully installed PyAudio")
        else:
            print("❌ Failed to install PyAudio")
            print("You may need to install it manually:")
            print("  macOS: brew install portaudio && pip install PyAudio")
            print("  Ubuntu: sudo apt-get install python3-pyaudio")
            print("  Windows: pip install PyAudio")
    
    # Check if OpenAI is available for advanced features
    has_openai = check_dependency('openai')
    
    print("\n🚀 Starting Voice Assistant...")
    
    if has_openai:
        print("Using advanced assistant with OpenAI integration")
        try:
            import main
            assistant = main.VoiceAssistant()
            assistant.run()
        except ImportError as e:
            print(f"Error importing advanced assistant: {e}")
            print("Falling back to simple assistant...")
            import simple_assistant
            assistant = simple_assistant.SimpleVoiceAssistant()
            assistant.run()
    else:
        print("Using simple assistant (no OpenAI API required)")
        try:
            import simple_assistant
            assistant = simple_assistant.SimpleVoiceAssistant()
            assistant.run()
        except ImportError as e:
            print(f"Error importing simple assistant: {e}")
            print("Please check that all files are in the correct location.")

if __name__ == "__main__":
    main()

