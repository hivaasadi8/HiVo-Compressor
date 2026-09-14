"""
🎬 انیمیشن progress زنده با کنترل نرخ آپدیت
"""
import time
from typing import Callable, Awaitable


class LiveProgress:
    """کلاس برای مدیریت آپدیت‌های progress بدون اسپم"""

    def __init__(self, edit_func: Callable[[str], Awaitable], card_func: Callable,
                 min_interval: float = 2.5):
        self.edit_func = edit_func
        self.card_func = card_func
        self.min_interval = min_interval
        self.last_update = 0.0
        self.last_pct = -1.0
        self.start_time = time.time()

    async def update(self, pct: float):
        now = time.time()
        # آپدیت فقط اگه زمان کافی گذشته یا تغییر محسوس داشته
        if now - self.last_update < self.min_interval:
            return
        if abs(pct - self.last_pct) < 1.0:
            return

        self.last_update = now
        self.last_pct = pct

        elapsed = int(now - self.start_time)
        eta = int(elapsed / max(pct, 0.1) * (100 - pct)) if pct > 1 else 0

        try:
            await self.edit_func(self.card_func(pct, elapsed, eta))
        except Exception:
            # اگه پیام یکسان بود یا خطای شبکه، بی‌خیال
            pass
