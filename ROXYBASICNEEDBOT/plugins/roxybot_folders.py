# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# Folder Structure Module - Preserve folder hierarchy from file captions
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ROXYBASICNEEDBOT.plugins.roxybot_filehandler import roxybot_user_files
from config import RoxyBotConfig
import logging

logger = logging.getLogger(__name__)

# Store folder structure: {user_id: {file_path: folder_path}}
roxybot_folder_structure = {}

# Store folder mode status: {user_id: True/False}
roxybot_folder_mode = {}


def roxybot_sanitize_folder_name(name: str) -> str:
    """Sanitize folder name to be valid"""
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    # Limit length
    return name[:50] if name else "Folder"


def roxybot_parse_folder_from_caption(caption: str) -> str:
    """
    Parse folder path from caption.
    Supports formats:
    - /folder/subfolder/filename
    - folder/subfolder/filename
    - [Folder] filename
    - {Folder} filename
    """
    if not caption:
        return ""
    
    caption = caption.strip()
    
    # Format: /folder/subfolder/filename or folder/subfolder/
    if '/' in caption:
        parts = caption.split('/')
        # If last part looks like a filename (has extension), use path before it
        if len(parts) > 1:
            if '.' in parts[-1]:
                folder_path = '/'.join(parts[:-1])
            else:
                folder_path = caption
            return folder_path.strip('/')
    
    # Format: [Folder] filename or [Folder/Subfolder]
    bracket_match = re.match(r'\[([^\]]+)\]', caption)
    if bracket_match:
        return bracket_match.group(1).strip()
    
    # Format: {Folder} filename or {Folder/Subfolder}
    brace_match = re.match(r'\{([^}]+)\}', caption)
    if brace_match:
        return brace_match.group(1).strip()
    
    return ""


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Folder Mode Commands

@Client.on_message(filters.command("folder") & filters.private)
async def roxybot_folder_command(client: Client, message: Message):
    """Toggle folder structure mode or set folder for files"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /folder")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user provided folder name
    command_parts = message.text.split(maxsplit=1)
    
    if len(command_parts) > 1:
        # User specified a folder name
        folder_name = roxybot_sanitize_folder_name(command_parts[1])
        
        if user_id not in roxybot_folder_structure:
            roxybot_folder_structure[user_id] = {}
        
        # Set current folder
        roxybot_folder_structure[user_id]["_current"] = folder_name
        roxybot_folder_mode[user_id] = True
        
        await message.reply_text(
            f"📁 **Fᴏʟᴅᴇʀ Sᴇᴛ:** `{folder_name}`\n\n"
            f"Aʟʟ ғɪʟᴇꜱ ʏᴏᴜ ꜱᴇɴᴅ ɴᴏᴡ ᴡɪʟʟ ʙᴇ ᴘʟᴀᴄᴇᴅ ɪɴ:\n"
            f"`{folder_name}/`\n\n"
            f"Uꜱᴇ /folder ᴀɢᴀɪɴ ᴛᴏ ꜱᴇᴇ ᴏᴘᴛɪᴏɴꜱ.\n\n"
            f"⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
        )
        return
    
    # Show folder options
    current_folder = roxybot_folder_structure.get(user_id, {}).get("_current", "")
    is_enabled = roxybot_folder_mode.get(user_id, False)
    
    status_emoji = "✅" if is_enabled else "❌"
    status_text = "Eɴᴀʙʟᴇᴅ" if is_enabled else "Dɪꜱᴀʙʟᴇᴅ"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Eɴᴀʙʟᴇ" if not is_enabled else "❌ Dɪꜱᴀʙʟᴇ", 
                callback_data="roxybot_folder_toggle"
            )
        ],
        [
            InlineKeyboardButton("📂 Vɪᴇᴡ Sᴛʀᴜᴄᴛᴜʀᴇ", callback_data="roxybot_folder_view"),
            InlineKeyboardButton("🗑️ Cʟᴇᴀʀ Aʟʟ", callback_data="roxybot_folder_clear")
        ],
        [
            InlineKeyboardButton("❓ Hᴏᴡ ᴛᴏ Uꜱᴇ", callback_data="roxybot_folder_help")
        ]
    ])
    
    text = f"""
📁 **Fᴏʟᴅᴇʀ Sᴛʀᴜᴄᴛᴜʀᴇ Mᴏᴅᴇ**

{status_emoji} **Sᴛᴀᴛᴜꜱ:** {status_text}
"""
    
    if current_folder:
        text += f"📂 **Cᴜʀʀᴇɴᴛ Fᴏʟᴅᴇʀ:** `{current_folder}/`\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━

Wɪᴛʜ ғᴏʟᴅᴇʀ ᴍᴏᴅᴇ, ʏᴏᴜʀ ZIP ᴡɪʟʟ
ᴘʀᴇꜱᴇʀᴠᴇ ғᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ!

━━━━━━━━━━━━━━━━━━
⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**
"""
    
    await message.reply_text(text, reply_markup=keyboard)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Folder callback handlers

@Client.on_callback_query(filters.regex("^roxybot_folder_"))
async def roxybot_folder_callback(client: Client, callback_query: CallbackQuery):
    """Handle folder structure callbacks"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "roxybot_folder_toggle":
        # Toggle folder mode
        current = roxybot_folder_mode.get(user_id, False)
        roxybot_folder_mode[user_id] = not current
        
        if roxybot_folder_mode[user_id]:
            await callback_query.answer("✅ Fᴏʟᴅᴇʀ ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ!")
        else:
            await callback_query.answer("❌ Fᴏʟᴅᴇʀ ᴍᴏᴅᴇ ᴅɪꜱᴀʙʟᴇᴅ!")
        
        # Refresh message
        await roxybot_refresh_folder_menu(callback_query)
        
    elif data == "roxybot_folder_view":
        await callback_query.answer("📂 Vɪᴇᴡɪɴɢ...")
        await roxybot_show_folder_structure(callback_query)
        
    elif data == "roxybot_folder_clear":
        if user_id in roxybot_folder_structure:
            roxybot_folder_structure[user_id] = {}
        await callback_query.answer("🗑️ Fᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ ᴄʟᴇᴀʀᴇᴅ!")
        await roxybot_refresh_folder_menu(callback_query)
        
    elif data == "roxybot_folder_help":
        await callback_query.answer("❓ Sʜᴏᴡɪɴɢ ʜᴇʟᴘ...")
        await roxybot_show_folder_help(callback_query)
        
    elif data == "roxybot_folder_back":
        await callback_query.answer("🔙 Bᴀᴄᴋ...")
        await roxybot_refresh_folder_menu(callback_query)


async def roxybot_refresh_folder_menu(callback_query: CallbackQuery):
    """Refresh the folder menu"""
    user_id = callback_query.from_user.id
    
    current_folder = roxybot_folder_structure.get(user_id, {}).get("_current", "")
    is_enabled = roxybot_folder_mode.get(user_id, False)
    
    status_emoji = "✅" if is_enabled else "❌"
    status_text = "Eɴᴀʙʟᴇᴅ" if is_enabled else "Dɪꜱᴀʙʟᴇᴅ"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Eɴᴀʙʟᴇ" if not is_enabled else "❌ Dɪꜱᴀʙʟᴇ", 
                callback_data="roxybot_folder_toggle"
            )
        ],
        [
            InlineKeyboardButton("📂 Vɪᴇᴡ Sᴛʀᴜᴄᴛᴜʀᴇ", callback_data="roxybot_folder_view"),
            InlineKeyboardButton("🗑️ Cʟᴇᴀʀ Aʟʟ", callback_data="roxybot_folder_clear")
        ],
        [
            InlineKeyboardButton("❓ Hᴏᴡ ᴛᴏ Uꜱᴇ", callback_data="roxybot_folder_help")
        ]
    ])
    
    text = f"""
📁 **Fᴏʟᴅᴇʀ Sᴛʀᴜᴄᴛᴜʀᴇ Mᴏᴅᴇ**

{status_emoji} **Sᴛᴀᴛᴜꜱ:** {status_text}
"""
    
    if current_folder:
        text += f"📂 **Cᴜʀʀᴇɴᴛ Fᴏʟᴅᴇʀ:** `{current_folder}/`\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━

Wɪᴛʜ ғᴏʟᴅᴇʀ ᴍᴏᴅᴇ, ʏᴏᴜʀ ZIP ᴡɪʟʟ
ᴘʀᴇꜱᴇʀᴠᴇ ғᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ!

━━━━━━━━━━━━━━━━━━
⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**
"""
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)


async def roxybot_show_folder_structure(callback_query: CallbackQuery):
    """Show current folder structure"""
    user_id = callback_query.from_user.id
    
    structure = roxybot_folder_structure.get(user_id, {})
    
    if not structure or (len(structure) == 1 and "_current" in structure):
        text = """
📂 **Fᴏʟᴅᴇʀ Sᴛʀᴜᴄᴛᴜʀᴇ**

━━━━━━━━━━━━━━━━━━

❌ Nᴏ ғᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ ʏᴇᴛ!

Sᴇɴᴅ ғɪʟᴇꜱ ᴡɪᴛʜ ᴄᴀᴘᴛɪᴏɴꜱ ʟɪᴋᴇ:
• `[Photos] image.jpg`
• `/Documents/Work/file.pdf`

━━━━━━━━━━━━━━━━━━
⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**
"""
    else:
        text = "📂 **Fᴏʟᴅᴇʀ Sᴛʀᴜᴄᴛᴜʀᴇ**\n\n"
        text += "━━━━━━━━━━━━━━━━━━\n\n"
        
        # Build folder tree
        folders = {}
        for file_path, folder in structure.items():
            if file_path == "_current":
                continue
            if folder not in folders:
                folders[folder] = []
            file_name = os.path.basename(file_path)
            folders[folder].append(file_name)
        
        for folder, files in folders.items():
            text += f"📁 **{folder}/**\n"
            for f in files[:5]:  # Show max 5 files
                text += f"   └ `{f[:25]}...`\n" if len(f) > 25 else f"   └ `{f}`\n"
            if len(files) > 5:
                text += f"   └ ... ᴀɴᴅ {len(files) - 5} ᴍᴏʀᴇ\n"
            text += "\n"
        
        text += "━━━━━━━━━━━━━━━━━━\n"
        text += "⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="roxybot_folder_back")
        ]
    ])
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)


async def roxybot_show_folder_help(callback_query: CallbackQuery):
    """Show folder mode help"""
    help_text = """
❓ **Hᴏᴡ ᴛᴏ Uꜱᴇ Fᴏʟᴅᴇʀ Mᴏᴅᴇ**

━━━━━━━━━━━━━━━━━━

**Mᴇᴛʜᴏᴅ 1:** Cᴏᴍᴍᴀɴᴅ
```
/folder Photos
```
Aʟʟ ғɪʟᴇꜱ ᴡɪʟʟ ɢᴏ ᴛᴏ `Photos/`

**Mᴇᴛʜᴏᴅ 2:** Cᴀᴘᴛɪᴏɴ
Sᴇɴᴅ ғɪʟᴇ ᴡɪᴛʜ ᴄᴀᴘᴛɪᴏɴ:
• `[Photos] sunset.jpg`
• `{Documents} report.pdf`
• `/Work/Projects/file.txt`

**Mᴇᴛʜᴏᴅ 3:** Sᴜʙғᴏʟᴅᴇʀꜱ
```
/folder Photos/Summer
```
Fɪʟᴇꜱ ɢᴏ ᴛᴏ `Photos/Summer/`

━━━━━━━━━━━━━━━━━━

📦 Wʜᴇɴ ʏᴏᴜ ᴄʀᴇᴀᴛᴇ ZIP, ᴛʜᴇ
ғᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ ɪꜱ ᴘʀᴇꜱᴇʀᴠᴇᴅ!

━━━━━━━━━━━━━━━━━━
⚡ **RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ**
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="roxybot_folder_back")
        ]
    ])
    
    await callback_query.message.edit_text(help_text, reply_markup=keyboard)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Function to get folder for a file (used by filehandler)

def roxybot_get_file_folder(user_id: int, file_path: str, caption: str = None) -> str:
    """
    Get folder path for a file.
    Priority:
    1. Folder from caption
    2. Current folder set by /folder command
    3. Empty (root)
    """
    if not roxybot_folder_mode.get(user_id, False):
        return ""
    
    # Try to parse from caption
    if caption:
        folder = roxybot_parse_folder_from_caption(caption)
        if folder:
            # Store the mapping
            if user_id not in roxybot_folder_structure:
                roxybot_folder_structure[user_id] = {}
            roxybot_folder_structure[user_id][file_path] = folder
            return folder
    
    # Use current folder
    current = roxybot_folder_structure.get(user_id, {}).get("_current", "")
    if current:
        if user_id not in roxybot_folder_structure:
            roxybot_folder_structure[user_id] = {}
        roxybot_folder_structure[user_id][file_path] = current
    
    return current


def roxybot_get_folder_structure(user_id: int) -> dict:
    """Get the folder structure for a user (file_path: folder_path)"""
    structure = roxybot_folder_structure.get(user_id, {})
    # Remove _current key
    return {k: v for k, v in structure.items() if k != "_current"}


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
