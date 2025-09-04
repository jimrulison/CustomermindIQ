"""
Background Tasks for CustomerMind IQ
Handles scheduled trial emails and other automated tasks
"""

import asyncio
import logging
from datetime import datetime, timedelta
from modules.email_system import process_scheduled_trial_emails

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundTaskManager:
    def __init__(self):
        self.running = False
        self.tasks = []
    
    async def start(self):
        """Start all background tasks"""
        if self.running:
            return
        
        self.running = True
        logger.info("Starting background task manager...")
        
        # Start trial email processor (runs every 5 minutes)
        trial_email_task = asyncio.create_task(self.trial_email_processor())
        self.tasks.append(trial_email_task)
        
        logger.info(f"Started {len(self.tasks)} background tasks")
    
    async def stop(self):
        """Stop all background tasks"""
        self.running = False
        logger.info("Stopping background task manager...")
        
        for task in self.tasks:
            task.cancel()
        
        # Wait for all tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        
        logger.info("Background task manager stopped")
    
    async def trial_email_processor(self):
        """Process scheduled trial emails every 5 minutes"""
        while self.running:
            try:
                logger.info("Processing scheduled trial emails...")
                await process_scheduled_trial_emails()
                logger.info("Trial email processing completed")
            except Exception as e:
                logger.error(f"Error processing trial emails: {str(e)}")
            
            # Wait 5 minutes before next run
            await asyncio.sleep(300)  # 300 seconds = 5 minutes

# Global instance
task_manager = BackgroundTaskManager()

# Convenience functions
async def start_background_tasks():
    """Start all background tasks"""
    await task_manager.start()

async def stop_background_tasks():
    """Stop all background tasks"""
    await task_manager.stop()