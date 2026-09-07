# Platform assumptions

Checked: 2026-09-07

This protocol relies only on documented ChatGPT capabilities and keeps uncertain
account limits outside the architecture.

## Confirmed

- ChatGPT can generate and edit images, and an attached image can be used as
  visual guidance. Built-in generation currently uses `gpt-image-2` and consumes
  included usage limits faster than an ordinary non-image turn. Availability and
  exact limits depend on plan/workspace settings.  
  Source: [ChatGPT image generation](https://learn.chatgpt.com/docs/image-generation)
- Projects preserve related chats, files, sources and project instructions.
  Local projects can expose folders; durable repository guidance belongs in
  `AGENTS.md` or checked-in documentation.  
  Source: [Projects and chats](https://learn.chatgpt.com/docs/projects)
- Codex reads repository `AGENTS.md` before work and applies more local guidance
  later in the instruction chain.  
  Source: [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Scheduled tasks can run in a desktop local project when the app and computer
  remain running. Web scheduled tasks can use uploaded/project context but cannot
  directly retain an arbitrary local folder between runs.  
  Source: [Scheduled tasks](https://learn.chatgpt.com/docs/automations)

## Architectural consequences

- The protocol binds references as actual media, not prose descriptions.
- Included image capacity is treated as finite and account-specific; no numeric
  quota is hard-coded.
- A retryable checkpoint exists for quota/tool interruption.
- Git is the durable text/state authority; generated image bytes are hash-bound
  when the current Work surface exposes a file artifact.
- No code pretends the ChatGPT subscription is an unattended image API.

## Inference, not platform guarantee

The board-first strategy is this project's engineering hypothesis: drawing
related shots in one generation should reduce within-episode visual drift because
the model resolves them in one image. It still requires the calibration fixture;
OpenAI documentation does not promise comic-character consistency across cells.

