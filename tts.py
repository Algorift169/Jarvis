import asyncio
import edge_tts
import pygame
import tempfile
import os
import time
from utils import logger

class TextToSpeech:
    def __init__(self):
        pygame.mixer.init()
        self.temp_files = []
        
        # Deep male voice - Thomas (most authoritative British male)
        self.voice = "en-GB-ThomasNeural"
        self.rate = "-5%"  # Slightly slower for more authority
        
    def speak(self, text):
        """Convert text to speech with deep male voice"""
        logger.info(f"Speaking: {text}")
        print(f"\n🔊 Jarvis: {text}")
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                self.temp_files.append(temp_filename)
            
            async def generate_speech():
                communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
                await communicate.save(temp_filename)
            
            asyncio.run(generate_speech())
            
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            try:
                os.unlink(temp_filename)
                self.temp_files.remove(temp_filename)
            except:
                pass
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"Jarvis: {text}")
    
    def stop(self):
        pygame.mixer.music.stop()
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files = []
    
    def __del__(self):
        self.stop()
