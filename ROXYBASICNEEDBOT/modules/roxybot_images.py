# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# Image URLs Configuration Module
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
from dotenv import load_dotenv

load_dotenv()

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Image URLs for bot messages
# You can use direct URLs to images (JPG, PNG, GIF)
# Example: https://i.imgur.com/example.jpg

class RoxyBotImages:
    """Image URLs and Sticker IDs configuration for bot messages"""
    
    # Welcome image - shown when user sends /start
    # Leave empty "" to disable image
    WELCOME_IMAGE_URL = os.getenv(
        "ROXYBOT_WELCOME_IMAGE", 
        "https://i.ibb.co/3mfDbZ66/file-29679.jpg"
    )
    
    # Force subscribe image - shown when user hasn't joined required channels
    # Leave empty "" to disable image
    FORCESUB_IMAGE_URL = os.getenv(
        "ROXYBOT_FORCESUB_IMAGE", 
        "https://i.ibb.co/XZthtr6f/file-29501.jpg"
    )
    
    # Help image - shown with /help command
    HELP_IMAGE_URL = os.getenv(
        "ROXYBOT_HELP_IMAGE", 
        "https://i.ibb.co/ymVJ5THL/file-29678.jpg"
    )
    
    # Stats image - shown with /stats command
    STATS_IMAGE_URL = os.getenv(
        "ROXYBOT_STATS_IMAGE", 
        "https://i.ibb.co/gZFnGrgB/file-29497.jpg"
    )
    
    # ZIP created success sticker (Sticker file_id)
    # To get sticker ID: Forward any sticker to @idstickerbot or use /getsticker command
    ZIP_SUCCESS_STICKER = os.getenv(
        "ROXYBOT_ZIP_SUCCESS_STICKER", 
        "CAACAgUAAxkBAAIFQWlHphxx_69VhcrwectJ18HShKzvAAL-EQACNA5QVFM_sWJ-N0KlHgQ"
    )
    
    # Ban sticker - shown when banned user tries to use the bot
    BAN_STICKER = os.getenv(
        "ROXYBOT_BAN_STICKER", 
        "CAACAgUAAxkBAAIFS2lH9u6q8c7Pwi4LRcmabgABUIqZDAAC3xEAAt7LUVQPJjIY8-rwtx4E"
    )
    
    @classmethod
    def get_welcome_image(cls) -> str:
        """Get welcome image URL"""
        return cls.WELCOME_IMAGE_URL.strip() if cls.WELCOME_IMAGE_URL else ""
    
    @classmethod
    def get_forcesub_image(cls) -> str:
        """Get force subscribe image URL"""
        return cls.FORCESUB_IMAGE_URL.strip() if cls.FORCESUB_IMAGE_URL else ""
    
    @classmethod
    def get_help_image(cls) -> str:
        """Get help image URL"""
        return cls.HELP_IMAGE_URL.strip() if cls.HELP_IMAGE_URL else ""
    
    @classmethod
    def get_stats_image(cls) -> str:
        """Get stats image URL"""
        return cls.STATS_IMAGE_URL.strip() if cls.STATS_IMAGE_URL else ""
    
    @classmethod
    def get_zip_success_sticker(cls) -> str:
        """Get ZIP success sticker ID"""
        return cls.ZIP_SUCCESS_STICKER.strip() if cls.ZIP_SUCCESS_STICKER else ""
    
    @classmethod
    def get_ban_sticker(cls) -> str:
        """Get ban sticker ID"""
        return cls.BAN_STICKER.strip() if cls.BAN_STICKER else ""


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
