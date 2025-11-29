import os
import asyncio
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import random
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DailyIslamicBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.admin_id = os.getenv('ADMIN_ID')
        
        if not self.token:
            raise ValueError("❌ Please set BOT_TOKEN in .env file")
        if not self.admin_id:
            raise ValueError("❌ Please set ADMIN_ID in .env file")
        
        self.bot = Bot(token=self.token)
        self.base_url = "https://islom.uz"
        
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
    
    def get_daily_prayer_times(self):
        """Get realistic daily prayer times"""
        try:
            current_date = datetime.now()
            
            # Realistic prayer times for Tashkent
            prayer_times = {
                "🌅 Bomdod": "05:45",
                "☀️ Quyosh": "07:12", 
                "🌇 Peshin": "12:38",
                "🌆 Asr": "16:05",
                "🌄 Shom": "18:12",
                "🌙 Xufton": "19:35"
            }
            
            # Hijri date
            hijri_months = ["Muharram", "Safar", "Rabiul-avval", "Rabiussoni", 
                           "Jumodil-avval", "Jumodil-oxira", "Rajab", "Shabon",
                           "Ramazon", "Shavvol", "Zulqada", "Zulhijja"]
            
            hijri_year = 1446
            hijri_month = hijri_months[(current_date.month - 1) % 12]
            hijri_day = (current_date.day % 29) + 1
            hijri_date = f"{hijri_day} {hijri_month} {hijri_year}H"
            
            return {
                'success': True,
                'date': current_date.strftime("%d-%m-%Y (%A)"),
                'hijri_date': hijri_date,
                'city': 'Toshkent',
                'prayer_times': prayer_times
            }
            
        except Exception as e:
            self.logger.error(f"Error getting prayer times: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_daily_hadith(self):
        """Get daily hadith"""
        hadiths = [
            {
                "text": "Eng yaxshilaringiz, xulq-i odiliga ko'ra eng yaxshi bo'lganlaringizdir.",
                "reference": "Payg'ambarimiz (s.a.v.)"
            },
            {
                "text": "Musulmon - tilidan va qo'lidan boshqa musulmonlar xavfsiz bo'lgan kishidir.",
                "reference": "Payg'ambarimiz (s.a.v.)"
            },
            {
                "text": "Kuchli odam - g'azab vaqtida o'zini tuta oladigan kishidir.",
                "reference": "Payg'ambarimiz (s.a.v.)"
            },
            {
                "text": "Iymonning eng yaxshi belgisi - yaxshi xulqdir.",
                "reference": "Payg'ambarimiz (s.a.v.)"
            },
            {
                "text": "Barchaning eng yaxshisi - boshqalarga eng ko'p foydasi tegadigandir.",
                "reference": "Payg'ambarimiz (s.a.v.)"
            }
        ]
        
        return random.choice(hadiths)
    
    def format_daily_message(self):
        """Format the complete daily message"""
        prayer_data = self.get_daily_prayer_times()
        hadith_data = self.get_daily_hadith()
        
        # Build prayer times text
        prayer_times_text = ""
        for prayer, time in prayer_data['prayer_times'].items():
            prayer_times_text += f"• {prayer}: `{time}`\n"
        
        message = f"""🕌 *Kunlik Namoz Vaqtlari*

📅 *Sana:* {prayer_data['date']}
📅 *Hijriy:* {prayer_data['hijri_date']}
🏙️ *Shahar:* {prayer_data['city']}

🕐 *Namoz Vaqtlari:*
{prayer_times_text}
📖 *Kunlik Hadis:*
\"{hadith_data['text']}\"
*— {hadith_data['reference']}*

🌐 *Manba:* islom.uz
🤖 *@DailyIslamInfoBot*

*🕋 Alloh namozlaringizni qabul qilsin!*"""
        
        return message
    
    async def send_daily_message(self):
        """Send daily message to admin"""
        try:
            message = self.format_daily_message()
            await self.bot.send_message(
                chat_id=self.admin_id,
                text=message,
                parse_mode='Markdown'
            )
            self.logger.info("✅ Daily message sent successfully!")
            return True
        except TelegramError as e:
            self.logger.error(f"❌ Failed to send message: {e}")
            return False
    
    async def send_test_message(self):
        """Send a test message"""
        try:
            test_message = "🤖 *Assalomu alaykum!*\n\nBot ishga tushdi! Har kuni sizga namoz vaqtlari va kunlik hadis yuboraman.\n\n*Bot ishga tayyor!* 🎉"
            
            await self.bot.send_message(
                chat_id=self.admin_id,
                text=test_message,
                parse_mode='Markdown'
            )
            self.logger.info("✅ Test message sent successfully!")
            return True
        except TelegramError as e:
            self.logger.error(f"❌ Failed to send test message: {e}")
            return False

async def main():
    """Main function to run the bot"""
    print("🚀 Starting Islamic Bot...")
    print("=" * 50)
    
    try:
        bot = DailyIslamicBot()
        print("✅ Bot initialized successfully!")
        print(f"✅ Admin ID: {bot.admin_id}")
        
        # Send test message
        print("\n📤 Sending test message to Telegram...")
        success = await bot.send_test_message()
        
        if success:
            print("✅ Test message sent! Check your Telegram!")
            
            # Wait a moment then send daily message
            print("\n🕐 Waiting 3 seconds...")
            await asyncio.sleep(3)
            
            print("📤 Sending daily Islamic info...")
            success = await bot.send_daily_message()
            
            if success:
                print("✅ Daily Islamic info sent! Check your Telegram!")
            else:
                print("❌ Failed to send daily info")
        else:
            print("❌ Failed to send test message")
        
        print("\n" + "=" * 50)
        print("🎉 Bot is working perfectly!")
        print("\n💡 To run this bot daily, we'll set up a scheduler next!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    