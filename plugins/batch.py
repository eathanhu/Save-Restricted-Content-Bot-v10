# Clone command handler
import signal
import sys
# Add signal handler for graceful shutdown
def signal_handler(sig, frame):
    print('\n⚠️ Interrupt received, cleaning up...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
@X.on_message(filters.command('clone'))
async def clone_cmd(c, m):
    uid = m.from_user.id
    
    # Check if banned
    from utils.func import is_user_banned
    if await is_user_banned(uid):
        await m.reply_text(
            "🚫 **You are banned from using this bot!**\n\n"
            "Contact @Franited to get unbanned."
        )
        return
    
    if await sub(c, m) == 1:
        return
    
    # Parse command
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        await m.reply_text(
            "**Usage:**\n"
            "• Single: `/clone https://t.me/channel/123`\n"
            "• Batch: `/clone https://t.me/channel/123-456`"
        )
        return
    
    link = args[1].strip()
    
    # Parse link
    if '-' in link.split('/')[-1]:
        # Batch clone
        base_link = link.rsplit('/', 1)[0]
        msg_range = link.rsplit('/', 1)[1]
        
        try:
            start_msg, end_msg = map(int, msg_range.split('-'))
        except:
            await m.reply_text("❌ Invalid link format. Use: `https://t.me/channel/start-end`")
            return
        
        count = end_msg - start_msg + 1
        
        # Check limits
        from config import CLONE_LIMIT_FREE, CLONE_LIMIT_PREMIUM, CLONE_LIMIT_PRIVATE_FREE, CLONE_LIMIT_PRIVATE_PREMIUM, OWNER_ID
        
        is_owner = uid in OWNER_ID
        is_premium = await is_premium_user(uid)
        
        # Extract channel info
        i, _, lt = E(f"{base_link}/{start_msg}")
        
        if not is_owner:
            if lt == 'private':
                max_limit = CLONE_LIMIT_PRIVATE_PREMIUM if is_premium else CLONE_LIMIT_PRIVATE_FREE
            else:
                max_limit = CLONE_LIMIT_PREMIUM if is_premium else CLONE_LIMIT_FREE
            
            if count > max_limit:
                await m.reply_text(
                    f"❌ Your limit is {max_limit} files.\n"
                    f"Requested: {count} files"
                )
                return
        
        # Start cloning
        await clone_batch(c, m, base_link, start_msg, end_msg, uid, i, lt)
    else:
        # Single clone
        await clone_single(c, m, link, uid)


async def clone_single(c, m, link, uid):
    """Clone single message"""
    i, msg_id, lt = E(link)
    
    if not i or not msg_id:
        await m.reply_text("❌ Invalid link format.")
        return
    
    pt = await m.reply_text("🔄 Cloning...")
    
    try:
        # Check if private channel
        if lt == 'private':
            uc = await get_uclient(uid)
            if not uc:
                await pt.edit(
                    "❌ This is a private channel.\n\n"
                    "Please use /login to access private channels."
                )
                return
            
            # Download and upload
            ubot = await get_ubot(uid)
            if not ubot:
                await pt.edit('Add bot with /setbot first')
                return
            
            msg = await get_msg(ubot, uc, i, msg_id, lt)
            if not msg:
                await pt.edit("❌ Message not found or inaccessible.")
                return
            
            # Process message (download/upload)
            res = await process_msg(ubot, uc, msg, str(m.chat.id), lt, uid, i)
            await pt.edit(f"✅ {res}")
        else:
            # Public channel - direct copy
            try:
                await c.copy_message(
                    chat_id=m.chat.id,
                    from_chat_id=i,
                    message_id=msg_id
                )
                await pt.edit("✅ Message cloned successfully!")
            except Exception as e:
                await pt.edit(f"❌ Error: {str(e)[:100]}")
    except Exception as e:
        await pt.edit(f"❌ Error: {str(e)[:100]}")


async def clone_batch(c, m, base_link, start_msg, end_msg, uid, channel_id, link_type):
    """Clone multiple messages"""
    from config import OWNER_ID
    
    count = end_msg - start_msg + 1
    success = 0
    failed = 0
    
    pt = await m.reply_text(f"🔄 Cloning {count} messages...")
    
    # Check if private
    is_private = link_type == 'private'
    
    if is_private:
        uc = await get_uclient(uid)
        if not uc:
            await pt.edit(
                "❌ This is a private channel.\n\n"
                "Please use /login to access private channels."
            )
            return
        
        ubot = await get_ubot(uid)
        if not ubot:
            await pt.edit('Add bot with /setbot first')
            return
    
    for msg_num in range(start_msg, end_msg + 1):
        try:
            if is_private:
                # Download and upload for private
                msg = await get_msg(ubot, uc, channel_id, msg_num, link_type)
                if msg:
                    res = await process_msg(ubot, uc, msg, str(m.chat.id), link_type, uid, channel_id)
                    if 'Done' in res or 'Sent' in res:
                        success += 1
                    else:
                        failed += 1
                else:
                    failed += 1
            else:
                # Public - direct copy
                try:
                    await c.copy_message(
                        chat_id=m.chat.id,
                        from_chat_id=channel_id,
                        message_id=msg_num
                    )
                    success += 1
                except Exception as copy_error:
                    failed += 1
                    print(f"Failed to copy message {msg_num}: {copy_error}")
            
            # Update progress every 5 messages
            if (msg_num - start_msg + 1) % 5 == 0:
                await pt.edit(
                    f"🔄 Progress: {msg_num - start_msg + 1}/{count}\n"
                    f"✅ Success: {success}\n"
                    f"❌ Failed: {failed}"
                )
            
            # Delay to avoid flood
            await asyncio.sleep(2 if is_private else 1)
            
        except Exception as e:
            failed += 1
            print(f"Error cloning message {msg_num}: {e}")
    
    # Final summary
    await pt.edit(
        f"✅ **Clone Complete!**\n\n"
        f"📊 Total: {count}\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}"
    )

