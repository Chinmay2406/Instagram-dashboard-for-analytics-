from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver with ChromeDriver path
chrome_service = Service("D:/cpa/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=chrome_service)

# Function to scrape Instagram profile data with Selenium
def scrape_instagram_with_selenium(profile_url):
    driver.get(profile_url)
    
    # Wait for the page to load fully
    time.sleep(5)  # Adjust this based on your internet speed
    
    # Get the page source
    html = driver.page_source
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract followers, following, posts from meta tag
    meta_tag = soup.find("meta", property="og:description")
    if meta_tag:
        content = meta_tag.attrs['content']
        data = content.split("-")[0]
        followers, following, posts = data.split(", ")
        
        # Extract bio
        bio = soup.find('div', {'class': '-vDIg'}).span.get_text() if soup.find('div', {'class': '-vDIg'}) else "No bio available"
        
        # Extract profile picture
        profile_pic = soup.find('img', {'class': '_6q-tv'}).attrs['src'] if soup.find('img', {'class': '_6q-tv'}) else "No profile picture found"
        
        # Extract website URL
        website_url = soup.find('a', {'class': 'yLUwa'}).attrs['href'] if soup.find('a', {'class': 'yLUwa'}) else "No website URL found"
        
        # Extract name
        full_name = soup.find('h1', {'class': 'rhpdm'}).get_text() if soup.find('h1', {'class': 'rhpdm'}) else "No full name found"
        
        # Check if the profile is verified
        is_verified = "Yes" if soup.find('span', {'class': 'coreSpriteVerifiedBadge'}) else "No"
        
        return {
            "followers": followers.split()[0],
            "following": following.split()[0],
            "posts": posts.split()[0],
            "bio": bio,
            "profile_pic": profile_pic,
            "website_url": website_url,
            "full_name": full_name,
            "is_verified": is_verified
        }
    else:
        return "Profile data not found."

# Example usage
profile_url = "https://www.instagram.com/the.rebel.kid/"
profile_data = scrape_instagram_with_selenium(profile_url)

# Print scraped data
if isinstance(profile_data, dict):
    print(f"Followers: {profile_data['followers']}")
    print(f"Following: {profile_data['following']}")
    print(f"Posts: {profile_data['posts']}")
    print(f"Bio: {profile_data['bio']}")
    print(f"Profile Picture URL: {profile_data['profile_pic']}")
    print(f"Website URL: {profile_data['website_url']}")
    print(f"Full Name: {profile_data['full_name']}")
    print(f"Verified: {profile_data['is_verified']}")
else:
    print(profile_data)

# Close the WebDriver after scraping
driver.quit()
