"""Config for the Instagram Carousel Generator.

Self-contained and fully local: no API, no key, no paid services. The only
external dependency is Playwright's Chromium (for rendering HTML -> PNG).
"""
import os
from pathlib import Path

CAROUSEL_ROOT = Path(__file__).resolve().parent.parent   # .../carousel

# --- Paths ---
ASSETS_DIR = CAROUSEL_ROOT / "assets"
KNOWLEDGE_DIR = CAROUSEL_ROOT / "knowledge"
RUNS_DIR = CAROUSEL_ROOT / "runs"
OUTPUT_DIR = CAROUSEL_ROOT / "output"
TEMPLATE = CAROUSEL_ROOT / "scripts" / "template-activate.html"

# --- Output canvas: Instagram carousel 4:5 (1080x1350) ---
CANVAS_W = int(os.getenv("CAROUSEL_W", "1080"))
CANVAS_H = int(os.getenv("CAROUSEL_H", "1350"))
RENDER_SCALE = int(os.getenv("CAROUSEL_RENDER_SCALE", "2"))
