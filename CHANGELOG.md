# Changelog

## 2026.11.2

- New skill `findings`, which gives one format for the list of findings. `audit` and `review` load it before they write a report. The user does not call it.
- `init` generates both project skills in one run, also when the calling skill needs only one.
- `init` asks the user which of the project's check commands to run, and runs none before that.
- `gates` asks where the gates are enforced before it proposes any. The shared pipeline is one choice among the local check command, hooks and the test suite.
- `hotspots.py` skips lockfiles and ranks a directory inside a repository. `dupblocks.py` skips files that git ignores.

## 2026.11.1

First release. The version is the year, the month and the number of the release in that month.

- Seven skills that hold the method: `audit`, `review`, `gates`, `tech-debt-triage`, `legacy-safe-change`, `strangler-migration` and `architecture-decision-records`.
- `init`, which generates two skills inside a project, `maintainability-checks` and `maintainability-records`, and generates them again when the project's toolchain or documentation layout changes.
- `help`, the map of the plugin.
