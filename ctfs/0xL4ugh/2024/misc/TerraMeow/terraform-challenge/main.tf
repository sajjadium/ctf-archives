resource "local_file" "flag" {
  content = "Hello-world!"
  filename = var.FLAG
}