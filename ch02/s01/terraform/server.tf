resource "google_compute_instance" "hello_world" {
  name         = "hello-world"
  machine_type = "f1-micro"

  network_interface {
    network = "default"

    access_config {}
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-1804-lts"
    }
  }

  labels = {
    environment = "dev"
  }
}