import sys
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

dag_id = "D_Check_all_load_end"
tags = ["daily", "check"]


def _task_failure_alert(context):
    from airflow_modules.utils import send_notification

    send_notification(dag_id, tags, "ERROR")


args = {"owner": "airflow", "retries": 3, "retry_delay": timedelta(minutes=10)}

with DAG(
    dag_id,
    description="Check all loading dags completed",
    schedule_interval="0 6 * * 0",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    on_failure_callback=_task_failure_alert,
    concurrency=5,  # can run N tasks at the same time
    max_active_runs=1,  # can run N DAGs at the same time
    tags=tags,
    default_args=args,
) as dag:
    dag_start = DummyOperator(task_id="dag_start")

    ##############################################
    # Task Group to wait for previous tasks finish
    ##############################################
    _allowed_states = ["success"]
    _failed_states = ["failed", "skipped"]
    _check_existence = True
    _poke_interval = 10
    _mode = "reschedule"
    _timeout = 7200

    wait_trunk_load = ExternalTaskSensor(
        task_id="wait_trunk_load",
        external_dag_id="D_Check_trunk_load_end",
        external_task_id="dag_end",
        allowed_states=_allowed_states,
        failed_states=_failed_states,
        check_existence=_check_existence,
        poke_interval=_poke_interval,
        execution_delta=timedelta(minutes=60 * 4 + 50),
        mode=_mode,
        timeout=_timeout,
    )

    wait_branch_load = ExternalTaskSensor(
        task_id="wait_branch_load",
        external_dag_id="D_Check_branch_load_end",
        external_task_id="dag_end",
        allowed_states=_allowed_states,
        failed_states=_failed_states,
        check_existence=_check_existence,
        poke_interval=_poke_interval,
        execution_delta=timedelta(minutes=0),
        mode=_mode,
        timeout=_timeout,
    )

    dag_end = DummyOperator(task_id="dag_end")

    (dag_start >> [wait_trunk_load, wait_branch_load] >> dag_end)
