# Agent Workbench Sandbox

A separate, intentionally small project for testing
[Agent Workbench](https://github.com/jackstan/agent-workbench) across a repository
boundary. It contains a duration parser, predefined acceptance tests, and a
proposal for one narrowly scoped fix. It contains no copied agent engine.
Sendable remains independent.

**Current state:** the original approved fix and a real local verifier–builder–verifier
repair cycle were merged in [PR #1](https://github.com/jackstan/agent-workbench-sandbox/pull/1).
All six original acceptance tests pass on `main`. The new GitHub workflow uses the
same coordinator on a hosted runner, with a separate publisher and visible stage
events. A dedicated API key and a live hosted trial are still required before
claiming that this new route has worked end to end. No deployment is enabled.

## Watch a repair cycle in GitHub

The reviewed `project.github.toml` allows only `src/duration.py`, at most two
repairs, and approval by jackstan's canonical GitHub user. `proposal.github.json`
defines the unchanged duration contract, including totals above 180 minutes.
The workflow consumes a pinned engine commit; it contains no copied engine.

1. Add a dedicated `OPENAI_API_KEY` in this repository's Actions secrets.
2. Open an operator-created candidate PR on an `agent/*` branch. The pilot uses
   an explicitly seeded regression that still passes the original six tests.
3. In **Actions → Agent Workbench → Run workflow**, select `main`, enter the PR
   number and its full head commit. This explicitly approves this candidate,
   proposal, scope and current base. It does not reuse the earlier Linear approval.
4. Follow the PR's pending verifier status to the live Actions run. The middle job
   prints each verifier result, repair reservation, builder completion and new
   verification as it happens. The final job publishes only the verified tree,
   adds verdict statuses and requests the Acceptance workflow.
5. Review the final PR and merge it yourself.

The run retains prompts, process output, review findings, patches, stage events and
a Git bundle as downloadable artifacts for 90 days. A live run must show a real
blocker, a repair handoff and a fresh PASS on the repaired commit before we call the
repair trial successful. A seeded regression proves the handoff, not natural bug
discovery or general agent reliability.

The workflow refuses GitHub reruns and repeated dispatch of the same approval
binding. Preserve its `agent-workbench/claims/*` tags; inspect uncertain runs instead
of deleting reservations. Missing credentials fail before reserving work.
The full guarantees and limits are in the engine's
[hosted workflow guide](https://github.com/jackstan/agent-workbench#run-the-cycle-visibly-in-github).

## Reproduce the task

Requires Python 3.11 or later:

```sh
python -m src.duration "1h 30m"
python -m unittest discover -s tests -v
```

The application now reports `90`. At the original seed revision it reported `30`.
Tests also cover order, whitespace, repeated units, invalid input, zero values,
and the actual command-line output. They were committed before any builder run.

The accepted change may edit only `src/duration.py`. The target is all six
predefined tests passing with their original contents. Do not weaken the tests.

## Install the separate engine

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-workbench.txt
agent-workbench check-config project.toml
```

`requirements-workbench.txt` pins an exact workbench commit tested during setup.
It includes the approval and hosted-cycle adapters; it is not a released version.
Advancing this pin is an explicit maintenance change.

## Optional local Linear approval route

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

This command ends at a persistent build authorization. Repeating the same
approval must fail, including after restarting the process. A lost response does
not release the approval; inspect the retained receipt rather than resetting state.

## What counts as completion

The Linear approval and local repair trials have been observed. Their
[public evidence](https://github.com/jackstan/agent-workbench/blob/main/docs/evidence/sandbox-repair-cycle.json)
includes exact commits and an independent counterexample reproducer.
The next milestone is the same rejection → repair → fresh verification executing
on GitHub-hosted runners, with inspectable logs and the PR left for human merge.
Keep the original tests fixed and record extra manual intervention. Fixture API
tests and the earlier local cycle do not satisfy the hosted milestone.
Scout discovery and deployed-release validation remain later trials.

The repository does not yet have an open-source license.
