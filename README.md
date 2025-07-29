# langhain-learn
Learning Langchain. Rough Random things

### Logging System Design Principles Followed

- Use one shared logger, not one-per-destination; route via filters.
- Handler selection is done via log-time fields (e.g., destination="json_file"), not logger names.
- Structlog processors transform structured event dicts, and must explicitly pass routing fields (like destination) to LogRecord.
- Define a clean setup_logging() + setup_structlog(), called once at startup.
- Don’t wrap loggers in classes/singletons—Python’s logging registry already ensures shared instances.
- Use get_logger() as a lazy, idempotent entry point, and optionally bind destination there for ergonomic use.
- Attach multiple handlers with filters to the same logger, using DestinationTagFilter.
- Write filters and processors at top-level for reuse and clarity—logging config is logic, not state.
- final design is clean, minimal, structured, extensible, and accurate to the Python logging+structlog model.