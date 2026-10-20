# Sandbox pilot

This is an independent test project for Agent Workbench. Never modify Sendable
or copy its configuration, identities, credentials, or workflows.

The duration parser deliberately contains a defect. Fix it only during an explicitly
approved builder run. The acceptance suite defines the outcome before that run;
do not weaken, delete, skip, or mark those tests as expected failures.

Approved automatic changes are restricted to `src/duration.py`.
Infrastructure and fixture maintenance are separate human-reviewed work.
Human approval, PR merge, and any release promotion remain separate gates.

Run `python -m unittest discover -s tests -v`. Four failures are expected at the
initial revision; the real builder's goal is all six tests passing.
