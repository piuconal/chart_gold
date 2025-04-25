from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests

# ==== Thông tin Telegram ====
BOT_TOKEN = "7730068417:AAHLkjKHDImE4SLlbzr_lG3xGCADNHwtpHM"
CHAT_ID = "2104586242"

# ==== Cấu hình driver Chrome (headless) ====
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(), options=options)

# ==== Chụp biểu đồ từ trang vàng nội địa ====
def capture_chart(url, asset_value, filename):
    driver = setup_driver()
    try:
        driver.get(url)
        time.sleep(3)
        select_element = driver.find_element(By.CSS_SELECTOR, "select[wire\\:model='assetId']")
        select = Select(select_element)
        select.select_by_value(asset_value)
        time.sleep(4)
        chart = driver.find_element(By.ID, "gold-price-chart")
        driver.execute_script("arguments[0].scrollIntoView(true);", chart)
        time.sleep(2)
        chart.screenshot(filename)
    finally:
        driver.quit()

# ==== Chụp biểu đồ vàng thế giới (iframe) ====
def capture_world_chart(filename):
    driver = setup_driver()
    try:
        driver.get("https://bieudogiavang.net/gia-vang-the-gioi")
        time.sleep(5)
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[id^='tradingview_']")
        driver.execute_script("arguments[0].scrollIntoView(true);", iframe)
        time.sleep(2)
        iframe.screenshot(filename)
    finally:
        driver.quit()

# ==== Gửi ảnh Telegram có caption ====
def send_photo(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(file_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": caption}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print(f"📤")
        else:
            print(f"❌")

# ==== Thực thi toàn bộ ====
def main():
    capture_chart("https://bieudogiavang.net/gia-vang-bao-tin-minh-chau", "123", "btmc.png")
    capture_chart("https://bieudogiavang.net/gia-vang-phu-quy", "78", "phuquy.png")
    capture_world_chart("thegioi.png")

    send_photo("btmc.png", "📊 Biểu đồ giá vàng Bảo Tín Minh Châu")
    send_photo("phuquy.png", "📊 Biểu đồ giá vàng Phú Quý")
    send_photo("thegioi.png", "🌍 Biểu đồ giá vàng Thế Giới")

if __name__ == "__main__":
    main()
