"""
🎨 کارت‌های HTML — گرافیک ۱۰/۱۰
هیچ پیامی متن خام نیست، همه کارت است.
"""
from datetime import datetime


# ═══════════════════════════════════════════
#   🔧 ابزارهای پایه
# ═══════════════════════════════════════════

def human_size(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    for u in ["KB", "MB", "GB", "TB"]:
        b /= 1024
        if b < 1024:
            return f"{b:.2f} {u}"
    return f"{b:.2f} PB"


def bar(pct: float, width: int = 18) -> str:
    pct = max(0, min(100, pct))
    f = int(pct / 100 * width)
    return "█" * f + "░" * (width - f)


def stars(ratio: float) -> str:
    if ratio >= 70: return "★★★★★"
    if ratio >= 55: return "★★★★☆"
    if ratio >= 40: return "★★★☆☆"
    if ratio >= 25: return "★★☆☆☆"
    if ratio >= 10: return "★☆☆☆☆"
    return "☆☆☆☆☆"


def box_top(title: str, icon: str = "⚡", width: int = 30) -> str:
    t = f"{icon} {title}"
    return f"╔{'═' * width}╗\n║ {t}{' ' * max(0, width - len(t) - 1)}║\n╚{'═' * width}╝"


def divider(char: str = "─", width: int = 32) -> str:
    return char * width


# ═══════════════════════════════════════════
#   🚀 1. خوش‌آمد
# ═══════════════════════════════════════════

def welcome(name: str, total_users: int, encoder: str, cores: int) -> str:
    return f"""{box_top("HiVo Compressor", "⚡")}

👋 سلام <b>{name}</b> عزیز!

╭─ 🎯 <b>چی فشرده می‌کنم</b>
│  🎬 ویدئو  ·  MP4 MKV AVI MOV
│  🖼️ عکس   ·  JPG PNG BMP
│  🎵 صدا   ·  MP3 WAV FLAC
│  📕 PDF   ·  سند
│  📦 فایل  ·  ZIP RAR ZST
╰────────────────────────

╭─ 🚀 <b>موتور فشرده‌سازی</b>
│  ⚙️ {encoder}
│  🔧 {cores} هسته CPU
│  ⚡ Multi-threaded
╰────────────────────────

╭─ 📊 <b>آمار زنده</b>
│  👥 کاربران: <code>{total_users:,}</code>
│  🕐 زمان: <code>{datetime.now():%H:%M}</code>
╰────────────────────────

{divider()}
📥 <b>فایل رو بفرست تا شروع کنیم!</b>
{divider()}"""


# ═══════════════════════════════════════════
#   📥 2. دریافت فایل
# ═══════════════════════════════════════════

def file_received(name: str, size: int, category: str, emoji: str, mime: str) -> str:
    short = name if len(name) <= 34 else name[:31] + "..."
    mime_short = mime.split("/")[-1].upper()

    return f"""{box_top("فایل دریافت شد", "📥")}

{emoji} <b>نام:</b>
   <code>{short}</code>

╭─ 📊 <b>مشخصات</b>
│  📦 حجم:  <code>{human_size(size)}</code>
│  🏷 نوع:  <code>{category}</code>
│  🔧 فرمت: <code>{mime_short}</code>
│  🕐 زمان: <code>{datetime.now():%H:%M:%S}</code>
╰────────────────────────

{divider()}
🎚 <b>سطح فشرده‌سازی رو انتخاب کن:</b>
{divider()}

⚡ <b>سریع</b>   → کم‌حجم‌ترین، فوری
⚖️ <b>متعادل</b> → پیشنهاد ما ✨
💎 <b>کیفیت</b>  → حفظ جزئیات"""


# ═══════════════════════════════════════════
#   ⏳ 3. دانلود
# ═══════════════════════════════════════════

def downloading(name: str, size: int, pct: float = 0.0) -> str:
    short = name if len(name) <= 34 else name[:31] + "..."
    return f"""{box_top("دریافت از تلگرام", "⏳")}

📄 <code>{short}</code>
📦 <b>حجم:</b> <code>{human_size(size)}</code>

{divider()}
<code>{bar(pct)}</code>  <b>{pct:5.1f}%</b>
{divider()}

🔽 در حال دانلود از سرور تلگرام...
<i>لطفاً صبر کن</i>"""


# ═══════════════════════════════════════════
#   ⚙️ 4. فشرده‌سازی (progress زنده)
# ═══════════════════════════════════════════

def compressing(name: str, pct: float, elapsed: int, eta: int,
                stage: str = "Encoding", encoder: str = "auto",
                mode_label: str = "⚖️ متعادل") -> str:
    short = name if len(name) <= 34 else name[:31] + "..."
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"][int(elapsed * 2) % 10]

    eta_str = f"~{eta}s" if eta > 0 else "—"

    return f"""{box_top("فشرده‌سازی جاری", "⚙️")}

📄 <code>{short}</code>
🎚 <b>سطح:</b> {mode_label}

{divider()}
<code>{bar(pct)}</code>  <b>{pct:5.1f}%</b>
{divider()}

{spinner} <b>مرحله:</b> <code>{stage}</code>
🚀 <b>موتور:</b> <code>{encoder}</code>

╭─ ⏱ <b>زمان</b>
│  سپری: <code>{elapsed}s</code>
│  باقی: <code>{eta_str}</code>
╰────────────────────────

<i>💡 پنجره رو نبند...</i>"""


# ═══════════════════════════════════════════
#   ✅ 5. نتیجه
# ═══════════════════════════════════════════

def result(original: int, compressed: int, ratio: float,
           encoder: str, elapsed: float, mode: str) -> str:
    saved = original - compressed
    mode_fa = {"fast": "⚡ سریع", "balanced": "⚖️ متعادل", "max": "💎 کیفیت"}.get(mode, mode)

    if ratio >= 50:
        verdict = "🎉 فوق‌العاده!"
    elif ratio >= 30:
        verdict = "✅ عالی"
    elif ratio >= 15:
        verdict = "👍 خوب"
    elif ratio > 0:
        verdict = "😐 کم"
    else:
        verdict = "⚠️ فایده‌ای نداشت"

    return f"""{box_top("فشرده‌سازی کامل!", "✅")}

🏆 <b>امتیاز:</b> {stars(ratio)}
📣 <b>{verdict}</b>

╭─ 📊 <b>آمار</b>
│  📥 اصلی:  <code>{human_size(original)}</code>
│  📤 جدید:  <code>{human_size(compressed)}</code>
│  💾 صرفه:  <code>{human_size(saved)}</code>
│  📉 کاهش:  <b>{ratio}%</b>
╰────────────────────────

╭─ ⚙️ <b>موتور</b>
│  🎚 سطح:  {mode_fa}
│  🚀 موتور: <code>{encoder}</code>
│  ⏱ زمان:  <code>{elapsed:.1f}s</code>
╰────────────────────────

{divider()}
📤 <b>فایل فشرده در راهه...</b>"""


def result_caption(compressed: int, ratio: float) -> str:
    return (
        f"╭──────────────────────╮\n"
        f"│  ✅ <b>HiVo Compressed</b>  │\n"
        f"╰──────────────────────╯\n"
        f"📦 <b>حجم نهایی:</b> <code>{human_size(compressed)}</code>\n"
        f"💾 <b>صرفه‌جویی:</b> <b>{ratio}%</b>\n"
        f"⚡ <i>ساخته‌شده با HiVo Compressor</i>"
    )


# ═══════════════════════════════════════════
#   ❌ 6. خطا
# ═══════════════════════════════════════════

def error_card(reason: str, hint: str = "") -> str:
    return f"""{box_top("خطا رخ داد", "❌")}

⚠️ <b>مشکل:</b>
   <code>{reason}</code>

{f"💡 <b>راهکار:</b>{chr(10)}   <i>{hint}</i>" if hint else ""}

{divider()}
🔁 دوباره تلاش کن یا فایل دیگه بفرست."""


# ═══════════════════════════════════════════
#   ⏸️ 7. Rate limit
# ═══════════════════════════════════════════

def rate_limit_card(seconds: int) -> str:
    return f"""{box_top("کمی صبر کن!", "⏸️")}

⏱ <b>زمان باقی‌مانده:</b> <code>{seconds}s</code>

برای جلوگیری از فشار روی سرور،
بین درخواست‌ها فاصله لازمه.

{divider()}
🙏 ممنون از صبرت!"""


# ═══════════════════════════════════════════
#   📊 8. آمار
# ═══════════════════════════════════════════

def stats_card(d: dict) -> str:
    return f"""{box_top("آمار زنده HiVo", "📊")}

╭─ 👥 <b>کاربران</b>
│  کل: <code>{d.get('users', 0):,}</code>
│  فعال امروز: <code>{d.get('today', 0):,}</code>
╰────────────────────────

╭─ 📁 <b>فایل‌های فشرده‌شده</b>
│  🎬 ویدئو: <code>{d.get('videos', 0):,}</code>
│  🖼️ عکس:   <code>{d.get('images', 0):,}</code>
│  🎵 صدا:   <code>{d.get('audios', 0):,}</code>
│  📕 PDF:   <code>{d.get('pdfs', 0):,}</code>
│  📦 فایل:  <code>{d.get('files', 0):,}</code>
╰────────────────────────

╭─ 💾 <b>صرفه‌جویی کل</b>
│  <code>{human_size(d.get('total_saved', 0))}</code>
╰────────────────────────

╭─ 🏆 <b>Top کاربران</b>
│  🥇 {d.get('top1', '—')}
│  🥈 {d.get('top2', '—')}
│  🥉 {d.get('top3', '—')}
╰────────────────────────

🕐 <b>آخرین بروزرسانی:</b> <code>{datetime.now():%H:%M}</code>"""


# ═══════════════════════════════════════════
#   ℹ️ 9. راهنما
# ═══════════════════════════════════════════

def help_card(support: str) -> str:
    return f"""{box_top("راهنمای HiVo", "ℹ️")}

╭─ 🎯 <b>چطور فشرده کنم؟</b>
│  1️⃣ فایل رو بفرست
│  2️⃣ سطح رو انتخاب کن
│  3️⃣ منتظر بمون
│  4️⃣ دریافت کن
╰────────────────────────

╭─ 🎚 <b>سطوح فشرده‌سازی</b>
│  ⚡ <b>سریع</b>
│     └ کم‌ترین حجم، سریع‌ترین
│  ⚖️ <b>متعادل</b> <i>(پیشنهاد)</i>
│     └ توازن بهینه
│  💎 <b>کیفیت</b>
│     └ حفظ جزئیات
╰────────────────────────

╭─ 📌 <b>نکات مهم</b>
│  • حداکثر حجم: <b>1.9 GB</b>
│  • ویدئو تا <b>90%</b> کاهش
│  • عکس‌ها → WebP
│  • PDF → Ghostscript
╰────────────────────────

{divider()}
📞 <b>پشتیبانی:</b> @{support}"""


# ═══════════════════════════════════════════
#   🎬 10. آماده‌سازی
# ═══════════════════════════════════════════

def preparing(name: str, mode: str) -> str:
    mode_fa = {"fast": "⚡ سریع", "balanced": "⚖️ متعادل", "max": "💎 کیفیت"}.get(mode, mode)
    short = name if len(name) <= 34 else name[:31] + "..."
    return f"""{box_top("آماده‌سازی...", "🎬")}

📄 <code>{short}</code>
🎚 <b>سطح انتخابی:</b> {mode_fa}

{divider()}
⏳ در حال آماده‌سازی موتور...
<i>چند لحظه صبر کن</i>"""


# ═══════════════════════════════════════════
#   👑 11. پنل ادمین
# ═══════════════════════════════════════════

def admin_panel(d: dict) -> str:
    return f"""{box_top("پنل مدیریت", "👑")}

╭─ 📊 <b>آمار کلی</b>
│  👥 کاربران: <code>{d.get('users', 0):,}</code>
│  📁 فایل‌ها: <code>{d.get('total_files', 0):,}</code>
│  💾 صرفه:    <code>{human_size(d.get('total_saved', 0))}</code>
╰────────────────────────

╭─ ⚙️ <b>وضعیت</b>
│  🚀 اجرا: <code>{d.get('uptime', '—')}</code>
│  📡 Run ID: <code>{d.get('run_id', '—')}</code>
╰────────────────────────

{divider()}
🎯 یه گزینه رو انتخاب کن:"""
