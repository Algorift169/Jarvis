from utils import logger

class InputHandler:
    """Handles both voice and text input"""
    
    def __init__(self, stt=None):
        self.stt = stt
        self.mode = "voice"  # Default mode: voice or text
        
    def set_mode(self, mode):
        if mode in ["voice", "text"]:
            self.mode = mode
            logger.info(f"Input mode switched to: {mode}")
            return f"Input mode switched to {mode}."
        return "Invalid mode. Use 'voice' or 'text'."
    
    def get_input(self, timeout=10):
        if self.mode == "voice" and self.stt:
            return self._get_voice_input(timeout)
        else:
            return self._get_text_input(timeout)
    
    def _get_voice_input(self, timeout):
        print("\n🎤 Voice mode - Speak now...")
        return self.stt.listen_command(timeout=timeout)
    
    def _get_text_input(self, timeout):
        print("\n⌨️ Text mode - Type your command (press Enter when done)")
        print("💡 Tip: Type 'switch to voice' to go back to voice mode")
        print("> ", end="", flush=True)
        try:
            return input().strip().lower()
        except:
            return ""

class CommandProcessor:
    def __init__(self, input_handler, brain, tts):
        self.input_handler = input_handler
        self.brain = brain
        self.tts = tts
    
    def process_special_command(self, command):
        cmd = command.lower()
        
        if "switch to voice" in cmd or "go to voice" in cmd:
            return self.input_handler.set_mode("voice")
        if "switch to text" in cmd or "go to text" in cmd or "text mode" in cmd:
            return self.input_handler.set_mode("text")
        if "what mode" in cmd or "current mode" in cmd:
            return f"Currently in {self.input_handler.mode} mode."
        
        return None
    
    def process(self, command):
        special_result = self.process_special_command(command)
        if special_result:
            return special_result
        return self.brain.process_command(command)