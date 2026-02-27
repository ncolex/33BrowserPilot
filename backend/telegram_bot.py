"""
Telegram Bot Integration for BrowserPilot
- Job completion notifications
- Remote control commands
- Keepalive alerts
"""
import os
import asyncio
from typing import Optional
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot: Optional[Bot] = None
        self.app = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize bot"""
        if not self.token or not self.chat_id:
            print("⚠️ Telegram not configured (missing TOKEN or CHAT_ID)")
            return
        
        try:
            self.bot = Bot(token=self.token)
            await self.bot.get_me()
            self._initialized = True
            print(f"✅ Telegram bot initialized: @{self.bot.username}")
        except Exception as e:
            print(f"❌ Telegram init failed: {e}")
            self._initialized = False
    
    async def send_message(self, message: str, parse_mode: str = "HTML"):
        """Send message to configured chat"""
        if not self._initialized:
            return
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
    
    async def notify_job_started(self, job_id: str, prompt: str, format: str):
        """Notify when a job starts"""
        message = (
            "🚀 <b>Job Started</b>\n\n"
            f"<b>ID:</b> <code>{job_id}</code>\n"
            f"<b>Task:</b> {prompt[:200]}\n"
            f"<b>Format:</b> {format}\n\n"
            "⏳ Processing..."
        )
        await self.send_message(message)
    
    async def notify_job_completed(self, job_id: str, format: str, download_url: str):
        """Notify when a job completes"""
        message = (
            "✅ <b>Job Completed!</b>\n\n"
            f"<b>ID:</b> <code>{job_id}</code>\n"
            f"<b>Format:</b> {format}\n\n"
            f"📥 <a href='{download_url}'>Download Result</a>"
        )
        await self.send_message(message)
    
    async def notify_job_failed(self, job_id: str, error: str):
        """Notify when a job fails"""
        message = (
            "❌ <b>Job Failed</b>\n\n"
            f"<b>ID:</b> <code>{job_id}</code>\n"
            f"<b>Error:</b> {error[:500]}"
        )
        await self.send_message(message)
    
    async def notify_keepalive_failed(self, status_code: int):
        """Notify when keepalive check fails"""
        message = (
            "⚠️ <b>KeepAlive Alert</b>\n\n"
            "🔴 HF Space health check failed!\n"
            f"<b>Status:</b> {status_code}\n\n"
            "The Space might be sleeping or down."
        )
        await self.send_message(message)
    
    async def notify_keepalive_restored(self):
        """Notify when keepalive check succeeds after failure"""
        message = (
            "✅ <b>KeepAlive Restored</b>\n\n"
            "🟢 HF Space is back online!\n\n"
            "Health check passed."
        )
        await self.send_message(message)

# Command handlers for bot control
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 <b>BrowserPilot Bot</b>\n\n"
        "Commands:\n"
        "/start - Show this help\n"
        "/status - Check system status\n"
        "/jobs - List recent jobs\n"
        "/ping - Check if bot is alive\n\n"
        "To create a job, send a message with your task."
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    await update.message.reply_text("🟢 Bot is alive!")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    from backend.main import smart_proxy_manager, tasks, streaming_sessions
    
    proxy_stats = smart_proxy_manager.get_proxy_stats()
    
    message = (
        "📊 <b>System Status</b>\n\n"
        f"<b>Active Jobs:</b> {len(tasks)}\n"
        f"<b>Active Streams:</b> {len(streaming_sessions)}\n"
        f"<b>Proxies Available:</b> {proxy_stats.get('available', 0)}/{proxy_stats.get('total', 0)}\n\n"
        f"<b>Uptime:</b> Running"
    )
    await update.message.reply_text(message)

async def jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /jobs command"""
    from backend.database import db
    
    jobs = await db.get_all_jobs(limit=5)
    
    if not jobs:
        await update.message.reply_text("📋 No jobs found.")
        return
    
    message = "📋 <b>Recent Jobs</b>\n\n"
    for job in jobs[:5]:
        status_emoji = {"completed": "✅", "failed": "❌", "running": "🔄"}.get(job.get("status"), "⏳")
        message += (
            f"{status_emoji} <code>{job.get('id', 'unknown')[:8]}</code>\n"
            f"   {job.get('prompt', 'No prompt')[:50]}...\n"
            f"   Format: {job.get('format', 'unknown')} | Status: {job.get('status', 'unknown')}\n\n"
        )
    
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages as job prompts"""
    from backend.main import create_job, JobRequest
    
    prompt = update.message.text
    
    if not prompt:
        return
    
    # Create a job request
    req = JobRequest(prompt=prompt, format="json", headless=True, enable_streaming=False)
    
    # Create the job
    try:
        result = await create_job(req)
        job_id = result["job_id"]
        
        await update.message.reply_text(
            f"✅ <b>Job Created!</b>\n\n"
            f"<b>ID:</b> <code>{job_id}</code>\n"
            f"<b>Task:</b> {prompt[:100]}...\n\n"
            "I'll notify you when it's done!"
        )
        
        # Also notify via notifier (for consistency)
        notifier = TelegramNotifier()
        await notifier.initialize()
        await notifier.notify_job_started(job_id, prompt, "json")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to create job: {str(e)}")

# Global bot instance
bot_notifier = TelegramNotifier()

async def start_bot():
    """Start the Telegram bot"""
    await bot_notifier.initialize()
    
    if not bot_notifier._initialized:
        print("⚠️ Telegram bot not started (missing credentials)")
        return
    
    # Create application
    application = Application.builder().token(bot_notifier.token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("jobs", jobs_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling
    print("🤖 Starting Telegram bot polling...")
    await application.start_polling(allowed_updates=Update.ALL_TYPES)
