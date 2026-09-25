import telebot
import requests
import time

# --- কনফিগারেশন ---
BOT_TOKEN = "8701736168:AAHhfQUelJm-Fl3BCGQmQ55biNdzYP6_EXw"
GROUP_CHAT_ID = -1004429028470
API_KEY = "MKR8MCYN7MZ" 
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api"

bot = telebot.TeleBot(BOT_TOKEN)
headers = {"mauthapi": API_KEY, "Content-Type": "application/json"}

# ডুপ্লিকেট মেসেজ আটকানোর ট্র্যাকার
sent_otp_ids = set()
sent_console_ids = set() 

# নাম্বারের মাঝখানের অংশ ★★★★★ দিয়ে হাইড করার ফাংশন
def mask_phone_number(phone):
    if not phone or phone == "Unknown": 
        return "Unknown"
    p = str(phone)
    return f"{p[:5]}★★★★★{p[-3:]}" if len(p) > 6 else f"{p[:2]}★★★★★{p[-2:]}"

def auto_checker():
    print("🔄 কনসোল এবং ওটিপি (ফুল মেসেজ মোড) ডিটেক্টর চালু হয়েছে...")
    
    while True:
        try:
            # === ১. ওটিপি লগ চেক ===
            otp_resp = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if otp_resp.get("meta", {}).get("status") == "ok":
                for otp_data in otp_resp.get("data", {}).get("otps", []):
                    oid = otp_data.get("otp_id")
                    if oid and oid not in sent_otp_ids:
                        masked_num = mask_phone_number(otp_data.get('number'))
                        msg = (f"⚡ **[SUCCESS LOG] NEW OTP** ⚡\n"
                               f"━━━━━━━━━━━━━━━━━━━\n"
                               f"🆔 **RID:** `{otp_resp.get('rid', 'N/A')}`\n"
                               f"📱 **নম্বর:** `{masked_num}`\n\n"
                               f"💬 **MESSAGE:**\n`{otp_data.get('message')}`\n"
                               f"━━━━━━━━━━━━━━━━━━━")
                        bot.send_message(GROUP_CHAT_ID, msg, parse_mode="Markdown")
                        sent_otp_ids.add(oid)

            # === ২. কনসোল লগ চেক (মেসেজ ও নাম্বারসহ) ===
            console_resp = requests.get(f"{BASE_URL}/console", headers=headers).json()
            if console_resp.get("meta", {}).get("status") == "ok":
                for hit in console_resp.get("data", {}).get("hits", []):
                    # প্রতিটি হিটের ইউনিক আইডি হিসেবে টাইম স্ট্যাম্প ব্যবহার করা হচ্ছে
                    console_id = str(hit.get("time")) 
                    
                    if console_id not in sent_console_ids:
                        # কনসোল থেকে নাম্বার এবং মেসেজ নেওয়া হচ্ছে
                        c_number = hit.get("number", "Unknown")
                        c_message = hit.get("message", "No message content in console")
                        masked_c_num = mask_phone_number(c_number)
                        
                        msg = (f"🖥️ **[CONSOLE LOG] NEW UPDATE**\n"
                               f"━━━━━━━━━━━━━━━━━━━\n"
                               f"📱 **Range:** `{hit.get('range')}`\n"
                               f"📞 **নম্বর:** `{masked_c_num}`\n"
                               f"🌍 **দেশ:** {hit.get('country')}\n\n"
                               f"💬 **CONSOLE MESSAGE:**\n`{c_message}`\n"
                               f"━━━━━━━━━━━━━━━━━━━")
                        bot.send_message(GROUP_CHAT_ID, msg, parse_mode="Markdown")
                        sent_console_ids.add(console_id)

        except Exception as e:
            print(f"❌ এরর: {e}")
            
        time.sleep(8) # ৮ সেকেন্ড পর পর চেক করবে

if __name__ == "__main__":
    auto_checker()
