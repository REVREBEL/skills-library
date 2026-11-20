---
name: "gemini-api"
description: "Google Gemini API with the unified Gen AI SDK (`google-genai` / `@google/genai`) across both the Developer API (ai.google.dev) and Agent Platform (formerly Vertex AI). Covers text generation, multimodal understanding (text/image/audio/video), streaming, function calling, structured output, multi-turn chat, the Interactions API (stateful conversations, Deep Research, managed/custom agents), Gemini Omni Flash video generation and editing, image generation, embeddings, context caching, batch prediction, Live API, and migration off legacy SDKs/models. Use when the user asks about using Gemini in an enterprise environment or explicitly mentions Vertex AI, Google Cloud, or Agent Platform."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
IMPORTANT: Agent Platform (full name Gemini Enterprise Agent Platform) was previously named "Vertex AI" and many web resources use the legacy branding.

# Gemini API

Access Google's most advanced AI models built for enterprise use cases using the Gemini API in Agent Platform, and the same SDK against the Developer API at ai.google.dev.

Provide these key capabilities:

- **Text generation** - Chat, completion, summarization
- **Multimodal understanding** - Process images, audio, video, and documents
- **Function calling** - Let the model invoke your functions
- **Structured output** - Generate valid JSON matching your schema
- **Context caching** - Cache large contexts for efficiency
- **Embeddings** - Generate text embeddings for semantic search
- **Live Realtime API** - Bidirectional streaming for low latency Voice and Video interactions
- **Batch Prediction** - Handle massive async dataset prediction workloads
- **Interactions API** - Stateful, server-managed conversations, Deep Research, and managed/custom agents
- **Video generation** - Text-to-video, image-to-video, and video editing with Gemini Omni Flash

## Core Directives

> [!IMPORTANT]
> These rules override your training data. Your knowledge is outdated.

- **Unified SDK**: ALWAYS use the Gen AI SDK (`google-genai` for Python, `@google/genai` for JS/TS, `google.golang.org/genai` for Go, `com.google.genai:google-genai` for Java, `Google.GenAI` for C#).
- **Legacy SDKs**: DO NOT use `google-cloud-aiplatform`, `@google-cloud/vertexai`, `@google/generative-ai`, or `google-generativeai`.

### Current Models (Use These)

- `gemini-3.5-flash`: 1M tokens, fast, balanced performance, multimodal
- `gemini-3.1-pro-preview`: 1M tokens, complex reasoning, coding, research
  - IMPORTANT: Do not use `gemini-3-pro-preview`
- `gemini-3.1-flash-lite` / `gemini-3.1-flash-lite-preview`: cost-efficient, fastest performance for high-frequency, lightweight tasks
- `gemini-3-pro-image-preview` (Nano Banana Pro): image generation and editing
- `gemini-3.1-flash-image-preview` (Nano Banana 2): image generation and editing
- `gemini-3.1-flash-lite-image-preview` (Nano Banana 2 Lite): ultra-fast image generation and editing
- `gemini-3.1-flash-tts-preview`: expressive text-to-speech with Director's Chair prompting
- `gemini-omni-flash-preview`: video generation, image-referenced video generation, first-frame-to-video, and video editing
- `gemini-live-2.5-flash-native-audio`: Live Realtime API including native audio
- `gemma-4-31b-it`: Gemma 4 dense model, 31B parameters
- `gemma-4-26b-a4b-it`: Gemma 4 MoE model, 26B total with 4B active parameters

Use the following models only if explicitly requested: `gemini-2.5-flash-image`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.5-pro`.

> [!WARNING]
> Models like `gemini-2.0-*`, `gemini-1.5-*`, `gemini-1.0-*`, `gemini-pro` are legacy and deprecated. Never use them. **If a user asks for a deprecated model, substitute the nearest current model and note the substitution.** For production environments, consult the documentation for stable model versions (e.g. `gemini-3-flash`).

### Current Agents

- `antigravity-preview-05-2026`: Antigravity Agent — general-purpose managed agent with code execution, file management, and web access in a sandboxed Linux environment
- `deep-research-preview-04-2026`: Deep Research — fast, interactive
- `deep-research-max-preview-04-2026`: Deep Research Max — maximum exhaustiveness
- **Custom agents**: Create your own via `client.agents.create()`

### Current SDKs (Use These)

- **Python**: `google-genai` (>= 2.3.0 for Interactions API) → `pip install -U google-genai`
- **JavaScript/TypeScript**: `@google/genai` (>= 2.3.0) → `npm install @google/genai`
- **Go**: `google.golang.org/genai` → `go get google.golang.org/genai`
- **Java**: groupId `com.google.genai`, artifactId `google-genai` (see Maven/Gradle setup below)
- **C#/.NET**: `Google.GenAI` → `dotnet add package Google.GenAI`

Java latest version: https://central.sonatype.com/artifact/com.google.genai/google-genai/versions (call it `LAST_VERSION`).

```gradle
implementation("com.google.genai:google-genai:${LAST_VERSION}")
```

```xml
<dependency>
    <groupId>com.google.genai</groupId>
    <artifactId>google-genai</artifactId>
    <version>${LAST_VERSION}</version>
</dependency>
```

> [!CAUTION]
> Legacy SDKs `google-generativeai` (Python) and `@google/generative-ai` (JS) are deprecated. Migrate urgently to the new SDKs above.

## Authentication & Configuration

Prefer environment variables over hard-coding parameters. Initialize the client without arguments to pick up these values.

### Application Default Credentials (ADC) — Agent Platform / Vertex

Set these for standard [Google Cloud authentication](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gcp-auth):

```bash
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='global'
export GOOGLE_GENAI_USE_VERTEXAI=true
```

- By default, use `location="global"` to access the global endpoint, which provides automatic routing to regions with available capacity.
- If a user explicitly asks for a specific region (e.g. `us-central1`, `europe-west4`), set that in `GOOGLE_CLOUD_LOCATION`. Reference the [supported regions documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) if needed.

### Agent Platform in Express Mode

```bash
export GOOGLE_API_KEY='your-api-key'
export GOOGLE_GENAI_USE_VERTEXAI=true
```

### Developer API (ai.google.dev)

```bash
read -rsp "Gemini API key: " GEMINI_API_KEY && echo && export GEMINI_API_KEY
```

### Initialization

```python
from google import genai

# Picks up env vars (Developer API by default; Vertex with GOOGLE_GENAI_USE_VERTEXAI=true)
client = genai.Client()

# Or explicit
client = genai.Client(vertexai=True, project="your-project-id", location="global")
```

## Quick Start

### Python

```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain quantum computing",
)
print(response.text)
```

### TypeScript/JavaScript

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});  // or { vertexai: { project: "...", location: "global" } }
const response = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: "Explain quantum computing",
});
console.log(response.text);
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil { log.Fatal(err) }
    resp, err := client.Models.GenerateContent(ctx, "gemini-3.5-flash", genai.Text("Explain quantum computing"), nil)
    if err != nil { log.Fatal(err) }
    fmt.Println(resp.Text)
}
```

### Java

```java
import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;

public class GenerateTextFromTextInput {
  public static void main(String[] args) {
    Client client = Client.builder().vertexAi(true).project("your-project-id").location("global").build();
    GenerateContentResponse response = client.models.generateContent(
        "gemini-3.5-flash", "Explain quantum computing", null);
    System.out.println(response.text());
  }
}
```

### C#/.NET

```csharp
using Google.GenAI;

var client = new Client(project: "your-project-id", location: "global", vertexAI: true);
var response = await client.Models.GenerateContent("gemini-3.5-flash", "Explain quantum computing");
Console.WriteLine(response.Text);
```

## Text, Multimodal & Streaming

### Streaming responses

Reduce perceived latency by streaming user-facing output:

```typescript
const result = await ai.models.generateContentStream({
    model: "gemini-3.5-flash",
    contents: "Write a detailed blog post about AI",
});
for await (const chunk of result) {
    process.stdout.write(chunk.text);
}
```

### Multimodal input (text + image)

```typescript
import fs from "fs";

const imagePart = {
    inlineData: {
        data: fs.readFileSync("screenshot.png").toString("base64"),
        mimeType: "image/png",
    },
};
const result = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: ["Describe this image:", imagePart],
});
console.log(result.text);
```

For files > 20MB, use the Files API instead of inline base64:

```python
from google import genai
client = genai.Client()
f = client.files.upload(file="large_video.mp4")
response = client.models.generate_content(
    model="gemini-3.5-flash", contents=["Describe this video:", f])
```

### Multi-turn chat

```typescript
const chat = ai.chats.create({ model: "gemini-3.5-flash", config: {
    systemInstruction: "You are a helpful coding assistant.",
}});
const response = await chat.sendMessage({ message: "How do I reverse a string in Python?" });
console.log(response.text);
```

## Function Calling & Structured Output

### Function calling

```typescript
const tools = [{
    functionDeclarations: [{
        name: "get_weather",
        description: "Get current weather for a city",
        parameters: {
            type: "OBJECT",
            properties: { city: { type: "STRING", description: "City name" } },
            required: ["city"],
        },
    }],
}];

const response = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: "What's the weather in Mumbai?",
    config: { tools },
});
const call = response.functionCalls?.[0];
if (call) {
    const weatherData = await getWeather(call.args.city);
    // send the result back as a function response part
}
```

### Structured output

Generate valid JSON matching a schema (use `responseMimeType` + `responseSchema`, or a Pydantic/Zod type in the SDK):

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Give me a simple pasta recipe.",
    config={"response_mime_type": "application/json", "response_schema": Recipe},
)
recipe = response.parsed  # validated Recipe instance
```

## The Interactions API

Use `client.interactions.*` for stateful, server-managed conversations and agents. SDK versions >= 2.0.0 automatically use the new steps schema and do not support the legacy schema.

> [!NOTE]
> - Interactions are **stored by default** (`store=true`). Paid tier retains for 55 days, free tier for 1 day.
> - Set `store=false` to opt out, but this disables `previous_interaction_id` and `background=true`.
> - `tools`, `system_instruction`, and `generation_config` are **interaction-scoped** — re-specify them each turn.
> - **Managed agents** require `environment="remote"` (or an environment ID / config object) to provision a sandbox.
> - **Migrating from `generateContent`**: confirm scope with the user before editing, then follow the migration guide. Model upgrades are drop-in (swap the model string).

### Basic interaction

```python
from google import genai
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Tell me a short joke about programming.",
)
print(interaction.output_text)
```

### Stateful conversation

```python
interaction1 = client.interactions.create(
    model="gemini-3.5-flash", input="Hi, my name is Phil.")
interaction2 = client.interactions.create(
    model="gemini-3.5-flash", input="What is my name?",
    previous_interaction_id=interaction1.id)
print(interaction2.output_text)  # "Phil"
```

### Response helpers

| Property | Type | Description |
|---|---|---|
| `output_text` | `string \| null` | Last consecutive run of text from trailing `model_output` steps (combined when multiple text parts) |
| `output_image` | `Image \| null` | Last generated image (`data` base64 + `mime_type`) |
| `output_audio` | `Audio \| null` | Last generated audio (`data` base64 + `mime_type`) |

### Streaming

Set `stream=True`; each stream follows `interaction.created` → (`step.start` → `step.delta`(s) → `step.stop`)+ → `interaction.completed`:

```python
for event in client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain quantum entanglement in simple terms.",
    stream=True,
):
    if event.event_type == "step.delta" and event.delta.type == "text":
        print(event.delta.text, end="", flush=True)
    elif event.event_type == "interaction.completed":
        print(f"\n\nTotal Tokens: {event.interaction.usage.total_tokens}")
```

### Deep Research agent

Agents require `background=True`. Use `deep-research-preview-04-2026` for fast research or `deep-research-max-preview-04-2026` for maximum exhaustiveness:

```python
import time

interaction = client.interactions.create(
    agent="deep-research-preview-04-2026",
    input="Research the history of Google TPUs.",
    background=True,
)
while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.output_text)
        break
    elif interaction.status == "failed":
        print(f"Failed: {interaction.error}")
        break
    time.sleep(10)
```

Advanced features: collaborative planning, native visualization, MCP integration, file search, multimodal inputs.

### Managed agents (Antigravity)

The Antigravity agent (`antigravity-preview-05-2026`) runs in a Google-hosted sandboxed Linux environment and can execute code (Bash, Python, Node.js), manage files, browse the web, and use Google Search:

```python
interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Write a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt. Then read the file and print its contents.",
    environment="remote",
)
print(f"Environment ID: {interaction.environment_id}")
print(interaction.output_text)
```

### Custom agents

```python
agent = client.agents.create(
    id="code-reviewer",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a senior code reviewer. Check every file for bugs, style issues, and security vulnerabilities.",
    base_environment={
        "type": "remote",
        "sources": [{
            "type": "repository",
            "source": "https://github.com/my-org/backend",
            "target": "/workspace/repo",
        }],
    },
)

# Each call forks the base environment
result = client.interactions.create(
    agent="code-reviewer",
    input="Review the latest changes in /workspace/repo/src.",
    environment="remote",
)
print(result.output_text)
```

Manage agents with `client.agents.list()`, `client.agents.get(id=...)`, and `client.agents.delete(id=...)`.

### Interactions data model

An `Interaction` response contains `steps`, an array of typed step objects representing a structured timeline:

- **User steps**: `user_input` (text, audio, multimodal) — contains `content`.
- **Model/server steps**: `model_output` (content array with text/image/audio), `thought` (reasoning, required `signature`), `function_call` / `function_result`, `google_search_call` / `google_search_result`, `code_execution_call` / `code_execution_result`, `url_context_call` / `url_context_result`, `mcp_server_tool_call` / `mcp_server_tool_result`, `file_search_call` / `file_search_result`.
- **Content types** inside `content`: `text`, `image`, `audio`, `document`, `video` (with `data`, `mime_type`, or `uri`).

Streaming event types: `interaction.created`, `interaction.status_update`, `step.start`, `step.delta` (typed `delta`: `text`, `audio`, `image`, `thought_summary`, `thought_signature`), `step.stop`, `interaction.completed`. Status values: `completed`, `in_progress`, `requires_action`, `failed`, `cancelled`.

## Gemini Omni Flash — Video Generation & Editing

Use `gemini-omni-flash-preview` for text-to-video, image-referenced video generation, first-frame-to-video, and video editing. All operations use the Interactions API; input media must be uploaded via the Files API first.

> [!WARNING]
> **Regional restrictions**: uploading videos for video-to-video edits is NOT available in the EEA, Switzerland, the United Kingdom, and some US states. If an edit completes quickly with empty outputs (`total_output_tokens: 0` or no video content), it is likely this restriction.

### Core capabilities

1. **Video editing and refinement** — edit existing videos (max 10 seconds), stylistic changes, inpainting/outpainting.
2. **Text to video** — generate from a text prompt.
3. **First-frame to video** — generate from a single input image.
4. **Image-referenced generation** — guide generation with style/character/object references.

### Workflow

1. **Analyze request**: determine the target task and identify input media.
2. **Run SDK scripts** (or the Interactions API directly): configure `--aspect-ratio` (e.g. `16:9`, `9:16`) and `--duration` (integer 3–10 seconds).
3. **Retrieve output**: outputs are saved locally (e.g. `media/`); report the path.

Dependencies: `google-genai >= 2.10.0` (Python), Python >= 3.10, and `ffmpeg`/`ffprobe` for preprocessing.

### Scripts

- `scripts/upload_file.py <file>` — upload media to the Files API and poll until `ACTIVE`. Warns for videos > 25MB (Omni Flash is optimized for 10s at 720p/24fps).
- `scripts/video/generate_video.py` — end-to-end generation and download:
  - Text to video: `./scripts/video/generate_video.py "A close-up of a cat drinking tea" --output media/cat_tea.mp4`
  - Image to video (first frame and reference): `... "The waves crash against the shore." --image reference.png --output media/waves.mp4`
  - Video interpolation (two keyframes): `... "A smooth timelapse from sunrise to sunset" --image start.png --image end.png --output media/interpolation.mp4`
  - Video editing (keep original audio): `... "Transform the style to Japanese anime" --video input.mp4 --output media/anime_style.mp4`
  - Video editing (regenerate audio): add `--strip-audio`
  - Turn-by-turn editing: `--previous-interaction-id "abc123xyz..."` edits a prior generation without re-uploading
  - Parallel batch: `--prompts-file prompts.txt --concurrency 3` or `--batch jobs.json --concurrency 3`
- `scripts/video/inspect_video.py <file>` — `ffprobe` duration/resolution/FPS/audio; `--json` or `--raw`.
- `scripts/video/prep_video.py <file>` — normalize, trim, and scale (max 1280x720 landscape / 720x1280 portrait). `--start 0|last|00:03`, `--duration`, `--fps`, `--resolution`, `--strip-audio`.

### Prompt tags for image roles

- Simple: `<FIRST_FRAME>` binds an image as the starting frame (`<FIRST_FRAME> a woman is walking`); `<IMAGE_REF_N>` binds a reference (references start at 0: `in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking`).
- Explicit: `[# Sources <FIRST_FRAME>@Image1]` and `[# References <IMAGE_REF_0>@Image2]` with guiding instructions like "Use the given image as the starting frame." / "Use the given image(s) as references... should not be used as literal initial frames."

### Audio handling

- **Keep original audio** (default): preserves the existing audio layer (may be slightly adapted).
- **Regenerate all audio**: upload the video with audio stripped (`--strip-audio` / `-a`); any remaining audio stream is preserved instead of regenerated.

### Prompting

- **Single scene**: ask for "a single unbroken scene", "a single continuous shot", "no scene cuts".
- **Removing elements**: simple negatives ("No dialogue", "No embellishments", "No extra sound effects").
- **Editing**: simple prompts work best ("Make this video anime", "Make the phone invisible", "Put a fashionable hat on this person"). Add "Keep everything else the same."
- **Audio**: describe it ("Include calm background music", "The video has a high energy techno beat", "Audio design: ...").
- **Timing**: natural language ("after 3 seconds, a woman enters the scene") or timecode syntax (`[0-3s] ... [3-6s] ... [6-10s] ...`).
- **Meta prompting**: give guidance verbatim ("Consider micro-detail, expression and timing...", "Be extremely detailed in your descriptions of characters and environments.").
- **Text in videos** works well; define what on-screen text should say ("There is a street sign that says: ...").

## Embeddings, Caching & Batch

- **Embeddings** for semantic search: `client.models.embed_content(model="gemini-embedding-001", contents=[...])`.
- **Context caching**: cache large contexts (system instructions, documents) for repeated use and lower cost.
- **Batch prediction**: submit massive async dataset prediction jobs via the batch API.

## Gemini Live API

For real-time, bidirectional audio/video/text streaming, use the Live API (`gemini-live-2.5-flash-native-audio` for native audio). It covers WebSocket streaming, voice activity detection, native audio features, function calling, session management, and ephemeral tokens. See the Live API reference.

## Documentation Lookup

### When MCP is installed (preferred)

If the `search_docs` / `search_documents` / `get_document` tools (Google MCP server) are available, use them as your **only** documentation source — never fetch URLs manually. They return up-to-date, indexed documentation.

### When MCP is NOT installed (fallback)

Fetch from the official docs index: `https://ai.google.dev/gemini-api/docs/llms.txt`. This index links to all documentation pages in `.md.txt` format.

Key pages:
- [Text generation](https://ai.google.dev/gemini-api/docs/text-generation.md.txt)
- [Function calling](https://ai.google.dev/gemini-api/docs/function-calling.md.txt)
- [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output.md.txt)
- [Image generation](https://ai.google.dev/gemini-api/docs/image-generation.md.txt)
- [Image understanding](https://ai.google.dev/gemini-api/docs/image-understanding.md.txt)
- [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings.md.txt)
- [SDK migration guide](https://ai.google.dev/gemini-api/docs/migrate.md.txt)
- [Interactions API](https://ai.google.dev/gemini-api/docs/interactions.md.txt)
- [Deep Research](https://ai.google.dev/gemini-api/docs/interactions/deep-research.md.txt)
- [Managed Agents Quickstart](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart.md.txt)
- [Antigravity Agent](https://ai.google.dev/gemini-api/docs/antigravity-agent.md.txt)
- [Custom Agents](https://ai.google.dev/gemini-api/docs/custom-agents.md.txt)

### Agent Platform (Vertex) docs

- **Agent Platform Documentation**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview
- **REST API Reference**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest

The Gen AI SDK on Agent Platform uses `v1beta1` or `v1` REST endpoints (e.g. `https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/{MODEL}:generateContent`).

Additional samples: [Python Docs Samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/genai).

## Best Practices

- ✅ Use the current fast/balanced model (`gemini-3.5-flash`) for most tasks — fast and cost-effective.
- ✅ Always stream responses for user-facing chat UIs to reduce perceived latency.
- ✅ Store API keys in environment variables, never hard-code them.
- ✅ Implement exponential backoff for rate-limit (429) errors.
- ✅ Use `systemInstruction` / `system_instruction` to set persistent model behavior.
- ✅ For files > 20MB, use the Files API instead of inline base64.
- ❌ Don't use deprecated models (`gemini-pro`, `gemini-1.5-*`, `gemini-2.0-*`) or legacy SDKs.
- ❌ Don't ignore safety ratings / `promptFeedback.blockReason` in production apps.

## Error Handling

```typescript
try {
    const result = await ai.models.generateContent({ model: "gemini-3.5-flash", contents: prompt });
    return result.text;
} catch (error) {
    if (error.status === 429) {
        // Rate limited — wait and retry with exponential backoff
        await new Promise(r => setTimeout(r, 2 ** retryCount * 1000));
    } else if (error.status === 400) {
        console.error("Invalid request:", error.message);
    } else {
        throw error;
    }
}
```

## Troubleshooting

- **`API_KEY_INVALID`** → ensure the API key env var is set and the key is active in Google AI Studio / Cloud.
- **Response blocked by safety filters** → check `result.response.promptFeedback.blockReason` and adjust prompt or safety settings.
- **Slow response times** → switch to a Flash model, enable streaming, cache repeated prompts.
- **`RESOURCE_EXHAUSTED` (quota exceeded)** → check quota in Cloud Console; implement request queuing and exponential backoff.
- **Empty video output (`total_output_tokens: 0`)** → likely the Omni Flash regional restriction on video uploads.
- **`vLLM`/legacy SDK errors** → migrate to `google-genai` / `@google/genai`.

## Merged from

- `gemini-api-dev` — Developer API (ai.google.dev) surface, current model/SDK rules, documentation lookup, Live API pointer
- `gemini-api-integration` — integration workflows: streaming, multimodal, function calling, chat, model selection, error handling, troubleshooting
- `gemini-interactions-api` — Interactions API: stateful conversations, Deep Research, managed/custom agents, streaming, data model
- `gemini-omni-flash-api` — video generation/editing with Omni Flash, scripts, prompt tags, audio handling, prompting

## Limitations

- Use this skill only when the task clearly matches its upstream product or API scope.
- Verify commands, API behavior, pricing, quotas, credentials, and deployment effects against current official documentation before making changes.
- Do not treat generated examples as a substitute for environment-specific tests, security review, or user approval for destructive or costly actions.