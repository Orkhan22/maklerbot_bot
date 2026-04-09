import requests
from bs4 import BeautifulSoup

TOKEN = "8666608099:AAFhdnrexdxUkfIeCpK_6zq1NdTEdQAVFKQ"
CHAT_ID = "644928091"
# Porsche Panamera 2015-ci il filtri
TURBO_URL = "https://turbo.az/avtomobiller?q%5Bmake%5D%5B%5D=21&q%5Bmodel%5D%5B%5D=536&q%5Byear_from%5D=2015&q%5Byear_to%5D=2015"

def check_turbo():
    print("--- Turbo.az axtarışı başladı ---")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(TURBO_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Turbo.az-da hər bir elan 'products-i' klassı içində olur
        items = soup.find_all('div', class_='products-i')

        if items:
            first_car = items[0]
            
            # Linki tapırıq
            link_tag = first_car.find('a', class_='products-i__link', href=True)
            car_link = "https://turbo.az" + link_tag['href'] if link_tag else "Link tapılmadı"
            
            # Qiyməti tapırıq
            price_val = first_car.find('div', class_='product-price')
            price_text = price_val.text.strip() if price_val else "Qiymət qeyd edilməyib"
            
            # Avtomobilin qısa məlumatları (Yürüş, mühərrik və s.)
            info = first_car.find('div', class_='products-i__attributes')
            info_text = info.text.strip() if info else "2015 model Panamera"

            msg = (
                f"🏎 *Yeni Porsche Panamera tapıldı! (2015)*\n\n"
                f"💰 *Qiymət:* {price_text}\n"
                f"ℹ️ *Məlumat:* {info_text}\n\n"
                f"🔗 [Maşına baxmaq üçün kliklə]({car_link})"
            )

            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
            )
            print(f"Turbo.az elanı göndərildi: {price_text}")
        else:
            print("Turbo.az-da uyğun elan tapılmadı.")

    except Exception as e:
        print(f"Turbo.az Xətası: {e}")

if __name__ == "__main__":
    check_turbo()
