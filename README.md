# Darshan-Tracker-

# Annamalaiyar Temple Booking Monitor

## Overview
A Python automation script that monitors the Annamalaiyar Temple's darshan booking website for available slots. When dates become available, it sends instant WhatsApp notifications using Twilio's messaging service.

## Technical Implementation

### 1. Main Components

#### TempleBookingMonitor Class
The core class that handles all monitoring functionality:

##### Key Methods:

1. **check_calendar_status()**
   - Purpose: Scrapes and processes calendar data
   - Returns: Dictionary with booked and available dates
   ```python
   {
       'booked': ['1', '2', '3'],
       'available': ['4', '5', '6']
   }
   ```
   - Implementation:
     - Uses Selenium to load booking page
     - Locates calendar elements using CSS selectors
     - Processes dates using class identifiers
     - Handles various edge cases and errors

2. **send_status_notification(status)**
   - Purpose: Sends WhatsApp notifications for available dates
   - Parameters: status dictionary from check_calendar_status()
   - Features:
     - Only sends when dates are available
     - Formats message with emojis
     - Sends to multiple recipients
   - Message Format:
     ```
     🕉 Temple Booking Status Update 🕉
     Time: [Timestamp]
     ✨ DATES AVAILABLE! ✨
     January 2025 Calendar Status:
     ----------------------------
     🟢 Available Dates: [Dates]
     🔴 Booked Dates: [Dates]
     Book now at: [URL]
     ```

3. **monitor(interval_minutes=5)**
   - Purpose: Main monitoring loop
   - Implementation:
     - Continuous monitoring cycle
     - Configurable check interval
     - Error handling and recovery
     - Resource management

4. **cleanup()**
   - Purpose: Resource cleanup
   - Actions:
     - Closes browser
     - Releases WebDriver resources
     - Handles cleanup errors

### 2. Browser Automation

#### Chrome Configuration

#### WebDriver Setup
- Uses Selenium WebDriver
- Implements explicit waits (20 seconds)
- Configures implicit waits (10 seconds)
- Handles connection timeouts

### 3. Calendar Monitoring Logic

#### Date Detection
- Booked Dates:
  ```python
  booked_dates = self.driver.find_elements(By.CLASS_NAME, "bookedClass")
  ```
- Available Dates:
  ```python
  available_dates = self.driver.find_elements(
      By.CSS_SELECTOR, 
      "td.day:not(.disabled):not(.bookedClass):not(.old):not(.new)"
  )
  ```

#### Date Processing
- Filters invalid dates
- Sorts dates numerically
- Converts to string format
- Handles edge cases

### 4. Notification System

#### Twilio Integration
- Uses Twilio WhatsApp API
- Handles multiple recipients
- Implements retry logic
- Validates message delivery

#### Message Construction
- Dynamic content based on available dates
- Formatted for readability
- Includes essential booking information
- Uses Unicode emojis for visual appeal

### 5. Error Handling

#### Browser Errors
- WebDriver initialization
- Page loading issues
- Element location failures
- Network timeouts

#### Notification Errors
- API connection issues
- Message delivery failures
- Authentication problems
- Rate limiting

#### General Error Management
- Exception logging
- Automatic retry mechanisms
- Graceful degradation
- Resource cleanup

## Configuration

### Environment Variables (.env)

### Dependencies (requirements.txt)

## Usage

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Script
```bash
python temple_monitor.py
```

### Monitoring Output
```
Starting Temple Booking Monitor...
Configuration loaded:
Account SID: AC1159...7b7
WhatsApp From: +14155238886
Notification Numbers: ['+919949197453']
Initializing Chrome WebDriver...
Initializing Twilio client...
Initialization complete.
```

## Troubleshooting

### Common Issues and Solutions

1. **WebDriver Errors**
   - Update Chrome: `brew install --cask google-chrome`
   - Update chromedriver
   - Check system compatibility

2. **Notification Failures**
   - Verify Twilio credentials
   - Check WhatsApp number format
   - Confirm recipient opt-in

3. **Website Access Issues**
   - Check internet connection
   - Verify URL accessibility
   - Monitor for IP restrictions

## Security Best Practices

1. **Credential Management**
   - Use .env for sensitive data
   - Never commit credentials
   - Rotate tokens regularly

2. **Browser Security**
   - Headless mode operation
   - Sandbox disabled safely
   - Secure connection handling

## Limitations

1. **Website Dependencies**
   - Specific to temple website structure
   - May need updates if site changes
   - Dependent on element classes/IDs

2. **Technical Requirements**
   - Chrome browser dependency
   - Internet connectivity needed
   - Twilio service requirement

## License
MIT License
