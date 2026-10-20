# Agent Workbench Sandbox

A separate, intentionally small project for testing
[Agent Workbench](https://github.com/jackstan/agent-workbench) across a repository
boundary. It contains a duration parser, predefined acceptance tests, and a
proposal for one narrowly scoped fix. It contains no copied agent engine.
Sendable remains independent.

**Current state:** the seeded application defect is present. Two acceptance tests
pass and four fail; the GitHub Acceptance workflow is intentionally red until the
future approved builder fixes it. No autonomous builder, publisher or deployment
is enabled. A real Linear approval has not yet been exercised.

## Reproduce the task

Requires Python 3.11 or later:

```sh
python -m src.duration "1h 30m"
python -m unittest discover -s tests -v
```

The application currently reports `30`; the required total is `90`.
Tests also cover order, whitespace, repeated units, invalid input, zero values,
and the actual command-line output. They were committed before any builder run.

The accepted change may edit only `src/duration.py`. The target is all six
predefined tests passing with their original contents. Do not repair the fixture
manually or weaken the tests to make the initial CI green.

## Install the separate engine

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-workbench.txt
agent-workbench check-config project.toml
```

`requirements-workbench.txt` pins an exact workbench commit tested during setup.
It includes the new approval adapter under review; it is not a released version.
Advancing this pin is an explicit maintenance change.

## Prepare the first live approval

The checked-in configuration has **synthetic UUIDs**. It cannot identify a real
approver or Linear project. Create a dedicated sandbox Linear project and app
creator, distinct from the human approver, then:

1. Copy `project.toml` to ignored `project.local.toml` and set the real human's
   canonical Linear UUID.
2. Copy `linear.example.toml` to ignored `linear.local.toml` and replace all four
   IDs with the dedicated sandbox organization/team/project/app identity.
3. Review both files as trusted operator settings. Resolve the current trusted
   `main` commit independently and use its exact SHA below.
4. Render the proposal without making network calls:

   ```sh
   agent-workbench prepare-linear-proposal project.local.toml proposal.json \
     --linear-config linear.local.toml --base-sha BASE_COMMIT
   ```

5. Have the configured app post the output's exact `body` as a top-level comment
   on the sandbox issue. The human reads it and posts a separate top-level comment:

   ```text
   agent-workbench approve PROPOSAL_COMMENT_UUID PROPOSAL_SHA256
   ```

   These placeholders come from the real comment and preparation output. A comment
   created by an agent acting on behalf of the human does not satisfy this gate.

Use the [approval and ledger guide](https://github.com/jackstan/agent-workbench/blob/16672ad5dcb9f975e6dc79e93b2df900cd5e3ce5/docs/linear-approval.md)
for the exact protocol, credential setup, limits and recovery.
Keep secrets out of the repository. Use a dedicated read-only Linear credential
through `AGENT_WORKBENCH_LINEAR_API_KEY` or `AGENT_WORKBENCH_LINEAR_ACCESS_TOKEN`.

Initialize a persistent ledger **once**, in an operator-owned directory outside
the worker checkout:

```sh
umask 077
mkdir -p ../workbench-state
agent-workbench ledger-init ../workbench-state/approvals.sqlite
```

Then consume the real approved proposal:

```sh
agent-workbench authorize-linear project.local.toml \
  --linear-config linear.local.toml \
  --issue ISSUE_UUID --proposal-comment PROPOSAL_COMMENT_UUID \
  --base-sha BASE_COMMIT --ledger ../workbench-state/approvals.sqlite
```

This currently ends at a persistent build authorization. Repeating the same
approval must fail, including after restarting the process. A lost response does
not release the approval; inspect the retained receipt rather than resetting state.

## What counts as completion

The first authorization trial requires a genuine proposal and human decision,
an inspectable receipt bound to this repository/base/scope, and demonstrated
replay rejection after restart. Fixture tests do not satisfy that live milestone.

The subsequent delivery trial will add isolated model execution, independent
review, a trusted publisher, a PR, human merge, and acceptance checks on `main`.
Keep the original tests fixed and record every extra manual intervention.
Scout discovery and deployed-release validation are later trials.

The repository does not yet have an open-source license.
