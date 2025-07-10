#!/usr/bin/env python3
"""
SightlineAI - Simple AI Assistant for Smart Glasses
Phase 1: Core Foundation with ChatGPT API Integration
"""

import os
import sys
from openai import OpenAI
from datetime import datetime

class SightlineAI:
    def __init__(self):
        """Initialize SightlineAI with API key and settings"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Error: OPENAI_API_KEY environment variable not set")
            print("Please set your OpenAI API key:")
            print("export OPENAI_API_KEY='your-key-here'")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.max_tokens = 150  # Optimized for smart glasses display
        self.model = "gpt-3.5-turbo"
        
        print("✓ SightlineAI initialized successfully")
        print(f"✓ Using model: {self.model}")
        print(f"✓ Max response length: {self.max_tokens} tokens")

    def query_chatgpt(self, prompt):
        """Send query to ChatGPT and return clean response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Keep responses concise and clear for display on smart glasses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error: {str(e)}"

    def format_for_display(self, text):
        """Format text for optimal display on smart glasses"""
        # Remove excessive whitespace
        formatted = text.replace('\n\n', '\n').strip()
        
        # Ensure no lines are too long (smart glasses have limited width)
        lines = formatted.split('\n')
        formatted_lines = []
        
        for line in lines:
            if len(line) <= 60:  # Optimal line length for glasses
                formatted_lines.append(line)
            else:
                # Break long lines at word boundaries
                words = line.split(' ')
                current_line = ""
                
                for word in words:
                    if len(current_line + " " + word) <= 60:
                        current_line += " " + word if current_line else word
                    else:
                        if current_line:
                            formatted_lines.append(current_line)
                        current_line = word
                
                if current_line:
                    formatted_lines.append(current_line)
        
        return '\n'.join(formatted_lines)

    def display_response(self, query, response):
        """Display the query and response in glasses-optimized format"""
        print("\n" + "="*60)
        print(f"Query: {query}")
        print("-"*60)
        formatted_response = self.format_for_display(response)
        print(formatted_response)
        print("="*60)

    def run_interactive_mode(self):
        """Run the interactive command-line interface"""
        print("\n🥽 SightlineAI - Interactive Mode")
        print("Type your questions below. Commands:")
        print("  'quit' or 'exit' - Exit the program")
        print("  'clear' - Clear screen")
        print("  'help' - Show this help")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n🎤 Your question: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                elif user_input.lower() == 'help':
                    print("\nSightlineAI Commands:")
                    print("  'quit' or 'exit' - Exit the program")
                    print("  'clear' - Clear screen")
                    print("  'help' - Show this help")
                    continue
                
                # Process the query
                print("🤖 Thinking...")
                response = self.query_chatgpt(user_input)
                self.display_response(user_input, response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def test_connection(self):
        """Test the ChatGPT API connection"""
        print("\n🔍 Testing ChatGPT API connection...")
        test_query = "Say 'Hello from SightlineAI!' in exactly 5 words."
        
        try:
            response = self.query_chatgpt(test_query)
            print(f"✓ API Test Successful!")
            self.display_response(test_query, response)
            return True
        except Exception as e:
            print(f"✗ API Test Failed: {e}")
            return False

def main():
    """Main function to run SightlineAI"""
    print("🚀 Starting SightlineAI...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize SightlineAI
    try:
        ai = SightlineAI()
    except SystemExit:
        return
    
    # Test API connection
    if not ai.test_connection():
        print("Please check your API key and internet connection.")
        return
    
    # Run interactive mode
    ai.run_interactive_mode()

if __name__ == "__main__":
    main()
