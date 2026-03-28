import speech_recognition as sr
from utils import logger

class SpeechToText:
    def __init__(self, mic_index=None):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        self.mic_index = mic_index
        
    def listen_for_wake_word(self, wake_word):
        """Listen until wake word is heard, return True when detected."""
        with sr.Microphone(device_index=self.mic_index) as source:
            logger.info(f"Listening for wake word: '{wake_word}'...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening for wake word...", end="", flush=True)
            
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"\nHeard: {text}")
                    if wake_word in text:
                        logger.info(f"Wake word detected: '{text}'")
                        return True
                except sr.WaitTimeoutError:
                    print(".", end="", flush=True)
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    logger.error(f"Recognition error: {e}")
                    continue

    def listen_command(self, timeout=5):
        """Listen for a command with natural pause detection."""
        with sr.Microphone(device_index=self.mic_index) as source:
            print("🎧 Listening... (waiting for you to finish speaking)", end="", flush=True)
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                print("\r🎧 Processing speech...", end="", flush=True)
                text = self.recognizer.recognize_google(audio).lower()
                logger.info(f"User said: {text}")
                print(f"\r✓ Command received: {text}")
                return text
            except sr.WaitTimeoutError:
                print("\r⏰ No speech detected")
                return ""
            except sr.UnknownValueError:
                print("\r❓ Could not understand")
                return ""
            except sr.RequestError as e:
                logger.error(f"Recognition error: {e}")
                print(f"\r⚠️ Error: {e}")
                return ""