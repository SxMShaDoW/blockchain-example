## Pre-reqs

* Python 3.5.2 or higher
* Pip
* `pip install pytest`
* `pip install pytest-cov`

### Steps to create a report on current dataset

`python report.py`

### Steps to generate random transactions

`python export_results.py`

### Running tests

`pytest .`

### Generating Code Coverage

`pytest --cov=. .`

## Using the "CI" Service

1.  `git clone <repo>` you want to monitor (i.e. `git clone https://github.com/SxMShaDoW/blockchain-example/`
2.  Copy the `cicd_github_monitor.py` inside the repo (already there in this case)
3.  Modify the creds section in `cicd_github_monitor.py` (Line 11)
4.  Modify the repo you want to monitor in `cicd_github_monitor.py` (Line 13) (`blockchain-example`)
5.  Run `python cicd_github_monitor.py`
