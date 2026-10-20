# Sandbox pilot

This is an independent test project for Agent Workbench. Never modify Sendable
or copy its configuration, identities, credentials, or workflows.

The original seeded defect and local repair cycle have been merged. A new pilot PR
may deliberately seed another defect; repair it only during an explicitly approved
builder run. The acceptance suite defines the outcome before that run;
do not weaken, delete, skip, or mark those tests as expected failures.

Approved automatic changes are restricted to `src/duration.py`.
Infrastructure and fixture maintenance are separate human-reviewed work.
Human approval, PR merge, and any release promotion remain separate gates.

Run `python -m unittest discover -s tests -v`. All six tests pass on current main.
Passing those tests alone does not establish the full proposal contract.
