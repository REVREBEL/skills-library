---
name: "hugging-face-gradio"
description: "Build Gradio web UIs and demos in Python, and deploy them on Hugging Face Spaces with ZeroGPU. Covers Gradio core (Interface, Blocks, ChatInterface), component signatures, event listeners, custom HTML components, the `gradio info`/`gradio predict` CLI; ZeroGPU rules (`@spaces.GPU`, duration/quota, CUDA availability model, process isolation, concurrency, CUDA build constraints); and the end-to-end workflow for building and publishing a tailored LoRA demo Space."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Gradio & Hugging Face Spaces

## When to Use

Use this skill when you need to build Gradio web UIs and demos in Python — creating or editing Gradio apps, components, event listeners, layouts, or chatbots — and when deploying them to Hugging Face Spaces, especially ZeroGPU hardware. Also use when building a tailored demo/playground Space for a LoRA, or writing/reviewing code that uses `@spaces.GPU`, configuring `python_version`/`requirements.txt` for ZeroGPU, or handling ZeroGPU-specific constraints.

Gradio is a Python library for building interactive web UIs and ML demos. This skill covers the core API, patterns, and examples, plus the ZeroGPU runtime and the LoRA Space publishing workflow.

## Guides

Detailed guides on specific topics (read these when relevant):

- [Quickstart](https://www.gradio.app/guides/quickstart)
- [The Interface Class](https://www.gradio.app/guides/the-interface-class)
- [Blocks and Event Listeners](https://www.gradio.app/guides/blocks-and-event-listeners)
- [Controlling Layout](https://www.gradio.app/guides/controlling-layout)
- [More Blocks Features](https://www.gradio.app/guides/more-blocks-features)
- [Custom CSS and JS](https://www.gradio.app/guides/custom-CSS-and-JS)
- [Streaming Outputs](https://www.gradio.app/guides/streaming-outputs)
- [Streaming Inputs](https://www.gradio.app/guides/streaming-inputs)
- [Sharing Your App](https://www.gradio.app/guides/sharing-your-app)
- [Custom HTML Components](https://www.gradio.app/guides/custom-HTML-components)
- [Python Client](https://www.gradio.app/guides/getting-started-with-the-python-client)
- [JS Client](https://www.gradio.app/guides/getting-started-with-the-js-client)

## Core Patterns

**Interface** (high-level): wraps a function with input/output components.

```python
import gradio as gr

def greet(name):
    return f"Hello {name}!"

gr.Interface(fn=greet, inputs="text", outputs="text").launch()
```

**Blocks** (low-level): flexible layout with explicit event wiring.

```python
import gradio as gr

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Greeting")
    btn = gr.Button("Greet")
    btn.click(fn=lambda n: f"Hello {n}!", inputs=name, outputs=output)

demo.launch()
```

**ChatInterface**: high-level wrapper for chatbot UIs.

```python
import gradio as gr

def respond(message, history):
    return f"You said: {message}"

gr.ChatInterface(fn=respond).launch()
```

## Key Component Signatures

### `Textbox(value=None, type="text", lines=1, max_lines=None, placeholder=None, label=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, autofocus=False, autoscroll=True, elem_classes=None, render=True, key=None, preserved_by_key="value", text_align=None, rtl=False, buttons=None, max_length=None, submit_btn=False, stop_btn=False, html_attributes=None)`
Creates a textarea for user string input or string output.

### `Number(value=None, label=None, placeholder=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", buttons=None, precision=None, minimum=None, maximum=None, step=1)`
Creates a numeric field.

### `Slider(minimum=0, maximum=100, value=None, step=None, precision=None, label=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", randomize=False, buttons=None)`
Slider from `minimum` to `maximum` with a step size.

### `Checkbox(value=False, label=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", buttons=None)`
Checkbox set to `True`/`False`.

### `Dropdown(choices=None, value=DefaultValue(), type="value", multiselect=None, allow_custom_value=False, max_choices=None, filterable=True, label=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", buttons=None)`
Dropdown of choices (single or multiple).

### `Radio(choices=None, value=None, type="value", label=None, info=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", rtl=False, buttons=None)`
Set of radio buttons; only one can be selected.

### `Image(value=None, format="webp", height=None, width=None, image_mode="RGB", sources=None, type="numpy", label=None, every=None, inputs=None, show_label=None, buttons=None, container=True, scale=None, min_width=160, interactive=None, visible=True, streaming=False, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", webcam_options=None, placeholder=None, watermark=None)`
Image upload (input) or display (output).

### `Audio(value=None, sources=None, type="numpy", label=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, streaming=False, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", format=None, autoplay=False, editable=True, buttons=None, waveform_options=None, loop=False, recording=False, subtitles=None, playback_position=0)`
Audio upload/record (input) or display (output).

### `Video(value=None, format=None, sources=None, height=None, width=None, label=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", webcam_options=None, include_audio=None, autoplay=False, buttons=None, loop=False, streaming=False, watermark=None, subtitles=None, playback_position=0)`
Video upload/record (input) or display (output).

### `File(value=None, file_count="single", file_types=None, type="filepath", label=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, height=None, interactive=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", allow_reordering=False, buttons=None)`
File upload (input) or download display (output).

### `Chatbot(value=None, label=None, every=None, inputs=None, show_label=None, container=True, scale=None, min_width=160, visible=True, elem_id=None, elem_classes=None, autoscroll=True, render=True, key=None, preserved_by_key="value", height=400, resizable=False, max_height=None, min_height=None, editable=None, latex_delimiters=None, rtl=False, buttons=None, watermark=None, avatar_images=None, sanitize_html=True, render_markdown=True, feedback_options=('Like','Dislike'), feedback_value=None, line_breaks=True, layout=None, placeholder=None, examples=None, allow_file_downloads=True, group_consecutive_messages=True, allow_tags=True, reasoning_tags=None, like_user_message=False)`
Displays user messages and responses.

### `Button(value="Run", every=None, inputs=None, variant="secondary", size="lg", icon=None, link=None, link_target="_self", visible=True, interactive=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", scale=None, min_width=None)`
Button with arbitrary `.click()` events.

### `Markdown(value=None, label=None, every=None, inputs=None, show_label=None, rtl=False, latex_delimiters=None, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", sanitize_html=True, line_breaks=False, header_links=False, height=None, max_height=None, min_height=None, buttons=None, container=False, padding=False)`
Renders arbitrary Markdown.

### `HTML(value=None, label=None, html_template="${value}", css_template="", js_on_load=None, apply_default_css=True, every=None, inputs=None, show_label=False, visible=True, elem_id=None, elem_classes=None, render=True, key=None, preserved_by_key="value", min_height=None, max_height=None, container=False, padding=False, autoscroll=False, buttons=None, server_functions=None, props=None)`
Arbitrary HTML.

## Custom HTML Components

If a task requires significant customization of an existing component or a component that doesn't exist in Gradio, create one with `gr.HTML`. It supports `html_template` (with `${}` JS expressions and `{{}}` Handlebars syntax), `css_template` for scoped styles, and `js_on_load` for interactivity — where `props.value` updates the component value and `trigger('event_name')` fires Gradio events. For reuse, subclass `gr.HTML` and define `api_info()` for API/MCP support. See the [full guide](https://www.gradio.app/guides/custom-HTML-components).

```python
import gradio as gr

class StarRating(gr.HTML):
    def __init__(self, label, value=0, **kwargs):
        html_template = """
        <h2>${label} rating:</h2>
        ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}
        """
        css_template = """
            img { height: 50px; display: inline-block; cursor: pointer; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """
        js_on_load = """
            const imgs = element.querySelectorAll('img');
            imgs.forEach((img, index) => {
                img.addEventListener('click', () => {
                    props.value = index + 1;
                });
            });
        """
        super().__init__(value=value, label=label, html_template=html_template,
                         css_template=css_template, js_on_load=js_on_load, **kwargs)

    def api_info(self):
        return {"type": "integer", "minimum": 0, "maximum": 5}


with gr.Blocks() as demo:
    gr.Markdown("# Restaurant Review")
    food_rating = StarRating(label="Food", value=3)
    service_rating = StarRating(label="Service", value=3)
    ambience_rating = StarRating(label="Ambience", value=3)
    average_btn = gr.Button("Calculate Average Rating")
    rating_output = StarRating(label="Average", value=3)

    def calculate_average(food, service, ambience):
        return round((food + service + ambience) / 3)

    average_btn.click(fn=calculate_average,
        inputs=[food_rating, service_rating, ambience_rating],
        outputs=rating_output)

demo.launch()
```

## Event Listeners

All event listeners share the same signature:

```python
component.event_name(
    fn: Callable | None | Literal["decorator"] = "decorator",
    inputs: Component | Sequence[Component] | set[Component] | None = None,
    outputs: Component | Sequence[Component] | set[Component] | None = None,
    api_name: str | None = None,
    api_description: str | None | Literal[False] = None,
    scroll_to_output: bool = False,
    show_progress: Literal["full", "minimal", "hidden"] = "full",
    show_progress_on: Component | Sequence[Component] | None = None,
    queue: bool = True,
    batch: bool = False,
    max_batch_size: int = 4,
    preprocess: bool = True,
    postprocess: bool = True,
    cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
    trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
    js: str | Literal[True] | None = None,
    concurrency_limit: int | None | Literal["default"] = "default",
    concurrency_id: str | None = None,
    api_visibility: Literal["public", "private", "undocumented"] = "public",
    time_limit: int | None = None,
    stream_every: float = 0.5,
    key: int | str | tuple[int | str, ...] | None = None,
    validator: Callable | None = None,
) -> Dependency
```

Supported events per component:

- **AnnotatedImage**: select
- **Audio**: stream, change, clear, play, pause, stop, start_recording, pause_recording, stop_recording, upload, input
- **BarPlot**: select, double_click
- **BrowserState**: change
- **Button**: click
- **Chatbot**: change, select, like, retry, undo, example_select, option_select, clear, copy, edit
- **Checkbox / CheckboxGroup**: change, input, select
- **ClearButton / DeepLinkButton / DownloadButton / DuplicateButton / LoginButton / UploadButton**: click
- **Code**: change, input, focus, blur
- **ColorPicker**: change, input, submit, focus, blur
- **Dataframe**: change, input, select, edit
- **Dataset**: click, select
- **DateTime**: change, submit
- **Dialogue**: change, input, submit
- **Dropdown**: change, input, select, focus, blur, key_up
- **File**: change, select, clear, upload, delete, download
- **FileExplorer**: change, input, select
- **Gallery**: select, upload, change, delete, preview_close, preview_open
- **HTML**: change, input, click, double_click, submit, stop, edit, clear, play, pause, end, start_recording, pause_recording, stop_recording, focus, blur, upload, release, select, stream, like, example_select, option_select, load, key_up, apply, delete, tick, undo, retry, expand, collapse, download, copy
- **HighlightedText**: change, select
- **Image / ImageSlider / SimpleImage**: clear, change, stream, select, upload, input
- **ImageEditor**: clear, change, input, select, upload, apply
- **JSON**: change
- **Label**: change, select
- **LinePlot / ScatterPlot**: select, double_click
- **Markdown**: change, copy
- **Model3D**: change, upload, edit, clear
- **MultimodalTextbox**: change, input, select, submit, focus, blur, stop
- **Navbar**: change
- **Number**: change, input, submit, focus, blur
- **ParamViewer**: change, upload
- **Plot**: change
- **Radio**: select, change, input
- **Slider**: change, input, release
- **State**: change
- **Textbox**: change, input, select, submit, focus, blur, stop, copy
- **Timer**: tick
- **Video**: change, clear, start_recording, stop_recording, stop, play, pause, end, upload, input

## Prediction CLI

The `gradio` CLI includes `info` and `predict` commands for interacting with Gradio apps programmatically — useful for coding agents and for smoke-testing published Spaces.

### `gradio info` — Discover endpoints and parameters

```bash
gradio info <space_id_or_url>
```

Returns a JSON payload describing all endpoints, their parameters (types and defaults), and return values:

```bash
gradio info gradio/calculator
# {
#   "/predict": {
#     "parameters": [
#       {"name": "num1", "required": true, "default": null, "type": {"type": "number"}},
#       {"name": "operation", "required": true, "default": null, "type": {"enum": ["add","subtract","multiply","divide"], "type": "string"}},
#       {"name": "num2", "required": true, "default": null, "type": {"type": "number"}}
#     ],
#     "returns": [{"name": "output", "type": {"type": "number"}}]
#   }
# }
```

File-type parameters show `"type": "filepath"` with instructions to include `"meta": {"_type": "gradio.FileData"}` — this signals the file will be uploaded to the remote server.

### `gradio predict` — Send predictions

```bash
gradio predict <space_id_or_url> <endpoint> <json_payload>
```

```bash
# Numeric prediction
gradio predict gradio/calculator /predict '{"num1": 5, "operation": "multiply", "num2": 3}'
# {"output": 15}

# Image generation
gradio predict black-forest-labs/FLUX.2-dev /infer '{"prompt": "A majestic dragon"}'
# {"Result": "/tmp/gradio/.../image.webp", "Seed": 1117868604}

# File upload (must include meta key)
gradio predict gradio/image_mod /predict '{"image": {"path": "/path/to/image.png", "meta": {"_type": "gradio.FileData"}}}'
# {"output": "/tmp/gradio/.../output.png"}
```

Both commands accept `--token` for private Spaces.

---

# ZeroGPU

Rules and patterns for ML demos on Hugging Face Spaces with **ZeroGPU** hardware. Applies to **Gradio SDK Spaces using ZeroGPU** only — Docker and Static Spaces cannot schedule onto ZeroGPU, and Streamlit runs as Docker. Authoritative docs: https://huggingface.co/docs/hub/spaces-zerogpu (for the current backing GPU, runtime versions, and tier thresholds, which change over time).

## Hardware

ZeroGPU exposes two GPU sizes that map to a fraction of the backing card:

| `size` | Slice of backing GPU | Quota cost |
|--------|----------------------|------------|
| `large` *(default)* | Half | 1x |
| `xlarge` | Full | 2x |

Default `large` gives half a physical GPU — memory bandwidth and compute are significantly lower than the full card. Use `xlarge` only when the workload genuinely needs the extra memory or compute. **Backing GPU changes without notice** — check the docs before sizing workloads.

## Basic Pattern

```python
import spaces
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="...", device="cuda")

@spaces.GPU
def generate(prompt: str) -> str:
    return pipe(prompt, max_new_tokens=100)[0]["generated_text"]
```

Key rules:

1. **Instantiate models at module scope** and call `.to("cuda")` eagerly. ZeroGPU handles the actual device mapping transparently.
2. **Decorate GPU functions with `@spaces.GPU`**. The decorator is a no-op outside ZeroGPU, so it is safe in all environments.
3. **Set `duration` to match the realistic worst-case workload** (default 60s). The platform pre-checks `requested duration` against the user's `remaining quota` — not actual run time — so a 10-second task left at 60s fails with `quota exceeded` once remaining quota drops below 60s. Smaller declared `duration` also ranks higher in the node-level queue.
4. **`torch.compile` is NOT supported.** Use PyTorch [AoTI](https://huggingface.co/blog/zerogpu-aoti) (torch 2.8+) instead.
5. **Use `size="xlarge"` sparingly.** It allocates the full backing GPU but costs 2x quota and tends to queue longer.

```python
@spaces.GPU(duration=120)
def generate_image(prompt: str):
    return pipe(prompt).images[0]
```

## CUDA Availability Model

Real GPU access is **only** available inside `@spaces.GPU`-decorated functions. Outside those functions, the GPU is not attached to the process. However, `import spaces` **monkey-patches `torch`** so that:

- `torch.cuda.is_available()` returns `True` globally.
- `.to("cuda")` / `device="cuda"` at module scope succeed without error.

This is intentional. Module-scope `model.to("cuda")` calls register tensors with the ZeroGPU backend, which writes them to a disk offload directory at a startup "pack" step and frees the RAM. When a `@spaces.GPU` call lands, a forked GPU worker streams those weights from disk into VRAM via a pinned-memory pipeline. Warm workers keep weights resident and skip the disk → VRAM step.

| Action | Where | Why |
|--------|-------|-----|
| `model.to("cuda")` / `pipe(..., device="cuda")` | **Module scope** | ZeroGPU registers the tensor and manages device migration |
| Actual CUDA computation (inference) | **Inside `@spaces.GPU`** | Real GPU is only attached during the decorated call |
| Branching on `torch.cuda.is_available()` | Avoid relying on it | Always returns `True` due to the monkey-patch |

Do not run inference or CUDA kernels at module scope. The standard device idiom still works:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModel.from_pretrained("...").to(device)
```

- **ZeroGPU** — `is_available()` is `True` (monkey-patched), model registered for migration.
- **Dedicated GPU / local GPU** — genuinely `True`.
- **CPU Spaces / local CPU** — resolves to `"cpu"`.

Do not hardcode `device="cuda"` — it breaks on CPU-only environments.

**Eager loading is the right default.** The Space process starts before any user arrives, so cold-start cost is paid once. Lazy loading (`global model; if model is None: ...`, `@lru_cache` wrappers) just pushes that cost onto the first user.

## Local Development: Just Install `spaces`

Do **not** wrap `import spaces` in `try/except` and redefine `spaces.GPU` as a no-op. Off-ZeroGPU, the `spaces` package is already a true no-op:

- Heavyweight behavior (CUDA monkey-patching, client init, startup hooks) is gated on `SPACES_ZERO_GPU`, set only on ZeroGPU.
- `@spaces.GPU` returns the undecorated function unchanged off-ZeroGPU.
- `import spaces` performs only lightweight imports.

The Gradio SDK base image installs `spaces` on every hardware tier, so duplicating a Space onto a dedicated GPU (T4, L4, A10G) or CPU basic needs no code changes. Add `spaces` to dependencies and import it unconditionally:

```python
import spaces

@spaces.GPU
def generate(prompt: str) -> str:
    ...
```

The `try/except ImportError` fallback is an anti-pattern: it must mimic every `@spaces.GPU` call shape, hides `spaces` from `requirements.txt`, and solves a non-problem.

## Duration and Quota

Declaring `@spaces.GPU(duration=N)` triggers three checks:

1. **Tier-max check** — each visitor tier has a per-call `duration` cap. Declaring more fails with `ZeroGPU illegal duration`, regardless of remaining quota.
2. **Quota pre-check** — the platform compares `requested duration` against the user's `remaining quota`. If `remaining < requested`, the call fails with `ZeroGPU quota exceeded` even if the work would have fit. The error shows explicit numbers, e.g. `"60s requested vs. 30s left"`.
3. **Queue priority** — the queue is node-level (requests from all Spaces on the same node compete); shorter declared `duration` ranks higher.

All three favor declaring the smallest realistic `duration` — including for short tasks. Explicit `@spaces.GPU(duration=15)` on a 10-second task avoids premature `quota exceeded` rejections and ranks higher.

> **`xlarge` doubles the request.** `requested = N * 2` when `size="xlarge"`, both for the tier-max and quota pre-check. So `@spaces.GPU(duration=60, size="xlarge")` is internally a 120s request.

**Dynamic duration** for variable workloads — pass a callable that estimates per request, so a static high `duration` doesn't lock out low-tier users:

```python
def estimate_duration(prompt, steps):
    return int(steps * 3.5)

@spaces.GPU(duration=estimate_duration)
def generate(prompt, steps):
    return pipe(prompt, num_inference_steps=steps).images[0]
```

## Process Isolation and Pickle

`@spaces.GPU`-decorated functions run in a **separate process** managed by the ZeroGPU scheduler. Arguments and return values cross the boundary via **pickle serialization**:

- **Only picklable objects** can be passed in or returned. Open file handles, DB connections, locks, lambdas, and closures over unpicklable state raise `PicklingError`.
- **Do NOT return CUDA tensors directly.** Unpickling a CUDA tensor in the main process triggers `torch.cuda._lazy_init()`, which ZeroGPU blocks. Convert to CPU first: `tensor.cpu()` or `tensor.cpu().numpy()`.
- CPU tensors, numpy arrays, PIL Images, and plain Python objects work fine.
- Large objects incur serialization overhead. Prefer lightweight returns (tensors, arrays, file paths, base64 strings).

### `gr.State` semantics across the boundary

Because handlers run in a separate process, `gr.State` values are **pickled on every yield** — NOT shared by reference:

- The generator receives a **copy** of the state (`id()` differs).
- In-place mutations inside the generator are **invisible** to other handlers until the mutated state is explicitly yielded back.
- Yielding `gr.update()` for a `gr.State` slot **skips the update** — other handlers see the pre-yield value.
- Each yield that returns the state object creates a **new copy** via pickle.

Practical guidance: don't assume reference semantics; every yield including a `gr.State` triggers a full pickle round-trip (minimize frequency for large state, use `gr.update()` on intermediate yields); CUDA tensors inside state must be moved to CPU before yielding.

## Concurrency

Handlers run **concurrently by default** on ZeroGPU. Code that worked in single-user testing can silently corrupt or leak data in production. Three rules:

1. **No mutable global state** — concurrent requests overwrite each other.
2. **No fixed file paths for outputs** — use `tempfile` for unique paths.
3. **Read-only globals are safe** — model objects, tokenizers, configs loaded once at startup and only read during requests are safe and encouraged.

## Call Granularity

Each entry into a `@spaces.GPU` function carries non-trivial cost — pickle round-trip, worker warm-up, CUDA re-attach, and a fresh pass through the node-level queue. Calling a decorated function from inside a hot loop multiplies these costs and adds a failure mode (a later iteration may fail to acquire a GPU slot).

Decorate the outer function that owns the loop, not the per-iteration worker:

```python
# Avoid — N GPU entries for N frames
def process_video(frames):
    return [process_frame(f) for f in frames]

@spaces.GPU(duration=...)
def process_frame(frame):
    ...

# Prefer — one GPU entry for the whole video
@spaces.GPU(duration=...)
def process_video(frames):
    return [process_frame(f) for f in frames]

def process_frame(frame):
    ...
```

If the loop mixes heavy CPU work with GPU work, wrapping the whole loop charges CPU time against the user's quota. When that cost is material, batching the GPU work so CPU pre/post-processing stays outside the decorator is a situational optimization — not the default.

## CUDA Build Constraints

HF Spaces builds Docker images in a CPU-only environment. **On ZeroGPU, the build phase has no `nvcc`** because the base image is `python:3.13` (dedicated-GPU Spaces use `nvidia/cuda:*-devel-*` and have `nvcc` at build time). A CUDA-dependent package whose only distribution is sdist — e.g. bare `flash-attn` — cannot be installed via `requirements.txt` on ZeroGPU. Only pre-built wheels work.

ZeroGPU **runtime** does have `nvcc` available, mounted from a CUDA devel image at `/cuda-image` since 2025-07 (added for AoTI support), which makes `torch.export` / AoTI workflows possible inside `@spaces.GPU` calls.

**Bottom line**: install every CUDA-dependent package from a pre-built wheel. If no wheel is on PyPI, build one externally (e.g. host on HF Hub) and pin the URL. For `flash-attn`, the upstream releases page ships a fairly complete wheel matrix covering most Python × CUDA × torch combinations.

## Example Caching

`gr.Examples` behavior is environment-dependent. On ZeroGPU:

- `cache_examples` defaults to `True` (Spaces sets `GRADIO_CACHE_EXAMPLES=true`).
- `cache_mode` defaults to `"lazy"` (Spaces sets `GRADIO_CACHE_MODE=lazy` only on ZeroGPU).

ZeroGPU defaults to `lazy` because eager caching pre-runs every example at app startup, but ZeroGPU has **no GPU attached at startup** — only during request handling. Eager caching of GPU-bound examples would fail there.

When `cache_examples=True`, the `run_on_click` / `run_examples_on_click` parameter is silently ignored. If your app relies on click-populates-only behavior, set `cache_examples=False` explicitly.

To reproduce locally: `GRADIO_CACHE_EXAMPLES=true GRADIO_CACHE_MODE=lazy python app.py`

## Dependency Management

### `python_version` pin in README frontmatter

Pinning `python_version` is **effectively required** for ZeroGPU. The runtime default is currently Python 3.10, so a local environment using 3.11+ will fail to install without an explicit pin. Pin to a ZeroGPU-supported version (3.12 is a reasonable default); the authoritative supported list lives in the [ZeroGPU docs](https://huggingface.co/docs/hub/spaces-zerogpu).

```yaml
# README.md frontmatter
python_version: "3.12"
```

Both `"3.12"` and `"3.12.12"` forms are accepted.

### Do not pin `spaces` in `requirements.txt`

The Space platform pins its own `spaces` version; a conflicting pin causes pip resolution to fail at build time. **Rule: do not include `spaces` in `requirements.txt`.**

- **Hand-written `requirements.txt`**: simply omit `spaces`.
- **uv** (`pyproject.toml`): declare `spaces` in `pyproject.toml` so uv co-resolves transitive constraints (notably `psutil`), then exclude it from the export:
  ```bash
  uv export --no-hashes --no-dev --no-emit-package spaces -o requirements.txt
  ```
- **pip-tools / Poetry**: use the equivalent exclude mechanism.

### Pin `torch` to match wheel tags

If you install a CUDA-dependent wheel via direct URL, the wheel filename encodes the `torch` major.minor it was built against (e.g. `cu12torch2.8`). Pin `torch==X.Y.Z` in `requirements.txt` to match — otherwise pip may resolve a different version and the Space fails on first import.

---

# Building & Publishing a LoRA Demo Space

Build and publish a Gradio demo on Hugging Face Spaces that runs inference with a user-provided LoRA. Use whenever someone asks to create, generate, ship, or publish "a Space", "a demo", "a Gradio app", or "a playground" for a LoRA — whether the base model is Qwen-Image, Qwen-Image-Edit, LTX-Video, Wan, FLUX, SDXL, or another diffusion model. The default target is ZeroGPU hardware; the default inference library is `diffusers` when the base model supports it. The output is a real, published Space (private by default), not a local script.

## What "good" looks like

The demo should feel handcrafted for this specific LoRA, not a generic template. Two LoRAs that share a task can still need different demos: a pose-control video LoRA and an outpainting video LoRA both take video in and produce video out, but the inputs, preprocessing, and controls are completely different. Concretely, a good demo:

- Loads fast and runs fast — minimal model loading, sensible step count, no wasted computation per call.
- Has a UI with exactly the controls this LoRA needs and nothing else. Excess sliders are a cost, not a feature.
- Shows the user what's happening — progress, intermediate outputs where useful, the seed used, a clear error when input is missing.
- Honors the LoRA's own recommendations from its model card: trigger words, recommended step count, guidance scale, LoRA scale, example inputs.
- Is creative where creativity helps (interactive canvases, before/after sliders, side-by-side previews) and plain where plainness is right.

## Workflow

1. Gather the LoRA info needed to pick a pipeline and design a UI.
2. Pick the base pipeline and inference recipe.
3. Design the UI for this specific LoRA's task and inputs.
4. Write `app.py`, `requirements.txt`, and `README.md` together; show all three for one batched approval.
5. Publish the Space (private).
6. Smoke-test it end-to-end before sharing.

Don't drip-feed questions across turns. Batch them.

### Phase 1 — Gather LoRA info

Required: a LoRA repo on the Hub (e.g. `username/my-lora`).

**First, try to read the repo without a token.** If it succeeds, the repo is public — proceed. If it fails with 401/403, the repo is private/gated and you need an authenticated session. **Don't immediately ask for a token** — check whether the user is already authenticated:

```python
from huggingface_hub import HfApi, get_token

cached_token = get_token()  # HF_TOKEN env var or cached CLI login
if cached_token:
    try:
        info = HfApi().whoami(token=cached_token)
        username = info["name"]
    except Exception:
        cached_token = None  # token exists but is invalid/expired
```

- If a valid cached token exists and can read the repo, use it — no prompt needed.
- If no cached token, or it can't read this private repo, ask once: *"I need a Hugging Face access token with **write** scope (to read the LoRA if it's private/gated, and to publish the Space). Create one at https://huggingface.co/settings/tokens. Paste it here."* The same token is reused for publishing.

**Then read the repo:**

- List files (`HfApi().list_repo_files(repo_id)`) — look for `.safetensors`, `README.md`, example media, multiple checkpoints.
- Fetch the model card (`ModelCard.load(repo_id)`). The `data` dict has structured fields; `text` has the README body.
- If multiple `.safetensors` exist, pick the README-recommended file, then `pytorch_lora_weights.safetensors`, then the latest training checkpoint, otherwise ask.

**From the model card, determine:**

- **Base model** — `base_model` field, or text mentions. Used to pick the pipeline.
- **Task** — `pipeline_tag` if set, else inferred from base model + README. The five tasks handled: `text-to-image`, `image-to-image`, `text-to-video`, `image-to-video`, `video-to-video`.
- **Trigger words** — often "trigger word", "instance prompt", "activation word".
- **Recommended inference recipe** — step count, guidance scale, true CFG scale, LoRA scale, resolution. Many cards include a Python snippet; trust its *parameters* (steps, guidance, CFG, LoRA scale, dtype). For *loading mechanics*, prefer `pipe.load_lora_weights(...)`.
- **Example prompts and media** — use as Gradio examples.
- **Sub-task / specific use case** — "what does this LoRA actually do" matters as much as the task category. A relighting LoRA, a face-swap LoRA, and a style LoRA are all image-to-image, but the UI for each differs.

When something can't be inferred, ask once in a single batched message. For task category, list the five options as a numbered choice. For sub-task, give a one-line description prompt ("what does this LoRA do? e.g. 'relight portraits', 'apply manga style', 'extend videos to wider aspect ratios'"). If the model card has nothing helpful, surface it: "The model card has no usable info. I'll need you to tell me: (1) base model, (2) what this LoRA does, (3) recommended step count and guidance scale if you know them."

### Phase 2 — Pick the base pipeline

**Step 1 — Load the reference for this base model family** (if present in the skill's `references/base-models/`): `qwen-image.md` (Qwen-Image + Qwen-Image-Edit), `ltx.md` (LTX family, including IC-LoRAs), `krea-2.md` (Krea 2 / K2). If the base model isn't covered, tell the user and ask whether to proceed by analogy or stop. Don't guess silently.

**Step 2 — Verify the pipeline class against the base model's own card. Mandatory.** A new base model variant might use the same pipeline class with a different repo path, or a new pipeline class entirely. Don't trust a reference table alone — it can lag a release:

```python
from huggingface_hub import ModelCard
base_card = ModelCard.load(base_model_id)
# Read base_card.text — find the diffusers inference snippet, note the pipeline class it imports.
```

Real examples where this matters:

- `Qwen-Image-Edit` uses `QwenImageEditPipeline`. `Qwen-Image-Edit-2509` and `Qwen-Image-Edit-2511` use `QwenImageEditPlusPipeline` — different class, different defaults, takes a list of images instead of one. A LoRA targeting 2511 loaded onto `QwenImageEditPipeline` produces broken output.
- LTX-Video uses `LTXPipeline`/`LTXImageToVideoPipeline`/`LTXConditionPipeline`. LTX-2 uses `LTX2Pipeline` from a different module path. LTX-2.3 sometimes needs a native pipeline outside diffusers.

If the base model card has no diffusers snippet, fall back to the reference table — and tell the user you're falling back.

**Step 3 — Diffusers vs native pipeline.** Default to `diffusers` when the base model has a diffusers pipeline class (Qwen-Image, Qwen-Image-Edit, most of LTX). Some LTX variants (notably LTX-2.3 with certain IC-LoRAs) need a native pipeline; the LTX reference says when. Diffusers gives standard `load_lora_weights` / `set_adapters` semantics; the native path needs LoRA-specific glue.

### Phase 3 — Design the UI for this LoRA

Reason from the LoRA's task and inputs to a UI — don't reach for a template. Read the per-task baseline UI patterns (`references/tasks.md`: T2I, I2I, T2V, I2V, V2V), then `references/adapting-to-the-lora.md` (the most important file — the same task can need very different UIs: a pose-control LTX LoRA needs video input + pose-extraction preview; an outpaint LTX LoRA needs an aspect-ratio picker + black-margin preview; a relighting Flux LoRA needs an image + a brush canvas).

**Self-check before writing the UI.** Write one sentence describing what a user does with this Space in 10 seconds. If it doesn't distinguish this LoRA from any other of the same task, the UI isn't shaped enough.

- ✅ "Upload a video, pick a target aspect ratio, click Generate; the model fills the empty margins."
- ✅ "Draw colored brush strokes where you want light, pick an illumination style, click Generate; the model relights the photo."
- ✅ "Upload a video of someone moving and an image of a different character; the model produces a video of the character doing the motion."
- ❌ "Type a prompt and click generate." (Generic T2I — say more.)
- ❌ "Upload an image and an instruction." (Generic edit — what kind of edit?)

**Gradio component freshness.** Gradio's component set evolves. Before defaulting to plain components, consider newer fits — `gr.ImageSlider` for before/after on edit LoRAs, `gr.BrowserState` for persistent prefs, `@gr.render` for input-dependent UIs. If unsure whether a component exists or its signature, web-fetch https://www.gradio.app/docs rather than guessing.

**Creative mode when stock and Hub custom components aren't enough.** If the LoRA's natural input is a shape no Gradio component expresses well — point sets, strokes, trajectories, multi-region annotations, 3D rotation gizmos, timeline scrubbers — drop down to custom HTML/JS via `gr.HTML` (see `references/creative-mode.md` for the primitives, the JSON wire format discipline, and pitfalls). Don't reach for creative mode just because it would be cool — reach for it when the input shape demands it, and don't skip the Hub custom components rung (e.g. `gradio_image_annotation`) before going fully bespoke.

**`gr.Examples` for media-input Spaces.** When no fitting example media is available from the model's own repo, pull from the shared input pools — images at [`linoyts/repo-to-space-example-inputs`](https://huggingface.co/datasets/linoyts/repo-to-space-example-inputs), videos at [`linoyts/repo-to-space-example-videos`](https://huggingface.co/datasets/linoyts/repo-to-space-example-videos). Both are CC0 with `categories` + `caption` metadata. Pick 2–3, preprocess to the shapes the model expects, bake the copies into the Space. Set `cache_examples=True, cache_mode="lazy"`.

### Phase 4 — Write the Space files

Tell the user concretely what's about to happen, naming the actual files: *"`app.py` (the Gradio demo and inference code), `requirements.txt` (Python dependencies), and `README.md` (Space configuration including ZeroGPU hardware setting). Then I'll show all three for your review before publishing."*

The three files are tightly coupled: `requirements.txt` is determined by what `app.py` imports; the `README.md` YAML frontmatter sets the SDK version, hardware, and title. Write them together, then show all three for approval in **one batched message**.

#### `app.py`

Compose from the phases above — don't paste from a template. Each section should be there because it's needed:

- Imports — `gradio as gr`, `torch`, `spaces`, the pipeline class, anything preprocessing needs.
- Constants — `LORA_REPO`, `BASE_MODEL`, recommended step count, guidance, LoRA scale, trigger word.
- Module-level model load — pipeline `from_pretrained`, `.to("cuda")`, `load_lora_weights`. If the LoRA repo is private, pass `token=os.environ["HF_TOKEN"]`.
- Preprocessing functions (if any) — pose extraction, padding, mask building. CPU code can run at module level; GPU code must be inside a `@spaces.GPU` function.
- The inference function — decorated with `@spaces.GPU(duration=...)`. Validates inputs, applies the trigger word, builds pipeline kwargs, returns outputs.
- The Gradio Blocks — the UI from Phase 3, wired to the inference function.

Common things to get right:

- Return the actually-used seed alongside the result so the user can reproduce.
- `gr.Progress(track_tqdm=True)` on the inference function surfaces diffusers' internal progress bar.
- Validate inputs — raise `gr.Error("Please upload an image first.")` when a required input is missing.
- On `gr.Examples`, use `cache_examples=True, cache_mode="lazy"` — plain `cache_examples=True` runs examples at build time and fails on ZeroGPU.

#### `requirements.txt`

Derive from what the Space actually needs, in this order:

1. **Every top-level non-stdlib import in `app.py`** — if `app.py` does `import cv2`, list `opencv-python`; `from controlnet_aux import OpenposeDetector` → `controlnet-aux`.
2. **What the base-model reference's "Required dependencies" subsection says** — e.g. `torchvision` for Qwen-Image (Qwen 2.5-VL text encoder), `imageio[ffmpeg]` for LTX (video export). These aren't picked up from imports because the pipeline imports them transitively at load time.
3. **What the LoRA's own model card explicitly mentions installing.**
4. **The diffusers/ML stack:** `diffusers`, `transformers`, `accelerate`, `peft`, `safetensors`. Default to plain (unpinned). Switch `diffusers` to `git+https://github.com/huggingface/diffusers` if the base-model reference says the model needs it (recent releases often do — Qwen-Image-Edit-2511 is a current example).

**What NOT to list:**

- **`gradio`** — controlled by `sdk_version:` in `README.md` frontmatter, not `requirements.txt`.
- **`torch`, `spaces`, `huggingface_hub`** — provided by the ZeroGPU runtime. Only add if you need a specific version pinned (rare, usually a sign something else is wrong).

**Bias for everything else: include rather than skip when uncertain.** A package the Space doesn't use causes a slightly slower build; a missing required package causes a startup crash that's much harder to diagnose.

**Two deps are NOT safe to add reflexively** on ZeroGPU:

- `xformers` — pinned to specific torch versions, frequent source of conflicts. The ZeroGPU runtime ships torch 2.8+, so any pinned version must support that. Blackwell gotcha: xformers' FA3 dispatch mis-gates the hardware and crashes at kernel launch with `CUDA invalid argument`. If a Space using xformers attention hits this, disable FA3 dispatch at module load:
  ```python
  try:
      from xformers.ops.fmha import _set_use_fa3
      _set_use_fa3(False)
  except Exception:
      pass
  ```
  Only include `xformers` if `app.py` actually uses it.
- `flash-attn` — needs a build step, often fails to install. Same torch 2.8+ alignment caveat. Only include if `app.py` actually uses it.

**Pin other versions only when you have a reason** (known incompatibility, or matching a model-card recipe).

#### `README.md`

Spaces are configured by the YAML frontmatter at the top of `README.md` — this selects ZeroGPU.

```
---
title: <human-readable title>
emoji: 🎨
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: <current Gradio version>
app_file: app.py
pinned: false
hardware: zero-a10g
short_description: <one short line for the Space tile, ~60 chars max>
models:
  - <base model repo>
  - <lora repo>
---

# <title>

A short description with links to the LoRA and base model.
```

Key fields:

- `sdk: gradio` — required for ZeroGPU.
- `sdk_version` — match the Gradio version you wrote against (`pip index versions gradio`, or https://www.gradio.app) rather than guessing.
- `hardware: zero-a10g` — the legacy string for ZeroGPU. The actual hardware is NVIDIA RTX Pro 6000 Blackwell, but the identifier is `zero-a10g`. ZeroGPU is available to PRO, Team, and Enterprise accounts; without a subscription the Space falls back to CPU.
- `models:` — list base and LoRA repos. Enables Hub caching and discovery.
- `short_description` — **keep it short (~60 characters or less).** The Hub's YAML validator rejects long values with a 400 from `https://huggingface.co/api/validate-yaml`, surfacing as an `HfHubHTTPError` during `create_repo`/`upload_file`. If you hit the 400, shorten this field.

#### Single batched approval — order of operations matters

**Write all three files first, then show them all together in one message.** Not "write app.py → talk → write requirements → talk → write README → talk." That produces three approval moments even without explicit asking.

1. Write `app.py`, `requirements.txt`, `README.md` in succession with **no intervening prose**.
2. Then, in a single message, ask for approval covering all three: *"Here's the Space — `app.py` (N lines), `requirements.txt`, and `README.md`. Review and confirm to publish, or tell me what to change."*
3. The user responds once, covering whatever they want changed across any of the three files.

Avoid: walking through `app.py`'s structure after writing it but before writing the others; asking "ready for the next one?"; showing one file inline and offering to "show the next when you're ready"; treating any of the three as optional.

### Phase 5 — Publish the Space

Use the authenticated session from Phase 1. Default to **private** so the user can vet the Space before flipping it public. Confirm the target username first: *"I'll publish to `{username}/{space_name}` — confirm?"*

```python
from huggingface_hub import HfApi, SpaceHardware

api = HfApi(token=hf_token)
username = api.whoami()["name"]
repo_id = f"{username}/{space_name}"

api.create_repo(
    repo_id=repo_id,
    repo_type="space",
    space_sdk="gradio",
    space_hardware=SpaceHardware.ZERO_A10G,
    private=True,
    exist_ok=True,
)

for path in ["app.py", "requirements.txt", "README.md"]:
    api.upload_file(path_or_fileobj=path, path_in_repo=path,
                    repo_id=repo_id, repo_type="space")
```

If the LoRA repo itself is private/gated, set the token as a Space secret so the Space can download the LoRA at runtime:

```python
api.add_space_secret(repo_id=repo_id, key="HF_TOKEN", value=HF_TOKEN)
```

…and in `app.py`, load the LoRA with `token=os.environ["HF_TOKEN"]`.

**Publish-time failures (before the build starts):**

- **`HfHubHTTPError: 400 Bad Request` from `validate-yaml`** during `create_repo`/`upload_file`. The README YAML failed server-side validation. Most commonly a too-long `short_description`; sometimes a stray field or malformed value. Fix: shorten `short_description` to ~60 chars and retry. If that doesn't fix it, look for typos in field names or invalid values (unsupported `colorFrom`/`colorTo` colors, invalid `hardware` string).
- **403 on `create_repo`** with `space_hardware="zero-a10g"`: user isn't on PRO/Team/Enterprise. Fix: retry `create_repo` without `space_hardware`, leave `hardware: zero-a10g` in the README YAML — the Space gets created on CPU. The user can then upgrade to PRO (auto-promotes) or apply for a [community GPU grant](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants).
- **401/403 on `upload_file`**: token doesn't have write scope. Fix: ask for a write-scoped token.

**Common build failures (after the build starts):**

- LoRA `weight_name` mismatch → check the actual filename via `list_repo_files`.
- Base model gated and token wasn't set as a Space secret.
- ZeroGPU not allocated (user not on PRO) → Space falls back to CPU and is unusably slow.
- Diffusers version doesn't recognize the pipeline class → pin to git diffusers in `requirements.txt`.
- Missing dependency at module load → see the `requirements.txt` derivation rules; most common case is a transitive dep like `torchvision` for Qwen-Image's text encoder.

If a build fails, offer to read the logs and propose a fix.

### Phase 6 — Smoke-test the Space

Before declaring the Space done and handing over the URL, exercise it once end-to-end. Several failure modes (wrong `weight_name`, wrong pipeline class, missing transitive dep, gated-base-model token issue) build cleanly and only surface at first inference. The `gradio info` / `gradio predict` CLI (see "Prediction CLI" above) does exactly this.

**Step 1 — Wait for the build.** `create_repo` returns immediately; the container image is still building. Poll `HfApi().get_space_runtime(repo_id).stage` until `RUNNING`:

```python
import time
from huggingface_hub import HfApi
api = HfApi(token=hf_token)
while True:
    stage = api.get_space_runtime(repo_id).stage
    if stage == "RUNNING": break
    if stage in {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR"}:
        raise RuntimeError(f"Build failed: {stage}. Logs: https://huggingface.co/spaces/{repo_id}/logs/container")
    time.sleep(15)
```

If the build fails, fetch the container logs (`https://huggingface.co/spaces/{repo_id}/logs/container`), read the traceback, and propose a fix. Don't run `gradio info` against a Space that isn't running — it'll hang or 503.

**Step 2 — Verify the endpoint signature.** `gradio info {repo_id} --token {hf_token}` returns the exposed endpoints and parameter types. Confirm: (a) the endpoint exists (default `/predict`, but Blocks Spaces often have a custom name from the function name), (b) parameters in order match `app.py`, (c) file-typed params show `"type": "filepath"`. If any of this is off, the UI may look correct but API calls will fail — fix and re-upload.

**Step 3 — Run one real inference.** Pick the lightest viable input — the simplest example from the LoRA card, or a `gr.Examples` entry. Pass `--token` for private Spaces. File inputs use `{"path": "...", "meta": {"_type": "gradio.FileData"}}`.

```bash
# Text-to-image:
gradio predict {repo_id} /predict '{"prompt": "...", "aspect_ratio": "1:1"}' --token $HF_TOKEN

# Image-to-image (file input):
gradio predict {repo_id} /predict '{"input_image": {"path": "/tmp/sample.jpg", "meta": {"_type": "gradio.FileData"}}, "prompt": "..."}' --token $HF_TOKEN
```

If you don't have a local sample image for I2I, lift one from the LoRA repo (`hf_hub_download(repo_id, filename="example.png")`) or the base model card.

**Caveat for creative-mode Spaces.** `gradio info`/`gradio predict` only exercise the Python endpoint — they tell you nothing about whether custom JS in a `gr.HTML` widget works. If the Space uses creative mode, after the API smoke-test passes, **open the Space URL in a browser and verify the interaction once** before sharing.

**Step 4 — Interpret the result.**

- **Returns successfully and output looks plausible** → done. Share the URL.
- **HTTPError 503 / "Space is sleeping"** → the Space spun down between steps 1 and 3. Wake it (`api.restart_space(repo_id)`) and retry.
- **Inference error mentioning `weight_name` / `safetensors`** → the LoRA filename in `app.py` doesn't match the actual file. Re-check `list_repo_files`, fix `weight_name=`, re-upload `app.py`.
- **Inference error mentioning a missing pipeline class/attribute** → diffusers version too old. Switch `requirements.txt` to `git+https://github.com/huggingface/diffusers` and re-upload.
- **`ImportError` at module load** → missing dep. Add it to `requirements.txt` and re-upload. The runtime logs (`/logs/run`) name the missing package.
- **OOM** → reduce default resolution or step count, or pick a smaller base variant.
- **Timeout / hangs** → bump `@spaces.GPU(duration=...)` and re-upload.

The smoke-test converts these from "user discovers it and reports back" to "you discover it and fix it before sharing."

## What to avoid

- A generic "one demo for all LoRAs" template. The whole point is to tailor.
- Lazy-loading the model inside the GPU function. Slow on ZeroGPU, and hides startup errors until first request.
- `torch.compile`. Not supported on ZeroGPU.
- `cache_examples=True` without `cache_mode="lazy"` on ZeroGPU.
- Uploading the LoRA weights into the Space repo. Pull from the LoRA's own Hub repo at runtime.
- Asking for the HF token only at the end, then discovering the LoRA was private all along and you couldn't read the model card.
- Exposing every diffusers knob. Pick the 1–3 controls that matter for this LoRA.
- Long preambles in the chat reply once the Space is published. The Space URL is the deliverable.

## Additional Reference

- [End-to-End Examples](examples.md) — complete working apps

## Merged from

- `huggingface-lora-space-builder` — end-to-end workflow for building and publishing a tailored LoRA demo Space (gather info, pick pipeline, design UI, write files, publish, smoke-test)
- `huggingface-zerogpu` — ZeroGPU runtime rules: `@spaces.GPU`, duration/quota, CUDA availability model, process isolation, concurrency, call granularity, CUDA build constraints, example caching, dependency management

## Limitations

- Use this skill only when the task clearly matches its upstream product or API scope.
- Verify commands, API behavior, pricing, quotas, credentials, and deployment effects against current official documentation before making changes.
- Do not treat generated examples as a substitute for environment-specific tests, security review, or user approval for destructive or costly actions.