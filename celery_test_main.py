from app import play_task, check_status
import time


def get_status(task_id):
    task_result = check_status(task_id)
    res = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    print(res)


if __name__ == '__main__':
    # from app import play_task, check_status
    # result = play_task.delay()
    from celery import current_app
    print(current_app.tasks.keys())
    result = play_task.apply_async()
    get_status(result.id)
    print('sleep 1s')
    # sleep doi worker xu ly
    time.sleep(1)
    get_status(result.id)
    time.sleep(1)
    get_status(result.id)