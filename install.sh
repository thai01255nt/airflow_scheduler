#!/bin/bash
airflow initdb

sed -i '/dags_are_paused_at_creation = True/c\dags_are_paused_at_creation = False' $AIRFLOW_HOME/airflow.cfg
sed -i '/max_active_runs_per_dag = 16/c\max_active_runs_per_dag = 1' $AIRFLOW_HOME/airflow.cfg
airflow variables --import $AIRFLOW_HOME/dags/env.json