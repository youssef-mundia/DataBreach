"""
Basic Telegram monitoring service
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

try:
    from telethon import TelegramClient, events
    from telethon.tl.types import Channel, Chat, User as TelegramUser
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    TelegramClient = None
    events = None

from config.settings import settings

logger = logging.getLogger(__name__)


class TelegramMonitoringService:
    """Telegram monitoring service"""
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.monitored_channels = set()
        self.message_handlers = []
        
    async def initialize(self):
        """Initialize Telegram client"""
        if not TELETHON_AVAILABLE:
            logger.error("Telethon not available. Install with: pip install telethon")
            return False
            
        if not settings.TELEGRAM_API_ID or not settings.TELEGRAM_API_HASH:
            logger.warning("Telegram API credentials not configured")
            return False
            
        try:
            self.client = TelegramClient(
                'session_databreach',
                settings.TELEGRAM_API_ID,
                settings.TELEGRAM_API_HASH
            )
            
            await self.client.start()
            self.is_connected = True
            
            # Setup event handlers
            self.client.add_event_handler(
                self._handle_new_message,
                events.NewMessage()
            )
            
            logger.info("Telegram client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Telegram client: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup Telegram client"""
        if self.client and self.is_connected:
            await self.client.disconnect()
            self.is_connected = False
            
    async def _handle_new_message(self, event):
        """Handle new Telegram messages"""
        try:
            message = event.message
            chat = await event.get_chat()
            
            # Basic message info
            message_data = {
                "message_id": message.id,
                "chat_id": chat.id,
                "chat_title": getattr(chat, 'title', 'Private Chat'),
                "text": message.text or "",
                "date": message.date.isoformat(),
                "sender_id": message.sender_id,
                "is_channel": isinstance(chat, Channel),
                "is_group": isinstance(chat, Chat)
            }
            
            # Check if this chat is monitored
            if chat.id in self.monitored_channels:
                await self._process_monitored_message(message_data)
                
        except Exception as e:
            logger.error(f"Error handling Telegram message: {e}")
    
    async def _process_monitored_message(self, message_data: Dict[str, Any]):
        """Process a message from a monitored channel"""
        try:
            # Simple keyword matching for now
            text = message_data.get("text", "").lower()
            
            # Common data breach keywords
            breach_keywords = [
                "breach", "leak", "hacked", "database", "dump", "stolen",
                "credentials", "passwords", "personal data", "exposed",
                "vulnerability", "exploit", "ransomware", "data loss"
            ]
            
            matches = [keyword for keyword in breach_keywords if keyword in text]
            
            if matches:
                logger.info(f"Potential breach detected in Telegram: {matches}")
                # In a real implementation, this would be saved to database
                # and trigger alerts
                
        except Exception as e:
            logger.error(f"Error processing monitored message: {e}")
    
    async def add_monitored_channel(self, channel_identifier: str) -> bool:
        """Add a channel to monitoring"""
        if not self.is_connected:
            logger.error("Telegram client not connected")
            return False
            
        try:
            # Get channel entity
            entity = await self.client.get_entity(channel_identifier)
            self.monitored_channels.add(entity.id)
            
            logger.info(f"Added channel to monitoring: {getattr(entity, 'title', channel_identifier)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add channel {channel_identifier}: {e}")
            return False
    
    async def remove_monitored_channel(self, channel_identifier: str) -> bool:
        """Remove a channel from monitoring"""
        try:
            entity = await self.client.get_entity(channel_identifier)
            self.monitored_channels.discard(entity.id)
            
            logger.info(f"Removed channel from monitoring: {getattr(entity, 'title', channel_identifier)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove channel {channel_identifier}: {e}")
            return False
    
    async def get_channel_info(self, channel_identifier: str) -> Optional[Dict[str, Any]]:
        """Get information about a Telegram channel"""
        if not self.is_connected:
            return None
            
        try:
            entity = await self.client.get_entity(channel_identifier)
            
            return {
                "id": entity.id,
                "title": getattr(entity, 'title', 'Unknown'),
                "username": getattr(entity, 'username', None),
                "description": getattr(entity, 'about', ''),
                "member_count": getattr(entity, 'participants_count', 0),
                "is_channel": isinstance(entity, Channel),
                "is_group": isinstance(entity, Chat)
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel info for {channel_identifier}: {e}")
            return None
    
    async def search_messages(self, channel_identifier: str, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search messages in a channel"""
        if not self.is_connected:
            return []
            
        try:
            messages = []
            async for message in self.client.iter_messages(channel_identifier, search=query, limit=limit):
                messages.append({
                    "id": message.id,
                    "text": message.text or "",
                    "date": message.date.isoformat(),
                    "sender_id": message.sender_id,
                    "views": getattr(message, 'views', 0)
                })
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to search messages in {channel_identifier}: {e}")
            return []
    
    async def get_monitored_channels_status(self) -> List[Dict[str, Any]]:
        """Get status of all monitored channels"""
        status_list = []
        
        for channel_id in self.monitored_channels:
            try:
                entity = await self.client.get_entity(channel_id)
                status_list.append({
                    "id": channel_id,
                    "title": getattr(entity, 'title', 'Unknown'),
                    "username": getattr(entity, 'username', None),
                    "status": "active"
                })
            except Exception as e:
                status_list.append({
                    "id": channel_id,
                    "title": "Unknown",
                    "username": None,
                    "status": f"error: {str(e)}"
                })
        
        return status_list


# Global instance
telegram_service = TelegramMonitoringService()