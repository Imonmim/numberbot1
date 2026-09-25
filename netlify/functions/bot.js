const fetch = require('node-fetch');

const BOT_TOKEN = process.env.BOT_TOKEN || "8701736168:AAHhfQUelJm-Fl3BCGQmQ55biNdzYP6_EXw";
const GROUP_CHAT_ID = process.env.GROUP_CHAT_ID || "-1004429028470";
const API_KEY = process.env.API_KEY || "MKR8MCYN7MZ"; 
const BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api";

const headers = { "mauthapi": API_KEY, "Content-Type": "application/json" };

function maskPhoneNumber(phone) {
    if (!phone || phone === "Unknown") return "Unknown";
    const p = String(phone);
    return p.length > 6 ? `${p.slice(0, 5)}★★★★★${p.slice(-3)}` : `${p.slice(0, 2)}★★★★★${p.slice(-2)}`;
}

exports.handler = async function(event, context) {
    try {
        // ওটিপি চেক
        const otpRes = await fetch(`${BASE_URL}/success-otp`, { headers });
        const otpResp = await otpRes.json();
        
        if (otpResp?.meta?.status === "ok") {
            for (const otpData of (otpResp?.data?.otps || [])) {
                const maskedNum = maskPhoneNumber(otpData.number);
                const msg = `⚡ **[SUCCESS LOG] NEW OTP** ⚡\n` +
                            `━━━━━━━━━━━━━━━━━━━\n` +
                            `🆔 **RID:** \`${otpResp.rid || 'N/A'}\`\n` +
                            `📱 **নম্বর:** \`${maskedNum}\`\n\n` +
                            `💬 **MESSAGE:**\n\`${otpData.message}\`\n` +
                            `━━━━━━━━━━━━━━━━━━━`;
                
                await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: GROUP_CHAT_ID, text: msg, parse_mode: 'Markdown' })
                });
            }
        }

        return {
            statusCode: 200,
            body: JSON.stringify({ message: "Checked successfully" })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
