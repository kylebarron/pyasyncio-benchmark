from importlib import import_module
import sqlite3

from benchmark.docker_utils import get_container_id
from benchmark.crud import insert_row, WorkerState
from benchmark.settings import get_settings


def run_test(library_name: str, test_name: str):
    mod = import_module(f"benchmark.tests.{library_name}.{test_name}")
    worker_state: WorkerState = mod.main()

    container_id = get_container_id()
    with sqlite3.connect(get_settings().DB_FILEPATH) as conn:
        insert_row(
            conn,
            library_name,
            test_name,
            container_id,
            get_settings().RUN_ID,
            worker_state,
        )
