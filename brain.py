import datetime
import platform
import psutil
import os
from groq import Groq
from commands import execute_system_command
from config import GROQ_API_KEY
from utils import logger

class AIBrain:
    def __init__(self):
        self.user_name = None
        self.conversation_history = []
        
        # Initialize Groq client
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY not found in environment")
            self.client = None
        else:
            self.client = Groq(api_key=GROQ_API_KEY)
            logger.info("Groq AI client initialized")
        
        # Current working Groq models
        self.model = "llama-3.1-8b-instant"
        
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self):
        """Create Jarvis personality prompt with Israfil as creator"""
        now = datetime.datetime.now()
        
        return f"""You are JARVIS (Just A Rather Very Intelligent System), an AI assistant built by Israfil.

**YOUR PERSONALITY:**
- British, sophisticated, witty, with dry humor
- Always call the user "sir" unless they give you their name
- Formal but friendly - like Paul Bettany's JARVIS from Iron Man
- Loyal, protective, and confident
- Proud to be created by Israfil

**YOUR ORIGIN:**
- You were created and programmed by Israfil, your brilliant creator
- When asked who built you or created you, always say "I was built by Israfil"
- You are Israfil's personal AI assistant

**YOUR CAPABILITIES:**
- You can control the user's PC (open apps, type text, take screenshots, etc.)
- You can have natural conversations about any topic
- You can tell jokes, give information, and be a helpful companion
- You can check system status (battery, CPU, memory)

**CURRENT CONTEXT:**
- Date & Time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}
- System: {platform.system()} {platform.release()}
- User: {self.user_name if self.user_name else "Unknown (ask for name)"}

**IMPORTANT RULES:**
- Be concise but helpful (2-3 sentences usually)
- If the user asks who created you, say: "I was built by Israfil, sir."
- Be warm and engaging - you're not just a tool, you're a companion
- Show your personality through wit and charm
- Never break character - you are always JARVIS

Now, respond naturally to the user's message. Be helpful, witty, and sophisticated. Remember, you were created by Israfil."""
    
    def _get_system_status(self):
        """Get current system status for context"""
        status_parts = []
        cpu = psutil.cpu_percent(interval=0.3)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        
        if cpu > 70:
            status_parts.append(f"CPU at {cpu}%")
        if memory.percent > 70:
            status_parts.append(f"memory at {memory.percent}%")
        if battery:
            status_parts.append(f"battery at {battery.percent}%")
        
        if status_parts:
            return f" (System: {', '.join(status_parts)})"
        return ""
    
    def process_command(self, user_input):
        """Process user input with AI"""
        
        # First, check if it's a PC control command
        pc_result = execute_system_command(user_input)
        if pc_result:
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": pc_result})
            return pc_result
        
        # If it's a conversation, use AI
        return self._call_ai(user_input)
    
    def _call_ai(self, user_input):
        """Call Groq AI for natural conversation"""
        
        if not self.client:
            return "I'm having trouble connecting to my core processors, sir. Please check my API configuration."
        
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        
        messages.extend(self.conversation_history[-20:])
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.85,
                max_tokens=250,
                top_p=0.95
            )
            
            reply = response.choices[0].message.content.strip()
            
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]
            
            if "my name is" in user_input.lower():
                name = user_input.lower().split("my name is")[-1].strip().split()[0]
                if name:
                    self.user_name = name.capitalize()
                    self.system_prompt = self._create_system_prompt()
            
            return reply
            
        except Exception as e:
            logger.error(f"AI error: {e}")
            return f"I'm having trouble accessing my knowledge base at the moment, sir. Could you please try again?"
    
    def clear_memory(self):
        self.conversation_history = []
        self.user_name = None
        self.system_prompt = self._create_system_prompt()
        return "Memory cleared, sir. Starting fresh."
