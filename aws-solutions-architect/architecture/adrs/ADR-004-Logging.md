# ADR-004 — Centralized Security Logging

**Status:** Accepted

CloudTrail organization/account events, AWS Config history, application logs, ALB access logs, and WAF logs are retained according to documented policies. Security audit logs use a dedicated encrypted S3 bucket with public access blocked and lifecycle rules.
