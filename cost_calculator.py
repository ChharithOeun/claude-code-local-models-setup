#!/usr/bin/env python3
"""
Claude Code vs Local Model Cost Calculator
Estimates monthly AI coding costs for API vs local Ollama setup.
"""

import sys

# ─── Claude API pricing (as of 2025) ─────────────────────────────────────────
CLAUDE_PRICES = {
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},   # per 1M tokens
    "claude-3-5-haiku":  {"input": 0.80, "output":  4.00},
    "claude-3-opus":     {"input": 15.0, "output": 75.00},
    "claude-sonnet-4":   {"input": 3.00, "output": 15.00},
}

# ─── Hardware presets ─────────────────────────────────────────────────────────
GPU_PRESETS = {
    "1": {"name": "RTX 3060 12GB",      "tdp_w": 170, "purchase": 250,  "vram": 12},
    "2": {"name": "RTX 3070 8GB",       "tdp_w": 220, "purchase": 300,  "vram":  8},
    "3": {"name": "RTX 3080 10GB",      "tdp_w": 320, "purchase": 400,  "vram": 10},
    "4": {"name": "RTX 4060 8GB",       "tdp_w": 115, "purchase": 300,  "vram":  8},
    "5": {"name": "RTX 4070 12GB",      "tdp_w": 200, "purchase": 500,  "vram": 12},
    "6": {"name": "RX 6700 XT 12GB",    "tdp_w": 230, "purchase": 200,  "vram": 12},
    "7": {"name": "RX 7800 XT 16GB",    "tdp_w": 263, "purchase": 400,  "vram": 16},
    "8": {"name": "CPU only (no GPU)",  "tdp_w":  65, "purchase":   0,  "vram":  0},
    "9": {"name": "Custom",             "tdp_w":   0, "purchase":   0,  "vram":  0},
}


def clear():
    print()


def banner():
    print("=" * 60)
    print("   Claude Code vs Local Model — Monthly Cost Calculator")
    print("=" * 60)
    print()


def ask_float(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number.")


def ask_int(prompt, choices=None, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            val = int(raw)
            if choices and str(val) not in choices:
                print(f"  Choose from: {', '.join(choices)}")
                continue
            return val
        except ValueError:
            print("  Please enter a whole number.")


def choose_claude_model():
    print("\nWhich Claude model do you use?")
    models = list(CLAUDE_PRICES.keys())
    for i, m in enumerate(models, 1):
        p = CLAUDE_PRICES[m]
        print(f"  {i}. {m:30s}  in=${p['input']}/1M  out=${p['output']}/1M")
    idx = ask_int("Choice", default=1)
    idx = max(1, min(idx, len(models)))
    return models[idx - 1]


def choose_gpu():
    print("\nWhat GPU do you have (or plan to buy)?")
    for k, v in GPU_PRESETS.items():
        print(f"  {k}. {v['name']}  (TDP ~{v['tdp_w']}W, ~${v['purchase']} used)")
    choice = str(ask_int("Choice", choices=list(GPU_PRESETS.keys()), default=1))
    gpu = GPU_PRESETS[choice].copy()
    if choice == "9":
        gpu["name"]     = input("  GPU name: ").strip() or "Custom GPU"
        gpu["tdp_w"]    = ask_float("  TDP in watts (find on GPU spec sheet)", 150)
        gpu["purchase"] = ask_float("  Purchase price USD (0 if already owned)", 0)
        gpu["vram"]     = ask_float("  VRAM in GB", 8)
    return gpu


def get_usage():
    print("\n── Usage Profile ──────────────────────────────────────")
    print("Estimate your daily token usage.")
    print("(A typical 'generate a function' prompt ≈ 500 input + 300 output tokens)")
    print()
    daily_input  = ask_float("Daily INPUT tokens (prompts + context)", 50000)
    daily_output = ask_float("Daily OUTPUT tokens (responses)", 20000)
    active_days  = ask_float("Active days per month", 22)
    hours_per_day = ask_float("Hours GPU is active per day", 6)
    electricity   = ask_float("Electricity rate (USD per kWh, US avg ≈ 0.13)", 0.13)
    return {
        "daily_input": daily_input,
        "daily_output": daily_output,
        "active_days": active_days,
        "hours_per_day": hours_per_day,
        "electricity": electricity,
    }


def calc_api_cost(model_name, usage):
    prices = CLAUDE_PRICES[model_name]
    monthly_input  = usage["daily_input"]  * usage["active_days"]
    monthly_output = usage["daily_output"] * usage["active_days"]
    cost_input  = monthly_input  / 1_000_000 * prices["input"]
    cost_output = monthly_output / 1_000_000 * prices["output"]
    return cost_input + cost_output, monthly_input, monthly_output


def calc_local_cost(gpu, usage):
    kwh_per_month = (gpu["tdp_w"] / 1000) * usage["hours_per_day"] * usage["active_days"]
    electricity_cost = kwh_per_month * usage["electricity"]
    return electricity_cost, kwh_per_month


def print_report(model_name, gpu, usage):
    api_cost, m_in, m_out = calc_api_cost(model_name, usage)
    local_elec, kwh       = calc_local_cost(gpu, usage)

    print()
    print("=" * 60)
    print("  MONTHLY COST REPORT")
    print("=" * 60)

    print(f"\n  Model selected : {model_name}")
    print(f"  GPU selected   : {gpu['name']}")
    print(f"\n  Monthly token usage:")
    print(f"    Input  : {m_in:>12,.0f} tokens")
    print(f"    Output : {m_out:>12,.0f} tokens")
    print(f"    Total  : {m_in+m_out:>12,.0f} tokens")

    print(f"\n  ── Claude API ──────────────────────────────")
    print(f"    Monthly cost : ${api_cost:>8.2f}")
    print(f"    Annual cost  : ${api_cost * 12:>8.2f}")

    print(f"\n  ── Local Model (Ollama) ────────────────────")
    print(f"    GPU power use: {kwh:>8.1f} kWh/month")
    print(f"    Electricity  : ${local_elec:>8.2f}/month")
    if gpu["purchase"] > 0:
        print(f"    Hardware cost: ${gpu['purchase']:>8.2f} (one-time)")
    else:
        print(f"    Hardware cost: $0.00 (already owned)")

    print(f"\n  ── Comparison ──────────────────────────────")
    monthly_savings = api_cost - local_elec
    annual_savings  = monthly_savings * 12
    pct_saving      = (monthly_savings / api_cost * 100) if api_cost > 0 else 0

    print(f"    Monthly savings : ${monthly_savings:>8.2f}  ({pct_saving:.0f}%)")
    print(f"    Annual savings  : ${annual_savings:>8.2f}")

    if gpu["purchase"] > 0:
        if monthly_savings > 0:
            breakeven_months = gpu["purchase"] / monthly_savings
            print(f"    Hardware payoff : {breakeven_months:.1f} months")
            if breakeven_months <= 12:
                print(f"                      ✓ Pays off within a year")
            elif breakeven_months <= 24:
                print(f"                      ✓ Pays off within 2 years")
            else:
                print(f"                      ✗ Long payoff — consider a cheaper GPU")
        else:
            print("    Hardware payoff : N/A (API is cheaper at this usage)")
    else:
        print("    Hardware payoff : Immediate (GPU already owned)")

    print()
    print("  ── Hybrid Recommendation ───────────────────")
    if api_cost < 5:
        print("    Your API usage is low ($<5/mo). API-only is fine.")
    elif api_cost < 15:
        print("    Consider hybrid: local for bulk, API for complex work.")
        print("    Potential savings with 70% local routing:")
        hybrid = api_cost * 0.30 + local_elec
        print(f"      Hybrid monthly cost: ${hybrid:.2f}  (vs ${api_cost:.2f} API-only)")
    else:
        print("    Local models recommended for routine tasks.")
        print("    Potential savings with 80% local routing:")
        hybrid = api_cost * 0.20 + local_elec
        print(f"      Hybrid monthly cost: ${hybrid:.2f}  (vs ${api_cost:.2f} API-only)")

    print()
    print("=" * 60)
    print()


def main():
    banner()

    print("This calculator estimates your monthly AI coding costs")
    print("comparing Claude API vs running models locally with Ollama.")
    print()

    model_name = choose_claude_model()
    gpu        = choose_gpu()
    usage      = get_usage()

    print_report(model_name, gpu, usage)

    again = input("Run another scenario? [y/N]: ").strip().lower()
    if again == "y":
        clear()
        main()
    else:
        print("Tip: pull qwen2.5-coder:7b to get started:")
        print("  ollama pull qwen2.5-coder:7b")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting.")
        sys.exit(0)
