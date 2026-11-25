---
name: legacy-safe-change
description: "Procedure for changing code that has no tests, or that you do not yet understand, without changing its behavior by accident. Pin the current behavior with characterization tests, find seams, make the smallest diff, and keep cleanup in a separate commit. Use before editing untested, legacy or unfamiliar code, including when the user asks only for a small fix there. To replace such code, use strangler-migration."
license: MIT
---

# Legacy safe change

Change untested code without guessing. Follow the steps below in order, and start a step only when the gate before it holds. How you refactor inside a step is your judgment.

## Workflow

Each step depends on the one before it.

Progress:
- [ ] Step 1. Name the exact behavior you will touch. Write it as one sentence with its inputs, outputs and side effects. If you cannot name it, you are not ready to change it.
- [ ] Step 2. Identify seams for hard dependencies, as described below, so that a test can run without the network, the clock, or other outside state.
- [ ] Step 3. Gate: a characterization test exists and passes. Capture the behavior as it is now, before any edit. Run the test against the untouched code and see it pass. Make no edit before this gate holds. The one exception is creating a seam that the test needs, under the conditions given below.
- [ ] Step 4. Make the minimal behavior diff, the smallest change that reaches the goal. Do not restructure anything else in the same commit.
- [ ] Step 5. Run the characterization tests and the surrounding suite, with the test command from the project skill `maintainability-checks`. Load it through this plugin's init skill, `upkeep:init`. The characterization tests must still pass. The exception is a change whose purpose is to alter that behavior. Then update the tests on purpose and say so in the commit message.
- [ ] Step 6. Put bounded Boy Scout cleanup, such as a rename, an extraction or the removal of dead code, in a separate commit after the behavior change is green.

## Characterization tests

- Assert what the code does now, including behavior that looks wrong. A characterization test records the current behavior and does not approve of it.
- When the current behavior looks like a bug, record it as a debt item through tech-debt-triage and keep the test asserting the current behavior. Fix the bug later as a separate, deliberate change. Never fix it inside the characterization step.
- For complex or large output, use the golden-master or approval style. Capture the full output once, compare later runs against it, and inspect each difference by hand.
- Cover the paths you will touch, not the whole module. The characterization suite for one change is small.

## Seams

A seam is a place where you can alter behavior without editing the code under test.

- Constructor or function parameters. Pass a fake clock, a fake random source, or a stub client.
- Subclass and override points. Override the method that performs the side effect.
- Module-level injection. In the test, patch the dependency at the module boundary, not deep inside the call chain.
- Environment and config. Point the code at a test fixture or a temp directory.

If no seam exists, creating one is itself a behavior-preserving change, for example extracting a method or adding a parameter with a default. Do it in its own commit, protected by an existing test or a golden master.

## Gotchas

- Hidden side effects make characterization tests flaky. They are the current time, randomness, environment variables, global state, the network and the filesystem. Fix each one to a known value through a seam before you trust a green test.
- A coverage tool reports which lines ran, not which results a test asserted. A line that runs in a test with no assertion is not characterized.
- A test written after the edit characterizes your new behavior, not the old one. That is why the gate comes before the edit.
- If the code cannot be tested at all and the real goal is to replace it, stop and use strangler-migration.
- Do not rely on a change looking equivalent. A small diff is not evidence. The passing characterization test is.
