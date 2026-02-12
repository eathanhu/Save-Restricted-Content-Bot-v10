# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_GROUP, OWNER_ID, FORCE_SUB
from utils.func import is_user_banned

async def check_banned(client, message):
    """Check if user is banned"""
    if await is_user_banned(message.from_user.id):
        await message.reply_text(
            "🚫 **You are banned from using this bot!**\n\n"
            "Contact @Franited to get unbanned."
        )
        return True
    return False

async def subscribe(app, message):
    # Check if user is banned first
    if await check_banned(app, message):
        return 1
        
    if FORCE_SUB:
        try:
          user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
          if str(user.status) == "ChatMemberStatus.BANNED":
              await message.reply_text("You are Banned. Contact -- Team SPY")
              return 1
        except UserNotParticipant:
            link = await app.export_chat_invite_link(FORCE_SUB)
            caption = f"Join our channel to use the bot"
            await message.reply_photo(photo="https://graph.org/file/d44f024a08ded19452152.jpg",caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now...", url=f"{link}")]]))
            return 1
        except Exception as ggn:
            await message.reply_text(f"Something Went Wrong. Contact admins... with following message {ggn}")
            return 1 
     
@app.on_message(filters.command("set"))
async def set(_, message):
    if await check_banned(_, message):
        return
        
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("clone", "📥 Clone messages from channel"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("setbot", "🧸 Add your bot for handling files"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("ban", "🚫 Ban a user"),
        BotCommand("unban", "✅ Unban a user"),
        BotCommand("unbanall", "✅ Unban all users"),
        BotCommand("rembot", "🤨 Remove your custom bot"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel login/batch/settings process"),
        BotCommand("stop", "🚫 Cancel batch process")
    ])
 
    await message.reply("✅ Commands configured successfully!")
 
 
 
 
help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "4. **/clone link or link-link**\n"
        "> Clone messages from public/private channels\n\n"
        "5. **/ban userID**\n"
        "> Ban a user (Owner only)\n\n"
        "6. **/unban userID**\n"
        "> Unban a user (Owner only)\n\n"
        "7. **/dl link**\n"
        "> Download videos (Not available in v3 if you are using)\n\n"
        "8. **/adl link**\n"
        "> Download audio (Not available in v3 if you are using)\n\n"
        "9. **/login**\n"
        "> Log into the bot for private channel access\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot\n\n"
        "11. **/stats**\n"
        "> Get bot stats\n\n"
        "12. **/plan**\n"
        "> Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "14. **/terms**\n"
        "> Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> Customize bot settings\n\n"
        "**__Powered by Team SPY__**"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")
 
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
    keyboard = InlineKeyboardMarkup([buttons])
 
    await message.delete()
 
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("help"))
async def help(client, message):
    if await check_banned(client, message):
        return
        
    join = await subscribe(client, message)
    if join == 1:
        return
     
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    await send_or_edit_help_page(client, callback_query.message, page_number)
     
    await callback_query.answer()

 
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    if await check_banned(client, message):
        return
        
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 
 
@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    if await check_banned(client, message):
        return
        
    plan_text = (
        "> 💰 **Premium Price**:\n\n Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰**Premium Price**\n\n Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms or click See Terms👇\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)


# Ban/Unban commands
@app.on_message(filters.command("ban") & filters.private)
async def ban_user_cmd(client, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply_text("❌ You don't have permission to use this command.")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: `/ban user_id` or `/ban @username`")
        return
    
    target = args[1]
    
    try:
        # Try to get user ID from username or ID
        if target.startswith('@'):
            user = await client.get_users(target)
            target_id = user.id
            target_name = user.first_name
        else:
            target_id = int(target)
            try:
                user = await client.get_users(target_id)
                target_name = user.first_name
            except:
                target_name = "Unknown"
        
        from utils.func import ban_user
        success = await ban_user(target_id, message.from_user.id)
        
        if success:
            await message.reply_text(f"✅ User {target_name} ({target_id}) has been banned.")
        else:
            await message.reply_text("❌ Failed to ban user.")
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


@app.on_message(filters.command("unban") & filters.private)
async def unban_user_cmd(client, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply_text("❌ You don't have permission to use this command.")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: `/unban user_id` or `/unban @username`")
        return
    
    target = args[1]
    
    try:
        if target.startswith('@'):
            user = await client.get_users(target)
            target_id = user.id
            target_name = user.first_name
        else:
            target_id = int(target)
            try:
                user = await client.get_users(target_id)
                target_name = user.first_name
            except:
                target_name = "Unknown"
        
        from utils.func import unban_user
        success = await unban_user(target_id)
        
        if success:
            await message.reply_text(f"✅ User {target_name} ({target_id}) has been unbanned.")
        else:
            await message.reply_text("❌ User was not banned.")
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


@app.on_message(filters.command("unbanall") & filters.private)
async def unban_all_cmd(client, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply_text("❌ You don't have permission to use this command.")
        return
    
    try:
        from utils.func import unban_all_users
        count = await unban_all_users()
        await message.reply_text(f"✅ Unbanned {count} users.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
