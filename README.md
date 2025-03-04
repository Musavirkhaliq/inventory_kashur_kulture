# inventory_kashur_kulture

## Local Development Setup

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
