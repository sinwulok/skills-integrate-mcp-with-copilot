Title: Add Group/Club models with mentor association

Description:
Create explicit `Group` or `Club` models that include name, description, schedule, capacity and a `mentor` foreign key to a user. Include model validations and string representations.

Why:
- Model-driven domain better than ad-hoc dicts
- Mentors can be scoped to manage their groups

Acceptance criteria:
- `Group` model and migrations
- Admin list shows `name` and `mentor`
- Mentor-scoped views that only show groups they manage

Labels: feature, backend
