# sample-full

A sample plugin that uses every capability a plugin can contribute. Copy it as a starting point for your own plugin.

| capability | where |
|------------|-------|
| a townhall hook (`task.started`) | `townhall-hooks.json`, runs `bin/on-started.sh` |
| a Claude MCP server (`sample`, tool `search_samples`) | `mcp/servers.json`, runs `mcp/server.mjs` |
| an agent type (`sample-helper`) | `agent-types/helper.toml`, selects the MCP tool |
| a session section (`sample`) | `ui/session.html`, uses `ui/townhall-plugin-sdk.js` |

## Permissions

- `api`: `tasks:read` for the section, `storage` for the hook's data folder
- `hooks`: `task.started`
- `claude`: the `search_samples` tool of the `sample` server
- `ui`: `session.section`

The user approves this list on install.
