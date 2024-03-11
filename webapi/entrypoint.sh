python cli.py load_plan_policy
python cli.py load_permission_policy
python cli.py alembic migrate heads
uvicorn webapi.main:app --port 8000 --host 0.0.0.0
