from backend.k8s_client import (create_k8s_job,
                        get_job_logs as get_pod_logs,
                        get_job_pod,
                        get_job_status as get_k8s_job_status
                        ,delete_job
                        )

from backend.db_manager import DatabaseManager
from kubernetes.client.exceptions import ApiException

db = DatabaseManager()



def create_job(job_name, image, command, cpu, memory, namespace):

    try:
        create_k8s_job(job_name, image, command, cpu, memory, namespace)

    except ApiException:
        delete_job(job_name, namespace)
        create_k8s_job(job_name, image, command, cpu, memory, namespace)
    
    db.delete_job(job_name)
    
    # Save job in database
    db.save_job(job_name, image, command, namespace)

    return {
        "message": "Job submitted",
        "job_name": job_name
    }
    
def get_job_status(job_name, namespace):

    status_data = get_k8s_job_status(job_name, namespace)

    active = status_data.get("active")
    succeeded = status_data.get("succeeded")
    failed = status_data.get("failed")
    completion_time = status_data.get("completion_time")

    if succeeded is not None and succeeded >= 1:
        status = "Completed"

    elif failed is not None and failed >= 1:
        status = "Failed"

    elif active is not None and active >= 1:
        status = "Running"

    elif completion_time is not None:
        status = "Completed"

    else:
        status = "Pending"

    db.update_job_status(
        job_name,
        status,
        status_data["start_time"],
        status_data["completion_time"]
    )

    return {
        "job_name": job_name,
        "status": status,
        "start_time": status_data["start_time"],
        "completion_time": status_data["completion_time"]
    }
    
def get_job_logs(job_name, namespace):

    pod_name = get_job_pod(job_name, namespace)

    if not pod_name:
        return {"message": "Pod not found yet"}

    logs = get_pod_logs(pod_name, namespace)

    return {
        "job_name": job_name,
        "logs": logs
    }
    

