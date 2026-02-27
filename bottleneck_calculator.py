"""
Bottleneck Calculator v3.0.0
- Light / Dark mode toggle
- Searchable dropdowns
- Simplified motherboard names (H510, B550, Z790…)
- Low Profile GPU models included
- VRAM shown in GPU names (8GB, 16GB…)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from dataclasses import dataclass

GITHUB_REPO   = "YOUR_USERNAME/BottleneckCalculator"
CURRENT_VER   = "3.0.0"
RELEASES_URL  = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
DOWNLOAD_PAGE = f"https://github.com/{GITHUB_REPO}/releases/latest"

# ─────────────────────────── THEMES ──────────────────────────────────────────
THEMES = {
    "light": {
        "primary":        "#1976D2",
        "primary_dark":   "#0D47A1",
        "primary_light":  "#BBDEFB",
        "accent":         "#FF6D00",
        "bg":             "#F5F5F5",
        "card":           "#FFFFFF",
        "error":          "#D32F2F",
        "warning":        "#F57C00",
        "success":        "#2E7D32",
        "on_primary":     "#FFFFFF",
        "on_bg":          "#212121",
        "on_surface":     "#212121",
        "secondary_text": "#616161",
        "divider":        "#BDBDBD",
        "shadow":         "#E0E0E0",
        "entry_bg":       "#FFFFFF",
        "entry_fg":       "#212121",
        "list_bg":        "#FFFFFF",
        "list_select":    "#BBDEFB",
        "topbar_bg":      "#1976D2",
        "topbar_fg":      "#FFFFFF",
        "topbar_sub":     "#BBDEFB",
        "gauge_track":    "#E0E0E0",
        "toggle_bg":      "#E3F2FD",
        "toggle_fg":      "#1976D2",
    },
    "dark": {
        "primary":        "#42A5F5",
        "primary_dark":   "#1565C0",
        "primary_light":  "#1E3A5F",
        "accent":         "#FF9800",
        "bg":             "#121212",
        "card":           "#1E1E1E",
        "error":          "#EF5350",
        "warning":        "#FFA726",
        "success":        "#66BB6A",
        "on_primary":     "#FFFFFF",
        "on_bg":          "#E0E0E0",
        "on_surface":     "#E0E0E0",
        "secondary_text": "#9E9E9E",
        "divider":        "#333333",
        "shadow":         "#000000",
        "entry_bg":       "#2C2C2C",
        "entry_fg":       "#E0E0E0",
        "list_bg":        "#2C2C2C",
        "list_select":    "#1E3A5F",
        "topbar_bg":      "#0D1B2A",
        "topbar_fg":      "#E0E0E0",
        "topbar_sub":     "#42A5F5",
        "gauge_track":    "#333333",
        "toggle_bg":      "#1E3A5F",
        "toggle_fg":      "#42A5F5",
    }
}

T = THEMES["light"].copy()   # active theme — mutated on toggle

# ─────────────────────────── DATA MODELS ─────────────────────────────────────
@dataclass
class CPU:
    name: str; cores: int; threads: int
    base_ghz: float; boost_ghz: float; tdp: int
    perf_score: int; socket: str; generation: str

@dataclass
class GPU:
    name: str; vram_gb: int; tdp: int
    perf_score: int; vendor: str; low_profile: bool = False

@dataclass
class Motherboard:
    name: str; socket: str; chipset: str
    max_ram_gb: int; pcie_gen: int

# ══════════════════════════════════════════════════════════════════════════════
#  CPU DATABASE
# ══════════════════════════════════════════════════════════════════════════════
CPU_LIST = [
    # Intel Arrow Lake LGA1851
    CPU("Intel Core Ultra 9 285K",   24,24,3.7,5.7,125, 92,"LGA1851","Arrow Lake"),
    CPU("Intel Core Ultra 7 265K",   20,20,3.9,5.5,125, 88,"LGA1851","Arrow Lake"),
    CPU("Intel Core Ultra 7 265KF",  20,20,3.9,5.5,125, 88,"LGA1851","Arrow Lake"),
    CPU("Intel Core Ultra 5 245K",   14,14,4.2,5.2,125, 82,"LGA1851","Arrow Lake"),
    CPU("Intel Core Ultra 5 245KF",  14,14,4.2,5.2,125, 82,"LGA1851","Arrow Lake"),
    # Intel 14th Gen LGA1700
    CPU("Intel Core i9-14900KS",     24,32,3.2,6.2,150, 93,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i9-14900K",      24,32,3.2,6.0,125, 91,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i9-14900KF",     24,32,3.2,6.0,125, 91,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i9-14900F",      24,32,2.0,5.8, 65, 87,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i7-14700K",      20,28,3.4,5.6,125, 88,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i7-14700KF",     20,28,3.4,5.6,125, 88,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i7-14700F",      20,28,2.1,5.4, 65, 84,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i5-14600K",      14,20,3.5,5.3,125, 80,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i5-14600KF",     14,20,3.5,5.3,125, 80,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i5-14500",       14,20,2.6,5.0, 65, 75,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i5-14400F",      10,16,2.5,4.7, 65, 68,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i5-14400",       10,16,2.5,4.7, 65, 68,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i3-14100F",       4, 8,3.5,4.7, 58, 52,"LGA1700","Raptor Lake Refresh"),
    CPU("Intel Core i3-14100",        4, 8,3.5,4.7, 58, 52,"LGA1700","Raptor Lake Refresh"),
    # Intel 13th Gen LGA1700
    CPU("Intel Core i9-13900KS",     24,32,3.2,6.0,150, 92,"LGA1700","Raptor Lake"),
    CPU("Intel Core i9-13900K",      24,32,3.0,5.8,125, 90,"LGA1700","Raptor Lake"),
    CPU("Intel Core i9-13900KF",     24,32,3.0,5.8,125, 90,"LGA1700","Raptor Lake"),
    CPU("Intel Core i9-13900F",      24,32,2.0,5.6, 65, 86,"LGA1700","Raptor Lake"),
    CPU("Intel Core i7-13700K",      16,24,3.4,5.4,125, 86,"LGA1700","Raptor Lake"),
    CPU("Intel Core i7-13700KF",     16,24,3.4,5.4,125, 86,"LGA1700","Raptor Lake"),
    CPU("Intel Core i7-13700F",      16,24,2.1,5.2, 65, 82,"LGA1700","Raptor Lake"),
    CPU("Intel Core i5-13600K",      14,20,3.5,5.1,125, 79,"LGA1700","Raptor Lake"),
    CPU("Intel Core i5-13600KF",     14,20,3.5,5.1,125, 79,"LGA1700","Raptor Lake"),
    CPU("Intel Core i5-13500",       14,20,2.5,4.8, 65, 73,"LGA1700","Raptor Lake"),
    CPU("Intel Core i5-13400F",      10,16,2.5,4.6, 65, 66,"LGA1700","Raptor Lake"),
    CPU("Intel Core i5-13400",       10,16,2.5,4.6, 65, 66,"LGA1700","Raptor Lake"),
    CPU("Intel Core i3-13100F",       4, 8,3.4,4.5, 58, 50,"LGA1700","Raptor Lake"),
    CPU("Intel Core i3-13100",        4, 8,3.4,4.5, 58, 50,"LGA1700","Raptor Lake"),
    # Intel 12th Gen LGA1700
    CPU("Intel Core i9-12900KS",     16,24,3.4,5.5,150, 84,"LGA1700","Alder Lake"),
    CPU("Intel Core i9-12900K",      16,24,3.2,5.2,125, 82,"LGA1700","Alder Lake"),
    CPU("Intel Core i9-12900KF",     16,24,3.2,5.2,125, 82,"LGA1700","Alder Lake"),
    CPU("Intel Core i7-12700K",      12,20,3.6,5.0,125, 78,"LGA1700","Alder Lake"),
    CPU("Intel Core i7-12700KF",     12,20,3.6,5.0,125, 78,"LGA1700","Alder Lake"),
    CPU("Intel Core i7-12700F",      12,20,2.1,4.9, 65, 75,"LGA1700","Alder Lake"),
    CPU("Intel Core i5-12600K",      10,16,3.7,4.9,125, 72,"LGA1700","Alder Lake"),
    CPU("Intel Core i5-12600KF",     10,16,3.7,4.9,125, 72,"LGA1700","Alder Lake"),
    CPU("Intel Core i5-12500",        6,12,3.0,4.6, 65, 65,"LGA1700","Alder Lake"),
    CPU("Intel Core i5-12400F",       6,12,2.5,4.4, 65, 63,"LGA1700","Alder Lake"),
    CPU("Intel Core i5-12400",        6,12,2.5,4.4, 65, 63,"LGA1700","Alder Lake"),
    CPU("Intel Core i3-12100F",       4, 8,3.3,4.3, 58, 47,"LGA1700","Alder Lake"),
    CPU("Intel Core i3-12100",        4, 8,3.3,4.3, 58, 47,"LGA1700","Alder Lake"),
    # Intel 11th Gen LGA1200
    CPU("Intel Core i9-11900K",       8,16,3.5,5.2,125, 65,"LGA1200","Rocket Lake"),
    CPU("Intel Core i9-11900KF",      8,16,3.5,5.2,125, 65,"LGA1200","Rocket Lake"),
    CPU("Intel Core i7-11700K",       8,16,3.6,5.0,125, 62,"LGA1200","Rocket Lake"),
    CPU("Intel Core i7-11700KF",      8,16,3.6,5.0,125, 62,"LGA1200","Rocket Lake"),
    CPU("Intel Core i7-11700F",       8,16,2.5,4.9, 65, 59,"LGA1200","Rocket Lake"),
    CPU("Intel Core i5-11600K",       6,12,3.9,4.9,125, 57,"LGA1200","Rocket Lake"),
    CPU("Intel Core i5-11600KF",      6,12,3.9,4.9,125, 57,"LGA1200","Rocket Lake"),
    CPU("Intel Core i5-11400F",       6,12,2.6,4.4, 65, 52,"LGA1200","Rocket Lake"),
    CPU("Intel Core i3-11100F",       4, 8,3.6,4.4, 65, 42,"LGA1200","Rocket Lake"),
    # Intel 10th Gen LGA1200
    CPU("Intel Core i9-10900K",      10,20,3.7,5.3,125, 60,"LGA1200","Comet Lake"),
    CPU("Intel Core i9-10900KF",     10,20,3.7,5.3,125, 60,"LGA1200","Comet Lake"),
    CPU("Intel Core i7-10700K",       8,16,3.8,5.1,125, 57,"LGA1200","Comet Lake"),
    CPU("Intel Core i7-10700KF",      8,16,3.8,5.1,125, 57,"LGA1200","Comet Lake"),
    CPU("Intel Core i7-10700F",       8,16,2.9,4.8, 65, 54,"LGA1200","Comet Lake"),
    CPU("Intel Core i5-10600K",       6,12,4.1,4.8,125, 52,"LGA1200","Comet Lake"),
    CPU("Intel Core i5-10600KF",      6,12,4.1,4.8,125, 52,"LGA1200","Comet Lake"),
    CPU("Intel Core i5-10400F",       6,12,2.9,4.3, 65, 46,"LGA1200","Comet Lake"),
    CPU("Intel Core i5-10400",        6,12,2.9,4.3, 65, 46,"LGA1200","Comet Lake"),
    CPU("Intel Core i3-10100F",       4, 8,3.6,4.3, 65, 38,"LGA1200","Comet Lake"),
    CPU("Intel Core i3-10100",        4, 8,3.6,4.3, 65, 38,"LGA1200","Comet Lake"),
    # Intel 9th Gen LGA1151
    CPU("Intel Core i9-9900KS",       8,16,4.0,5.0,127, 56,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i9-9900K",        8,16,3.6,5.0, 95, 54,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i9-9900KF",       8,16,3.6,5.0, 95, 54,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i7-9700K",        8, 8,3.6,4.9, 95, 50,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i7-9700KF",       8, 8,3.6,4.9, 95, 50,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i5-9600K",        6, 6,3.7,4.6, 95, 45,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i5-9600KF",       6, 6,3.7,4.6, 95, 45,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i5-9400F",        6, 6,2.9,4.1, 65, 40,"LGA1151","Coffee Lake R"),
    CPU("Intel Core i3-9100F",        4, 4,3.6,4.2, 65, 33,"LGA1151","Coffee Lake R"),
    # Intel 8th Gen LGA1151
    CPU("Intel Core i7-8700K",        6,12,3.7,4.7, 95, 47,"LGA1151","Coffee Lake"),
    CPU("Intel Core i7-8700",         6,12,3.2,4.6, 65, 44,"LGA1151","Coffee Lake"),
    CPU("Intel Core i5-8600K",        6, 6,3.6,4.3, 95, 41,"LGA1151","Coffee Lake"),
    CPU("Intel Core i5-8400",         6, 6,2.8,4.0, 65, 37,"LGA1151","Coffee Lake"),
    CPU("Intel Core i3-8100",         4, 4,3.6,3.6, 65, 30,"LGA1151","Coffee Lake"),
    # Intel 7th Gen LGA1151
    CPU("Intel Core i7-7700K",        4, 8,4.2,4.5, 91, 38,"LGA1151","Kaby Lake"),
    CPU("Intel Core i7-7700",         4, 8,3.6,4.2, 65, 35,"LGA1151","Kaby Lake"),
    CPU("Intel Core i5-7600K",        4, 4,3.8,4.2, 91, 32,"LGA1151","Kaby Lake"),
    CPU("Intel Core i5-7500",         4, 4,3.4,3.8, 65, 29,"LGA1151","Kaby Lake"),
    CPU("Intel Core i3-7100",         2, 4,3.9,3.9, 51, 22,"LGA1151","Kaby Lake"),
    # Intel 6th Gen LGA1151
    CPU("Intel Core i7-6700K",        4, 8,4.0,4.2, 91, 35,"LGA1151","Skylake"),
    CPU("Intel Core i7-6700",         4, 8,3.4,4.0, 65, 32,"LGA1151","Skylake"),
    CPU("Intel Core i5-6600K",        4, 4,3.5,3.9, 91, 28,"LGA1151","Skylake"),
    CPU("Intel Core i5-6500",         4, 4,3.2,3.6, 65, 25,"LGA1151","Skylake"),
    CPU("Intel Core i3-6100",         2, 4,3.7,3.7, 51, 19,"LGA1151","Skylake"),
    # Intel HEDT LGA2066
    CPU("Intel Core i9-10980XE",     18,36,3.0,4.8,165, 78,"LGA2066","Cascade Lake-X"),
    CPU("Intel Core i9-10940X",      14,28,3.3,4.8,165, 74,"LGA2066","Cascade Lake-X"),
    CPU("Intel Core i9-10920X",      12,24,3.5,4.8,165, 71,"LGA2066","Cascade Lake-X"),
    CPU("Intel Core i9-10900X",      10,20,3.5,4.7,165, 68,"LGA2066","Cascade Lake-X"),
    CPU("Intel Core i9-9980XE",      18,36,3.0,4.5,165, 72,"LGA2066","Skylake-X"),
    CPU("Intel Core i7-9800X",        8,16,3.8,4.5,165, 60,"LGA2066","Skylake-X"),
    # Intel HEDT LGA2011-3
    CPU("Intel Core i7-6950X",       10,20,3.0,3.5,140, 45,"LGA2011-3","Broadwell-E"),
    CPU("Intel Core i7-6900K",        8,16,3.2,3.7,140, 40,"LGA2011-3","Broadwell-E"),
    # AMD Ryzen 9000 Zen 5 AM5
    CPU("AMD Ryzen 9 9950X",         16,32,4.3,5.7,170, 97,"AM5","Zen 5"),
    CPU("AMD Ryzen 9 9900X",         12,24,4.4,5.6,120, 91,"AM5","Zen 5"),
    CPU("AMD Ryzen 7 9800X3D",        8,16,4.7,5.2,120,100,"AM5","Zen 5"),
    CPU("AMD Ryzen 7 9700X",          8,16,3.8,5.5, 65, 87,"AM5","Zen 5"),
    CPU("AMD Ryzen 5 9600X",          6,12,3.9,5.4, 65, 82,"AM5","Zen 5"),
    CPU("AMD Ryzen 5 9600",           6,12,3.8,5.3, 65, 80,"AM5","Zen 5"),
    # AMD Ryzen 7000 Zen 4 AM5
    CPU("AMD Ryzen 9 7950X",         16,32,4.5,5.7,170, 95,"AM5","Zen 4"),
    CPU("AMD Ryzen 9 7950X3D",       16,32,4.2,5.7,120, 98,"AM5","Zen 4"),
    CPU("AMD Ryzen 9 7900X",         12,24,4.7,5.6,170, 89,"AM5","Zen 4"),
    CPU("AMD Ryzen 9 7900X3D",       12,24,4.4,5.6,120, 92,"AM5","Zen 4"),
    CPU("AMD Ryzen 9 7900",          12,24,3.7,5.4, 65, 86,"AM5","Zen 4"),
    CPU("AMD Ryzen 7 7800X3D",        8,16,4.5,5.0,120, 96,"AM5","Zen 4"),
    CPU("AMD Ryzen 7 7700X",          8,16,4.5,5.4,105, 85,"AM5","Zen 4"),
    CPU("AMD Ryzen 7 7700",           8,16,3.8,5.3, 65, 82,"AM5","Zen 4"),
    CPU("AMD Ryzen 5 7600X",          6,12,4.7,5.3,105, 78,"AM5","Zen 4"),
    CPU("AMD Ryzen 5 7600",           6,12,3.8,5.1, 65, 75,"AM5","Zen 4"),
    CPU("AMD Ryzen 5 7500F",          6,12,3.7,5.0, 65, 73,"AM5","Zen 4"),
    # AMD Ryzen 5000 Zen 3 AM4
    CPU("AMD Ryzen 9 5950X",         16,32,3.4,4.9,105, 88,"AM4","Zen 3"),
    CPU("AMD Ryzen 9 5900X",         12,24,3.7,4.8,105, 83,"AM4","Zen 3"),
    CPU("AMD Ryzen 9 5900",          12,24,3.0,4.7, 65, 80,"AM4","Zen 3"),
    CPU("AMD Ryzen 7 5800X3D",        8,16,3.4,4.5,105, 87,"AM4","Zen 3"),
    CPU("AMD Ryzen 7 5800X",          8,16,3.8,4.7,105, 78,"AM4","Zen 3"),
    CPU("AMD Ryzen 7 5800",           8,16,3.4,4.6, 65, 75,"AM4","Zen 3"),
    CPU("AMD Ryzen 5 5600X",          6,12,3.7,4.6, 65, 72,"AM4","Zen 3"),
    CPU("AMD Ryzen 5 5600",           6,12,3.5,4.4, 65, 69,"AM4","Zen 3"),
    CPU("AMD Ryzen 5 5600G",          6,12,3.9,4.4, 65, 64,"AM4","Zen 3"),
    CPU("AMD Ryzen 5 5500",           6,12,3.6,4.2, 65, 60,"AM4","Zen 3"),
    CPU("AMD Ryzen 3 5300G",          4, 8,4.0,4.2, 65, 47,"AM4","Zen 3"),
    CPU("AMD Ryzen 3 5100",           4, 8,3.8,3.8, 65, 40,"AM4","Zen 3"),
    # AMD Ryzen 3000 Zen 2 AM4
    CPU("AMD Ryzen 9 3950X",         16,32,3.5,4.7,105, 78,"AM4","Zen 2"),
    CPU("AMD Ryzen 9 3900X",         12,24,3.8,4.6,105, 72,"AM4","Zen 2"),
    CPU("AMD Ryzen 9 3900",          12,24,3.1,4.3, 65, 68,"AM4","Zen 2"),
    CPU("AMD Ryzen 7 3800X",          8,16,3.9,4.5,105, 65,"AM4","Zen 2"),
    CPU("AMD Ryzen 7 3800XT",         8,16,3.9,4.7,105, 66,"AM4","Zen 2"),
    CPU("AMD Ryzen 7 3700X",          8,16,3.6,4.4, 65, 63,"AM4","Zen 2"),
    CPU("AMD Ryzen 5 3600X",          6,12,3.8,4.4, 95, 60,"AM4","Zen 2"),
    CPU("AMD Ryzen 5 3600XT",         6,12,3.8,4.5, 95, 61,"AM4","Zen 2"),
    CPU("AMD Ryzen 5 3600",           6,12,3.6,4.2, 65, 57,"AM4","Zen 2"),
    CPU("AMD Ryzen 5 3500X",          6, 6,3.6,4.1, 65, 52,"AM4","Zen 2"),
    CPU("AMD Ryzen 3 3300X",          4, 8,3.8,4.3, 65, 43,"AM4","Zen 2"),
    CPU("AMD Ryzen 3 3100",           4, 8,3.6,3.9, 65, 39,"AM4","Zen 2"),
    # AMD Ryzen 2000 Zen+ AM4
    CPU("AMD Ryzen 7 2700X",          8,16,3.7,4.3,105, 52,"AM4","Zen+"),
    CPU("AMD Ryzen 7 2700",           8,16,3.2,4.1, 65, 48,"AM4","Zen+"),
    CPU("AMD Ryzen 5 2600X",          6,12,3.6,4.2, 95, 46,"AM4","Zen+"),
    CPU("AMD Ryzen 5 2600",           6,12,3.4,3.9, 65, 43,"AM4","Zen+"),
    CPU("AMD Ryzen 3 2200G",          4, 4,3.5,3.7, 65, 30,"AM4","Zen+"),
    # AMD Ryzen 1000 Zen AM4
    CPU("AMD Ryzen 7 1800X",          8,16,3.6,4.0, 95, 44,"AM4","Zen"),
    CPU("AMD Ryzen 7 1700X",          8,16,3.4,3.8, 95, 41,"AM4","Zen"),
    CPU("AMD Ryzen 7 1700",           8,16,3.0,3.7, 65, 38,"AM4","Zen"),
    CPU("AMD Ryzen 5 1600X",          6,12,3.6,4.0, 95, 38,"AM4","Zen"),
    CPU("AMD Ryzen 5 1600",           6,12,3.2,3.6, 65, 35,"AM4","Zen"),
    CPU("AMD Ryzen 5 1500X",          4, 8,3.5,3.7, 65, 29,"AM4","Zen"),
    CPU("AMD Ryzen 3 1300X",          4, 4,3.5,3.7, 65, 27,"AM4","Zen"),
    CPU("AMD Ryzen 3 1200",           4, 4,3.1,3.4, 65, 23,"AM4","Zen"),
    # AMD Threadripper sTRX4
    CPU("AMD Threadripper 3990X",    64,128,2.9,4.3,280, 90,"sTRX4","Zen 2"),
    CPU("AMD Threadripper 3970X",    32, 64,3.7,4.5,280, 86,"sTRX4","Zen 2"),
    CPU("AMD Threadripper 3960X",    24, 48,3.8,4.5,280, 83,"sTRX4","Zen 2"),
    # AMD Threadripper TR4
    CPU("AMD Threadripper 2990WX",   32, 64,3.0,4.2,250, 72,"TR4","Zen+"),
    CPU("AMD Threadripper 2950X",    16, 32,3.5,4.4,180, 64,"TR4","Zen+"),
    CPU("AMD Threadripper 2920X",    12, 24,3.5,4.3,180, 58,"TR4","Zen+"),
    # AMD Threadripper PRO sTR5
    CPU("AMD Threadripper PRO 7985WX",64,128,3.2,5.1,350, 99,"sTR5","Zen 4"),
    CPU("AMD Threadripper PRO 7965WX",24, 48,3.8,5.3,350, 96,"sTR5","Zen 4"),
    CPU("AMD Threadripper PRO 7955WX",16, 32,4.5,5.3,350, 93,"sTR5","Zen 4"),
]

# ══════════════════════════════════════════════════════════════════════════════
#  GPU DATABASE  — names include VRAM size. Low Profile models tagged.
#  perf_score: 0-100 unified scale (RTX 4090/5090 = 100)
# ══════════════════════════════════════════════════════════════════════════════
GPU_LIST = [
    # ── NVIDIA RTX 50 ────────────────────────────────────────────────────────
    GPU("NVIDIA RTX 5090 32GB",         32,575,100,"NVIDIA"),
    GPU("NVIDIA RTX 5080 16GB",         16,360, 91,"NVIDIA"),
    GPU("NVIDIA RTX 5070 Ti 16GB",      16,300, 83,"NVIDIA"),
    GPU("NVIDIA RTX 5070 12GB",         12,250, 76,"NVIDIA"),
    GPU("NVIDIA RTX 5060 Ti 16GB",      16,180, 68,"NVIDIA"),
    GPU("NVIDIA RTX 5060 Ti 8GB",        8,180, 66,"NVIDIA"),
    GPU("NVIDIA RTX 5060 8GB",           8,150, 58,"NVIDIA"),
    # ── NVIDIA RTX 40 ────────────────────────────────────────────────────────
    GPU("NVIDIA RTX 4090 24GB",         24,450,100,"NVIDIA"),
    GPU("NVIDIA RTX 4080 Super 16GB",   16,320, 88,"NVIDIA"),
    GPU("NVIDIA RTX 4080 16GB",         16,320, 86,"NVIDIA"),
    GPU("NVIDIA RTX 4070 Ti Super 16GB",16,285, 80,"NVIDIA"),
    GPU("NVIDIA RTX 4070 Ti 12GB",      12,285, 77,"NVIDIA"),
    GPU("NVIDIA RTX 4070 Super 12GB",   12,220, 74,"NVIDIA"),
    GPU("NVIDIA RTX 4070 12GB",         12,200, 69,"NVIDIA"),
    GPU("NVIDIA RTX 4060 Ti 16GB",      16,165, 63,"NVIDIA"),
    GPU("NVIDIA RTX 4060 Ti 8GB",        8,165, 62,"NVIDIA"),
    GPU("NVIDIA RTX 4060 8GB",           8,115, 55,"NVIDIA"),
    GPU("NVIDIA RTX 4050 6GB",           6, 70, 45,"NVIDIA"),
    # ── NVIDIA RTX 30 ────────────────────────────────────────────────────────
    GPU("NVIDIA RTX 3090 Ti 24GB",      24,450, 84,"NVIDIA"),
    GPU("NVIDIA RTX 3090 24GB",         24,350, 82,"NVIDIA"),
    GPU("NVIDIA RTX 3080 Ti 12GB",      12,350, 79,"NVIDIA"),
    GPU("NVIDIA RTX 3080 12GB",         12,350, 77,"NVIDIA"),
    GPU("NVIDIA RTX 3080 10GB",         10,320, 75,"NVIDIA"),
    GPU("NVIDIA RTX 3070 Ti 8GB",        8,290, 70,"NVIDIA"),
    GPU("NVIDIA RTX 3070 8GB",           8,220, 68,"NVIDIA"),
    GPU("NVIDIA RTX 3060 Ti 8GB",        8,200, 64,"NVIDIA"),
    GPU("NVIDIA RTX 3060 12GB",         12,170, 54,"NVIDIA"),
    GPU("NVIDIA RTX 3050 8GB",           8,130, 43,"NVIDIA"),
    GPU("NVIDIA RTX 3050 6GB",           6,130, 40,"NVIDIA"),
    # ── NVIDIA RTX 20 ────────────────────────────────────────────────────────
    GPU("NVIDIA RTX 2080 Ti 11GB",      11,250, 72,"NVIDIA"),
    GPU("NVIDIA RTX 2080 Super 8GB",     8,250, 65,"NVIDIA"),
    GPU("NVIDIA RTX 2080 8GB",           8,215, 63,"NVIDIA"),
    GPU("NVIDIA RTX 2070 Super 8GB",     8,215, 60,"NVIDIA"),
    GPU("NVIDIA RTX 2070 8GB",           8,175, 57,"NVIDIA"),
    GPU("NVIDIA RTX 2060 Super 8GB",     8,175, 52,"NVIDIA"),
    GPU("NVIDIA RTX 2060 6GB",           6,160, 48,"NVIDIA"),
    # ── NVIDIA GTX 16 ────────────────────────────────────────────────────────
    GPU("NVIDIA GTX 1660 Ti 6GB",        6,120, 40,"NVIDIA"),
    GPU("NVIDIA GTX 1660 Super 6GB",     6,125, 40,"NVIDIA"),
    GPU("NVIDIA GTX 1660 6GB",           6,120, 37,"NVIDIA"),
    GPU("NVIDIA GTX 1650 Super 4GB",     4,100, 31,"NVIDIA"),
    GPU("NVIDIA GTX 1650 4GB",           4, 75, 26,"NVIDIA"),
    GPU("NVIDIA GTX 1650 LP 4GB",        4, 75, 24,"NVIDIA", True),   # Low Profile
    # ── NVIDIA GTX 10 ────────────────────────────────────────────────────────
    GPU("NVIDIA GTX 1080 Ti 11GB",      11,250, 55,"NVIDIA"),
    GPU("NVIDIA GTX 1080 8GB",           8,180, 48,"NVIDIA"),
    GPU("NVIDIA GTX 1070 Ti 8GB",        8,180, 44,"NVIDIA"),
    GPU("NVIDIA GTX 1070 8GB",           8,150, 41,"NVIDIA"),
    GPU("NVIDIA GTX 1060 6GB",           6,120, 33,"NVIDIA"),
    GPU("NVIDIA GTX 1060 3GB",           3,120, 30,"NVIDIA"),
    GPU("NVIDIA GTX 1050 Ti 4GB",        4, 75, 22,"NVIDIA"),
    GPU("NVIDIA GTX 1050 Ti LP 4GB",     4, 75, 21,"NVIDIA", True),   # Low Profile
    GPU("NVIDIA GTX 1050 2GB",           2, 75, 17,"NVIDIA"),
    GPU("NVIDIA GTX 1050 LP 2GB",        2, 75, 16,"NVIDIA", True),   # Low Profile
    GPU("NVIDIA GT 1030 2GB",            2, 30,  8,"NVIDIA"),
    GPU("NVIDIA GT 1030 LP 2GB",         2, 30,  7,"NVIDIA", True),   # Low Profile
    # ── NVIDIA GTX 900 ───────────────────────────────────────────────────────
    GPU("NVIDIA GTX 980 Ti 6GB",         6,250, 38,"NVIDIA"),
    GPU("NVIDIA GTX 980 4GB",            4,165, 32,"NVIDIA"),
    GPU("NVIDIA GTX 970 4GB",            4,145, 28,"NVIDIA"),
    GPU("NVIDIA GTX 960 2GB",            2,120, 19,"NVIDIA"),
    GPU("NVIDIA GTX 950 2GB",            2, 90, 15,"NVIDIA"),
    GPU("NVIDIA GTX 750 Ti LP 2GB",      2, 60, 10,"NVIDIA", True),   # Low Profile
    GPU("NVIDIA GTX 750 LP 1GB",         1, 55,  8,"NVIDIA", True),   # Low Profile
    # ── AMD RX 9000 ──────────────────────────────────────────────────────────
    GPU("AMD RX 9070 XT 16GB",          16,304, 83,"AMD"),
    GPU("AMD RX 9070 16GB",             16,220, 76,"AMD"),
    # ── AMD RX 7000 ──────────────────────────────────────────────────────────
    GPU("AMD RX 7900 XTX 24GB",         24,355, 93,"AMD"),
    GPU("AMD RX 7900 XT 20GB",          20,315, 87,"AMD"),
    GPU("AMD RX 7900 GRE 16GB",         16,260, 80,"AMD"),
    GPU("AMD RX 7800 XT 16GB",          16,263, 73,"AMD"),
    GPU("AMD RX 7700 XT 12GB",          12,245, 66,"AMD"),
    GPU("AMD RX 7600 XT 16GB",          16,190, 57,"AMD"),
    GPU("AMD RX 7600 8GB",               8,165, 53,"AMD"),
    # ── AMD RX 6000 ──────────────────────────────────────────────────────────
    GPU("AMD RX 6950 XT 16GB",          16,335, 83,"AMD"),
    GPU("AMD RX 6900 XT 16GB",          16,300, 79,"AMD"),
    GPU("AMD RX 6800 XT 16GB",          16,300, 75,"AMD"),
    GPU("AMD RX 6800 16GB",             16,250, 70,"AMD"),
    GPU("AMD RX 6750 XT 12GB",          12,250, 64,"AMD"),
    GPU("AMD RX 6700 XT 12GB",          12,230, 62,"AMD"),
    GPU("AMD RX 6700 10GB",             10,175, 58,"AMD"),
    GPU("AMD RX 6650 XT 8GB",            8,176, 53,"AMD"),
    GPU("AMD RX 6600 XT 8GB",            8,160, 51,"AMD"),
    GPU("AMD RX 6600 8GB",               8,132, 48,"AMD"),
    GPU("AMD RX 6500 XT 4GB",            4, 65, 28,"AMD"),
    GPU("AMD RX 6400 4GB",               4, 53, 22,"AMD"),
    GPU("AMD RX 6400 LP 4GB",            4, 53, 21,"AMD", True),     # Low Profile
    # ── AMD RX 5000 ──────────────────────────────────────────────────────────
    GPU("AMD RX 5700 XT 8GB",            8,225, 52,"AMD"),
    GPU("AMD RX 5700 8GB",               8,180, 48,"AMD"),
    GPU("AMD RX 5600 XT 6GB",            6,150, 43,"AMD"),
    GPU("AMD RX 5500 XT 8GB",            8,130, 33,"AMD"),
    GPU("AMD RX 5500 XT 4GB",            4,130, 30,"AMD"),
    # ── AMD Vega ─────────────────────────────────────────────────────────────
    GPU("AMD Radeon VII 16GB",          16,300, 54,"AMD"),
    GPU("AMD RX Vega 64 8GB",            8,295, 44,"AMD"),
    GPU("AMD RX Vega 56 8GB",            8,210, 40,"AMD"),
    # ── AMD RX 500 ───────────────────────────────────────────────────────────
    GPU("AMD RX 590 8GB",                8,225, 29,"AMD"),
    GPU("AMD RX 580 8GB",                8,185, 26,"AMD"),
    GPU("AMD RX 570 4GB",                4,150, 22,"AMD"),
    GPU("AMD RX 560 4GB",                4, 80, 15,"AMD"),
    GPU("AMD RX 550 LP 4GB",             4, 50, 10,"AMD", True),     # Low Profile
    GPU("AMD RX 550 LP 2GB",             2, 50,  8,"AMD", True),     # Low Profile
    # ── Intel Arc B (Battlemage) ──────────────────────────────────────────────
    GPU("Intel Arc B580 12GB",          12,190, 60,"Intel"),
    GPU("Intel Arc B570 10GB",          10,150, 54,"Intel"),
    # ── Intel Arc A (Alchemist) ───────────────────────────────────────────────
    GPU("Intel Arc A770 16GB",          16,225, 53,"Intel"),
    GPU("Intel Arc A770 8GB",            8,225, 52,"Intel"),
    GPU("Intel Arc A750 8GB",            8,190, 47,"Intel"),
    GPU("Intel Arc A580 8GB",            8,175, 41,"Intel"),
    GPU("Intel Arc A380 6GB",            6, 75, 20,"Intel"),
    GPU("Intel Arc A310 4GB",            4, 50, 12,"Intel"),
    GPU("Intel Arc A310 LP 4GB",         4, 50, 11,"Intel", True),   # Low Profile
]

# ══════════════════════════════════════════════════════════════════════════════
#  MOTHERBOARD DATABASE — simplified chipset-only names (H510, B550, Z790…)
# ══════════════════════════════════════════════════════════════════════════════
MB_LIST = [
    # ── Intel LGA1851 (Arrow Lake) ────────────────────────────────────────────
    Motherboard("Z890 (LGA1851)",    "LGA1851","Z890", 192,5),
    Motherboard("B860 (LGA1851)",    "LGA1851","B860", 192,5),
    Motherboard("H810 (LGA1851)",    "LGA1851","H810", 128,5),
    # ── Intel LGA1700 (12th/13th/14th Gen) ────────────────────────────────────
    Motherboard("Z790 (LGA1700)",    "LGA1700","Z790", 128,5),
    Motherboard("H770 (LGA1700)",    "LGA1700","H770",  64,5),
    Motherboard("B760 (LGA1700)",    "LGA1700","B760",  64,5),
    Motherboard("H610 (LGA1700)",    "LGA1700","H610",  64,5),
    Motherboard("Z690 (LGA1700)",    "LGA1700","Z690", 128,5),
    # ── Intel LGA1200 (10th/11th Gen) ─────────────────────────────────────────
    Motherboard("Z590 (LGA1200)",    "LGA1200","Z590", 128,4),
    Motherboard("H570 (LGA1200)",    "LGA1200","H570",  64,4),
    Motherboard("B560 (LGA1200)",    "LGA1200","B560",  64,4),
    Motherboard("H510 (LGA1200)",    "LGA1200","H510",  64,4),
    Motherboard("Z490 (LGA1200)",    "LGA1200","Z490", 128,3),
    Motherboard("H470 (LGA1200)",    "LGA1200","H470",  64,3),
    Motherboard("B460 (LGA1200)",    "LGA1200","B460",  64,3),
    Motherboard("H410 (LGA1200)",    "LGA1200","H410",  64,3),
    # ── Intel LGA1151 (6th–9th Gen) ───────────────────────────────────────────
    Motherboard("Z390 (LGA1151)",    "LGA1151","Z390", 128,3),
    Motherboard("H370 (LGA1151)",    "LGA1151","H370",  64,3),
    Motherboard("B365 (LGA1151)",    "LGA1151","B365",  64,3),
    Motherboard("B360 (LGA1151)",    "LGA1151","B360",  64,3),
    Motherboard("H310 (LGA1151)",    "LGA1151","H310",  32,3),
    Motherboard("Z370 (LGA1151)",    "LGA1151","Z370", 128,3),
    Motherboard("Z270 (LGA1151)",    "LGA1151","Z270", 128,3),
    Motherboard("B250 (LGA1151)",    "LGA1151","B250",  64,3),
    Motherboard("Z170 (LGA1151)",    "LGA1151","Z170", 128,3),
    Motherboard("H170 (LGA1151)",    "LGA1151","H170",  64,3),
    Motherboard("B150 (LGA1151)",    "LGA1151","B150",  64,3),
    Motherboard("H110 (LGA1151)",    "LGA1151","H110",  32,3),
    # ── Intel LGA2066 HEDT ────────────────────────────────────────────────────
    Motherboard("X299 (LGA2066)",    "LGA2066","X299", 256,3),
    # ── Intel LGA2011-3 HEDT ──────────────────────────────────────────────────
    Motherboard("X99 (LGA2011-3)",   "LGA2011-3","X99",128,3),
    # ── AMD AM5 ───────────────────────────────────────────────────────────────
    Motherboard("X870E (AM5)",       "AM5","X870E", 256,5),
    Motherboard("X870 (AM5)",        "AM5","X870",  192,5),
    Motherboard("X670E (AM5)",       "AM5","X670E", 128,5),
    Motherboard("X670 (AM5)",        "AM5","X670",  128,5),
    Motherboard("B650E (AM5)",       "AM5","B650E", 128,5),
    Motherboard("B650 (AM5)",        "AM5","B650",  128,5),
    Motherboard("A620 (AM5)",        "AM5","A620",   64,5),
    # ── AMD AM4 ───────────────────────────────────────────────────────────────
    Motherboard("X570 (AM4)",        "AM4","X570",  128,4),
    Motherboard("B550 (AM4)",        "AM4","B550",  128,4),
    Motherboard("A520 (AM4)",        "AM4","A520",   64,4),
    Motherboard("X470 (AM4)",        "AM4","X470",   64,3),
    Motherboard("B450 (AM4)",        "AM4","B450",   64,3),
    Motherboard("X370 (AM4)",        "AM4","X370",   64,3),
    Motherboard("B350 (AM4)",        "AM4","B350",   64,3),
    Motherboard("A320 (AM4)",        "AM4","A320",   32,3),
    Motherboard("X300 (AM4)",        "AM4","X300",   32,3),
    Motherboard("A300 (AM4)",        "AM4","A300",   32,3),
    # ── AMD sTRX4 ─────────────────────────────────────────────────────────────
    Motherboard("TRX40 (sTRX4)",     "sTRX4","TRX40",256,4),
    # ── AMD TR4 ───────────────────────────────────────────────────────────────
    Motherboard("X399 (TR4)",        "TR4","X399",   256,3),
    # ── AMD sTR5 ──────────────────────────────────────────────────────────────
    Motherboard("TRX50 (sTR5)",      "sTR5","TRX50", 512,5),
]

# ══════════════════════════════════════════════════════════════════════════════
#  BOTTLENECK ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def calculate_bottleneck(cpu: CPU, gpu: GPU, mb: Motherboard):
    gap = cpu.perf_score - gpu.perf_score
    bn_pct = abs(gap) * 0.55

    thread_penalty = 0.0
    if cpu.cores <= 4 and gpu.perf_score >= 60:
        thread_penalty = min((gpu.perf_score - 60) * 0.12, 10.0)

    pcie_penalty = 0.0
    if mb.pcie_gen <= 3 and gpu.perf_score >= 75:
        pcie_penalty = min((gpu.perf_score - 75) * 0.10, 5.0)

    total_pct = min(bn_pct + thread_penalty + pcie_penalty, 68.0)
    THRESHOLD = 8
    if gap > THRESHOLD:
        side = "GPU"
    elif gap < -THRESHOLD:
        side = "CPU"
    else:
        side = "Balanced"
        total_pct = min(total_pct, 7.0)

    compatible = (cpu.socket == mb.socket)
    breakdown = {
        "cpu_perf_score":  cpu.perf_score,
        "gpu_perf_score":  gpu.perf_score,
        "performance_gap": round(float(gap), 1),
        "thread_penalty":  round(thread_penalty, 1),
        "pcie_penalty":    round(pcie_penalty, 1),
    }

    suggestions = []
    if not compatible:
        suggestions.append(
            f"🔴  INCOMPATIBLE: {cpu.name} uses socket {cpu.socket} but "
            f"{mb.name} requires socket {mb.socket}. This system will NOT boot."
        )
    if side == "GPU" and total_pct >= 10:
        target = min(cpu.perf_score, 100)
        recs = sorted([g for g in GPU_LIST if g.perf_score >= target-6 and g.name != gpu.name],
                      key=lambda g: abs(g.perf_score - target))
        rec = recs[0].name if recs else "a higher-tier GPU"
        suggestions.append(
            f"🎮  GPU Bottleneck ({total_pct:.0f}%): Your {cpu.name} (CPU score "
            f"{cpu.perf_score}) is significantly stronger than your {gpu.name} "
            f"(GPU score {gpu.perf_score}). The GPU is the limiting factor. "
            f"Upgrading to the {rec} would balance this build."
        )
    if side == "CPU" and total_pct >= 10:
        target = min(gpu.perf_score, 100)
        recs = sorted([c for c in CPU_LIST if c.perf_score >= target-6
                       and c.name != cpu.name and c.socket == mb.socket],
                      key=lambda c: abs(c.perf_score - target))
        rec = recs[0].name if recs else f"a stronger CPU (socket {mb.socket})"
        suggestions.append(
            f"🖥️  CPU Bottleneck ({total_pct:.0f}%): Your {gpu.name} (GPU score "
            f"{gpu.perf_score}) is significantly stronger than your {cpu.name} "
            f"(CPU score {cpu.perf_score}). Upgrade to {rec} to unleash your GPU."
        )
    if thread_penalty > 3:
        suggestions.append(
            f"🔧  Low core count ({cpu.cores} cores): Modern game engines need "
            "6–8+ cores. Your CPU may cause stuttering with this GPU."
        )
    if pcie_penalty > 1:
        suggestions.append(
            f"📡  PCIe Gen {mb.pcie_gen} bandwidth may limit your high-end GPU. "
            "A PCIe Gen 4 or Gen 5 board removes this constraint."
        )
    if gpu.vram_gb < 8 and gpu.perf_score >= 45:
        suggestions.append(
            f"💾  Only {gpu.vram_gb} GB VRAM: Modern titles at 1440p/4K often "
            "need 10–12+ GB. Expect texture pop-in or VRAM overflow stutters."
        )
    if gpu.low_profile:
        suggestions.append(
            "📐  Low Profile GPU: Make sure your case supports LP cards. "
            "LP GPUs typically have reduced cooling headroom — ensure good airflow."
        )
    if side == "Balanced":
        suggestions.append(
            f"✅  Well-matched build! {cpu.name} ({cpu.perf_score}) and "
            f"{gpu.name} ({gpu.perf_score}) are within {abs(gap)} pts — "
            "neither component is significantly limiting the other."
        )
        suggestions.append(
            "💡  Enable XMP/EXPO in BIOS, use a fast NVMe SSD (PCIe 4.0+), "
            "and ensure good case airflow to squeeze out maximum performance."
        )
    if not suggestions:
        suggestions.append("✅  Solid build. Fast RAM and NVMe SSD will complete the picture.")

    return {"bottleneck_pct": round(total_pct, 1), "side": side,
            "breakdown": breakdown, "suggestions": suggestions,
            "compatible": compatible, "gap": gap}

# ──────────────────────────── UPDATE CHECK ───────────────────────────────────
def check_update():
    try:
        import urllib.request, json as _j
        with urllib.request.urlopen(RELEASES_URL, timeout=5) as r:
            data = _j.loads(r.read())
        latest = data.get("tag_name","").lstrip("v")
        if latest and latest != CURRENT_VER:
            return latest, data.get("html_url", DOWNLOAD_PAGE)
    except Exception:
        pass
    return None, None

# ══════════════════════════════════════════════════════════════════════════════
#  SEARCHABLE COMBOBOX WIDGET
# ══════════════════════════════════════════════════════════════════════════════
class SearchCombo(tk.Frame):
    """Entry + Listbox dropdown with live search filtering."""
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent, bg=T["card"])
        self._all     = list(values)
        self._filtered= list(values)
        self._var     = tk.StringVar()
        self._open    = False

        self._entry = tk.Entry(self, textvariable=self._var,
                               font=("Segoe UI",9),
                               bg=T["entry_bg"], fg=T["entry_fg"],
                               insertbackground=T["entry_fg"],
                               relief="flat", bd=0,
                               highlightthickness=1,
                               highlightbackground=T["divider"],
                               highlightcolor=T["primary"])
        self._entry.pack(fill="x", ipady=5, padx=0)

        # Popup (Toplevel so it overlaps siblings)
        self._popup = tk.Toplevel(self)
        self._popup.withdraw()
        self._popup.overrideredirect(True)
        self._popup.attributes("-topmost", True)

        frame = tk.Frame(self._popup, bg=T["divider"], bd=1)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        self._lb = tk.Listbox(frame, font=("Segoe UI",9),
                              bg=T["list_bg"], fg=T["on_surface"],
                              selectbackground=T["list_select"],
                              selectforeground=T["on_surface"],
                              relief="flat", bd=0,
                              activestyle="none",
                              height=10,
                              yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._lb.yview)
        scrollbar.pack(side="right", fill="y")
        self._lb.pack(side="left", fill="both", expand=True)
        self._populate(self._all)

        # Bindings
        self._var.trace_add("write", self._on_type)
        self._entry.bind("<FocusIn>",  self._show)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Down>",     self._focus_list)
        self._entry.bind("<Return>",   self._pick_first)
        self._lb.bind("<<ListboxSelect>>", self._on_select)
        self._lb.bind("<Return>",      self._on_select)
        self._lb.bind("<Escape>",      lambda e: self._hide())
        self._lb.bind("<FocusOut>",    self._on_focus_out)

        # Set default
        if self._all:
            self._var.set(self._all[0])

    # ── Theme refresh ─────────────────────────────────────────────────────────
    def refresh_theme(self):
        self.configure(bg=T["card"])
        self._entry.configure(bg=T["entry_bg"], fg=T["entry_fg"],
                              insertbackground=T["entry_fg"],
                              highlightbackground=T["divider"],
                              highlightcolor=T["primary"])
        frame = self._popup.winfo_children()[0] if self._popup.winfo_children() else None
        if frame:
            frame.configure(bg=T["divider"])
        self._lb.configure(bg=T["list_bg"], fg=T["on_surface"],
                           selectbackground=T["list_select"],
                           selectforeground=T["on_surface"])

    def _populate(self, items):
        self._lb.delete(0, "end")
        for it in items:
            self._lb.insert("end", it)

    def _on_type(self, *_):
        q = self._var.get().lower()
        self._filtered = [v for v in self._all if q in v.lower()] if q else list(self._all)
        self._populate(self._filtered)
        if not self._open:
            self._show()

    def _show(self, *_):
        self._open = True
        self._popup.deiconify()
        self._reposition()

    def _hide(self):
        self._open = False
        self._popup.withdraw()

    def _reposition(self):
        self.update_idletasks()
        x = self._entry.winfo_rootx()
        y = self._entry.winfo_rooty() + self._entry.winfo_height()
        w = self._entry.winfo_width()
        self._popup.geometry(f"{w}x220+{x}+{y}")

    def _on_focus_out(self, event):
        # Delay to allow listbox click to register
        self.after(150, self._check_focus)

    def _check_focus(self):
        try:
            focused = self._popup.focus_get()
            if focused not in (self._lb, self._entry):
                self._hide()
                # Restore to last valid value if entry doesn't match
                if self._var.get() not in self._all:
                    self._var.set(self._all[0] if self._all else "")
        except Exception:
            pass

    def _focus_list(self, *_):
        if self._filtered:
            self._lb.focus_set()
            self._lb.selection_set(0)

    def _pick_first(self, *_):
        if self._filtered:
            self._var.set(self._filtered[0])
        self._hide()

    def _on_select(self, *_):
        sel = self._lb.curselection()
        if sel:
            self._var.set(self._filtered[sel[0]])
        self._hide()
        self._entry.focus_set()

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════
class BottleneckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._dark = False
        self.title(f"Bottleneck Calculator  v{CURRENT_VER}")
        self.geometry("980x860")
        self.minsize(840,750)
        self.configure(bg=T["bg"])
        self._all_widgets: list[tk.Widget] = []
        self._build_ui()
        self.after(2000, lambda: threading.Thread(target=self._update_check, daemon=True).start())

    # ── THEME TOGGLE ──────────────────────────────────────────────────────────
    def _toggle_theme(self):
        self._dark = not self._dark
        new = THEMES["dark"] if self._dark else THEMES["light"]
        T.update(new)
        self._apply_theme()

    def _apply_theme(self):
        self.configure(bg=T["bg"])
        self._restyle_all(self)

    def _restyle_all(self, widget):
        cls = widget.__class__.__name__
        try:
            if isinstance(widget, SearchCombo):
                widget.refresh_theme()
                return
            if cls == "Frame":
                bg = widget.cget("bg")
                # Map old colors to new
                for old_key, new_key in [("bg","bg"),("card","card"),("primary_light","primary_light"),
                                          ("primary","primary"),("divider","divider"),("topbar_bg","topbar_bg")]:
                    if bg == THEMES["dark" if not self._dark else "light"][old_key]:
                        widget.configure(bg=T[old_key])
                        break
            elif cls == "Label":
                self._restyle_label(widget)
            elif cls == "Button":
                self._restyle_button(widget)
            elif cls == "Canvas":
                widget.configure(bg=T["card"])
                self._redraw_gauge_if_needed(widget)
            elif cls == "Text":
                widget.configure(bg=T["card"], fg=T["on_surface"])
        except Exception:
            pass
        for child in widget.winfo_children():
            self._restyle_all(child)

    def _restyle_label(self, lbl):
        try:
            old_bg = lbl.cget("bg")
            old_fg = lbl.cget("fg")
            other = THEMES["dark" if not self._dark else "light"]
            color_map = {
                other["bg"]:           T["bg"],
                other["card"]:         T["card"],
                other["primary_light"]:T["primary_light"],
                other["primary"]:      T["primary"],
                other["topbar_bg"]:    T["topbar_bg"],
                other["divider"]:      T["divider"],
            }
            fg_map = {
                other["on_surface"]:     T["on_surface"],
                other["on_bg"]:          T["on_bg"],
                other["secondary_text"]: T["secondary_text"],
                other["primary"]:        T["primary"],
                other["primary_dark"]:   T["primary_dark"],
                other["on_primary"]:     T["on_primary"],
                other["topbar_fg"]:      T["topbar_fg"],
                other["topbar_sub"]:     T["topbar_sub"],
                other["divider"]:        T["divider"],
                other["success"]:        T["success"],
                other["warning"]:        T["warning"],
                other["error"]:          T["error"],
                other["accent"]:         T["accent"],
            }
            new_bg = color_map.get(old_bg, old_bg)
            new_fg = fg_map.get(old_fg, old_fg)
            lbl.configure(bg=new_bg, fg=new_fg)
        except Exception:
            pass

    def _restyle_button(self, btn):
        try:
            txt = btn.cget("text")
            if "☀️" in txt or "🌙" in txt:
                btn.configure(bg=T["toggle_bg"], fg=T["toggle_fg"],
                              activebackground=T["primary_light"])
                btn.configure(text=("☀️  Light Mode" if self._dark else "🌙  Dark Mode"))
            elif "CALCULATE" in txt:
                btn.configure(bg=T["accent"], fg="#FFFFFF",
                              activebackground="#E65100")
        except Exception:
            pass

    def _redraw_gauge_if_needed(self, canvas):
        if canvas is self.gauge:
            self._draw_gauge(self._last_pct, self._last_side)

    # ── BUILD ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self._last_pct  = 0.0
        self._last_side = "—"
        self._topbar()
        self._selector()
        self._results()
        self._footer()

    # ── TOP BAR ───────────────────────────────────────────────────────────────
    def _topbar(self):
        bar = tk.Frame(self, bg=T["topbar_bg"], height=58)
        bar.pack(fill="x"); bar.pack_propagate(False)

        tk.Label(bar, text="⚡  Bottleneck Calculator",
                 font=("Segoe UI",17,"bold"),
                 fg=T["topbar_fg"], bg=T["topbar_bg"]).pack(side="left", padx=20, pady=12)

        # Dark/light toggle button
        self.toggle_btn = tk.Button(bar, text="🌙  Dark Mode",
                                    font=("Segoe UI",9,"bold"),
                                    bg=T["toggle_bg"], fg=T["toggle_fg"],
                                    activebackground=T["primary_light"],
                                    relief="flat", cursor="hand2",
                                    bd=0, padx=12, pady=6,
                                    command=self._toggle_theme)
        self.toggle_btn.pack(side="right", padx=12, pady=12)

        tk.Label(bar, text=f"v{CURRENT_VER}", font=("Segoe UI",9),
                 fg=T["topbar_sub"], bg=T["topbar_bg"]).pack(side="right", padx=0, pady=20)

    # ── SELECTOR ──────────────────────────────────────────────────────────────
    def _selector(self):
        outer = tk.Frame(self, bg=T["bg"], pady=10)
        outer.pack(fill="x", padx=18)
        card = self._card(outer); card.pack(fill="x")

        tk.Label(card, text="🔧  Select Your Components",
                 font=("Segoe UI",11,"bold"),
                 fg=T["primary"], bg=T["card"]).pack(anchor="w", padx=18, pady=(12,4))

        grid = tk.Frame(card, bg=T["card"]); grid.pack(fill="x", padx=18, pady=(0,6))
        for i in range(3): grid.columnconfigure(i, weight=1)

        cpu_names = [c.name for c in CPU_LIST]
        mb_names  = [m.name for m in MB_LIST]
        gpu_names = [g.name for g in GPU_LIST]

        tk.Label(grid, text="🖥️  CPU", font=("Segoe UI",9,"bold"),
                 fg=T["secondary_text"], bg=T["card"]).grid(row=0,column=0,sticky="w",padx=6,pady=(6,2))
        tk.Label(grid, text="🔌  Motherboard Chipset", font=("Segoe UI",9,"bold"),
                 fg=T["secondary_text"], bg=T["card"]).grid(row=0,column=1,sticky="w",padx=6,pady=(6,2))
        tk.Label(grid, text="🎮  GPU", font=("Segoe UI",9,"bold"),
                 fg=T["secondary_text"], bg=T["card"]).grid(row=0,column=2,sticky="w",padx=6,pady=(6,2))

        self.cpu_cb = SearchCombo(grid, cpu_names)
        self.cpu_cb.grid(row=1, column=0, sticky="ew", padx=6)
        self.mb_cb  = SearchCombo(grid, mb_names)
        self.mb_cb.grid(row=1, column=1, sticky="ew", padx=6)
        self.gpu_cb = SearchCombo(grid, gpu_names)
        self.gpu_cb.grid(row=1, column=2, sticky="ew", padx=6)

        # Stats bar
        info = tk.Frame(card, bg=T["primary_light"]); info.pack(fill="x")
        tk.Label(info,
                 text=f"  {len(CPU_LIST)} CPUs  •  {len(GPU_LIST)} GPUs (incl. LP models)  •  {len(MB_LIST)} Chipsets  —  type to search",
                 font=("Segoe UI",8), fg=T["primary_dark"],
                 bg=T["primary_light"]).pack(side="left", pady=4, padx=6)

        btn_row = tk.Frame(card, bg=T["card"]); btn_row.pack(pady=10)
        self.calc_btn = tk.Button(btn_row, text="  CALCULATE BOTTLENECK  ",
                                  font=("Segoe UI",11,"bold"),
                                  bg=T["accent"], fg="white",
                                  activebackground="#BF360C",
                                  relief="flat", cursor="hand2",
                                  bd=0, padx=28, pady=10,
                                  command=self._calculate)
        self.calc_btn.pack()
        self._hover(self.calc_btn, T["accent"], "#E65100")

    # ── RESULTS PANEL ─────────────────────────────────────────────────────────
    def _results(self):
        outer = tk.Frame(self, bg=T["bg"])
        outer.pack(fill="both", expand=True, padx=18, pady=(0,6))

        top = tk.Frame(outer, bg=T["bg"]); top.pack(fill="x")

        # Gauge card
        gc = self._card(top); gc.pack(side="left", fill="both", expand=True, pady=(0,6), padx=(0,5))
        tk.Label(gc, text="Bottleneck Gauge", font=("Segoe UI",10,"bold"),
                 fg=T["primary"], bg=T["card"]).pack(anchor="w", padx=14, pady=(10,0))
        self.gauge = tk.Canvas(gc, width=310, height=215, bg=T["card"], highlightthickness=0)
        self.gauge.pack(padx=10, pady=(0,10))
        self._draw_gauge(0,"—")

        # Breakdown card
        bc = self._card(top); bc.pack(side="left", fill="both", expand=True, pady=(0,6), padx=(5,0))
        tk.Label(bc, text="Score Breakdown", font=("Segoe UI",10,"bold"),
                 fg=T["primary"], bg=T["card"]).pack(anchor="w", padx=14, pady=(10,2))
        self.score_frame = tk.Frame(bc, bg=T["card"])
        self.score_frame.pack(fill="both", expand=True, padx=14, pady=(0,10))
        tk.Label(self.score_frame,
                 text="Run a calculation to see results.\n\n"
                      "Positive gap = CPU stronger = GPU bottleneck\n"
                      "Negative gap = GPU stronger = CPU bottleneck",
                 font=("Segoe UI",9), fg=T["secondary_text"],
                 bg=T["card"], justify="left").pack(anchor="nw", pady=8)

        # Suggestions card
        sc = self._card(outer); sc.pack(fill="both", expand=True)
        hdr = tk.Frame(sc, bg=T["primary_light"]); hdr.pack(fill="x")
        tk.Label(hdr, text="💡  Suggestions & Recommendations",
                 font=("Segoe UI",10,"bold"), fg=T["primary_dark"],
                 bg=T["primary_light"]).pack(anchor="w", padx=14, pady=7)
        tf = tk.Frame(sc, bg=T["card"]); tf.pack(fill="both", expand=True)
        self.sug_text = tk.Text(tf, font=("Segoe UI",10), fg=T["on_surface"],
                                bg=T["card"], relief="flat", bd=0,
                                state="disabled", wrap="word",
                                height=8, padx=14, pady=10)
        self.sug_text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tf, command=self.sug_text.yview)
        self.sug_text.configure(yscrollcommand=sb.set); sb.pack(side="right", fill="y")
        self._set_suggestions(["Type in any box to search, then click CALCULATE."])

    def _footer(self):
        tk.Frame(self, bg=T["divider"], height=1).pack(fill="x")
        foot = tk.Frame(self, bg=T["bg"]); foot.pack(fill="x", padx=18, pady=5)
        self.update_lbl = tk.Label(foot, text="Checking for updates…",
                                   font=("Segoe UI",9),
                                   fg=T["secondary_text"], bg=T["bg"])
        self.update_lbl.pack(side="left")
        tk.Label(foot, text="Scores based on published benchmarks. For reference only.",
                 font=("Segoe UI",8), fg=T["divider"], bg=T["bg"]).pack(side="right")

    # ── GAUGE ─────────────────────────────────────────────────────────────────
    def _draw_gauge(self, pct, side):
        self._last_pct  = pct
        self._last_side = side
        c = self.gauge; c.delete("all")
        W,H,cx,cy,r = 310,215,155,150,112

        # Gradient-like track
        c.create_arc(cx-r,cy-r,cx+r,cy+r, start=0, extent=180,
                     style="arc", outline=T["gauge_track"], width=20)

        if side == "Balanced" or pct < 8:   color = T["success"]
        elif pct < 20:  color = "#8BC34A"
        elif pct < 35:  color = "#FBC02D"
        elif pct < 50:  color = T["warning"]
        else:           color = T["error"]

        extent = int(pct/100*180)
        if extent > 0:
            c.create_arc(cx-r,cy-r,cx+r,cy+r, start=180, extent=-extent,
                         style="arc", outline=color, width=20)

        lbl = f"{pct:.1f}%" if pct > 0 else "—"
        c.create_text(cx, cy-24, text=lbl,
                      font=("Segoe UI",30,"bold"), fill=color)
        c.create_text(cx, cy+10, text="Bottleneck",
                      font=("Segoe UI",10), fill=T["secondary_text"])

        sc = {"CPU":T["warning"],"GPU":T["primary"],"Balanced":T["success"]}.get(side,T["secondary_text"])
        c.create_text(cx, cy+35, text=(f"Side: {side}" if side not in("—","") else ""),
                      font=("Segoe UI",12,"bold"), fill=sc)
        c.create_text(cx-r-8,cy+8, text="0%",
                      font=("Segoe UI",8), fill=T["secondary_text"], anchor="e")
        c.create_text(cx+r+8,cy+8, text="100%",
                      font=("Segoe UI",8), fill=T["secondary_text"], anchor="w")

    # ── BREAKDOWN ─────────────────────────────────────────────────────────────
    def _set_breakdown(self, bd, side, gap):
        for w in self.score_frame.winfo_children(): w.destroy()
        rows = [
            ("CPU Perf Score",   bd["cpu_perf_score"],  T["primary"],  str(int(bd["cpu_perf_score"]))),
            ("GPU Perf Score",   bd["gpu_perf_score"],  "#9C27B0",     str(int(bd["gpu_perf_score"]))),
            ("Performance Gap",  bd["performance_gap"], T["success"] if gap>0 else T["error"], f"{bd['performance_gap']:+.0f}"),
            ("Thread Penalty",   bd["thread_penalty"],  T["warning"],  f"{bd['thread_penalty']:.1f}"),
            ("PCIe Penalty",     bd["pcie_penalty"],    T["warning"],  f"{bd['pcie_penalty']:.1f}"),
        ]
        for label, _, color, display in rows:
            row = tk.Frame(self.score_frame, bg=T["card"]); row.pack(fill="x", pady=2)
            tk.Label(row, text=label, font=("Segoe UI",9),
                     fg=T["secondary_text"], bg=T["card"],
                     anchor="w", width=18).pack(side="left")
            tk.Label(row, text=display, font=("Segoe UI",9,"bold"),
                     fg=color, bg=T["card"],
                     width=6, anchor="e").pack(side="right")
            tk.Frame(self.score_frame, bg=T["divider"], height=1).pack(fill="x")

        note = {"GPU":"▲ CPU>GPU score → GPU bottleneck",
                "CPU":"▼ GPU>CPU score → CPU bottleneck",
                "Balanced":"≈ Balanced (gap ≤8 pts)"}.get(side,"")
        tk.Label(self.score_frame, text=note, font=("Segoe UI",8,"italic"),
                 fg=T["primary"], bg=T["card"],
                 wraplength=230, justify="left").pack(anchor="w", pady=(6,0))

    # ── SUGGESTIONS ───────────────────────────────────────────────────────────
    def _set_suggestions(self, items):
        self.sug_text.configure(state="normal")
        self.sug_text.delete("1.0","end")
        for s in items:
            self.sug_text.insert("end", s+"\n\n")
        self.sug_text.configure(state="disabled")

    # ── CALCULATE ─────────────────────────────────────────────────────────────
    def _calculate(self):
        cpu_n = self.cpu_cb.get()
        gpu_n = self.gpu_cb.get()
        mb_n  = self.mb_cb.get()

        cpu = next((c for c in CPU_LIST if c.name==cpu_n), None)
        gpu = next((g for g in GPU_LIST if g.name==gpu_n), None)
        mb  = next((m for m in MB_LIST  if m.name==mb_n),  None)

        if not (cpu and gpu and mb):
            messagebox.showerror("Not Found",
                "One or more components not found.\nPlease select from the dropdown suggestions.")
            return

        r = calculate_bottleneck(cpu, gpu, mb)
        self._draw_gauge(r["bottleneck_pct"], r["side"])
        self._set_breakdown(r["breakdown"], r["side"], r["gap"])
        self._set_suggestions(r["suggestions"])

        if not r["compatible"]:
            messagebox.showwarning("Socket Mismatch",
                f"⚠️  {cpu.name}  ({cpu.socket})\n"
                f"    is NOT compatible with\n"
                f"    {mb.name}  ({mb.socket})\n\n"
                "The CPU won't physically fit this motherboard!")

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def _update_check(self):
        latest, url = check_update()
        if latest:
            self.update_lbl.configure(
                text=f"🔔  Update v{latest} available — click to download",
                fg=T["accent"], cursor="hand2")
            self.update_lbl.bind("<Button-1>", lambda e: webbrowser.open(url))
        else:
            self.update_lbl.configure(text="✔  Up to date", fg=T["success"])

    # ── HELPERS ───────────────────────────────────────────────────────────────
    def _card(self, parent):
        return tk.Frame(parent, bg=T["card"],
                        highlightbackground=T["shadow"], highlightthickness=1)

    def _hover(self, w, n, h):
        w.bind("<Enter>", lambda e: w.configure(bg=h))
        w.bind("<Leave>", lambda e: w.configure(bg=n))


if __name__ == "__main__":
    app = BottleneckApp()
    app.mainloop()
