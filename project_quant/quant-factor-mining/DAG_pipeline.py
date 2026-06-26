import textwrap
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.sdk import DAG

with DAG("quant_factor_mining",
        default_args={
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
        trigger_rule = TriggerRule.ALL_DONE
    )
    t3 = BashOperator(
        task_id = "factor_calculation",
        bash_command='powershell.exe -Command '
        '"cd E:\\Handout\\project\\project_quant\\quant-factor-mining; '
        '.venv-win\\Scripts\\python.exe task_3.py '
        '--date {{ ds }} --batch {{ run_id }}"',
    )
    task_retry = BashOperator(
        task_id = "retry_downloading",
        bash_command='powershell.exe -Command '
        '"cd E:\\Handout\\project\\project_quant\\quant-factor-mining; '
        '.venv-win\\Scripts\\python.exe task_retry.py '
        '--date {{ ds }} --batch {{ run_id }}"',
        trigger_rule = TriggerRule.ALL_FAILED
    )
    

t1 >> t2 >> t3
t1 >> task_retry