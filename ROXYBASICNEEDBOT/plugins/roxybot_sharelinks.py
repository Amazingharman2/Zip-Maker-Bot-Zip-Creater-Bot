# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# Share Links Module - Generate temporary download links for ZIP files
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
import time
import secrets
import hashlib
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import RoxyBotConfig
import logging

logger = logging.getLogger(__name__)

# Store shared links: {link_id: {"file_id": str, "user_id": int, "expires": datetime, "downloads": int, "max_downloads": int}}
roxybot_shared_links = {}

# Link expiry options (in hours)
LINK_EXPIRY_OPTIONS = {
    "1h": 1,
    "6h": 6,
    "12h": 12,
    "24h": 24,
    "48h": 48,
    "7d": 168
}


def roxybot_generate_link_id(length: int = 12) -> str:
    """Generate a unique link ID"""
    return secrets.token_urlsafe(length)[:length]


def roxybot_cleanup_expired_links():
    """Remove expired links from memory"""
    now = datetime.now()
    expired = [link_id for link_id, data in roxybot_shared_links.items() 
               if data["expires"] < now]
    for link_id in expired:
        del roxybot_shared_links[link_id]
    return len(expired)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Share Link Command - Create shareable link for a file

@Client.on_message(filters.command("share") & filters.private)
async def roxybot_share_command(client: Client, message: Message):
    """Create a shareable link for a file - must reply to a file"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /share")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if replying to a file
    if not message.reply_to_message:
        await message.reply_text(
            "🔗 **Sʜᴀʀᴇ Lɪɴᴋ**\n\n"
            "**Uꜱᴀɢᴇ:** Rᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ ᴡɪᴛʜ /share\n\n"
            "Tʜɪꜱ ᴡɪʟʟ ᴄʀᴇᴀᴛᴇ ᴀ ᴛᴇᴍᴘᴏʀᴀʀʏ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n"
            "ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ꜱʜᴀʀᴇ ᴡɪᴛʜ ᴏᴛʜᴇʀꜱ!\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    reply_msg = message.reply_to_message
    
    # Get file_id from the message
    file_id = None
    file_name = "File"
    file_size = 0
    
    if reply_msg.document:
        file_id = reply_msg.document.file_id
        file_name = reply_msg.document.file_name or "Document"
        file_size = reply_msg.document.file_size
    elif reply_msg.video:
        file_id = reply_msg.video.file_id
        file_name = reply_msg.video.file_name or "Video"
        file_size = reply_msg.video.file_size
    elif reply_msg.audio:
        file_id = reply_msg.audio.file_id
        file_name = reply_msg.audio.file_name or "Audio"
        file_size = reply_msg.audio.file_size
    elif reply_msg.photo:
        file_id = reply_msg.photo.file_id
        file_name = "Photo.jpg"
        file_size = reply_msg.photo.file_size
    elif reply_msg.voice:
        file_id = reply_msg.voice.file_id
        file_name = "Voice.ogg"
        file_size = reply_msg.voice.file_size
    
    if not file_id:
        await message.reply_text(
            "❌ **Nᴏ ғɪʟᴇ ғᴏᴜɴᴅ!**\n\n"
            "Pʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ (ᴅᴏᴄᴜᴍᴇɴᴛ/ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ/ᴘʜᴏᴛᴏ)\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Show expiry options
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1 Hᴏᴜʀ", callback_data=f"roxybot_share_1h_{file_id[:50]}"),
            InlineKeyboardButton("6 Hᴏᴜʀꜱ", callback_data=f"roxybot_share_6h_{file_id[:50]}")
        ],
        [
            InlineKeyboardButton("12 Hᴏᴜʀꜱ", callback_data=f"roxybot_share_12h_{file_id[:50]}"),
            InlineKeyboardButton("24 Hᴏᴜʀꜱ", callback_data=f"roxybot_share_24h_{file_id[:50]}")
        ],
        [
            InlineKeyboardButton("48 Hᴏᴜʀꜱ", callback_data=f"roxybot_share_48h_{file_id[:50]}"),
            InlineKeyboardButton("7 Dᴀʏꜱ", callback_data=f"roxybot_share_7d_{file_id[:50]}")
        ],
        [
            InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="roxybot_share_cancel")
        ]
    ])
    
    # Store file info temporarily
    roxybot_shared_links[f"temp_{user_id}"] = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "message_id": reply_msg.id
    }
    
    # Format file size
    size_str = roxybot_format_size(file_size)
    
    await message.reply_text(
        f"🔗 **Cʀᴇᴀᴛᴇ Sʜᴀʀᴇ Lɪɴᴋ**\n\n"
        f"📁 **Fɪʟᴇ:** `{file_name}`\n"
        f"📊 **Sɪᴢᴇ:** {size_str}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"⏱️ **Sᴇʟᴇᴄᴛ Lɪɴᴋ Exᴘɪʀʏ Tɪᴍᴇ:**\n\n"
        f"⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**",
        reply_markup=keyboard
    )


def roxybot_format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


# Handle expiry selection
@Client.on_callback_query(filters.regex("^roxybot_share_"))
async def roxybot_share_callback(client: Client, callback_query: CallbackQuery):
    """Handle share link creation"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "roxybot_share_cancel":
        if f"temp_{user_id}" in roxybot_shared_links:
            del roxybot_shared_links[f"temp_{user_id}"]
        await callback_query.answer("❌ Cᴀɴᴄᴇʟʟᴇᴅ!")
        await callback_query.message.edit_text(
            "❌ **Sʜᴀʀᴇ Lɪɴᴋ Cᴀɴᴄᴇʟʟᴇᴅ**\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Parse expiry from callback data
    parts = data.split("_")
    if len(parts) < 3:
        return
    
    expiry_key = parts[2]  # e.g., "1h", "6h", etc.
    
    if expiry_key not in LINK_EXPIRY_OPTIONS:
        await callback_query.answer("❌ Iɴᴠᴀʟɪᴅ ᴏᴘᴛɪᴏɴ!", show_alert=True)
        return
    
    # Get temp file info
    temp_key = f"temp_{user_id}"
    if temp_key not in roxybot_shared_links:
        await callback_query.answer("❌ Sᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ! Uꜱᴇ /share ᴀɢᴀɪɴ.", show_alert=True)
        return
    
    file_info = roxybot_shared_links[temp_key]
    del roxybot_shared_links[temp_key]
    
    # Generate link
    link_id = roxybot_generate_link_id()
    expiry_hours = LINK_EXPIRY_OPTIONS[expiry_key]
    expires_at = datetime.now() + timedelta(hours=expiry_hours)
    
    # Store link data
    roxybot_shared_links[link_id] = {
        "file_id": file_info["file_id"],
        "file_name": file_info["file_name"],
        "file_size": file_info["file_size"],
        "user_id": user_id,
        "expires": expires_at,
        "downloads": 0,
        "max_downloads": 100,  # Limit downloads
        "created": datetime.now()
    }
    
    # Get bot username
    bot_me = await client.get_me()
    bot_username = bot_me.username
    
    # Create share link
    share_link = f"https://t.me/{bot_username}?start=dl_{link_id}"
    
    # Format expiry display
    if expiry_hours < 24:
        expiry_display = f"{expiry_hours} ʜᴏᴜʀ(ꜱ)"
    else:
        expiry_display = f"{expiry_hours // 24} ᴅᴀʏ(ꜱ)"
    
    await callback_query.answer("✅ Lɪɴᴋ ᴄʀᴇᴀᴛᴇᴅ!")
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Cᴏᴘʏ Lɪɴᴋ", url=share_link)
        ],
        [
            InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ Lɪɴᴋ", callback_data=f"roxybot_dellink_{link_id}")
        ]
    ])
    
    await callback_query.message.edit_text(
        f"✅ **Sʜᴀʀᴇ Lɪɴᴋ Cʀᴇᴀᴛᴇᴅ!**\n\n"
        f"📁 **Fɪʟᴇ:** `{file_info['file_name']}`\n"
        f"📊 **Sɪᴢᴇ:** {roxybot_format_size(file_info['file_size'])}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🔗 **Lɪɴᴋ:**\n`{share_link}`\n\n"
        f"⏱️ **Exᴘɪʀᴇꜱ ɪɴ:** {expiry_display}\n"
        f"📅 **Exᴘɪʀᴇꜱ ᴀᴛ:** {expires_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**",
        reply_markup=keyboard
    )
    
    logger.info(f"✅ Created share link {link_id} for user {user_id}, expires in {expiry_hours}h")


# Handle link deletion
@Client.on_callback_query(filters.regex("^roxybot_dellink_"))
async def roxybot_delete_link_callback(client: Client, callback_query: CallbackQuery):
    """Delete a share link"""
    user_id = callback_query.from_user.id
    link_id = callback_query.data.replace("roxybot_dellink_", "")
    
    if link_id in roxybot_shared_links:
        # Check ownership
        if roxybot_shared_links[link_id]["user_id"] != user_id:
            await callback_query.answer("❌ Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ʟɪɴᴋꜱ!", show_alert=True)
            return
        
        del roxybot_shared_links[link_id]
        await callback_query.answer("✅ Lɪɴᴋ ᴅᴇʟᴇᴛᴇᴅ!")
        await callback_query.message.edit_text(
            "🗑️ **Sʜᴀʀᴇ Lɪɴᴋ Dᴇʟᴇᴛᴇᴅ**\n\n"
            "Tʜᴇ ʟɪɴᴋ ɪꜱ ɴᴏ ʟᴏɴɢᴇʀ ᴀᴄᴛɪᴠᴇ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.info(f"✅ User {user_id} deleted share link {link_id}")
    else:
        await callback_query.answer("❌ Lɪɴᴋ ɴᴏᴛ ғᴏᴜɴᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ!", show_alert=True)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# View my links command

@Client.on_message(filters.command("mylinks") & filters.private)
async def roxybot_mylinks_command(client: Client, message: Message):
    """Show all active share links for user"""
    user_id = message.from_user.id
    
    # Cleanup expired first
    roxybot_cleanup_expired_links()
    
    # Get user's links
    user_links = {lid: data for lid, data in roxybot_shared_links.items() 
                  if isinstance(data, dict) and data.get("user_id") == user_id}
    
    if not user_links:
        await message.reply_text(
            "🔗 **Mʏ Sʜᴀʀᴇ Lɪɴᴋꜱ**\n\n"
            "❌ Nᴏ ᴀᴄᴛɪᴠᴇ ꜱʜᴀʀᴇ ʟɪɴᴋꜱ!\n\n"
            "Uꜱᴇ /share ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ʟɪɴᴋ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    bot_me = await client.get_me()
    bot_username = bot_me.username
    
    text = "🔗 **Mʏ Aᴄᴛɪᴠᴇ Sʜᴀʀᴇ Lɪɴᴋꜱ**\n\n"
    text += f"📊 **Tᴏᴛᴀʟ:** {len(user_links)}\n\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, (link_id, data) in enumerate(user_links.items(), 1):
        expires_in = data["expires"] - datetime.now()
        hours_left = int(expires_in.total_seconds() / 3600)
        
        text += f"{i}. 📁 `{data['file_name'][:20]}...`\n"
        text += f"   ⏱️ Exᴘɪʀᴇꜱ ɪɴ: {hours_left}ʜ\n"
        text += f"   📥 Dᴏᴡɴʟᴏᴀᴅꜱ: {data['downloads']}\n"
        text += f"   🔗 `t.me/{bot_username}?start=dl_{link_id}`\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━\n"
    text += "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
    
    await message.reply_text(text)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Handle download from share link (called from start command)

async def roxybot_handle_share_download(client: Client, message: Message, link_id: str):
    """Handle file download from share link"""
    user_id = message.from_user.id
    
    # Cleanup expired links
    roxybot_cleanup_expired_links()
    
    if link_id not in roxybot_shared_links:
        await message.reply_text(
            "❌ **Lɪɴᴋ Nᴏᴛ Fᴏᴜɴᴅ!**\n\n"
            "Tʜɪꜱ ʟɪɴᴋ ᴍᴀʏ ʜᴀᴠᴇ ᴇxᴘɪʀᴇᴅ ᴏʀ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    link_data = roxybot_shared_links[link_id]
    
    # Check if expired
    if datetime.now() > link_data["expires"]:
        del roxybot_shared_links[link_id]
        await message.reply_text(
            "❌ **Lɪɴᴋ Exᴘɪʀᴇᴅ!**\n\n"
            "Tʜɪꜱ ꜱʜᴀʀᴇ ʟɪɴᴋ ʜᴀꜱ ᴇxᴘɪʀᴇᴅ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Check download limit
    if link_data["downloads"] >= link_data["max_downloads"]:
        await message.reply_text(
            "❌ **Dᴏᴡɴʟᴏᴀᴅ Lɪᴍɪᴛ Rᴇᴀᴄʜᴇᴅ!**\n\n"
            "Tʜɪꜱ ʟɪɴᴋ ʜᴀꜱ ʀᴇᴀᴄʜᴇᴅ ɪᴛꜱ ᴍᴀxɪᴍᴜᴍ ᴅᴏᴡɴʟᴏᴀᴅꜱ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Send file
    status_msg = await message.reply_text(
        "📥 **Pʀᴇᴘᴀʀɪɴɢ Dᴏᴡɴʟᴏᴀᴅ...**\n\n"
        f"📁 `{link_data['file_name']}`\n\n"
        "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
    )
    
    try:
        await client.send_document(
            chat_id=user_id,
            document=link_data["file_id"],
            caption=(
                f"📁 **{link_data['file_name']}**\n\n"
                f"📊 **Sɪᴢᴇ:** {roxybot_format_size(link_data['file_size'])}\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚡ Sʜᴀʀᴇᴅ ᴠɪᴀ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
            )
        )
        
        # Increment download count
        roxybot_shared_links[link_id]["downloads"] += 1
        
        await status_msg.delete()
        logger.info(f"✅ User {user_id} downloaded file from link {link_id}")
        
    except Exception as e:
        logger.error(f"❌ Error sending shared file: {e}")
        await status_msg.edit_text(
            f"❌ **Eʀʀᴏʀ ꜱᴇɴᴅɪɴɢ ғɪʟᴇ!**\n\n{str(e)}\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
