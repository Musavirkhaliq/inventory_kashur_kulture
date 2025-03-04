# inventory_kashur_kulture

## Local Development Setup

clone the repository

```bash
git clone https://github.com/Musavirkhaliq/planner.git
```

change directory

```bash
cd planner
```

create a virtual environment

```bash
python -m venv venv
```

install dependencies

```bash
pip install -r requirements.txt
```

````
run the server
```bash
 python -m uvicorn app.main:app --reload --port 9000
```
```

view app here
http://localhost:9000/

view swagger api docs here
http://localhost:9000/docs

view redoc api docs here
http://localhost:9000/redoc
````

Authentication

- Use the default admin/public credentials
- username: admin
- password: password

Musavir Khaliq
5:00 AM
https://docs.google.com/document/d/1tRaTOgA-mOhXLNwmGuzqn80Hlilcue7EPtTeNsQgW40/edit?pli=1&tab=t.0#heading=h.rlr22ukcvzmm
Musavir Khaliq
5:05 AM
├── app/
│ ├── api/ # API routes
│ │ ├── admin/ # Admin-specific endpoints
│ │ │ ├── routes.py
│ │ │ └── dependencies.py
│ │ ├── public/ # Public/customer-facing endpoints
│ │ │ ├── routes.py
│ │ │ └── dependencies.py
│ │ └── **init**.py
│ ├── core/ # Core utilities and configuration
│ │ ├── config.py
│ │ ├── security.py # Authentication/Authorization logic
│ │ └── exceptions.py
│ ├── cr
