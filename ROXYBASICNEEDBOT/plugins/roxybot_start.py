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

from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatWriteForbidden, ChatIdInvalid, ChannelPrivate
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
from config import RoxyBotConfig
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Track notified users to avoid duplicate notifications
roxybot_notified_users = set()

# Track banned users who have been notified (to show message only once per session)
roxybot_banned_notified = set()


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Global Ban Check - Highest priority handler that stops all processing for banned users

@Client.on_message(filters.private, group=-1000)
async def roxybot_global_ban_check(client: Client, message: Message):
    """Global ban check - runs FIRST before any other handler"""
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    
    # Admins bypass all checks
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id in admin_ids:
        return  # Allow processing to continue
    
    # Check if banned and get ban info
    ban_info = await roxybot_db.roxybot_get_ban_info(user_id)
    
    if ban_info["is_banned"]:
        # Allow /start command to pass through - it will show ban message every time
        if message.text and message.text.strip().startswith("/start"):
            return  # Let the start handler show the ban message
        
        ban_reason = ban_info["reason"] or "No reason provided"
        
        # For all other messages, show ban message once per session then block
        if user_id not in roxybot_banned_notified:
            roxybot_banned_notified.add(user_id)
            await message.reply_text(
                "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
                "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n\n"
                f"📝 <b>Rᴇᴀꜱᴏɴ:</b> {ban_reason}\n\n"
                "Iғ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴀᴅᴍɪɴ.</blockquote>\n\n"
                "<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>"
            )
            
            # Send ban sticker if configured
            try:
                from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
                ban_sticker = RoxyBotImages.get_ban_sticker()
                if ban_sticker:
                    await message.reply_sticker(sticker=ban_sticker)
            except Exception as e:
                logger.warning(f"⚠️ Could not send ban sticker: {e}")
            
            logger.info(f"🚫 Banned user {user_id} tried to use the bot - blocked (Reason: {ban_reason})")
        
        # Stop propagation - no other handlers will process this message
        raise StopPropagation
    
    # Check Force Subscribe (for non-banned users)
    # Allow /start command to pass through - it will handle fsub check itself
    if message.text and message.text.strip().startswith("/start"):
        return  # Let the start handler check force sub
    
    # Check force subscribe for all other messages
    from ROXYBASICNEEDBOT.plugins.roxybot_forcesub import roxybot_check_force_sub, roxybot_send_force_sub_message
    fsub_result = await roxybot_check_force_sub(client, user_id)
    
    if not fsub_result["is_subscribed"]:
        # Show force sub message once per session
        if user_id not in roxybot_notified_users:
            roxybot_notified_users.add(user_id)
            await roxybot_send_force_sub_message(message, fsub_result["not_joined"])
            logger.info(f"🔒 User {user_id} not subscribed - showing force sub message")
        
        # Stop propagation - user must subscribe first
        raise StopPropagation


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Helper function to send log channel notification

async def roxybot_send_log(client: Client, message: str):
    """Send message to log channel"""
    log_channel = RoxyBotConfig.ROXYBOT_LOG_CHANNEL
    
    if not log_channel or log_channel == 0:
        logger.warning("⚠️ LOG_CHANNEL not configured")
        return False
    
    try:
        await client.send_message(
            chat_id=log_channel,
            text=message,
            disable_web_page_preview=True
        )
        return True
    except (ChatWriteForbidden, ChatIdInvalid, ChannelPrivate) as e:
        logger.error(f"❌ Cannot send to log channel: {type(e).__name__}")
    except Exception as e:
        logger.error(f"❌ Log channel error: {e}")
    return False


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Start Command Handler

@Client.on_message(filters.command("start") & filters.private)
async def roxybot_start_command(client: Client, message: Message):
    """Start command handler"""
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    first_name = message.from_user.first_name or "User"
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /start")
    logger.info(f"👤 User: {first_name} (@{username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"💬 Chat ID: {message.chat.id}")
    logger.info("=" * 50)
    
    # Check if user is banned (skip for admins)
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id not in admin_ids:
        ban_info = await roxybot_db.roxybot_get_ban_info(user_id)
        if ban_info["is_banned"]:
            ban_reason = ban_info["reason"] or "No reason provided"
            
            # Always show ban message with reason when banned user uses /start
            await message.reply_text(
                "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
                "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n\n"
                f"📝 <b>Rᴇᴀꜱᴏɴ:</b> {ban_reason}\n\n"
                "Iғ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴀᴅᴍɪɴ.</blockquote>\n\n"
                "<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>"
            )
            
            # Always send ban sticker when banned user uses /start
            try:
                from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
                ban_sticker = RoxyBotImages.get_ban_sticker()
                if ban_sticker:
                    await message.reply_sticker(sticker=ban_sticker)
            except Exception as e:
                logger.warning(f"⚠️ Could not send ban sticker: {e}")
            
            logger.info(f"🚫 Banned user {user_id} tried to use /start (Reason: {ban_reason})")
            return
    
    # Check Force Subscribe (skip for admins)
    if user_id not in admin_ids:
        from ROXYBASICNEEDBOT.plugins.roxybot_forcesub import roxybot_check_force_sub, roxybot_send_force_sub_message
        fsub_result = await roxybot_check_force_sub(client, user_id)
        if not fsub_result["is_subscribed"]:
            await roxybot_send_force_sub_message(message, fsub_result["not_joined"])
            logger.info(f"🔒 User {user_id} not subscribed to required channels")
            return
    
    # Check for share link download parameter
    command_parts = message.text.split()
    if len(command_parts) > 1:
        param = command_parts[1]
        if param.startswith("dl_"):
            # Handle share link download
            link_id = param[3:]  # Remove "dl_" prefix
            try:
                from ROXYBASICNEEDBOT.plugins.roxybot_sharelinks import roxybot_handle_share_download
                await roxybot_handle_share_download(client, message, link_id)
                return
            except Exception as e:
                logger.error(f"Error handling share link: {e}")
    
    # Check if user ALREADY EXISTS in database (proper tracking)
    existing_user = await roxybot_db.roxybot_get_user_stats(user_id)
    is_truly_new_user = existing_user is None
    
    # 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
    # Welcome message with bot features
    
    roxy_welcome_text = f"""
✨ <b>Hᴇʏ {first_name}, Wᴇʟᴄᴏᴍᴇ!</b>

📂 <b>Yᴏᴜʀ Uʟᴛɪᴍᴀᴛᴇ Zɪᴘ Mᴀᴋᴇʀ Bᴏᴛ!</b> ⚡

<blockquote>📦 <b>Wʜᴀᴛ I ᴄᴀɴ ᴅᴏ:</b>
• Cʀᴇᴀᴛᴇ ZIP ғɪʟᴇꜱ ғʀᴏᴍ ʏᴏᴜʀ ғɪʟᴇꜱ
• Pᴀꜱꜱᴡᴏʀᴅ-ᴘʀᴏᴛᴇᴄᴛᴇᴅ ZIPꜱ (AES-256)
• Sᴜᴘᴘᴏʀᴛ ᴘʜᴏᴛᴏꜱ, ᴠɪᴅᴇᴏꜱ, ᴅᴏᴄᴜᴍᴇɴᴛꜱ, ᴀᴜᴅɪᴏ
• Cᴜꜱᴛᴏᴍ ɴᴀᴍᴇ ʏᴏᴜʀ ZIP ғɪʟᴇꜱ
• Fᴀꜱᴛ & ᴇғғɪᴄɪᴇɴᴛ ᴄᴏᴍᴘʀᴇꜱꜱɪᴏɴ
• Bᴇᴀᴜᴛɪғᴜʟ ᴘʀᴏɢʀᴇꜱꜱ ᴛʀᴀᴄᴋɪɴɢ

👉 Uꜱᴇ /help ғᴏʀ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ & ᴄᴏᴍᴍᴀɴᴅꜱ</blockquote>

<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>
"""
    
    # Create inline keyboard
    roxy_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📱 Tᴇʟᴇɢʀᴀᴍ", url="https://t.me/roxybasicneedbot1"),
            InlineKeyboardButton("🌐 Wᴇʙꜱɪᴛᴇ", url="https://roxybasicneedbot.unaux.com/?i=1")
        ],
        [
            InlineKeyboardButton("📺 YᴏᴜTᴜʙᴇ", url="https://www.youtube.com/@roxybasicneedbot"),
            InlineKeyboardButton("📸 Iɴꜱᴛᴀɢʀᴀᴍ", url="https://www.instagram.com/roxybasicneedbot1")
        ],
        [
            InlineKeyboardButton("💼 Pᴏʀᴛғᴏʟɪᴏ", url="https://aratt.ai/@roxybasicneedbot")
        ]
    ])
    
    # Reply FIRST (Important for UX)
    try:
        logger.info(f"📤 Sending welcome message to user {user_id}...")
        
        # Try to send with image if configured (uses URL from RoxyBotImages)
        from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
        welcome_image = RoxyBotImages.get_welcome_image()
        
        if welcome_image:
            # Send photo with caption
            await message.reply_photo(
                photo=welcome_image,
                caption=roxy_welcome_text,
                reply_markup=roxy_keyboard
            )
        else:
            # Send text only
            await message.reply_text(
                text=roxy_welcome_text,
                reply_markup=roxy_keyboard,
                disable_web_page_preview=True
            )
        
        logger.info(f"✅ /start response sent successfully to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send welcome message to {user_id}: {type(e).__name__}: {e}")
        # Fallback to text only
        try:
            await message.reply_text(
                text=roxy_welcome_text,
                reply_markup=roxy_keyboard,
                disable_web_page_preview=True
            )
        except:
            pass
        return

    # Add user to database (After reply)
    try:
        await roxybot_db.roxybot_add_user(
            user_id=user_id,
            username=username,
            first_name=first_name
        )
        logger.info(f"✅ User {user_id} added/updated in database")
    except Exception as e:
        logger.error(f"⚠️ Failed to add user {user_id} to DB: {e}")
    
    # Send new user notification to log channel (only for TRULY new users from database check)
    if is_truly_new_user:
        roxybot_notified_users.add(user_id)
        
        # Get total users
        total_users = await roxybot_db.roxybot_get_total_users()
        
        new_user_msg = f"""
<b>👤 Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Bᴏᴛ</b>

<blockquote>📝 <b>Uꜱᴇʀ Dᴇᴛᴀɪʟꜱ:</b>
├ Nᴀᴍᴇ: {first_name}
├ Uꜱᴇʀɴᴀᴍᴇ: @{username}
├ Uꜱᴇʀ ID: <code>{user_id}</code>
└ Tɪᴍᴇ: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📊 <b>Tᴏᴛᴀʟ Uꜱᴇʀꜱ:</b> {total_users}</blockquote>

<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>
"""
        
        log_sent = await roxybot_send_log(client, new_user_msg)
        if log_sent:
            logger.info(f"✅ New user notification sent to log channel for user {user_id}")
        else:
            logger.warning(f"⚠️ Failed to send new user notification for {user_id}")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Help Command Handler

@Client.on_message(filters.command("help") & filters.private)
async def roxybot_help_command(client: Client, message: Message):
    """Help command handler"""
    user_id = message.from_user.id
    
    # Check if user is banned
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id not in admin_ids:
        is_banned = await roxybot_db.roxybot_is_banned(user_id)
        if is_banned:
            await message.reply_text(
                "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
                "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.</blockquote>\n\n"
                "<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>"
            )
            return
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /help")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    roxy_help_text = """
📚 <b>Rᴏxʏ Zɪᴘ Mᴀᴋᴇʀ Bᴏᴛ - Hᴇʟᴘ</b>

<blockquote>🎯 <b>Hᴏᴡ ᴛᴏ ᴜꜱᴇ:</b>
1️⃣ Sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇꜱ (ᴘʜᴏᴛᴏꜱ/ᴠɪᴅᴇᴏꜱ/ᴀᴜᴅɪᴏ/ᴅᴏᴄꜱ)
2️⃣ Uꜱᴇ /files ᴛᴏ ᴠɪᴇᴡ ǫᴜᴇᴜᴇ
3️⃣ Uꜱᴇ /create ᴏʀ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄʀᴇᴀᴛᴇ ZIP
4️⃣ Oᴘᴛɪᴏɴᴀʟʟʏ ᴀᴅᴅ ᴘᴀꜱꜱᴡᴏʀᴅ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ!</blockquote>

<blockquote>💡 <b>Cᴏᴍᴍᴀɴᴅꜱ:</b>
• /start - Sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
• /create - Cʀᴇᴀᴛᴇ ZIP ғʀᴏᴍ ᴄᴏʟʟᴇᴄᴛᴇᴅ ғɪʟᴇꜱ
• /files - Vɪᴇᴡ & ᴍᴀɴᴀɢᴇ ǫᴜᴇᴜᴇᴅ ғɪʟᴇꜱ
• /cancel - Cᴀɴᴄᴇʟ ᴄᴜʀʀᴇɴᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ
• /help - Sʜᴏᴡ ʜᴇʟᴘ ᴍᴇꜱꜱᴀɢᴇ
• /stats - Vɪᴇᴡ ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ</blockquote>

<blockquote>🖼️ <b>Tʜᴜᴍʙɴᴀɪʟ Cᴏᴍᴍᴀɴᴅꜱ:</b>
• /addthumb - Sᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ
• /delthumb - Rᴇᴍᴏᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ
• /viewthumb - Vɪᴇᴡ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ</blockquote>

<blockquote>🔐 <b>Pᴀꜱꜱᴡᴏʀᴅ Pʀᴏᴛᴇᴄᴛɪᴏɴ:</b>
Uꜱᴇ ᴛʜᴇ "Cʀᴇᴀᴛᴇ ᴡɪᴛʜ Pᴀꜱꜱᴡᴏʀᴅ" ʙᴜᴛᴛᴏɴ ғʀᴏᴍ /files
ᴛᴏ ᴄʀᴇᴀᴛᴇ AES-256 ᴇɴᴄʀʏᴘᴛᴇᴅ ZIP ᴀʀᴄʜɪᴠᴇꜱ!</blockquote>

<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>
"""
    
    try:
        # Check for help image from RoxyBotImages config
        from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
        help_image = RoxyBotImages.get_help_image()
        
        if help_image:
            await message.reply_photo(
                photo=help_image,
                caption=roxy_help_text
            )
        else:
            await message.reply_text(roxy_help_text)
            
        logger.info(f"✅ /help response sent to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send help message to {user_id}: {e}")
        # Fallback to text
        try:
            await message.reply_text(roxy_help_text)
        except:
            pass


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Stats Command Handler

@Client.on_message(filters.command("stats") & filters.private)
async def roxybot_stats_command(client: Client, message: Message):
    """Statistics command handler"""
    user_id = message.from_user.id
    
    # Check if user is banned
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id not in admin_ids:
        is_banned = await roxybot_db.roxybot_is_banned(user_id)
        if is_banned:
            await message.reply_text(
                "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
                "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.</blockquote>\n\n"
                "<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>"
            )
            return
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /stats")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Get user stats
    roxy_user_stats = await roxybot_db.roxybot_get_user_stats(user_id)
    roxy_total_users = await roxybot_db.roxybot_get_total_users()
    
    if roxy_user_stats:
        roxy_stats_text = f"""
📊 <b>Yᴏᴜʀ Sᴛᴀᴛɪꜱᴛɪᴄꜱ</b>

<blockquote>👤 <b>Uꜱᴇʀ:</b> {message.from_user.first_name}
🆔 <b>Uꜱᴇʀ ID:</b> <code>{user_id}</code>
📦 <b>Tᴏᴛᴀʟ ZIPꜱ Cʀᴇᴀᴛᴇᴅ:</b> {roxy_user_stats.get('zip_count', 0)}

🌍 <b>Gʟᴏʙᴀʟ Sᴛᴀᴛꜱ:</b>
👥 <b>Tᴏᴛᴀʟ Uꜱᴇʀꜱ:</b> {roxy_total_users}</blockquote>

<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>
"""
    else:
        roxy_stats_text = "❌ Uɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ. Pʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ!"
    
    try:
        # Check for stats image from RoxyBotImages config
        from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
        stats_image = RoxyBotImages.get_stats_image()
        
        if stats_image:
            await message.reply_photo(
                photo=stats_image,
                caption=roxy_stats_text
            )
        else:
            await message.reply_text(roxy_stats_text)
            
        logger.info(f"✅ /stats response sent to user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send stats message to {user_id}: {e}")
        # Fallback to text
        try:
            await message.reply_text(roxy_stats_text)
        except:
            pass


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Catch-all handler for debugging - logs ALL incoming messages
@Client.on_message(filters.private, group=-999)
async def roxybot_log_all_messages(client: Client, message: Message):
    """Log all incoming messages for debugging"""
    user_id = message.from_user.id if message.from_user else "Unknown"
    username = message.from_user.username if message.from_user else "Unknown"
    
    msg_type = "Unknown"
    if message.text:
        msg_type = f"Text: {message.text[:50]}..."
    elif message.photo:
        msg_type = "Photo"
    elif message.video:
        msg_type = "Video"
    elif message.document:
        msg_type = f"Document: {message.document.file_name}"
    elif message.sticker:
        msg_type = "Sticker"
    
    logger.info(f"📩 INCOMING MESSAGE | User: {user_id} (@{username}) | Type: {msg_type}")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
