# IDE Setup Guide — Local Models with Ollama

Step-by-step integration for each major editor.

---

## Prerequisites

Ollama must be installed and running before any IDE integration works.

```bash
# Install Ollama
# Linux/macOS:
curl -fsSL https://ollama.com/install.sh | sh

# Windows:
winget install Ollama.Ollama
# or download installer: https://ollama.com/download/windows

# Pull the recommended model
ollama pull qwen2.5-coder:7b

# Start Ollama with 32k context window
# Linux/macOS:
OLLAMA_NUM_CTX=32768 ollama serve

# Windows (PowerShell):
$env:OLLAMA_NUM_CTX=32768; ollama serve
# or set permanently in System Environment Variables

# Test it's working
curl http://localhost:11434/api/tags
```

---

## VS Code + Continue Extension

The Continue extension is the best open-source AI coding assistant for VS Code. It supports Ollama natively.

### Step 1: Install Continue

1. Open VS Code
2. Extensions panel (`Ctrl+Shift+X`)
3. Search "Continue"
4. Install the **Continue - Codestral, Claude, and more** extension by Continue

### Step 2: Configure Ollama backend

Open the Continue config file:
- Click the Continue icon in the sidebar
- Click the gear icon → "Open config.json"
- Or navigate to: `~/.continue/config.json`

Replace the contents with:

```json
{
  "models": [
    {
      "title": "Qwen 2.5 Coder 7B (Local)",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b",
      "apiBase": "http://localhost:11434",
      "contextLength": 32768
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen Local Autocomplete",
    "provider": "ollama",
    "model": "qwen2.5-coder:7b",
    "apiBase": "http://localhost:11434"
  },
  "allowAnonymousTelemetry": false,
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "apiBase": "http://localhost:11434"
  }
}
```

### Step 3: Enable tab autocomplete

1. Open VS Code settings (`Ctrl+,`)
2. Search "Continue: Enable Tab Autocomplete"
3. Enable it

### Step 4: Use it

- `Ctrl+I` — inline edit (select code first)
- `Ctrl+L` — open chat sidebar
- `Tab` — accept autocomplete suggestion
- `Alt+\` — trigger autocomplete manually

### Optional: Add Claude API as fallback

```json
{
  "models": [
    {
      "title": "Qwen Local (Free)",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "Claude Sonnet (API)",
      "provider": "anthropic",
      "model": "claude-sonnet-4-6",
      "apiKey": "YOUR_ANTHROPIC_API_KEY"
    }
  ]
}
```

Switch between models in the Continue sidebar dropdown.

---

## Cursor with Local Backend

Cursor supports custom OpenAI-compatible API endpoints. Ollama exposes one at `http://localhost:11434/v1`.

### Step 1: Open Cursor Settings

`Ctrl+Shift+J` → Settings → Models

### Step 2: Add custom model

1. Click "Add Model"
2. Fill in:
   - **Model name**: `qwen2.5-coder:7b`
   - **Base URL**: `http://localhost:11434/v1`
   - **API Key**: `ollama` (any string — Ollama ignores it)
3. Click "Verify"

### Step 3: Select the model

In the Cursor chat panel, click the model dropdown and select your local model.

### Limitations with Cursor

- Cursor's Composer (multi-file AI) may not work as well with local models
- Local models have smaller context windows than Claude/GPT-4
- Tab autocomplete in Cursor uses their proprietary model, not your local one

**Recommendation:** Use Cursor's tab completion with their service (subscription), use local Ollama for chat/edit commands.

---

## JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)

### Option A: Continue Plugin (recommended)

1. JetBrains Marketplace → search "Continue"
2. Install **Continue** plugin
3. Restart IDE
4. Configure: `~/.continue/config.json` (same as VS Code config above)

### Option B: AI Assistant with Local Model

JetBrains AI Assistant supports custom endpoints in newer versions:

1. Settings → Tools → AI Assistant
2. Enable "Use custom AI provider"
3. Set endpoint: `http://localhost:11434/v1`
4. API key: `ollama`
5. Model: `qwen2.5-coder:7b`

### Option C: CodeGPT Plugin

1. Install [CodeGPT](https://plugins.jetbrains.com/plugin/21056-codegpt) plugin
2. Settings → CodeGPT → Provider: Ollama
3. Model: `qwen2.5-coder:7b`
4. Host: `http://localhost:11434`

---

## Neovim

### Option A: gen.nvim (simplest)

```lua
-- Using lazy.nvim
{
  "David-Kunz/gen.nvim",
  opts = {
    model = "qwen2.5-coder:7b",
    host = "localhost",
    port = "11434",
    display_mode = "float",  -- or "split"
    show_prompt = true,
    show_model = true,
    no_auto_close = false,
  },
  keys = {
    { "<leader>ai", ":Gen<CR>",         mode = { "n", "v" }, desc = "AI Generate" },
    { "<leader>ac", ":Gen Chat<CR>",    mode = { "n" },      desc = "AI Chat" },
  },
}
```

Usage: Select code in visual mode → `<leader>ai` → choose action

### Option B: ollama.nvim

```lua
{
  "nomnivore/ollama.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  opts = {
    model = "qwen2.5-coder:7b",
    url = "http://localhost:11434",
    prompts = {
      Explain = {
        prompt = "Explain this code:\n```$ftype\n$sel\n```",
      },
      Fix = {
        prompt = "Fix this code and explain what was wrong:\n```$ftype\n$sel\n```",
      },
    },
  },
}
```

### Option C: codecompanion.nvim (most feature-rich)

```lua
{
  "olimorris/codecompanion.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-treesitter/nvim-treesitter",
  },
  config = function()
    require("codecompanion").setup({
      adapters = {
        ollama = function()
          return require("codecompanion.adapters").extend("ollama", {
            schema = {
              model = { default = "qwen2.5-coder:7b" },
              num_ctx = { default = 32768 },
            },
          })
        end,
      },
      strategies = {
        chat     = { adapter = "ollama" },
        inline   = { adapter = "ollama" },
        agent    = { adapter = "ollama" },
      },
    })
  end,
}
```

---

## Emacs

### gptel with Ollama backend

```elisp
(use-package gptel
  :config
  (gptel-make-ollama "Ollama"
    :host "localhost:11434"
    :stream t
    :models '(qwen2.5-coder:7b))
  (setq gptel-model   "qwen2.5-coder:7b"
        gptel-backend (gptel-make-ollama "Ollama"
                        :host "localhost:11434"
                        :stream t
                        :models '(qwen2.5-coder:7b))))
```

Usage: `M-x gptel` to open chat buffer.

---

## Zed

Zed has built-in Ollama support:

1. Open settings: `Ctrl+,`
2. Add to your settings.json:

```json
{
  "assistant": {
    "default_model": {
      "provider": "ollama",
      "model": "qwen2.5-coder:7b"
    },
    "version": "2"
  }
}
```

---

## Helix

Helix doesn't have native AI completion, but you can use external tools:

### With llm CLI tool

```bash
pip install llm llm-ollama
llm install llm-ollama
llm -m ollama/qwen2.5-coder:7b "explain this: $(cat myfile.py)"
```

Use in terminal alongside Helix, pipe code through it.

---

## Terminal-Only Workflow (any editor)

If you prefer to stay in the terminal:

```bash
# Interactive chat
ollama run qwen2.5-coder:7b

# One-shot queries
ollama run qwen2.5-coder:7b "write a Python function to parse CSV"

# Pipe code for review
cat myfile.py | ollama run qwen2.5-coder:7b "review this code for bugs"

# With aichat CLI (supports Ollama)
pip install aichat
aichat -m ollama:qwen2.5-coder:7b
```

---

## Ollama OpenAI-Compatible API Reference

Any tool that supports a custom OpenAI API endpoint works with Ollama:

```
Base URL:  http://localhost:11434/v1
API Key:   ollama  (any string)
Model:     qwen2.5-coder:7b  (or any pulled model)

Endpoints:
  POST /v1/chat/completions
  POST /v1/completions
  GET  /v1/models
```

Example with curl:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "messages": [
      {"role": "user", "content": "Write a bubble sort in Python"}
    ]
  }'
```

---

## Windows-Specific Notes

**Set environment variables permanently:**
1. Search "Environment Variables" in Start menu
2. System Properties → Environment Variables
3. Add under System Variables:
   - `OLLAMA_NUM_CTX` = `32768`
   - `OLLAMA_KEEP_ALIVE` = `10m`

**Ollama as Windows service:**
Ollama installs as a system tray app on Windows. Right-click the tray icon to start/stop.

**Firewall:**
If accessing Ollama from WSL or another machine, allow port 11434 through Windows Firewall. Set `OLLAMA_HOST=0.0.0.0:11434` to listen on all interfaces.

**AMD GPU on Windows:**
```powershell
# Enable DirectML backend (experimental)
$env:OLLAMA_GPU_DRIVER="dml"
ollama serve
```

ROCm on Windows is not officially supported; use the DirectML path or run Ollama in WSL2 with ROCm for Linux.
