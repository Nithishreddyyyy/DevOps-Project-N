# Staff Increment Management

FastAPI + MongoDB web application for managing faculty records, appraisal criteria, score calculation, and PDF report generation.

This README is based on the current implementation in the project files.

## What This Project Does

- Maintains faculty details (name, department, designation, contact, qualifications, experience, date of joining).
- Maintains appraisal criteria with category, weight, and active/inactive status.
- Assigns multiple criteria per faculty member and calculates total score from criterion weights.
- Generates downloadable PDF reports for one faculty member or all faculty members.
- Provides server-rendered pages using Jinja2 templates.

## Tech Stack

- Backend: FastAPI
- Database: MongoDB (Motor async client)
- Templating: Jinja2
- PDF Generation: ReportLab
- App Server: Uvicorn

## Project Structure

```text
Staff-Incriment-Management/
	README.md
	requirements.txt
	app/
		main.py
		config/
			database.py
		models/
			faculty.py
			appraisalCat.py
			FacultyCritScore.py
		routes/
			faculty_route.py
			appraisalCat_route.py
			crit_score_route.py
		schema/
			faculty_schema.py
			appraisalCat_schema.py
			crit_score_schema.py
		services/
			faculty_service.py
			appraisalCat_service.py
			faculty_crit_score_service.py
		templates/
			index.html
			faculty.html
			criteria.html
			scores.html
		static/
			css/style.css
			js/script.js
```

## Application Flow

1. `app/main.py` creates the FastAPI app, mounts static files, and includes route modules.
2. Route files in `app/routes/` handle page rendering and form submissions.
3. Service files in `app/services/` perform MongoDB CRUD and score logic.
4. `app/config/database.py` provides Mongo client and collections.
5. Templates in `app/templates/` render UI pages.

## Routes and Pages

### Home

- `GET /`
	- Renders `app/templates/index.html`.

### Faculty Management

- `GET /faculty/`
	- Shows add form and all faculty table.
- `POST /faculty/create`
	- Creates a faculty record from form input.
- `GET /faculty/delete/{id}`
	- Deletes a faculty record.

### Criteria Management

- `GET /criteria/`
	- Shows add form and criteria list.
- `POST /criteria/create`
	- Adds criterion with category, name, and weight.
- `GET /criteria/deactivate/{id}`
	- Marks criterion inactive.
- `GET /criteria/activate/{id}`
	- Marks criterion active.
- `GET /criteria/delete/{id}`
	- Deletes criterion.

### Score Management and Reports

- `GET /scores/`
	- Initializes missing score documents.
	- Shows faculty with selected criteria and computed total score.
- `POST /scores/update/{faculty_id}`
	- Updates selected criteria for a faculty member.
- `GET /scores/pdf/{faculty_id}`
	- Downloads single faculty appraisal PDF.
- `GET /scores/pdf/all`
	- Downloads all-faculty appraisal PDF.

## Data Collections

Defined in `app/config/database.py`:

- `faculty`
- `criteria`
- `scores`
- `documents_metadata` (currently defined, not actively used in routes)

## Local Setup

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd Staff-Incriment-Management
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Use the top-level requirements for this app:

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB connection

Current connection is hard-coded in `app/config/database.py` as `MONGO_URI`.

Replace it with your own MongoDB URI before running in your environment.

### 5. Run the app

```bash
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/`

## Notes About Current Codebase

- `app/schema/crit_score_schema.py` is currently empty.
- `app/routes/faculty_route.py` imports update/get helper functions that are not exposed as routes yet.
- `app/services/appraisalCat_service.py` contains `update_criteria(...)`, but update is not currently wired to a route.
- `app/requirements.txt` contains a large set of unrelated packages; the root `requirements.txt` is the relevant lightweight dependency list for this app.

## Future Improvements

- Move `MONGO_URI` to environment variables (for security and portability).
- Add validation rules and error handling for all form inputs.
- Add edit/update routes for faculty and criteria.
- Add tests for route and service layers.
- Add authentication/authorization for admin operations.