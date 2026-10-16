"velociraptor" = {
  name    = "velociraptor"
  desc    = "Velociraptor server for SENGOAD"
  cores   = 2
  memory  = 4096
  clone   = "Ubuntu_2204_x64"
  dns     = "{{ip_range}}.1"
  ip      = "{{ip_range}}.53/24"
  gateway = "{{ip_range}}.1"
}
