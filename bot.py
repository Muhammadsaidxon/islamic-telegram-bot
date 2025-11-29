import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class IslamicBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        if not self.token:
            raise ValueError("❌ Please set BOT_TOKEN in .env file")
        
        print("✅ Bot initialized successfully!")
        print(f"✅ Token starts with: {self.token[:10]}...")

if __name__ == "__main__":
    try:
        bot = IslamicBot()
        print("🚀 Bot is ready to be developed!")
        print("📝 Next: We'll add the web scraper and bot functionality")
    except Exception as e:
        print(f"❌ Error: {e}")
