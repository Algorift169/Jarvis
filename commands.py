from pc_controller import pc_control
from utils import logger

def execute_system_command(command):
    """Check if command is a PC control command"""
    result = pc_control.execute(command)
    if result:
        logger.info(f"Executed PC command: {command}")
        return result
    return None