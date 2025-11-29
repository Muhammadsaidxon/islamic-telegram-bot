import os
import asyncio
from datetime import datetime
import random
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IslamicBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.admin_id = os.getenv('ADMIN_ID')
        
        if not self.token:
            raise ValueError("BOT_TOKEN not found")
        if not self.admin_id:
            raise ValueError("ADMIN_ID not found")
            
        self.bot = Bot(token=self.token)
        print("✅ Islamic Bot Started on Render!")
    
    def create_daily_message(self):
        """Create the daily message"""
        current_date = datetime.now()
        
        # Prayer times
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
        
        # Build message
        prayer_text = "\n".join([f"• {prayer}: `{time}`" for prayer, time in prayer_times.items()])
        
        message = f"""🕌 *Kunlik Namoz Vaqtlari*

📅 *Sana:* {current_date.strftime('%d-%m-%Y')}
🏙️ *Shahar:* Toshkent

🕐 *Namoz Vaqtlari:*
{prayer_text}

📖 *Kunlik Hadis:*
\"{random.choice(hadiths)}\"

🤖 *@DailyIslamInfoBot*
*🕋 Alloh namozlaringizni qabul qilsin!*"""
        
        return message
    
    async def send_message(self):
        """Send message to Telegram"""
        try:
            message = self.create_daily_message()
            await self.bot.send_message(
                chat_id=self.admin_id,
                text=message,
                parse_mode='Markdown'
            )
            print(f"✅ Message sent at {datetime.now()}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    async def run(self):
        """Main bot loop"""
        print("🚀 Bot running on Render - 24/7!")
        
        # Send immediate test
        print("📤 Sending test message...")
        await self.send_message()
        
        while True:
            now = datetime.now()
            # Send daily at 8:00 AM
            if now.hour == 8 and now.minute == 0:
                await self.send_message()
            # Wait 60 seconds
            await asyncio.sleep(60)

if __name__ == "__main__":
    bot = IslamicBot()
    asyncio.run(bot.run())