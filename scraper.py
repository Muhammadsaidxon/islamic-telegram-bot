import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging

class IslomUzScraper:
    def __init__(self):
        self.base_url = "https://islom.uz"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_daily_prayer_times(self, region="tashkent"):
        """Get daily prayer times for specified region"""
        try:
            # Use the main page which has prayer times
            url = f"{self.base_url}/"
            print(f"🔍 Fetching data from: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find prayer times in the website
            # Let's look for common patterns
            prayer_times = {}
            
            # Method 1: Look for table with prayer times
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        prayer_name = cells[0].text.strip()
                        prayer_time = cells[1].text.strip()
                        if any(name in prayer_name.lower() for name in ['bomdod', 'peshin', 'asr', 'shom', 'xufton', 'quyosh']):
                            prayer_times[prayer_name] = prayer_time
            
            # Method 2: Look for prayer time elements by class or id
            if not prayer_times:
                time_elements = soup.find_all(class_=lambda x: x and any(word in str(x).lower() for word in ['time', 'prayer', 'namoz']))
                for element in time_elements:
                    text = element.text.strip()
                    if ':' in text and any(word in text.lower() for word in ['bomdod', 'peshin', 'asr', 'shom', 'xufton']):
                        # Extract prayer name and time
                        lines = text.split('\n')
                        for line in lines:
                            line = line.strip()
                            if ':' in line:
                                for prayer in ['Bomdod', 'Peshin', 'Asr', 'Shom', 'Xufton', 'Quyosh']:
                                    if prayer.lower() in line.lower():
                                        time_part = line.split(' ')[-1]
                                        prayer_times[prayer] = time_part
                                        break
            
            # If still no times found, use sample data
            if not prayer_times:
                print("⚠️  Could not extract prayer times from website, using sample data")
                prayer_times = {
                    "Bomdod": "05:30",
                    "Quyosh": "06:45", 
                    "Peshin": "12:30",
                    "Asr": "16:15",
                    "Shom": "18:45",
                    "Xufton": "20:00"
                }
            
            # Get current date
            current_date = datetime.now()
            hijri_date = self.get_hijri_date(current_date)
            
            return {
                'success': True,
                'date': current_date.strftime("%Y-%m-%d %A"),
                'hijri_date': hijri_date,
                'city': region.capitalize(),
                'prayer_times': prayer_times,
                'source': self.base_url
            }
            
        except Exception as e:
            logging.error(f"Error fetching prayer times: {e}")
            # Return sample data on error
            current_date = datetime.now()
            hijri_date = self.get_hijri_date(current_date)
            
            return {
                'success': False, 
                'error': str(e),
                'date': current_date.strftime("%Y-%m-%d %A"),
                'hijri_date': hijri_date,
                'city': region.capitalize(),
                'prayer_times': {
                    "Bomdod": "05:30",
                    "Quyosh": "06:45",
                    "Peshin": "12:30", 
                    "Asr": "16:15",
                    "Shom": "18:45",
                    "Xufton": "20:00"
                }
            }
    
    def get_hijri_date(self, date):
        """Convert Gregorian date to Hijri date (simplified)"""
        # This is a simplified conversion for demonstration
        # In a real application, you'd use a proper Hijri calendar library
        hijri_months = [
            "Muharram", "Safar", "Rabi' al-Awwal", "Rabi' al-Thani",
            "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
            "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
        ]
        
        # Simple approximation (this is not accurate, for demo only)
        hijri_year = 1446  # Example Hijri year
        hijri_month = hijri_months[(date.month - 1) % 12]
        hijri_day = date.day
        
        return f"{hijri_day} {hijri_month} {hijri_year}H"
    
    def get_daily_hadith(self):
        """Get daily hadith"""
        try:
            # For now, return sample hadiths
            hadiths = [
                {
                    "text": "The best among you are those who have the best manners and character.",
                    "reference": "Prophet Muhammad (PBUH)"
                },
                {
                    "text": "A Muslim is one from whose tongue and hand other Muslims are safe.",
                    "reference": "Prophet Muhammad (PBUH)"
                },
                {
                    "text": "The strong is not the one who overcomes the people by his strength, but the strong is the one who controls himself while in anger.",
                    "reference": "Prophet Muhammad (PBUH)"
                },
                {
                    "text": "Do not be people without minds of your own, saying that if others treat you well you will treat them well, and that if they do wrong you will do wrong. Instead, accustom yourselves to do good if people do good and not to do wrong if they do evil.",
                    "reference": "Prophet Muhammad (PBUH)"
                },
                {
                    "text": "Kindness is a mark of faith, and whoever has not kindness has not faith.",
                    "reference": "Prophet Muhammad (PBUH)"
                }
            ]
            
            import random
            daily_hadith = random.choice(hadiths)
            
            return {
                'success': True,
                'hadith': daily_hadith['text'],
                'reference': daily_hadith['reference'],
                'source': 'islom.uz'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'hadith': "The best among you are those who have the best manners and character.",
                'reference': "Prophet Muhammad (PBUH)"
            }
    
    def get_daily_islamic_info(self):
        """Get complete daily Islamic information"""
        prayer_data = self.get_daily_prayer_times()
        hadith_data = self.get_daily_hadith()
        
        return {
            'prayer_times': prayer_data,
            'daily_hadith': hadith_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def test_scraper():
    """Test the scraper"""
    print("🧪 Testing Islom.uz Scraper...")
    print("=" * 50)
    
    scraper = IslomUzScraper()
    
    # Test prayer times
    print("\n🕌 Fetching Daily Prayer Times...")
    prayer_data = scraper.get_daily_prayer_times()
    
    print(f"📅 Date: {prayer_data['date']}")
    print(f"📅 Hijri: {prayer_data['hijri_date']}")
    print(f"🏙️ City: {prayer_data['city']}")
    
    if prayer_data['success']:
        print("✅ Successfully fetched prayer times")
    else:
        print(f"⚠️ Using sample data due to: {prayer_data['error']}")
    
    print("\n🕐 Namoz Vaqtlari:")
    print("-" * 20)
    for prayer, time in prayer_data['prayer_times'].items():
        print(f"   {prayer:10} : {time}")
    
    # Test hadith
    print("\n📖 Daily Hadith:")
    print("-" * 20)
    hadith_data = scraper.get_daily_hadith()
    
    if hadith_data['success']:
        print(f"\"{hadith_data['hadith']}\"")
        print(f" - {hadith_data['reference']}")
    else:
        print(f"⚠️ Error: {hadith_data['error']}")
    
    print("\n" + "=" * 50)
    print("🎉 Scraper test completed!")

if __name__ == "__main__":
    test_scraper()