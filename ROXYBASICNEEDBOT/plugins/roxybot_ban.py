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
from config import RoxyBotConfig
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Ban/Unban Commands - Admin Only


def roxybot_is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    return user_id in admin_ids


@Client.on_message(filters.command("ban") & filters.private)
async def roxybot_ban_command(client: Client, message: Message):
    """Ban a user from using the bot - Admin only"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /ban")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user is admin
    if not roxybot_is_admin(user_id):
        await message.reply_text(
            "❌ **Aᴄᴄᴇꜱꜱ Dᴇɴɪᴇᴅ!**\n\n"
            "Tʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ғᴏʀ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Parse command: /ban <user_id> [reason]
    command_parts = message.text.split(maxsplit=2)
    
    if len(command_parts) < 2:
        await message.reply_text(
            "⚠️ **Uꜱᴀɢᴇ:**\n\n"
            "`/ban <user_id> [reason]`\n\n"
            "📝 **Exᴀᴍᴘʟᴇꜱ:**\n"
            "• `/ban 123456789`\n"
            "• `/ban 123456789 Spamming`\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Get target user ID
    try:
        target_user_id = int(command_parts[1])
    except ValueError:
        await message.reply_text(
            "❌ **Iɴᴠᴀʟɪᴅ Uꜱᴇʀ ID!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴜꜱᴇʀ ID.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Don't allow banning admins
    if roxybot_is_admin(target_user_id):
        await message.reply_text(
            "❌ **Cᴀɴɴᴏᴛ Bᴀɴ Aᴅᴍɪɴ!**\n\n"
            "Yᴏᴜ ᴄᴀɴɴᴏᴛ ʙᴀɴ ᴀɴᴏᴛʜᴇʀ ᴀᴅᴍɪɴ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Get ban reason if provided
    reason = command_parts[2] if len(command_parts) > 2 else "No reason provided"
    
    # Check if already banned
    is_banned = await roxybot_db.roxybot_is_banned(target_user_id)
    if is_banned:
        await message.reply_text(
            f"⚠️ **Aʟʀᴇᴀᴅʏ Bᴀɴɴᴇᴅ!**\n\n"
            f"Uꜱᴇʀ `{target_user_id}` ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Ban the user
    success = await roxybot_db.roxybot_ban_user(target_user_id, user_id, reason)
    
    if success:
        await message.reply_text(
            f"🚫 **Uꜱᴇʀ Bᴀɴɴᴇᴅ!**\n\n"
            f"<blockquote>🆔 **Uꜱᴇʀ ID:** `{target_user_id}`\n"
            f"📝 **Rᴇᴀꜱᴏɴ:** {reason}\n"
            f"👮 **Bᴀɴɴᴇᴅ Bʏ:** `{user_id}`\n"
            f"📅 **Dᴀᴛᴇ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</blockquote>\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        logger.info(f"✅ User {target_user_id} banned by admin {user_id}")
    else:
        await message.reply_text(
            "❌ **Fᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ ᴜꜱᴇʀ!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )


@Client.on_message(filters.command("unban") & filters.private)
async def roxybot_unban_command(client: Client, message: Message):
    """Unban a user - Admin only"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /unban")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user is admin
    if not roxybot_is_admin(user_id):
        await message.reply_text(
            "❌ **Aᴄᴄᴇꜱꜱ Dᴇɴɪᴇᴅ!**\n\n"
            "Tʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ғᴏʀ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Parse command: /unban <user_id>
    command_parts = message.text.split()
    
    if len(command_parts) < 2:
        await message.reply_text(
            "⚠️ **Uꜱᴀɢᴇ:**\n\n"
            "`/unban <user_id>`\n\n"
            "📝 **Exᴀᴍᴘʟᴇ:**\n"
            "• `/unban 123456789`\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Get target user ID
    try:
        target_user_id = int(command_parts[1])
    except ValueError:
        await message.reply_text(
            "❌ **Iɴᴠᴀʟɪᴅ Uꜱᴇʀ ID!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴜꜱᴇʀ ID.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Check if user is banned
    is_banned = await roxybot_db.roxybot_is_banned(target_user_id)
    if not is_banned:
        await message.reply_text(
            f"⚠️ **Nᴏᴛ Bᴀɴɴᴇᴅ!**\n\n"
            f"Uꜱᴇʀ `{target_user_id}` ɪꜱ ɴᴏᴛ ʙᴀɴɴᴇᴅ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Unban the user
    success = await roxybot_db.roxybot_unban_user(target_user_id)
    
    if success:
        # Clear the banned notification tracking so user can use bot again
        try:
            from ROXYBASICNEEDBOT.plugins.roxybot_start import roxybot_banned_notified
            roxybot_banned_notified.discard(target_user_id)
        except:
            pass
        
        await message.reply_text(
            f"✅ **Uꜱᴇʀ Uɴʙᴀɴɴᴇᴅ!**\n\n"
            f"<blockquote>🆔 **Uꜱᴇʀ ID:** `{target_user_id}`\n"
            f"👮 **Uɴʙᴀɴɴᴇᴅ Bʏ:** `{user_id}`\n"
            f"📅 **Dᴀᴛᴇ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</blockquote>\n\n"
            "<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>"
        )
        logger.info(f"✅ User {target_user_id} unbanned by admin {user_id}")
    else:
        await message.reply_text(
            "❌ **Fᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴜꜱᴇʀ!**\n\n"
            "Pʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Helper function to check ban status (for other modules to import)

async def roxybot_check_banned(client: Client, message: Message) -> bool:
    """
    Check if user is banned and send ban message if so.
    Returns True if user is banned, False otherwise.
    """
    user_id = message.from_user.id
    
    # Admins are never banned
    if roxybot_is_admin(user_id):
        return False
    
    is_banned = await roxybot_db.roxybot_is_banned(user_id)
    
    if is_banned:
        await message.reply_text(
            "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
            "Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n\n"
            "Iғ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴀᴅᴍɪɴ.\n\n"
            "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return True
    
    return False


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
