import os
import json
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN", "8701736168:AAHhfQUelJm-Fl3BCGQmQ55biNdzYP6_EXw")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-1004429028470"))
API_KEY = os.getenv("API_KEY", "MKR8MCYN7MZ")
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api"

headers = {"mauthapi": API_KEY, "Content-Type": "application/json"}

def mask_phone_number(phone):
    if not phone or phone == "Unknown": 
        return "Unknown"
    p = str(phone)
    return f"{p[:5]}★★★★★{p[-3:]}" if len(p) > 6 else f"{p[:2]}★★★★★{p[-2:]}"

def handler(event, context):
    try:
        # === ১. ওটিপি লগ চেক ===
        otp_resp = requests.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10).json()
        if otp_resp.get("meta", {}).get("status") == "ok":
            for otp_data in otp_resp.get("data", {}).get("otps", []):
                masked_num = mask_phone_number(otp_data.get('number'))
                msg = (f"⚡ **[SUCCESS LOG] NEW OTP** ⚡\n"
                       f"━━━━━━━━━━━━━━━━━━━\n"
                       f"🆔 **RID:** `{otp_resp.get('rid', 'N/A')}`\n"
                       f"📱 **নম্বর:** `{masked_num}`\n\n"
                       f"💬 **MESSAGE:**\n`{otp_data.get('message')}`\n"
                       f"━━━━━━━━━━━━━━━━━━━")
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                    "chat_id": GROUP_CHAT_ID,
                    "text": msg,
                    "parse_mode": "Markdown"
                })

        # === ২. কনসোল লগ চেক ===
        console_resp = requests.get(f"{BASE_URL}/console", headers=headers, timeout=10).json()
        if console_resp.get("meta", {}).get("status") == "ok":
            for hit in console_resp.get("data", {}).get("hits", []):
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
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                    "chat_id": GROUP_CHAT_ID,
                    "text": msg,
                    "parse_mode": "Markdown"
                })

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "Checked successfully"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
