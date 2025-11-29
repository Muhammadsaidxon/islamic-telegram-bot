import os
import asyncio
import requests
from datetime import datetime
import random
from telegram import Bot
from telegram.error import TelegramError
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DeployedIslamicBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.admin_id = os.getenv('ADMIN_ID')
        
        if not self.token:
            raise ValueError("BOT_TOKEN not set")
        if not self.admin_id:
            raise ValueError("ADMIN_ID not set")
        
        self.bot = Bot(token=self.token)
        print("🤖 Islamic Bot Started Successfully!")
    
    def get_daily_data(self):
        """Get daily Islamic data"""
        current_date = datetime.now()
        
        # Prayer times for Tashkent
        prayer_times = {
            "🌅 Bomdod": "05:45",
            "☀️ Quyosh": "07:12", 
            "🌇 Peshin": "12:38",
            "🌆 Asr": "16:05",
            "🌄 Shom": "18:12",
            "🌙 Xufton": "19:35"
        }
        
        # Hadith collection
        hadiths = [
            "Eng yaxshilaringiz, xulq-i odiliga ko'ra eng yaxshi bo'lganlaringizdir. - Payg'ambarimiz (s.a.v.)",
            "Musulmon - tilidan va qo'lidan boshqa musulmonlar xavfsiz bo'lgan kishidir. - Payg'ambarimiz (s.a.v.)",
            "Kuchli odam - g'azab vaqtida o'zini tuta oladigan kishidir. - Payg'ambarimiz (s.a.v.)"
        ]
        
        return {
            'date': current_date.strftime("%d-%m-%Y"),
            'prayer_times': prayer_times,
            'hadith': random.choice(hadiths)
        }
    
    def format_message(self):
        """Format the message"""
        data = self.get_daily_data()
        
        prayer_text = ""
        for prayer, time in data['prayer_times'].items():
            prayer_text += f"• {prayer}: `{time}`\n"
        
        message = f"""🕌 *Kunlik Namoz Vaqtlari*

📅 *Sana:* {data['date']}
🏙️ *Shahar:* Toshkent

🕐 *Namoz Vaqtlari:*
{prayer_text}
📖 *Kunlik Hadis:*
\"{data['hadith']}\"

🤖 *@DailyIslamInfoBot*
*🕋 Alloh namozlaringizni qabul qilsin!*"""
        
        return message
    
    async def send_message(self):
        """Send message to Telegram"""
        try:
            message = self.format_message()
            await self.bot.send_message(
                chat_id=self.admin_id,
                text=message,
                parse_mode='Markdown'
            )
            print(f"✅ Message sent at {datetime.now()}")
            return True
        except TelegramError as e:
            print(f"❌ Error: {e}")
            return False
    
    async def run(self):
        """Main bot loop"""
        print("🚀 Bot is running on cloud...")
        
        while True:
            current_time = datetime.now().strftime("%H:%M")
            
            # Send at 08:00 every day
            if current_time == "08:00":
                await self.send_message()
            
            # Also send every 6 hours for testing
            elif current_time in ["08:00", "14:00", "20:00", "02:00"]:
                await self.send_message()
            
            # Wait 60 seconds before checking again
            await asyncio.sleep(60)

async def main():
    bot = DeployedIslamicBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())