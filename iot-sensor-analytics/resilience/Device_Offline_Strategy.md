# Offline Device Strategy
Edge devices buffer up to 60 minutes, reconnect with exponential backoff/jitter, retain original event time and sequence number, and replay at a bounded rate to avoid reconnect storms.
