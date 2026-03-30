# Claude Code + Local Models via Ollama

> The setup guide Anthropic won't write. Save $15-30/month by running AI coding assistants locally.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Models: Qwen | DeepSeek | Mistral](https://img.shields.io/badge/Models-Qwen%20%7C%20DeepSeek%20%7C%20Mistral-blue)](model_comparison.md)
[![AMD GPU Supported](https://img.shields.io/badge/GPU-AMD%20%7C%20NVIDIA%20%7C%20CPU-green)](setup_guide.md)

---

## Why This Exists

Claude Code is one of the most capable AI coding tools available. But heavy usage hits $15–30/month in API costs fast — and that's just for one developer.

**Local models via Ollama are free.** No API key. No usage limits. No billing surprises.

The problem: nobody has written a clear guide for connecting them. This repo fixes that.

**What you'll have after following this guide:**
- `qwen2.5-coder:7b` (or similar) running locally for bulk completions, fast iteration, throwaway queries
- Claude Code (Anthropic API) reserved for complex reasoning, architecture decisions, multi-file refactors
- A hybrid workflow that cuts costs by 60–90% without sacrificing quality where it matters

---

## Quick Start

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh   # Linux/macOS
# Windows: https://ollama.com/download/windows

# 2. Pull a coding model (start here)
ollama pull qwen2.5-coder:7b

# 3. Set context window to 32k (default is too small for code)
OLLAMA_NUM_CTX=32768 ollama serve

# 4. Test it
ollama run qwen2.5-coder:7b "Write a Python function to parse JSON from a file"
```

For full IDE integration, see [setup_guide.md](setup_guide.md).

---

## Model Selection Guide

Choose based on your hardware. If in doubt, start with **qwen2.5-coder:7b**.

| Model | Size | Min VRAM | Context Window | HumanEval | Best For |
|-------|------|----------|----------------|-----------|----------|
| **Qwen 2.5 Coder 7B** ⭐ | 4.7 GB | 6 GB | 32k | 88.4% | Daily driver, fast, high quality |
| Qwen 2.5 Coder 14B | 9 GB | 12 GB | 128k | 89.9% | Better quality, still fast |
| Qwen 2.5 Coder 32B | 19 GB | 24 GB | 128k | 90.2% | Best local quality |
| DeepSeek Coder V2 Lite | 8.9 GB | 10 GB | 16k | 81.1% | Good alternative, MIT license |
| Code Llama 34B | 20 GB | 24 GB | 16k | 53.7% | Older, larger, lower scores |
| Mistral Codestral 22B | 13 GB | 16 GB | 32k | 81.1% | Polyglot, non-English code comments |
| StarCoder2 15B | 9 GB | 12 GB | 16k | 46.2% | Research-grade, HF-licensed |

**Notes:**
- VRAM figures are approximate; actual use depends on quantization (Q4/Q5/Q8)
- HumanEval scores from official evals; real-world quality varies by task
- "Min VRAM" assumes Q4_K_M quantization — the best size/quality tradeoff
- Models too large for VRAM will run on CPU (much slower, still functional)

### Quantization Trade-offs

| Quantization | Size Multiplier | Quality | Use When |
|---|---|---|---|
| Q4_K_M | 0.55x | Good | Best default — fits most GPUs |
| Q5_K_M | 0.67x | Better | More VRAM headroom |
| Q8_0 | 1.0x | Best local quality | Near-FP16, needs lots of VRAM |
| FP16 | 2.0x | Full quality | Research only, enormous VRAM |

```bash
# Pull specific quantization
ollama pull qwen2.5-coder:7b-instruct-q5_K_M
ollama pull qwen2.5-coder:14b-instruct-q4_K_M
```

---

## Ollama Setup & Tuning

### Install

```bash
# Linux / macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
winget install Ollama.Ollama
# or download from https://ollama.com/download/windows

# Verify
ollama --version
```

### Pull Models

```bash
ollama pull qwen2.5-coder:7b        # recommended start
ollama pull deepseek-coder-v2:lite  # alternative
ollama list                         # see what you have
```

### Context Window — This Is Critical

Default context window is 2048 tokens. **That's not enough for real code.** A single file can exceed that.

```bash
# Set before starting Ollama server
export OLLAMA_NUM_CTX=32768    # 32k context (sweet spot)
export OLLAMA_NUM_CTX=65536    # 64k context (needs more VRAM)
ollama serve
```

Or create a Modelfile for persistent settings:

```dockerfile
# Modelfile.qwen-code
FROM qwen2.5-coder:7b
PARAMETER num_ctx 32768
PARAMETER num_predict 4096
PARAMETER temperature 0.1
PARAMETER top_p 0.9
```

```bash
ollama create qwen-code -f Modelfile.qwen-code
ollama run qwen-code
```

### Memory Management

```bash
# Check how much VRAM your model uses
nvidia-smi   # NVIDIA
rocm-smi     # AMD ROCm

# Ollama keeps model in memory for 5 minutes after last use
# Change keepalive:
export OLLAMA_KEEP_ALIVE=10m   # keep loaded 10 minutes
export OLLAMA_KEEP_ALIVE=0     # unload immediately after request
export OLLAMA_KEEP_ALIVE=-1    # keep forever (max performance)
```

### AMD GPU Setup

Ollama supports AMD GPUs via ROCm (Linux) or DirectML (Windows experimental):

```bash
# Linux - ROCm path
# Install ROCm first: https://rocm.docs.amd.com/
export HSA_OVERRIDE_GFX_VERSION=10.3.0  # adjust for your GPU
ollama serve

# Verify AMD GPU is being used
ollama run qwen2.5-coder:7b "hello"
# Check rocm-smi — GPU memory should be in use

# Windows - DirectML (experimental)
# Set in environment variables:
OLLAMA_GPU_DRIVER=dml
```

**AMD GPU compatibility notes:**
- RX 6000 series (RDNA2): Works well with ROCm 5.7+
- RX 7000 series (RDNA3): Works well with ROCm 6.0+
- RX 5000 series (RDNA1): Limited support, may need CPU fallback
- Vega/Polaris: CPU fallback recommended

**CPU fallback** (slower, but it works):
```bash
# Ollama automatically falls back to CPU if GPU fails
# Force CPU:
CUDA_VISIBLE_DEVICES="" ROCR_VISIBLE_DEVICES="" ollama serve
```

---

## IDE Integration

See [setup_guide.md](setup_guide.md) for full step-by-step instructions. Summary:

### VS Code + Continue Extension

1. Install [Continue](https://marketplace.visualstudio.com/items?itemName=Continue.continue) from VS Code marketplace
2. Open Continue settings (`~/.continue/config.json`)
3. Add Ollama provider:

```json
{
  "models": [
    {
      "title": "Qwen 2.5 Coder 7B (Local)",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Local Autocomplete",
    "provider": "ollama",
    "model": "qwen2.5-coder:7b"
  }
}
```

### Cursor with Local Backend

Cursor supports OpenAI-compatible APIs. Ollama exposes one at `http://localhost:11434/v1`:

1. Cursor Settings → Models → Add Model
2. Base URL: `http://localhost:11434/v1`
3. API Key: `ollama` (any string works)
4. Model: `qwen2.5-coder:7b`

### JetBrains (IntelliJ, PyCharm, etc.)

Install the [Continue plugin](https://plugins.jetbrains.com/plugin/22707-continue) — same config as VS Code above.

### Neovim

Use [gen.nvim](https://github.com/David-Kunz/gen.nvim) or [ollama.nvim](https://github.com/nomnivore/ollama.nvim):

```lua
-- lazy.nvim
{
  "David-Kunz/gen.nvim",
  opts = {
    model = "qwen2.5-coder:7b",
    host = "localhost",
    port = "11434",
  }
}
```

---

## Cost Comparison

Run the included calculator for your specific usage:

```bash
python cost_calculator.py
```

Quick reference:

| Usage Level | Claude API / month | Local Model / month | Savings |
|---|---|---|---|
| Light (50k tokens/day) | ~$4.50 | ~$0.03 electricity | 99% |
| Medium (200k tokens/day) | ~$18 | ~$0.12 electricity | 99% |
| Heavy (500k tokens/day) | ~$45 | ~$0.30 electricity | 99% |

**Hardware break-even** (one-time cost for a dedicated GPU):
- RTX 3060 12GB (~$250 used): Break-even vs API in ~17 months at medium usage
- RX 6700 XT 12GB (~$200 used): Break-even in ~13 months
- Already have a GPU: Break-even is immediate

Electricity assumptions: 150W GPU, $0.12/kWh, 8 hours/day active.

---

## The Recommended Hybrid Workflow

This is the real-world setup that works:

```
┌─────────────────────────────────────────────────────┐
│                  Your Coding Session                 │
├─────────────────┬───────────────────────────────────┤
│   Claude Code   │     Local Ollama (qwen2.5-coder)  │
│   (Anthropic)   │                                   │
├─────────────────┼───────────────────────────────────┤
│ Complex refactor│ Tab completion                    │
│ Architecture    │ Docstring generation              │
│ Multi-file edits│ Quick "how do I..." questions     │
│ Code review     │ Boilerplate generation            │
│ Debugging hard  │ Repetitive transformations        │
│   problems      │ Test stub generation              │
│ API/library Q&A │ Rename/format/lint fixes          │
└─────────────────┴───────────────────────────────────┘
```

**Decision rule:** If it needs reasoning across multiple files or deep context, use Claude Code. If it's a single-file operation or you'd be asking the same question 10 times today, use local.

---

## Performance Comparison

| Metric | Claude 3.5 Sonnet (API) | Qwen 2.5 Coder 7B (Local) |
|---|---|---|
| First token latency | 500ms–2s | 200–800ms (GPU) / 2–10s (CPU) |
| Tokens/second | 40–80 (streaming) | 30–60 (6GB GPU) / 5–15 (CPU) |
| Context window | 200k tokens | 32k (configured) |
| Code quality | Excellent | Very good (7B) / Excellent (32B) |
| Multi-file reasoning | Excellent | Limited |
| Instruction following | Excellent | Good |
| Languages supported | All | All major |
| Internet knowledge | Aug 2024 cutoff | Varies by model |

**Where local models match or beat API:**
- Short function completion
- Boilerplate and scaffolding
- Format/style transformations
- Language-specific syntax (especially Qwen for Python/JS/TS)
- Test generation for isolated functions

**Where Claude Code wins:**
- Cross-file refactoring
- Architecture decisions requiring broad knowledge
- Debugging with complex stack traces
- Understanding unfamiliar codebases
- Tasks requiring up-to-date library knowledge

---

## Troubleshooting

### "Ollama runs out of memory"

```bash
# Check what's loaded
ollama ps

# Reduce context window
OLLAMA_NUM_CTX=8192 ollama serve

# Use smaller quantization
ollama pull qwen2.5-coder:7b-instruct-q4_0   # smallest

# Unload between requests
export OLLAMA_KEEP_ALIVE=0
```

### Context Window Exceeded Errors

```bash
# Symptoms: responses cut off, model ignores early context
# Fix: verify your context setting is actually applied
curl http://localhost:11434/api/show -d '{"name": "qwen2.5-coder:7b"}'
# Look for "num_ctx" in parameters

# If not set, use Modelfile approach (see above)
```

### Model Quality Issues

```bash
# Try higher quantization
ollama pull qwen2.5-coder:7b-instruct-q8_0

# Adjust temperature (lower = more deterministic/correct for code)
# In Modelfile:
PARAMETER temperature 0.05

# Try the 14B model if 7B quality isn't sufficient
ollama pull qwen2.5-coder:14b
```

### AMD GPU Not Detected

```bash
# Linux
rocminfo | grep Agent   # should list your GPU
export HSA_OVERRIDE_GFX_VERSION=10.3.0  # for RDNA2

# Check Ollama logs
journalctl -u ollama -n 50

# Confirm Ollama sees GPU
OLLAMA_DEBUG=1 ollama serve 2>&1 | grep -i gpu

# Fallback: confirm CPU works
ollama run qwen2.5-coder:7b "hello" --verbose
```

### Slow Responses on CPU

CPU inference is slow but functional. Optimization options:

```bash
# Use a smaller model
ollama pull qwen2.5-coder:1.5b

# Reduce output length
PARAMETER num_predict 512

# Use 4-bit quantization
ollama pull qwen2.5-coder:7b-instruct-q4_0
```

---

## Files in This Repo

| File | Contents |
|---|---|
| `README.md` | This guide |
| `cost_calculator.py` | Interactive cost comparison calculator |
| `model_comparison.md` | Detailed benchmark tables and model notes |
| `setup_guide.md` | Step-by-step IDE setup for each editor |
| `CHANGELOG.md` | Version history |

---

## Contributing

PRs welcome, especially:
- Benchmark results for models not listed
- IDE integration guides (Emacs, Helix, Zed, etc.)
- AMD/Apple Silicon specific tuning tips
- Windows-specific gotchas

---

## License

MIT — use freely, commercial or personal.
