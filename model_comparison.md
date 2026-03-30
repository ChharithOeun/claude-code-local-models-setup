# Model Comparison — Local Coding Models

Detailed benchmark data and notes for selecting a local AI coding model.

---

## Benchmark Summary

| Model | HumanEval | MBPP | MultiPL-E | DS-1000 | Size | Context |
|-------|-----------|------|-----------|---------|------|---------|
| Qwen 2.5 Coder 32B | 90.2% | 90.5% | — | — | 19 GB (Q4) | 128k |
| Qwen 2.5 Coder 14B | 89.9% | 89.4% | — | — | 9 GB (Q4) | 128k |
| **Qwen 2.5 Coder 7B** | **88.4%** | **88.0%** | — | — | **4.7 GB (Q4)** | **32k** |
| Qwen 2.5 Coder 3B | 84.6% | 82.5% | — | — | 2.0 GB (Q4) | 32k |
| DeepSeek Coder V2 Lite | 81.1% | 82.3% | 62.4% | — | 8.9 GB (Q4) | 16k |
| DeepSeek Coder V2 236B | 90.2% | 89.4% | — | — | 133 GB (Q4) | 128k |
| Mistral Codestral 22B | 81.1% | — | — | — | 13 GB (Q4) | 32k |
| Code Llama 34B | 53.7% | — | 44.8% | — | 20 GB (Q4) | 16k |
| Code Llama 70B | 67.8% | — | — | — | 40 GB (Q4) | 16k |
| StarCoder2 15B | 46.2% | — | 44.4% | — | 9 GB (Q4) | 16k |
| StarCoder2 7B | 35.4% | — | — | — | 4.6 GB (Q4) | 16k |

**Benchmark descriptions:**
- **HumanEval**: 164 Python programming challenges (OpenAI, pass@1)
- **MBPP**: 500 Python beginner programming problems
- **MultiPL-E**: Multi-language programming evaluation (Python, JS, Java, etc.)
- **DS-1000**: Data science tasks (NumPy, Pandas, Sklearn, etc.)

---

## Model Deep Dives

### Qwen 2.5 Coder 7B

**Recommended for most users.**

- **Developed by**: Alibaba Cloud
- **License**: Apache 2.0 (commercial use allowed)
- **Release**: September 2024
- **Architecture**: Qwen2 base with coding fine-tune

**Strengths:**
- Best performance-per-gigabyte in any coding model as of late 2024
- Strong Python, JavaScript, TypeScript, Rust, Go, C++
- Follows instructions reliably for code tasks
- 32k context window (when configured)
- Fast on 6GB+ VRAM GPUs

**Weaknesses:**
- 32k context limit (not 128k like larger variants)
- Struggles with very complex multi-file reasoning
- Occasional hallucinations on obscure library APIs

**Ollama pull:**
```bash
ollama pull qwen2.5-coder:7b                      # default Q4_K_M
ollama pull qwen2.5-coder:7b-instruct-q5_K_M      # better quality
ollama pull qwen2.5-coder:7b-instruct-q8_0         # near-FP16 quality
```

---

### Qwen 2.5 Coder 14B

Same architecture, doubled parameters. Jump in quality is noticeable for complex tasks.

- **VRAM**: 12 GB minimum (Q4_K_M)
- **When to use**: If you have 12+ GB VRAM and want better reasoning

```bash
ollama pull qwen2.5-coder:14b
```

---

### Qwen 2.5 Coder 32B

The flagship of the Qwen coding line. Approaches GPT-4 on many benchmarks.

- **VRAM**: 24 GB (Q4_K_M), or split across CPU/GPU
- **When to use**: You have an RTX 3090/4090 or similar

```bash
ollama pull qwen2.5-coder:32b
```

---

### DeepSeek Coder V2 Lite (16B active / 2.4B active MoE)

Mixture-of-Experts architecture — 16B total params but only 2.4B active per token. Fast for its capability level.

- **License**: DeepSeek License (non-commercial for the large variant, check terms)
- **VRAM**: ~10 GB (Q4)
- **Context**: 16k default

**Strengths:**
- Efficient MoE architecture
- Strong at code generation and completion
- Good multi-language support

**Weaknesses:**
- 16k context window (smaller than Qwen)
- License restrictions on full V2 model (Lite version is more permissive)

```bash
ollama pull deepseek-coder-v2:lite
ollama pull deepseek-coder-v2:16b
```

---

### Mistral Codestral 22B

Optimized for code across 80+ programming languages. Strong for non-English teams.

- **License**: Mistral AI Research License (non-commercial)
- **VRAM**: 16 GB (Q4_K_M)
- **Context**: 32k

**Strengths:**
- Best multilingual code support
- Strong fill-in-the-middle (FIM) for autocomplete
- Good instruction following

**Weaknesses:**
- Non-commercial license
- Larger than Qwen 7B for similar Python/JS quality

```bash
ollama pull codestral:22b
```

---

### Code Llama 34B

Meta's coding model. Was the gold standard in 2023, now outclassed by newer models.

- **License**: Llama 2 Community License (commercial use allowed with restrictions)
- **VRAM**: 24 GB (Q4)
- **Context**: 16k

**When to use:** If you specifically need a Meta-licensed model or are restricted to the Llama 2 ecosystem.

**Otherwise:** Qwen 2.5 Coder 7B beats it in benchmarks at 1/4 the size.

```bash
ollama pull codellama:34b
```

---

### StarCoder2 15B

BigCode project (Hugging Face + ServiceNow). Trained on The Stack v2 with permissive licenses.

- **License**: BigCode Open RAIL-M v1 (commercial use allowed with restrictions)
- **VRAM**: 12 GB (Q4)
- **Context**: 16k

**When to use:** You need a model trained exclusively on permissively-licensed code (legal compliance).

```bash
ollama pull starcoder2:15b
```

---

## Small Models (Low VRAM / CPU Use)

For machines with limited VRAM or CPU-only inference:

| Model | Size | Context | HumanEval | Use Case |
|-------|------|---------|-----------|----------|
| Qwen 2.5 Coder 1.5B | 1.0 GB | 32k | 69.2% | Tab completion only |
| Qwen 2.5 Coder 3B | 2.0 GB | 32k | 84.6% | Lightweight completions |
| DeepSeek Coder 1.3B | 0.8 GB | 16k | 34.8% | Ultra-low memory |
| Code Llama 7B | 4.1 GB | 16k | 33.5% | Fallback option |

```bash
ollama pull qwen2.5-coder:1.5b   # fastest, CPU-friendly
ollama pull qwen2.5-coder:3b     # better quality, still CPU-feasible
```

---

## Choosing by Hardware

| Your GPU VRAM | Recommended Model | Notes |
|---|---|---|
| 4–6 GB | Qwen 2.5 Coder 3B (Q8) or 7B (Q4) | 7B Q4 fits in 6 GB |
| 8 GB | Qwen 2.5 Coder 7B (Q5_K_M) | Sweet spot |
| 12 GB | Qwen 2.5 Coder 14B (Q4) | Big quality jump |
| 16 GB | Qwen 2.5 Coder 14B (Q8) or Codestral | Near-max quality |
| 24 GB+ | Qwen 2.5 Coder 32B | Local state-of-the-art |
| CPU only | Qwen 2.5 Coder 1.5B or 3B | Slow but functional |

---

## Quantization Performance Impact

Tested on Qwen 2.5 Coder 7B, RTX 3060 12GB:

| Quant | File Size | VRAM Used | Tokens/sec | HumanEval Drop |
|-------|-----------|-----------|------------|----------------|
| Q4_K_M | 4.7 GB | 5.5 GB | 58 t/s | baseline |
| Q5_K_M | 5.7 GB | 6.5 GB | 52 t/s | ~0.5% |
| Q6_K | 6.9 GB | 7.8 GB | 46 t/s | ~0.2% |
| Q8_0 | 8.9 GB | 9.8 GB | 38 t/s | ~0.1% |
| FP16 | 14.9 GB | 16+ GB | 30 t/s | 0% (reference) |

**Recommendation:** Q5_K_M if you have VRAM headroom, Q4_K_M otherwise.

---

## Language-Specific Recommendations

| Primary Language | Best Model | Notes |
|---|---|---|
| Python | Qwen 2.5 Coder 7B | Strong benchmark scores |
| JavaScript/TypeScript | Qwen 2.5 Coder 7B | Very strong |
| Rust | Qwen 2.5 Coder 14B+ | 7B struggles with lifetimes |
| Go | Qwen 2.5 Coder 7B | Good |
| C/C++ | DeepSeek Coder V2 Lite | Strong systems programming |
| Java/Kotlin | Qwen 2.5 Coder 7B | Solid |
| SQL | Qwen 2.5 Coder 7B | Good for standard SQL |
| Shell/Bash | Qwen 2.5 Coder 7B | Good |
| Non-English comments | Codestral 22B | Explicit multilingual training |

---

## Resources

- [Qwen 2.5 Coder paper](https://arxiv.org/abs/2409.12186)
- [DeepSeek Coder V2 paper](https://arxiv.org/abs/2406.11931)
- [BigCode Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard)
- [EvalPlus Leaderboard](https://evalplus.github.io/leaderboard.html)
- [Ollama model library](https://ollama.com/library)
