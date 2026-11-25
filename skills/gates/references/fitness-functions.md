# Architecture fitness functions

Load this file when the task asks for architecture rules, which are layering, dependency direction, cycles, or protected interfaces. Implement the rules in the test suite so that they run on every CI build. Start with cycles and layering. Add another rule only when a real violation has happened or is about to.

## Rules worth their cost

1. **No dependency cycles** between modules or packages.
2. **Layering.** Dependencies point one way through the project's layers. For example, a domain layer imports neither the infrastructure nor the user interface.
3. **Public interface.** Other modules may import only a module's `index` or `api` entry, never its internals.
4. **Forbidden edges.** For example, nothing outside `billing/` imports the payment SDK.

## Implementing a rule

Use the dependency or architecture tool that `maintainability-checks` lists. Read the directory tree first, and write each rule against the project's real module names and paths. Check three things in the tool's documentation before you rely on a rule:

- The severity at which a violation changes the exit code.
- How a rule refers to "the same module". A public-interface rule must allow a module to import its own internals and forbid only the imports from other modules.
- The order in which the tool expects layers, from highest to lowest or the reverse.

## Verification

With any tool, seed a violation and see the gate fail with the rule name and the file in the message. Then remove the seed and see the gate pass. Until you have seen a fitness function fail, you do not know that it works.
