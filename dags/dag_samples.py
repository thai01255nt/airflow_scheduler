from datetime import timedelta
import requests, os, json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

#set default Varuabke


def get_system_config(env_path):
    with open(env_path) as json_data_file:
        data = json.load(json_data_file)
    return data

ENV = Variable.get("env_config",deserialize_json=True)


PIPELINEWISE_API_EXECUTOR = ENV["PIPELINEWISE_API_EXECUTOR"]

DAG_CONFIG = {}
DAG_CONFIG["dag_id"] = ENV["dag_id"]
DAG_CONFIG["description"] = "This is a test dag"
DAG_CONFIG["schedule_interval"] = ENV["SCHEDULE_INTERVAL"]

POST_BODY = ENV["POST_BODY"]


def get_default_transfer_args():
    default_args = {
        'owner': "airflow",
        'depends_on_past': False,
        'start_date': days_ago(0),
        'email': ['vmo@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'retry_delay': timedelta(seconds=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'dag': dag,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    }
    return default_args


def run_transfer():
    response = requests.post(PIPELINEWISE_API_EXECUTOR, json=POST_BODY)
    if response.status_code != 200:
        raise Exception(response.content)
    print(response.content.decode('ascii'))
    return


def create(dag_config):
    dag = DAG(
        dag_id=dag_config["dag_id"],
        default_args=get_default_transfer_args(),
        description=dag_config["description"],
        schedule_interval=dag_config["schedule_interval"]
    )

    run_transfer_task = PythonOperator(
        task_id='run_transfer_task',
        python_callable=run_transfer,
        dag=dag,
        retries=0
    )

    return dag


globals()[DAG_CONFIG["dag_id"]] = create(DAG_CONFIG)
