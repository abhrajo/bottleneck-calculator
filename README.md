# ⚡ Bottleneck Calculator

A **Material Design** desktop application for calculating CPU/GPU/Motherboard bottlenecks.

## Features
- 🎨 Google Material Design UI (blue/orange theme)
- 🖥️ 40+ CPUs — Intel 12th/13th/14th Gen, AMD Ryzen 3000/5000/7000
- 🎮 40+ GPUs — NVIDIA RTX 30/40, AMD RX 6000/7000, Intel Arc
- 🔌 30+ Motherboards — with socket/chipset compatibility checking
- 📊 Visual gauge showing bottleneck % with score breakdown
- 💡 Smart suggestions for component upgrades
- 🔔 Auto-update check via GitHub releases

---

## Bottleneck Calculation Method

The engine combines four weighted factors:

| Factor | Description |
|---|---|
| Tier Gap | Raw performance tier difference between CPU & GPU (1–10 scale) |
| Core Penalty | Extra penalty when GPU is high-end but CPU has few cores |
| Gaming Clock Factor | Boost clock vs GPU tier — reflects single-threaded gaming demands |
| PCIe Penalty | Older PCIe gen bandwidth limiting high-end GPUs |

**Result interpretation:**
- **< 10%** — Perfectly balanced ✅
- **10–25%** — Minor bottleneck, acceptable ⚠️
- **25–40%** — Noticeable bottleneck, upgrade worth considering 🔶
- **> 40%** — Severe bottleneck, upgrade strongly recommended 🔴

---

## License
MIT — free to use, modify, distribute.
