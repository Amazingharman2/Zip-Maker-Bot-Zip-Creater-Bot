# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
# Instagram: roxybasicneedbot1
# Portfolio: https://aratt.ai/@roxybasicneedbot
# 
# Bot & Website Developer 🤖
# Creator of Roxy BasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
# 
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

from pyrogram import Client, filters
from pyrogram.types import Message
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Thumbnail Management Module
# /addthumb - Add custom thumbnail (reply to photo)
# /delthumb - Delete custom thumbnail
# /viewthumb - View current thumbnail


@Client.on_message(filters.command("addthumb") & filters.private)
async def roxybot_addthumb_command(client: Client, message: Message):
    """Add custom thumbnail - user must reply to a photo"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /addthumb")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if replying to a photo
    if not message.reply_to_message:
        await message.reply_text(
            "🖼️ **Aᴅᴅ Cᴜꜱᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ**\n\n"
            "**Uꜱᴀɢᴇ:** Rᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴡɪᴛʜ /addthumb\n\n"
            "Tʜᴇ ᴘʜᴏᴛᴏ ᴡɪʟʟ ʙᴇ ᴜꜱᴇᴅ ᴀꜱ ᴛʜᴜᴍʙɴᴀɪʟ ғᴏʀ ʏᴏᴜʀ ZIP ғɪʟᴇꜱ.\n\n"
            "📐 **Rᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ ꜱɪᴢᴇ:** 320x320 ᴘɪxᴇʟꜱ\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    reply_msg = message.reply_to_message
    
    # Check if the reply is a photo
    if not reply_msg.photo:
        await message.reply_text(
            "❌ **Pʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ!**\n\n"
            "Sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ғɪʀꜱᴛ, ᴛʜᴇɴ ʀᴇᴘʟʏ ᴛᴏ ɪᴛ ᴡɪᴛʜ /addthumb\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Get the photo file_id (highest quality)
    photo_file_id = reply_msg.photo.file_id
    
    # Save to database
    success = await roxybot_db.roxybot_set_thumbnail(user_id, photo_file_id)
    
    if success:
        await message.reply_text(
            "✅ **Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ!**\n\n"
            "Yᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇᴛ.\n"
            "Iᴛ ᴡɪʟʟ ʙᴇ ᴜꜱᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ ZIP ғɪʟᴇꜱ!\n\n"
            "📝 **Cᴏᴍᴍᴀɴᴅꜱ:**\n"
            "• /viewthumb - Vɪᴇᴡ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ\n"
            "• /delthumb - Dᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.info(f"✅ Thumbnail set for user {user_id}")
    else:
        await message.reply_text(
            "❌ **Eʀʀᴏʀ ꜱᴀᴠɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.error(f"❌ Failed to set thumbnail for user {user_id}")


@Client.on_message(filters.command("delthumb") & filters.private)
async def roxybot_delthumb_command(client: Client, message: Message):
    """Delete custom thumbnail"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /delthumb")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user has a thumbnail
    current_thumb = await roxybot_db.roxybot_get_thumbnail(user_id)
    
    if not current_thumb:
        await message.reply_text(
            "ℹ️ **Nᴏ Cᴜꜱᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ**\n\n"
            "Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴇᴛ.\n\n"
            "Uꜱᴇ /addthumb ᴛᴏ ᴀᴅᴅ ᴏɴᴇ!\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Delete thumbnail
    success = await roxybot_db.roxybot_delete_thumbnail(user_id)
    
    if success:
        await message.reply_text(
            "🗑️ **Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ!**\n\n"
            "Yᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.\n"
            "Dᴇғᴀᴜʟᴛ ᴛʜᴜᴍʙɴᴀɪʟ ᴡɪʟʟ ʙᴇ ᴜꜱᴇᴅ ɴᴏᴡ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.info(f"✅ Thumbnail deleted for user {user_id}")
    else:
        await message.reply_text(
            "❌ **Eʀʀᴏʀ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.error(f"❌ Failed to delete thumbnail for user {user_id}")


@Client.on_message(filters.command("viewthumb") & filters.private)
async def roxybot_viewthumb_command(client: Client, message: Message):
    """View current thumbnail"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /viewthumb")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Get user's thumbnail
    thumb_file_id = await roxybot_db.roxybot_get_thumbnail(user_id)
    
    if not thumb_file_id:
        await message.reply_text(
            "ℹ️ **Nᴏ Cᴜꜱᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ**\n\n"
            "Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴇᴛ.\n"
            "Dᴇғᴀᴜʟᴛ ᴛʜᴜᴍʙɴᴀɪʟ ᴡɪʟʟ ʙᴇ ᴜꜱᴇᴅ ғᴏʀ ZIPꜱ.\n\n"
            "Uꜱᴇ /addthumb ᴛᴏ ᴀᴅᴅ ᴀ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ!\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    try:
        # Send the thumbnail
        await message.reply_photo(
            photo=thumb_file_id,
            caption=(
                "🖼️ **Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴᴀɪʟ**\n\n"
                "Tʜɪꜱ ɪᴍᴀɢᴇ ɪꜱ ᴜꜱᴇᴅ ғᴏʀ ʏᴏᴜʀ ZIP ғɪʟᴇꜱ.\n\n"
                "📝 **Cᴏᴍᴍᴀɴᴅꜱ:**\n"
                "• /addthumb - Cʜᴀɴɢᴇ ᴛʜᴜᴍʙɴᴀɪʟ\n"
                "• /delthumb - Rᴇᴍᴏᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ\n\n"
                "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
            )
        )
        logger.info(f"✅ Thumbnail shown to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Error showing thumbnail for user {user_id}: {e}")
        await message.reply_text(
            "❌ **Eʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ!**\n\n"
            "Yᴏᴜʀ ꜱᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴍᴀʏ ʙᴇ ᴇxᴘɪʀᴇᴅ.\n"
            "Pʟᴇᴀꜱᴇ ꜱᴇᴛ ᴀ ɴᴇᴡ ᴏɴᴇ ᴡɪᴛʜ /addthumb\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Helper function to get user thumbnail for ZIP creation

async def roxybot_get_user_thumbnail(client: Client, user_id: int) -> str:
    """
    Get user's custom thumbnail path for ZIP creation.
    Downloads the thumbnail from file_id and returns the local path.
    Returns None if no custom thumbnail is set.
    """
    try:
        thumb_file_id = await roxybot_db.roxybot_get_thumbnail(user_id)
        
        if not thumb_file_id:
            return None
        
        # Download thumbnail to temp location
        thumb_path = await client.download_media(
            thumb_file_id,
            file_name=f"downloads/thumb_{user_id}.jpg"
        )
        
        return thumb_path
    except Exception as e:
        logger.error(f"❌ Error getting user thumbnail: {e}")
        return None


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
