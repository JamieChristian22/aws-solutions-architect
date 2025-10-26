resource "aws_redshiftserverless_namespace" "analytics" {
  namespace_name = "retail-analytics-namespace"
  admin_username = "adminuser"
  admin_user_password = "ChangeMe123!"
}

resource "aws_redshiftserverless_workgroup" "analytics_wg" {
  workgroup_name = "retail-analytics-wg"
  namespace_name = aws_redshiftserverless_namespace.analytics.namespace_name
}
