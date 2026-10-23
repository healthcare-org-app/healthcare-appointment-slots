# Working on this repo

Contract-first Flask API (`openapi.yaml` at the root, code in `app/`, pytest in `tests/`, Postman collection in `postman/`). CI checks: `ci` (pytest) and `quality-gate`, the [Postman agent quality gate](https://github.com/Postman-Devrel/postman-agent-quality-gate) (config `quality-gate.yml`, caller `.github/workflows/quality-gate.yml`). The gate comes from the `postman-agent-quality-gate` Claude Code plugin (enabled in `.claude/settings.json`). For Postman work, see `postman/skills/`.

## The loop for any change to the contract, the code or the Postman objects

Follow the `gate-loop` skill, with **appointment-slots-developer** (`.claude/agents/`) as the coder and `postman-agent-quality-gate:gate-verdict` as the reviewer.

1. **Branch.** Work on a branch, never on `main`. appointment-slots-developer changes the contract first, then code, tests and the collection, checks locally (`pytest -q`, `npx github:Postman-Devrel/postman-agent-quality-gate#v1 run`), pushes, and reports the branch and the full commit SHA.
2. **Verdict.** After every push, and on every CI event about a failing `quality-gate` check, call gate-verdict with the branch and that exact SHA. Do not read the CI output yourself and do not fix from the raw event.
3. **Fix.** If FAILED, give the brief word for word to the **same** appointment-slots-developer (SendMessage), which pushes to the **same branch**. Back to step 2 with the new SHA.
4. **Stop** after 3 rounds, or on PASSED, and report: rounds, rating per round, what changed, the branch or PR link, and the gaps.

## Rules

- Never merge, force-push or push to `main` unless the user asks for it.
- Never edit `quality-gate.yml`, `.github/` or `.claude/` to get a better verdict. If the gate itself looks wrong, say so and stop.
- Never rename or remove a field, path or response that consumers use, and never make an existing request field required: add next to it, or version the API.
- Never move or rename `openapi.yaml`, `service.yaml` or `app/`, nor the repo or service names.
- Never call `https://myhealthcare.dev` (production, `servers[0]` in the spec). The collection's `baseUrl` stays `http://localhost:8601`.
- Never add, change or remove a gate exception (`contract-lint.exceptions` in `quality-gate.yml`): flag the finding for a human instead.
- No secrets in files.
- A `not_available` or degraded step is a gap, not a pass: say so in the report.
