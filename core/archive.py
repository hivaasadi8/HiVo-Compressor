"""
📦 موتور فشرده‌سازی فایل/آرشیو
Zstd (سریع + بهترین)
"""
import asyncio
from pathlib import Path


class ArchiveCompressor:
    LEVELS = {"fast": 3, "balanced": 10, "max": 19}

    @classmethod
    async def compress(cls, input_path: Path, output_path: Path,
                       mode: str = "balanced", progress_cb=None) -> dict:
        original = input_path.stat().st_size
        level = cls.LEVELS.get(mode, 10)

        # -T0 یعنی استفاده از همه‌ی هسته‌ها
        cmd = [
            "zstd",
            f"-{level}",
            "-T0",
            "--long=27",
            "-f",
            str(input_path),
            "-o", str(output_path),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"Zstd failed: {stderr.decode()[:200]}")

        compressed = output_path.stat().st_size

        return {
            "original_size":   original,
            "compressed_size": compressed,
            "ratio":           round((1 - compressed / original) * 100, 1),
            "encoder":         f"Zstd-{level}",
        }
