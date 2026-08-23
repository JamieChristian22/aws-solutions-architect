# IAM Design

## Human Roles
- `PlatformReadOnly`: inventory and troubleshooting without mutation.
- `PlatformOperator`: approved operational actions; no IAM administration.
- `SecurityAudit`: read access to logs/findings/configuration.
- `InfrastructureAdmin`: restricted production infrastructure changes through controlled workflow.

## Workload Roles
`ecsTaskExecutionRole` is limited to image pull/log delivery needs. Application task role receives only application-required service access.

## CI/CD
GitHub Actions assumes a dedicated deployment role through OIDC. Trust is restricted to the repository and protected branch/environment. No long-lived AWS access key is required.

## Policy Review Rules
- wildcard `Resource: "*"` permitted only for AWS APIs that do not support resource scoping or documented read/list operations
- write permissions require explicit resource ARNs
- production role assumptions are logged
- access review occurs quarterly
