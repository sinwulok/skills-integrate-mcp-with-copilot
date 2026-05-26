Title: Customize admin site for club management

Description:
Improve the admin interface with `list_display`, `search_fields`, `list_filter` and custom querysets to help mentors and admins manage groups, members and events.

Why:
- Faster operations for admins/mentors

Acceptance criteria:
- Admin shows columns: name, mentor, current_participants
- Search by group name and filter by mentor
- Custom `get_queryset` to scope mentor view

Labels: ui, enhancement
