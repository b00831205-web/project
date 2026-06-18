import textwrap
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG("quant_factor_mining",
        default_args={
            "depends_on_past": True,
            "retries":1,
            "retry_delay":timedelta(minutes=5)
        },
        description="quant_factor_mining pipeline version 0.1, using S&P 500",
        schedule = timedelta(days=1),
        start_date=datetime(2020,1,1),
        catchup=False,
        tags = ['quant_factor_mining'],
        ) as dag:
    t1 = BashOperator(
        task_id = "data_downloading",
        bash_command='powershell.exe -Command '
        '"cd E:\\Handout\\project\\project_quant\\quant-factor-mining; '
        '.venv-win\\Scripts\\python.exe task_1.py '
        '--date {{ ds }} --batch {{ run_id }}"',
    )
    t2 = BashOperator(
        task_id = "data_cleaning",
        depends_on_past=True,
        bash_command='powershell.exe -Command '
        '"cd E:\\Handout\\project\\project_quant\\quant-factor-mining; '
        '.venv-win\\Scripts\\python.exe task_2.py '
        '--date {{ ds }} --batch {{ run_id }}"',
    )
    t3 = BashOperator(
        task_id = "factor_calculation",
        depends_on_past=True,
        bash_command='powershell.exe -Command '
        '"cd E:\\Handout\\project\\project_quant\\quant-factor-mining; '
        '.venv-win\\Scripts\\python.exe task_3.py '
        '--date {{ ds }} --batch {{ run_id }}"',
    )
    

t1 >> t2 >> t3