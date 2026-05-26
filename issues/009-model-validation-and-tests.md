Title: Add model validation and tests

Description:
Ensure models enforce validation (e.g., capacity limits, email uniqueness) and add unit/integration tests for core flows (signup, unregister, permissions).

Why:
- Prevent data inconsistencies and regressions

Acceptance criteria:
- `clean()` or validators added for key models
- Test suite with tests for signup/unregister and role checks
- CI hint or local `pytest` instructions in README

Labels: tests, quality