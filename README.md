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

<!-- Structure -->

app/
├── _pycache_/
├── customers/
│ ├── router.py
│ ├── schemas.py
│ └── services.py
├── invoices/
│ ├── router.py
│ ├── schemas.py
│ └── services.py
├── products/
│ ├── router.py
│ ├── schemas.py
│ └── services.py
├── restock/
│ ├── router.py
│ ├── schemas.py
│ └── services.py
├── sales/
│ ├── router.py
│ ├── schemas.py
│ └── services.py
├── models/
│ ├── customer_models.py
│ ├── invoice_models.py
│ ├── products_models.py
│ ├── restock_models.py
│ ├── sale_models.py
├── utils/
│ ├──utils.py

├── venv/
├── **init**.py
├── api_router.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── node_modules/
├── static/
├── templates/
└── venv/

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
