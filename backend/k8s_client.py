from kubernetes import client, config

config.load_incluster_config()
batch_v1 = client.BatchV1Api()


def create_k8s_job(job_name,image,command,cpu,memory,namespace):

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=job_name,
                            image=image,
                            command=["sh", "-c", command],
                            resources=client.V1ResourceRequirements(
                                limits={"cpu":cpu,"memory":memory}
                            )
                        )
                    ],
                    restart_policy="Never"
                )
            )
        )
    )
    
    batch_v1.create_namespaced_job(namespace=namespace,body=job)

def get_job_status(job_name, namespace):

    job = batch_v1.read_namespaced_job(
        name=job_name,
        namespace=namespace
    )

    status = job.status

    return {
        "active": status.active,
        "succeeded": status.succeeded,
        "failed": status.failed,
        "start_time": str(status.start_time) if status.start_time else None,
        "completion_time": str(status.completion_time) if status.completion_time else None
    }

core_v1 = client.CoreV1Api()

def get_job_pod(job_name, namespace):

    pods = core_v1.list_namespaced_pod(namespace)

    for pod in pods.items:
        if pod.metadata.labels and pod.metadata.labels.get("job-name") == job_name:
            return pod.metadata.name

    return None

def get_job_logs(pod_name, namespace="default"):
    logs = core_v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace
    )

    return logs

def delete_job(job_name, namespace):
    batch_v1.delete_namespaced_job(
        name=job_name,
        namespace=namespace,
        propagation_policy="Background"
    )

