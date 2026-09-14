"""
🎨 دکمه‌های شیشه‌ای — با ایموجی معنادار
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(support: str = "HiVoSupport") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 آمار",    callback_data="stats"),
            InlineKeyboardButton("ℹ️ راهنما",  callback_data="help"),
        ],
        [InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{support}")],
    ])


def quality_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ سریع — فوری و کم‌حجم", callback_data="q:fast")],
        [InlineKeyboardButton("⚖️ متعادل — پیشنهاد ما ✨", callback_data="q:balanced")],
        [InlineKeyboardButton("💎 کیفیت — حفظ جزئیات",   callback_data="q:max")],
        [InlineKeyboardButton("🗑 لغو", callback_data="cancel")],
    ])


def result_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 منوی اصلی", callback_data="back")],
    ])


def stats_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 بروزرسانی", callback_data="stats")],
        [InlineKeyboardButton("◀ بازگشت",     callback_data="back")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 منوی اصلی", callback_data="back")],
    ])


def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 آمار کامل", callback_data="admin:stats"),
            InlineKeyboardButton("📢 پیام همگانی", callback_data="admin:broadcast"),
        ],
        [InlineKeyboardButton("◀ بازگشت", callback_data="back")],
    ])
