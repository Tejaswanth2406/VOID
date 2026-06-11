"""
CSTI Engine — Utilities
Logging, formatting, metrics, and helper functions.
"""

from __future__ import annotations
import time
import json
import math
import textwrap
from datetime import datetime
from typing import Any


# ── Color Terminal Output ──────────────────────────────────────────────────────

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE    = "\033[34m"
    WHITE   = "\033[37m"

    @staticmethod
    def bold(s: str) -> str:     return f"{Color.BOLD}{s}{Color.RESET}"
    @staticmethod
    def cyan(s: str) -> str:     return f"{Color.CYAN}{s}{Color.RESET}"
    @staticmethod
    def green(s: str) -> str:    return f"{Color.GREEN}{s}{Color.RESET}"
    @staticmethod
    def yellow(s: str) -> str:   return f"{Color.YELLOW}{s}{Color.RESET}"
    @staticmethod
    def red(s: str) -> str:      return f"{Color.RED}{s}{Color.RESET}"
    @staticmethod
    def magenta(s: str) -> str:  return f"{Color.MAGENTA}{s}{Color.RESET}"
    @staticmethod
    def dim(s: str) -> str:      return f"{Color.DIM}{s}{Color.RESET}"
    @staticmethod
    def blue(s: str) -> str:     return f"{Color.BLUE}{s}{Color.RESET}"


# ── Logger ─────────────────────────────────────────────────────────────────────

class CSTILogger:
    """Structured logger for the CSTI engine with level filtering and file output."""

    LEVELS = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "SILENT": 99}

    def __init__(self, name: str = "CSTI", level: str = "INFO", log_file: str | None = None):
        self.name = name
        self.level = self.LEVELS.get(level.upper(), 1)
        self.log_file = log_file
        self._entries: list[dict] = []

    def _write(self, level: str, msg: str, data: dict | None = None):
        if self.LEVELS.get(level, 0) < self.level:
            return
        ts = datetime.now().strftime("%H:%M:%S")
        entry = {"ts": ts, "level": level, "name": self.name, "msg": msg, "data": data}
        self._entries.append(entry)

        color_map = {
            "DEBUG": Color.dim,
            "INFO":  Color.cyan,
            "WARN":  Color.yellow,
            "ERROR": Color.red,
        }
        colorize = color_map.get(level, lambda x: x)
        prefix = f"{Color.dim(ts)} {colorize(f'[{self.name}:{level}]')}"
        print(f"{prefix} {msg}")
        if data and self.level == 0:
            print(Color.dim(json.dumps(data, indent=2)))

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")

    def debug(self, msg: str, data: dict | None = None): self._write("DEBUG", msg, data)
    def info(self,  msg: str, data: dict | None = None): self._write("INFO",  msg, data)
    def warn(self,  msg: str, data: dict | None = None): self._write("WARN",  msg, data)
    def error(self, msg: str, data: dict | None = None): self._write("ERROR", msg, data)

    def section(self, title: str):
        """Print a visible section divider."""
        if self.level <= 1:
            print(f"\n{Color.bold(Color.cyan('─' * 55))}")
            print(Color.bold(Color.cyan(f"  {title}")))
            print(Color.bold(Color.cyan('─' * 55)))

    def get_entries(self, level: str | None = None) -> list[dict]:
        if level is None:
            return self._entries
        return [e for e in self._entries if e["level"] == level]


# ── Metrics ────────────────────────────────────────────────────────────────────

class MetricsTracker:
    """Tracks numeric metrics over time with statistics."""

    def __init__(self):
        self._series: dict[str, list[tuple[float, float]]] = {}  # name → [(timestamp, value)]

    def record(self, name: str, value: float):
        if name not in self._series:
            self._series[name] = []
        self._series[name].append((time.time(), value))

    def latest(self, name: str) -> float | None:
        series = self._series.get(name, [])
        return series[-1][1] if series else None

    def mean(self, name: str) -> float | None:
        series = self._series.get(name, [])
        if not series:
            return None
        vals = [v for _, v in series]
        return sum(vals) / len(vals)

    def trend(self, name: str, window: int = 5) -> float:
        """Positive = improving, negative = declining."""
        series = self._series.get(name, [])
        if len(series) < 2:
            return 0.0
        recent = [v for _, v in series[-window:]]
        if len(recent) < 2:
            return 0.0
        return recent[-1] - recent[0]

    def summary(self) -> dict:
        result = {}
        for name, series in self._series.items():
            vals = [v for _, v in series]
            result[name] = {
                "latest": round(vals[-1], 4) if vals else None,
                "mean":   round(sum(vals) / len(vals), 4) if vals else None,
                "min":    round(min(vals), 4) if vals else None,
                "max":    round(max(vals), 4) if vals else None,
                "trend":  round(self.trend(name), 4),
                "count":  len(vals),
            }
        return result

    def ascii_sparkline(self, name: str, width: int = 20) -> str:
        """Render a small sparkline for a metric series."""
        series = self._series.get(name, [])
        if len(series) < 2:
            return "─" * width
        vals = [v for _, v in series[-width:]]
        mn, mx = min(vals), max(vals)
        if mx == mn:
            return "─" * len(vals)
        blocks = " ▁▂▃▄▅▆▇█"
        chars = []
        for v in vals:
            idx = int((v - mn) / (mx - mn) * (len(blocks) - 1))
            chars.append(blocks[idx])
        return "".join(chars)


# ── Text Formatting ────────────────────────────────────────────────────────────

def wrap(text: str, width: int = 70, indent: str = "") -> str:
    """Word-wrap text preserving paragraph breaks."""
    paragraphs = text.split("\n")
    result = []
    for para in paragraphs:
        if para.strip():
            result.append(textwrap.fill(para, width=width, initial_indent=indent,
                                        subsequent_indent=indent))
        else:
            result.append("")
    return "\n".join(result)


def truncate(text: str, max_len: int = 100, suffix: str = "…") -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len - len(suffix)] + suffix


def format_delta(before: float, after: float, label: str = "") -> str:
    delta = after - before
    sign = "+" if delta >= 0 else ""
    color = Color.green if delta >= 0 else Color.red
    return f"{label}{before:.4f} → {after:.4f} ({color(f'{sign}{delta:.4f}')})"


def render_bar(value: float, max_value: float = 1.0, width: int = 20,
               fill: str = "█", empty: str = "░") -> str:
    filled = int((value / max_value) * width) if max_value > 0 else 0
    filled = min(filled, width)
    return fill * filled + empty * (width - filled)


def format_table(rows: list[dict], columns: list[str] | None = None) -> str:
    """Format a list of dicts as an ASCII table."""
    if not rows:
        return "(empty)"
    cols = columns or list(rows[0].keys())
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    sep = "┼".join("─" * (widths[c] + 2) for c in cols)
    header = "│".join(f" {c:<{widths[c]}} " for c in cols)
    lines = [header, sep]
    for row in rows:
        lines.append("│".join(f" {str(row.get(c, '')):<{widths[c]}} " for c in cols))
    return "\n".join(lines)


# ── JSON helpers ───────────────────────────────────────────────────────────────

def safe_json_parse(text: str) -> dict | list | None:
    """Try to parse JSON, stripping markdown fences if present."""
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        # parts[1] is the code block content
        if len(parts) >= 2:
            text = parts[1]
            if text.startswith("json"):
                text = text[4:]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def pretty_json(obj: Any, indent: int = 2) -> str:
    return json.dumps(obj, indent=indent, default=str)


# ── Timing ─────────────────────────────────────────────────────────────────────

class Timer:
    """Simple context-manager timer."""

    def __init__(self, name: str = ""):
        self.name = name
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *_):
        self.elapsed = round(time.time() - self._start, 3)

    def __str__(self) -> str:
        return f"{self.name}: {self.elapsed}s" if self.name else f"{self.elapsed}s"


# ── Math helpers ───────────────────────────────────────────────────────────────

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    mn, mx = min(values), max(values)
    if mx == mn:
        return [0.5] * len(values)
    return [(v - mn) / (mx - mn) for v in values]


def weighted_mean(values: list[float], weights: list[float]) -> float:
    if not values or not weights:
        return 0.0
    total_w = sum(weights)
    if total_w == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / total_w