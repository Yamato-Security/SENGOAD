"velociraptor" = {
  name               = "velociraptor"
  linux_sku          = "22_04-lts-gen2"
  linux_version      = "latest"
  ami                = "ami-04c332520bd9cedb4"
  private_ip_address = "{{ip_range}}.53"
  password           = "3tDb-P7Rz!vQ4nX9"
  instance_type      = "t3.medium" # 2 CPU / 4 GB
}
