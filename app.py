import random
import time
import webview
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

KEYWORDS = {
    '1': ('music', ['lofi hip hop beats', 'live acoustic concert', 'synthwave mix', 'Top 100 Music', 'indie rock playlist']),
    '2': ('makeup', ['everyday makeup routine', 'glam makeup tutorial', 'skincare routine steps', 'makeup product review', 'easy eyeliner tutorial']),
    '3': ('gaming', ['minecraft lets play', 'elden ring gameplay', 'speedrun world record', 'valorant competitive', 'retro gaming documentary']),
    '4': ('vlogs', ['day in the life vlog', 'solo travel documentary', 'tokyo street food vlog', 'productive morning routine', 'moving vlog']),
    '5': ('languages', ['learn spanish beginner', 'japanese pronunciation guide', 'polyglot conversation', 'french language basics', 'english accent training'])
}

class Api:
    def calibrate(self, choice):
        if choice not in KEYWORDS:
            return "Invalid choice."
            
        category_name, terms = KEYWORDS[choice]
        random.shuffle(terms)
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--remote-allow-origins=*')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            for term in terms:
                driver.get('https://youtube.com')
                time.sleep(5)
                
                try:
                    search_box = driver.find_element(By.NAME, 'search_query')
                    search_box.clear()
                    search_box.send_keys(term)
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(5)
                    
                    shorts_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-reel-item-renderer a, a[href*='/shorts/']")
                    if shorts_elements:
                        valid_shorts = [s for s in shorts_elements if s.is_displayed()]
                        if valid_shorts:
                            random.choice(valid_shorts).click()
                            time.sleep(1)
                            
                            for _ in range(5):
                                time.sleep(1)
                                try:
                                    body = driver.find_element(By.TAG_NAME, 'body')
                                    body.send_keys(Keys.ARROW_DOWN)
                                except:
                                    break
                except Exception as e:
                    print(f"Skipping term due to error: {e}")
                    continue
            driver.quit()
            return f"Finished calibrating {category_name.upper()}!"
        except Exception as e:
            driver.quit()
            return f"Error: {str(e)}"

if __name__ == '__main__':
    api = Api()
    webview.create_window('Feed Optimiser', 'index.html', js_api=api, width=400, height=300)
    webview.start()