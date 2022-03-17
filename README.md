# Overview

- Extracts, Transforms and Loads data into Mongo DB
- Mongo express (viewer app) available (Docker required)
- Additional field, `original_report`
- Generated Data Reports
- Test cases

# Running

1. To spin up MongoDB and Mongo Express (for viewing the database), run
`docker-compose up` N/B: Must have docker installed

2. Goto `http://127.0.0.1:8081` to see the visual database

3. To run the etl app, run `python3 main.py`


# Testing
 To run tests, use:  ` python3 -m unittest discover`

