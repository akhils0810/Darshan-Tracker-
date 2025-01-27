from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio configuration with debug prints
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM')
NOTIFICATION_NUMBERS = os.getenv('NOTIFICATION_NUMBERS', '+919949197453').split(',')

print("Configuration loaded:")
print(f"Account SID: {TWILIO_ACCOUNT_SID[:6]}...{TWILIO_ACCOUNT_SID[-4:]}")
print(f"WhatsApp From: {TWILIO_WHATSAPP_FROM}")
print(f"Notification Numbers: {NOTIFICATION_NUMBERS}")

class TempleBookingMonitor:
    def __init__(self):
        try:
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Initialize WebDriver with explicit wait
            print("Initializing Chrome WebDriver...")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.implicitly_wait(10)
            
            # Initialize Twilio client
            print("Initializing Twilio client...")
            self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            self.url = "https://annamalaiyar.hrce.tn.gov.in/ticketing/service_collection.php?tid=20343&scode=21&sscode=1&target_type=&fees_slno=3778463716&group_id=4&action=P"
            print("Initialization complete.")
            
        except Exception as e:
            print(f"Error in initialization: {e}")
            raise

    def check_calendar_status(self):
        try:
            print(f"Loading URL: {self.url}")
            self.driver.get(self.url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Wait for and verify calendar presence
            calendar = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-condensed"))
            )
            print("Calendar found on page")
            
            # Find and process booked dates
            print("Looking for booked dates...")
            booked_dates = self.driver.find_elements(By.CLASS_NAME, "bookedClass")
            booked = []
            for date in booked_dates:
                date_text = date.text.strip()
                print(f"Found booked date element: {date_text}")
                if date_text and not date_text.startswith('new'):
                    booked.append(date_text)
            
            # Find and process available dates
            print("Looking for available dates...")
            available_dates = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "td.day:not(.disabled):not(.bookedClass):not(.old):not(.new)"
            )
            available = []
            for date in available_dates:
                date_text = date.text.strip()
                print(f"Found available date element: {date_text}")
                if date_text:
                    available.append(date_text)
            
            # Sort and return results
            booked = sorted([int(d) for d in booked])
            available = sorted([int(d) for d in available])
            
            result = {
                'booked': [str(d) for d in booked],
                'available': [str(d) for d in available]
            }
            print(f"Calendar status: {result}")
            return result
            
        except Exception as e:
            print(f"Error checking calendar status: {e}")
            print("Page source:")
            try:
                print(self.driver.page_source[:500] + "...")  # Print first 500 chars
            except:
                print("Could not get page source")
            return {'booked': [], 'available': []}

    def send_status_notification(self, status):
        try:
            # Only send notification if there are available dates
            if not status['available']:
                print("No available dates found - skipping notification")
                return
                
            message = (
                f"🕉 Temple Booking Status Update 🕉\n"
                f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"✨ DATES AVAILABLE! ✨\n\n"
                f"January 2025 Calendar Status:\n"
                f"----------------------------\n"
                f"🟢 Available Dates: {', '.join(status['available'])}\n\n"
                f"🔴 Booked Dates: {', '.join(status['booked']) if status['booked'] else 'None'}\n\n"
                f"Book now at:\n{self.url}"
            )
            
            print(f"Available dates found! Sending message:\n{message}")
            
            for number in NOTIFICATION_NUMBERS:
                try:
                    response = self.twilio_client.messages.create(
                        body=message,
                        from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
                        to=f"whatsapp:{number}"
                    )
                    print(f"Message sent to {number}, SID: {response.sid}")
                except Exception as e:
                    print(f"Error sending to {number}: {e}")
                    
        except Exception as e:
            print(f"Error in send_status_notification: {e}")

    def monitor(self, interval_minutes=5):
        print(f"Starting monitoring at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        while True:
            try:
                status = self.check_calendar_status()
                self.send_status_notification(status)
                
                print(f"Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                print("Retrying in 1 minute...")
                time.sleep(60)

    def cleanup(self):
        try:
            self.driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error in cleanup: {e}")

if __name__ == "__main__":
    try:
        print("Starting Temple Booking Monitor...")
        monitor = TempleBookingMonitor()
        monitor.monitor()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if 'monitor' in locals():
            monitor.cleanup() 
