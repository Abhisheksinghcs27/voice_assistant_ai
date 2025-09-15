#!/usr/bin/env python3
"""
Demo Script for AI Voice Assistant
This script demonstrates the assistant's capabilities with example commands.
"""

import time
import threading
from assistant_modules import ModuleManager

def demo_commands():
    """Demonstrate various assistant commands"""
    
    print("🎤 AI Voice Assistant - Demo Mode")
    print("=" * 50)
    print("This demo will show you what the assistant can do!")
    print()
    
    # Initialize module manager
    module_manager = ModuleManager()
    
    # Demo commands
    demo_commands = [
        "What time is it?",
        "What's the date today?",
        "Search for artificial intelligence",
        "Open calculator",
        "Weather in New York",
        "Calculate 15 plus 27",
        "Create a note",
        "Play music",
        "Send email",
        "Set reminder to call mom",
        "Open wifi settings"
    ]
    
    print("📋 Available Commands:")
    for i, cmd in enumerate(demo_commands, 1):
        print(f"  {i:2d}. {cmd}")
    
    print("\n🎯 Demo Responses:")
    print("-" * 50)
    
    for i, command in enumerate(demo_commands, 1):
        print(f"\n{i:2d}. Command: {command}")
        print(f"    Response: {module_manager.process_command(command)}")
        time.sleep(0.5)  # Small delay for readability
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nTo try these commands with voice:")
    print("1. Run: python simple_assistant.py")
    print("2. Click 'Start Listening'")
    print("3. Speak any of the commands above")
    print("\nOr type commands in the text input field!")

def interactive_demo():
    """Interactive demo where user can type commands"""
    
    print("🎤 AI Voice Assistant - Interactive Demo")
    print("=" * 50)
    print("Type commands to see how the assistant responds!")
    print("Type 'quit' or 'exit' to end the demo")
    print("Type 'help' to see available commands")
    print()
    
    module_manager = ModuleManager()
    
    while True:
        try:
            command = input("You: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            elif command.lower() == 'help':
                print("\n📋 Available Commands:")
                print("• What time is it?")
                print("• What's the date today?")
                print("• Search for [topic]")
                print("• Open [application] (calculator, notes, safari, etc.)")
                print("• Weather in [city]")
                print("• Calculate [expression]")
                print("• Create a note")
                print("• Play music")
                print("• Send email")
                print("• Set reminder [text]")
                print("• Open wifi settings")
                print()
                continue
            
            if command:
                response = module_manager.process_command(command)
                print(f"Assistant: {response}")
                print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except EOFError:
            print("\n\nGoodbye! 👋")
            break

def main():
    """Main demo function"""
    
    print("🎤 AI Voice Assistant - Demo")
    print("=" * 50)
    print("Choose a demo mode:")
    print("1. Automatic demo (shows all capabilities)")
    print("2. Interactive demo (type commands)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                demo_commands()
                break
            elif choice == '2':
                interactive_demo()
                break
            elif choice == '3':
                print("Goodbye! 👋")
                break
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break

if __name__ == "__main__":
    main()

