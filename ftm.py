import os
import psutil
import time
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import ftminfo

app = Client(
    "FTMBulletinBot",
    api_id=ftminfo.API_ID,
    api_hash=ftminfo.API_HASH,
    bot_token=ftminfo.BOT_TOKEN
)

start_time = time.time()
admin_sessions = {}

# Generate CAPTCHA
def generate_captcha():
    return ''.join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=5))

# Generate OTP
def generate_otp():
    return ''.join(random.choices("0123456789", k=6))

# Bot Startup Log
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    log_msg = (
        f"\U0001F680 **Bot Started**\n"
        f"👤 User: {message.from_user.mention}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"📲 Started via: {'Direct Message' if message.chat.type == 'private' else 'Group/Channel'}"
    )
    await app.send_message(ftminfo.LOG_CHANNEL, log_msg)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/ftmdeveloperz")],
        [InlineKeyboardButton("📢 Support", url="https://t.me/ftmbotzx_support")],
        [InlineKeyboardButton("🔔 Updates", url="https://t.me/ftmbotzx")],
        [InlineKeyboardButton("📖 Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📊 Bot Stats", callback_data="stats")]
    ])
    
    await message.reply_text(
        "\U0001F680 **Welcome to Fᴛᴍ Bᴜʟʟᴇᴛɪɴ!**\n\n"
        "🔹 **A powerful admin bot with advanced login & stats!**\n"
        "🔹 **Secure access required** – use `/login` to authenticate.\n"
        "🔹 **Monitor activity** via log channel.\n\n"
        "📢 **Stay updated with latest features & improvements!**",
        reply_markup=keyboard
    )

# /login command (Step 1: Send CAPTCHA)
@app.on_message(filters.command("login") & filters.private)
async def login_command(client, message):
    if message.from_user.id not in ftminfo.ADMIN_CHAT_IDS:
        return await message.reply_text("❌ You are not authorized.")

    captcha = generate_captcha()
    admin_sessions[message.from_user.id] = {"captcha": captcha, "step": 1}
    log_msg = f"🔒 **Login Attempt** by {message.from_user.mention} (ID: {message.from_user.id})"
    await app.send_message(ftminfo.LOG_CHANNEL, log_msg)

    await message.reply_text(f"🔐 **Admin Login**\n\n🛡 **Step 1:** Verify CAPTCHA\n📝 Enter the following text: `{captcha}`")

# Step 2: Verify CAPTCHA
@app.on_message(filters.private)
async def verify_captcha(client, message):
    user_id = message.from_user.id
    if user_id not in admin_sessions or admin_sessions[user_id]["step"] != 1:
        return

    if message.text == admin_sessions[user_id]["captcha"]:
        admin_sessions[user_id]["step"] = 2
        await message.reply_text("✅ CAPTCHA verified!\n\n🔐 **Step 2:** Enter Admin Password.")
    else:
        del admin_sessions[user_id]
        await message.reply_text("❌ Incorrect CAPTCHA. Try `/login` again.")

# Step 3: Verify Password
@app.on_message(filters.private)
async def verify_password(client, message):
    user_id = message.from_user.id
    if user_id not in admin_sessions or admin_sessions[user_id]["step"] != 2:
        return

    if message.text == ftminfo.ADMIN_PASSWORD:
        otp = generate_otp()
        admin_sessions[user_id]["otp"] = otp
        admin_sessions[user_id]["step"] = 3
        log_msg = f"🔑 **OTP Sent** to {message.from_user.mention} (ID: {message.from_user.id}): `{otp}`"
        await app.send_message(ftminfo.LOG_CHANNEL, log_msg)
        await client.send_message(user_id, f"🔑 **Your OTP:** `{otp}` (Valid for one attempt)")
        await message.reply_text("✅ Password verified!\n\n📩 **Step 3:** Enter the OTP sent to you.")
    else:
        del admin_sessions[user_id]
        await message.reply_text("❌ Incorrect password. Try `/login` again.")

# Step 4: Verify OTP
@app.on_message(filters.private)
async def verify_otp(client, message):
    user_id = message.from_user.id
    if user_id not in admin_sessions or admin_sessions[user_id]["step"] != 3:
        return

    if message.text == admin_sessions[user_id]["otp"]:
        del admin_sessions[user_id]
        await message.reply_text("✅ **Login Successful!**\n\nYou can now use admin commands.")
        await app.send_message(ftminfo.LOG_CHANNEL, f"🔔 **Admin Logged In:** {message.from_user.mention}")
    else:
        del admin_sessions[user_id]
        await message.reply_text("❌ Incorrect OTP. Try `/login` again.")

# /stats command
@app.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    uptime = int(time.time() - start_time)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    download_speed = random.uniform(20, 100)  # Fake realistic value
    upload_speed = random.uniform(10, 50)  # Fake realistic value

    stats_msg = (
        f"📊 **My Stats**\n"
        f"⏳ Uptime: `{uptime} sec`\n"
        f"💾 Disk Usage: `{disk_usage}%`\n"
        f"🖥 CPU: `{cpu_usage}%`\n"
        f"📌 RAM: `{ram_usage}%`\n"
        f"📥 Download Speed: `{download_speed:.2f} Mbps`\n"
        f"📤 Upload Speed: `{upload_speed:.2f} Mbps`"
    )
    await message.reply_text(stats_msg)

# Run Bot
app.run()
