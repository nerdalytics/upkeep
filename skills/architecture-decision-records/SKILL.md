---
name: architecture-decision-records
description: "Writes or supersedes an architecture decision record (ADR) with context, options considered, decision and consequences, in the project's own location, numbering and template. Use when the user asks for an ADR or to document a decision, or when a significant architectural or tooling choice has just been made, changed or reversed in the conversation."
license: MIT
---

# Architecture decision records

Record a decision so that a later reader understands why it was made. You cannot know the project's conventions in advance, so find them before you write anything.

An ADR is for a significant, long-lived architecture decision. Its reader is a future developer who needs to know why the system has this structure or constraint. Classify the decision before you write. A product or business decision belongs in the product documentation that its owner keeps. The code and its tests already record an implementation detail. A process agreement belongs in the team's conventions. For those, say where the decision belongs and do not write an ADR, because a copy in the repository becomes a second source of truth.

## Workflow

Progress:
- [ ] Step 1. Load the project skill `maintainability-records` through this plugin's init skill, `upkeep:init`. It returns at once when it is current, and generates it when not. If it names another skill as the owner of decision records, hand the decision to that skill and stop here.
- [ ] Step 2. Take the location, the file naming and numbering, the template and the status vocabulary from `maintainability-records`. Read two existing records and match them. When the project has no records yet, the init skill has asked the user where they go, and the template is `assets/adr-template.md`.
- [ ] Step 3. Take the next number from the directory contents, never from memory. Check for superseded records on the same topic.
- [ ] Step 4. Write the record from the project's own template, or from `assets/adr-template.md` if the project has none. The context states the forces. The options are real alternatives with their trade-offs. The consequences include the negative ones.
- [ ] Step 5. If this decision replaces an earlier one, create a new record that supersedes it, and update the old record's status and link. Never rewrite the decision in an accepted record.

## Status lifecycle

A record starts as `proposed` and becomes `accepted`. An accepted record later becomes `deprecated` or `superseded by ADR-NNNN`. Use the project's vocabulary if it differs. An accepted record does not change. A correction or a reversal is a new record.

## Gotchas

- An ADR needs the alternatives that were considered. At least one real option appears with its trade-off, even if the team rejected it quickly.
- The consequences include what gets worse, such as new coupling, migration cost or lock-in.
- An ADR is not a meeting transcript or a list of implementation details. Keep it short, with context, options, decision and consequences.
- Write one decision per record. "Adopt X and refactor Y and change Z" is three records.
- The number comes from a listing of the ADR directory at the time you write. Another session can take a number between your check and your write, so check again immediately before you create the file.
- Use the project's template when it has one, even if `assets/adr-template.md` looks better. A record that matches the others in the repo is easier to find and read.
- Whether a decision is significant is a judgment call. A change to a module boundary, a storage technology, a public contract, or a build or deploy toolchain qualifies. Renaming a variable does not.
