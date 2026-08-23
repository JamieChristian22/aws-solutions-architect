# Network Architecture

```mermaid
flowchart TB
  IGW[Internet Gateway]
  ALB[Public ALB]
  NAT1[NAT Gateway AZ-A]
  NAT2[NAT Gateway AZ-B]
  APP1[Private App Subnet A]
  APP2[Private App Subnet B]
  DB1[Private DB Subnet A]
  DB2[Private DB Subnet B]

  IGW --> ALB
  ALB --> APP1
  ALB --> APP2
  APP1 --> NAT1 --> IGW
  APP2 --> NAT2 --> IGW
  APP1 --> DB1
  APP2 --> DB2
  DB1 --- DB2
```

CIDR plan:
- VPC: `10.40.0.0/16`
- Public A: `10.40.0.0/24`
- Public B: `10.40.1.0/24`
- Private App A: `10.40.10.0/24`
- Private App B: `10.40.11.0/24`
- Private DB A: `10.40.20.0/24`
- Private DB B: `10.40.21.0/24`
