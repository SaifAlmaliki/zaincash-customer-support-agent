# Fictional intake screenshots

Everything in this folder is made up for a local demo. These are not customer receipts, bank records, or ZainCash screens.

`fictional-receipt.png` is a generated picture. The reference `DEMO-2410000123`, the amount `50000 IQD`, and the error text are synthetic. Do not treat any value in the image as a real transaction.

To reproduce readable/unreadable vision and bilingual-review smoke checks, run `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt INTAKE_MODEL=google/gemini-2.5-flash uv --directory backend run python -m tests.intake.live_probe` from the repository root. It generates images in memory, calls the configured provider, and prints measured observations, latency and available costs. It is opt-in and is not part of pytest.
