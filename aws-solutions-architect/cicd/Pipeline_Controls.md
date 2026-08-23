# CI/CD Pipeline Controls

## Pull Request
Every infrastructure change must pass:
1. Terraform formatting.
2. Terraform validation.
3. IaC security scanning for HIGH/CRITICAL findings.
4. Terraform plan in a nonproduction approval context.
5. Human review of resource additions, replacements, security changes, and cost implications.

## Production
Merges to `main` can enter the protected `production` GitHub environment. The environment should require an authorized reviewer.

## Identity
AWS access is established with GitHub OIDC and short-lived role credentials. No AWS access keys are stored in repository secrets.

## Rollback
Terraform itself is not an application rollback system. If an infrastructure change is unsafe, revert the Git commit, create a new plan, review the reverse changes, and apply. For stateful resources, validate backup/recovery implications before any destructive reversal.
