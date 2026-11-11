# townhall-plugins

The official plugin marketplace for [townhall](https://github.com/WilliamThogersen/townhall). Townhall ships it built in under the name `townhall-official`.

Most plugins here are declarative: they contribute a theme, prompts and agent types. `sample-full` also contributes a hook, a Claude MCP server and a session section to show how they are written.

| plugin | contributes |
|--------|-------------|
| `theme-slate` | a blue-grey theme with a dark and a light palette (`theme.css`) |
| `starter-prompts` | extra starter prompts for the home screen |
| `agent-types` | the `tester` and `reviewer` agent types |
| `sample-full` | a sample that shows every capability: a hook, a Claude MCP server, an agent type and a session section (see [its README](plugins/sample-full/README.md)) |

## Layout

```
.townhall-plugin/marketplace.json     the index: name, owner, one entry per plugin
plugins/<name>/
  .townhall-plugin/plugin.json        identity, permissions, contributions
  ...                                 the files plugin.json points at
scripts/validate.py                   the check CI runs
```

## Add a plugin

1. Create `plugins/<name>/` with a `.townhall-plugin/plugin.json`. The name uses letters, digits, `.`, `-` and `_`, starts with a letter or digit and is at most 64 characters.
2. List what the plugin contributes under `contributes`, with paths relative to the plugin folder (no `..`, no absolute paths).
3. Declare exactly what it needs under `permissions`. A prompts contribution needs `"prompts": ["starters"]` and so on; the user approves that list on install.
4. Add an entry to `.townhall-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
5. Run `python3 scripts/validate.py`.

## Private and custom marketplaces

A private or team marketplace uses the same format: a git repo with a `.townhall-plugin/marketplace.json` listing plugins whose `source` is a `./folder` inside the repo, a GitHub repo, a git url or a folder of another repo. Add it in townhall by link, `owner/repo`, git url or local folder; private repos work over ssh or with your git credentials.

## Validate

```
python3 scripts/validate.py
```

It needs Python 3 and nothing else. It checks that every JSON file parses, that every marketplace source folder exists, and that every path in each `plugin.json` exists inside its plugin. The same check runs in GitHub Actions on every push and pull request.

## Format reference

[docs/plugins.md](https://github.com/WilliamThogersen/townhall/blob/main/docs/plugins.md) in the townhall repo.

## License

MIT, see `LICENSE`.
