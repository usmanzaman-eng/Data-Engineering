# Data pipeline task
After succesfully running the data-generator.py file we successfully got data in our minio-bucket.
Next thing we did was created services in our docker compose to consume the data from minio and apply different transformation techniques and finally store in a MongoDB for persistent storage.
To run the service go to the minio-deployment directory and run "docker compose up"
The ipynb file provided was for the hour for which we generated the data in minio bucket.This wasn't scheduled.
