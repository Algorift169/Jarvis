import time
import sys
from stt import SpeechToText
from tts import TextToSpeech
from brain import AIBrain
from input_handler import InputHandler, CommandProcessor
from config import WAKE_WORD, RECOGNITION_TIMEOUT, MIC_INDEX, GROQ_API_KEY
from utils import logger

def print_banner():
    print("\n" + "="*50)
    print("⚡ JARVIS AI SYSTEM ONLINE ⚡")
    print("="*50)
    print("Built by Israfil")
    print("="*50 + "\n")

def main():
    if not GROQ_API_KEY:
        logger.error("Groq API key not found!")
        print("\n❌ ERROR: Groq API key not found!")
        print("Please add your Groq API key to .env file")
        print("Create .env with: GROQ_API_KEY=gsk_xxxxxxxxxxxx")
        print("Get free key at: https://console.groq.com")
        return
    
    logger.info("Initializing JARVIS AI System...")
    print_banner()
    
    try:
        stt = SpeechToText(mic_index=MIC_INDEX)
        tts = TextToSpeech()
        brain = AIBrain()
        input_handler = InputHandler(stt=stt)
        command_processor = CommandProcessor(input_handler, brain, tts)
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        print(f"Error: {e}")
        return
    
    # Welcome message
    welcome = "Hello sir, I'm Jarvis, your personal AI assistant built by Israfil. How can I help you today?"
    tts.speak(welcome)
    logger.info("JARVIS is ready")
    
    print(f"\n🎤 CURRENT MODE: {input_handler.mode.upper()}")
    print(f"💬 To change mode, say or type: 'switch to text' or 'switch to voice'")
    print(f"🔊 Wake word: '{WAKE_WORD}' (only in voice mode)\n")
    
    active = False
    conversation_timeout = 60
    last_activity = time.time()
    
    while True:
        try:
            if input_handler.mode == "text":
                if not active:
                    print("\n⌨️ TEXT MODE ACTIVE - Type your command:")
                active = True
                
                command = input_handler.get_input()
                
                if command:
                    last_activity = time.time()
                    print(f"\n👤 You: {command}")
                    
                    if command.lower() in ["goodbye", "exit", "quit", "shutdown"]:
                        print("\n🛑 Shutting down JARVIS...")
                        farewell = "Goodbye, sir. It's been a pleasure."
                        tts.speak(farewell)
                        break
                    
                    print("🤔 Processing...", end="", flush=True)
                    response = command_processor.process(command)
                    print("\r" + " " * 20 + "\r", end="", flush=True)
                    
                    print(f"🎯 JARVIS: {response}")
                    tts.speak(response)
                    print()
                continue
            
            else:
                if not active:
                    if stt.listen_for_wake_word(WAKE_WORD):
                        active = True
                        last_activity = time.time()
                        tts.speak("Yes, sir? I'm listening.")
                        print("\n🎧 [VOICE MODE ACTIVE] Speak naturally. I'll wait until you finish.")
                        print("💬 Say 'goodbye' to end session or 'switch to text' to change mode.\n")
                        continue
                
                if active:
                    if time.time() - last_activity > conversation_timeout:
                        active = False
                        tts.speak("I'll be here if you need me, sir. Say the wake word to continue.")
                        print("\n💤 [VOICE MODE STANDBY] Say 'jarvis' to wake me up.\n")
                        continue
                    
                    command = stt.listen_command(timeout=RECOGNITION_TIMEOUT)
                    
                    if command:
                        last_activity = time.time()
                        print(f"\n👤 You: {command}")
                        
                        if command.lower() in ["goodbye", "exit", "quit", "thank you", "bye"]:
                            active = False
                            response = "You're welcome, sir. I'll be here when you need me. Say the wake word to resume."
                            print(f"🎯 JARVIS: {response}")
                            tts.speak(response)
                            print("\n💤 [STANDBY MODE] Say 'jarvis' to wake me up.\n")
                            continue
                        
                        print("🤔 Processing...", end="", flush=True)
                        response = command_processor.process(command)
                        print("\r" + " " * 20 + "\r", end="", flush=True)
                        
                        print(f"🎯 JARVIS: {response}")
                        tts.speak(response)
                        print()
                    else:
                        print("💭 (No command detected. I'm still listening...)", end="\r", flush=True)
                    
        except KeyboardInterrupt:
            print("\n\n" + "="*50)
            print("🛑 JARVIS system shutting down...")
            print("="*50)
            print("Built by Israfil")
            print("="*50)
            farewell = "Goodbye, sir. It's been a pleasure."
            tts.speak(farewell)
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"⚠️ Error: {e}")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 JARVIS offline.")
