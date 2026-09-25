const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');

// --- কনফিগারেশন ---
const BOT_TOKEN = "8701736168:AAHhfQUelJm-Fl3BCGQmQ55biNdzYP6_EXw";
const GROUP_CHAT_ID = -1004429028470;
const API_KEY = "MKR8MCYN7MZ"; 
const BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api";

const bot = new TelegramBot(BOT_TOKEN, { polling: false });
const headers = { "mauthapi": API_KEY, "Content-Type": "application/json" };

// ডুপ্লিকেট মেসেজ আটকানোর ট্র্যাকার
const sentOtpIds = new Set();
const sentConsoleIds = new Set();

// নাম্বারের মাঝখানের অংশ ★★★★★ দিয়ে হাইড করার ফাংশন
function maskPhoneNumber(phone) {
    if (!phone || phone === "Unknown") return "Unknown";
    const p = String(phone);
    return p.length > 6 ? `${p.slice(0, 5)}★★★★★${p.slice(-3)}` : `${p.slice(0, 2)}★★★★★${p.slice(-2)}`;
}

async function autoChecker() {
    console.log("🔄 কনসোল এবং ওটিপি (ফুল মেসেজ মোড) ডিটেক্টর চালু হয়েছে...");

    try {
        // === ১. ওটিপি লগ চেক ===
        const otpRes = await fetch(`${BASE_URL}/success-otp`, { headers });
        const otpResp = await otpRes.json();
        
        if (otpResp?.meta?.status === "ok") {
            const otps = otpResp?.data?.otps || [];
            for (const otpData of otps) {
                const oid = otpData.otp_id;
                if (oid && !sentOtpIds.has(oid)) {
                    const maskedNum = maskPhoneNumber(otpData.number);
                    const msg = `⚡ **[SUCCESS LOG] NEW OTP** ⚡\n` +
                                `━━━━━━━━━━━━━━━━━━━\n` +
                                `🆔 **RID:** \`${otpResp.rid || 'N/A'}\`\n` +
                                `📱 **নম্বর:** \`${maskedNum}\`\n\n` +
                                `💬 **MESSAGE:**\n\`${otpData.message}\`\n` +
                                `━━━━━━━━━━━━━━━━━━━`;
                    
                    await bot.sendMessage(GROUP_CHAT_ID, msg, { parse_mode: "Markdown" });
                    sentOtpIds.add(oid);
                }
            }
        }

        // === ২. কনসোল লগ চেক ===
        const consoleRes = await fetch(`${BASE_URL}/console`, { headers });
        const consoleResp = await consoleRes.json();

        if (consoleResp?.meta?.status === "ok") {
            const hits = consoleResp?.data?.hits || [];
            for (const hit of hits) {
                const consoleId = String(hit.time);
                if (!sentConsoleIds.has(consoleId)) {
                    const cNumber = hit.number || "Unknown";
                    const cMessage = hit.message || "No message content in console";
                    const maskedCNum = maskPhoneNumber(cNumber);

                    const msg = `🖥️ **[CONSOLE LOG] NEW UPDATE**\n` +
                                `━━━━━━━━━━━━━━━━━━━\n` +
                                `📱 **Range:** \`${hit.range}\`\n` +
                                `📞 **নম্বর:** \`${maskedCNum}\`\n` +
                                `🌍 **দেশ:** ${hit.country}\n\n` +
                                `💬 **CONSOLE MESSAGE:**\n\`${cMessage}\`\n` +
                                `━━━━━━━━━━━━━━━━━━━`;

                    await bot.sendMessage(GROUP_CHAT_ID, msg, { parse_mode: "Markdown" });
                    sentConsoleIds.add(consoleId);
                }
            }
        }
    } catch (e) {
        console.error(`❌ এরর: ${e.message}`);
    }
}

// প্রতি ৮ সেকেন্ড পর পর চেক করবে
setInterval(autoChecker, 8000);
