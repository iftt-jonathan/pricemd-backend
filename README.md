# pricemd-backend
This is the repository for the backend of PriceMD
Tech stack: AWS Lambda serverless, Python runtime, S3 for data storage.

Goals:
 - ✅ Get CI pipeline going
 - ✅ Get working Lambda uploads
 - Set up API to call dummy hospital CSV info and test on frontend
 - Set up some testing to make sure we don't break anything
 - Flesh out API from there

### Local development
Run `setup.sh` on WSL or Linux machine. Set Python environment in VS Code to `.venv` folder.

### Deploy to AWS
Run `deploy.sh`, ensure `terraform` executable is accessible and has a configured AWS account.

Contributors: Jonathan Ballard, Matheus Plinta, Rebekah Daniels