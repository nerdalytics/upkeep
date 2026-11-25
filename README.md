# upkeep

`upkeep` is a Claude Code plugin that helps you keep a codebase easy
to change. It can measure a repository, review changes, add checks to CI, rank
technical debt, guide changes to untested code, plan the replacement of a
legacy system, and record architecture decisions.

## Requirements

- Claude Code on macOS, Linux, or Windows under WSL
- `git`
- Python 3.9 or later

## Install

In Claude Code, add this repository as a marketplace and install the plugin:

```
/plugin marketplace add nerdalytics/upkeep
/plugin install upkeep@upkeep
```

## Usage

Run `/upkeep:help`, or ask Claude what the upkeep plugin can
do. The help skill explains each skill, the order to use them in, and where
they write their reports.
