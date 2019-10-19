provider "google" {
  credentials = "${file("credentials/gcloud.json")}"
  project     = "${jsondecode(file("credentials/gcloud.json"))["project_id"]}"
  region      = "${var.region}"
  zone        = "${var.zone}"
}

provider "twilio" {
  account_sid = "${jsondecode(file("credentials/twilio.json"))["account_sid"]}"
  auth_token  = "${jsondecode(file("credentials/twilio.json"))["auth_token"]}"
}

data "archive_file" "app_zip" {
  type        = "zip"
  output_path = "${path.root}/dist/app.zip"

  source {
    filename = "main.py"
    content = "${file("${path.root}/app/app.py")}"
  }
  source {
    filename = "config.yaml"
    content = "${file("${path.root}/config.yaml")}"
  }
  source {
    filename = "requirements.txt"
    content = "${file("${path.root}/requirements.txt")}"
  }
}

resource "random_id" "bucket" {
  byte_length = 8
}

resource "google_storage_bucket" "function_bucket" {
  name = "function-bucket-${random_id.bucket.hex}"
}

resource "google_storage_bucket_object" "app_zip" {
  name   = "app.${lower(replace(data.archive_file.app_zip.output_base64sha256, "=", ""))}.zip"
  bucket = "${google_storage_bucket.function_bucket.name}"
  source = "${data.archive_file.app_zip.output_path}"
}

resource "random_id" "app_function" {
  byte_length = 8
}

resource "google_cloudfunctions_function" "app" {
  name                  = "call-router-${random_id.app_function.hex}"
  available_memory_mb   = 256
  source_archive_bucket = "${google_storage_bucket_object.app_zip.bucket}"
  source_archive_object = "${google_storage_bucket_object.app_zip.output_name}"
  timeout               = 60
  entry_point           = "${var.func}"
  trigger_http          = true
  runtime               = "python37"
}

resource "twilio_phone_number" "helpline" {
  friendly_name = "HTM Helpline"

  country_code = "GB"

  address_sid = "${jsondecode(file("credentials/twilio.json"))["address_sid"]}"

  voice {
    primary_url = "${google_cloudfunctions_function.app.https_trigger_url}"
    primary_http_method = "GET"
  }
}

output "number" {
  value = "${twilio_phone_number.helpline.number}"
}
