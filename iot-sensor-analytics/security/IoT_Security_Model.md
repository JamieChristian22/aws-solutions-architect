# IoT Security Model
Unique X.509 certificate per device. IoT policy restricts connect client ID and publish topic. Certificates are inventoried, rotated, and revoked individually. Device private keys should be hardware-backed where possible. KMS, IAM roles, CloudTrail, blocked public S3 access, private OpenSearch, and schema validation provide cloud-side defense in depth.
