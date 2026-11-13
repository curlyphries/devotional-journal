"""
The study library: one module per group of topics, each exporting TOPICS,
plus traits.py exporting TRAITS. Loaded and validated by apps.guides.library.

Content rules (enforced by review, and where possible by library.validate):
  * Scripture is cited by reference only. The app fetches the words itself.
  * Every reference must exist (tests check each one against verse counts).
  * Teaching stays within what Christians broadly hold in common.
"""
