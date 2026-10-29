# Hosted proof explorer

The repository-root `render.yaml` defines a Free Docker web service. It uses
`Dockerfile.render`, whose dedicated ignore file admits only the generator,
its shared styles, the project protocol, curated demo assets, and the annotation endpoint. API keys, local run records,
chat logs, and uploaded documents are excluded from the image.

In Render, create a Blueprint from this repository and enter `OPENAI_API_KEY`
as a private environment value. Render generates `PROOF_AGENT_PASSWORD`;
the username is `professor`. Retrieve the password from the service's
Environment settings and sign in over its HTTPS URL. The server refuses
to start without both login values. Do not put either secret in Git.

The service root opens the generator. **Explore the demo** opens `/demo/home.html` on the same host; the high-contrast paper is at `/demo/papers/high-contrast/`. Its dictionary works locally in the browser. AI annotations use the server’s existing API configuration and `PROOF_DISCUSSION_MODEL` when set. `/healthz` is a public status-only
health check; the UI, demos, annotation and generation endpoints, and saved explorers require
authentication. This service does not expose the separate AI chat interface.

Free hosting uses temporary storage. Download results with **Save explorer**;
restarts, redeploys, and idle shutdowns clear saved runs. Keep the browser
open while a job is generating. For durable storage, choose a paid service,
attach a disk, set `PROOF_EXPLORER_DATA_DIR` to a directory on that disk, and
set `PROOF_EXPLORER_EPHEMERAL=false`.

Hosting and model usage are separate: generation still consumes the API
account's credits. The existing optional `OPENAI_API_BASE`,
`PROOF_EXPLORER_SEARCH_MODEL`, and `PROOF_EXPLORER_MAX_TOKENS` settings apply.
No example generation runs automatically at startup.

Local checks (no API requests):

```sh
python3 -m unittest discover -s tests -p 'test_explorer*.py'
node --test tests/test_explorer_view.cjs
docker build -f Dockerfile.render -t proof-explorer-render:local .
```

Render references: [web services](https://render.com/docs/web-services),
[free-service storage limits](https://render.com/docs/free#local-files-lost-on-redeploy).
