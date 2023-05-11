import requests
import time

# ส่วนของ Config
line_notify_token = 'UtzezjrTAJhMKqWwJ1TRYBaxCFT9MkKtJuekiyODMrh'
line_notify_api = 'https://notify-api.line.me/api/notify'

# ส่วนของ Function สำหรับส่งข้อความแจ้งเตือนไปยัง LINE Notify
def send_line_notify(notification_message):
    """
    ส่งข้อความไปยังไลน์ Notify
    """
    headers = {
        "Authorization": f"Bearer {line_notify_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "message": notification_message
    }
    requests.post(line_notify_api, headers=headers, data=data)

# รับค่าราคาทองคำประจำวัน
def get_gold_price():
    """
    ดึงราคาทองคำประจำวันจากเว็บไซต์ https://www.goldtraders.or.th/
    """
    gold_price_url = "https://www.goldtraders.or.th/"
    response = requests.get(gold_price_url)
    response.encoding = 'utf-8'
    content = response.text
    gold_price_start_tag = '<td class="text-right">สกุลเงินไทย / บาท</td>\n<td class="text-right">'
    gold_price_end_tag = '</td>\n<td class="text-right">'
    start_index = content.index(gold_price_start_tag) + len(gold_price_start_tag)
    end_index = content.index(gold_price_end_tag)
    return float(content[start_index:end_index].replace(",", ""))

# ราคาทองคำล่าสุด
last_gold_price = 0

# ส่วนของการเรียกใช้ Function เพื่อส่ง Notification เมื่อมีการเปลี่ยนแปลงของราคาทองคำ
while True:
    gold_price = get_gold_price()
    if gold_price != last_gold_price:
        last_gold_price = gold_price
        notification_message = f"ราคาทองคำประจำวัน {time.strftime('%d/%m/%Y')} เวลา {time.strftime('%H:%M:%S')} คือ {last_gold_price:.2f} บาท"
        send_line_notify(notification_message)
    time.sleep(60) # หน่วงเวลา 1 นาทีก่อนที่จะดึงราคาทองคำอีกครั้ง
