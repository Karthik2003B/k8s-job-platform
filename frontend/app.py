import streamlit as st
import requests

BASE_URL = "http://backend-service:8000"

st.set_page_config(page_title="Kubernetes Job Platform", layout="wide")

st.title("🚀 Kubernetes Job Platform")

# ------------------------------
# Submit Job
# ------------------------------

st.header("Submit Job")

col1, col2 = st.columns(2)

with col1:
    job_name = st.text_input("Job Name", "test-job")
    image = st.text_input("Container Image", "python:3.11")
    command = st.text_input(
        "Command",
        'python -c "print(\'Hello from Kubernetes\')"'
    )

with col2:
    cpu = st.text_input("CPU Limit", "500m")
    memory = st.text_input("Memory Limit", "256Mi")
    namespace = st.text_input("Namespace", "default")

if st.button("Submit Job"):

    response = requests.post(
        f"{BASE_URL}/jobs",
        params={
            "job_name": job_name,
            "image": image,
            "command": command,
            "cpu": cpu,
            "memory": memory,
            "namespace": namespace
        }
    )

    if response.status_code == 200:

        data = response.json()

        st.success(f"Job '{data['job_name']}' submitted successfully!")

        st.info("You can now check the job status or view logs.")

    else:

        st.error("Failed to submit job")

st.divider()

# ------------------------------
# Job Status
# ------------------------------

st.header("Check Job Status")

status_job_name = st.text_input("Job Name for Status", "test-job")

if st.button("Get Status"):

    response = requests.get(
        f"{BASE_URL}/jobs/{status_job_name}",
        params={"namespace": namespace}
    )

    data = response.json()

    st.subheader("Job Status")

    status = data.get("status")

    if status == "Completed":
        st.success("✅ Job Completed")

    elif status == "Running":
        st.warning("⏳ Job Running")

    elif status == "Failed":
        st.error("❌ Job Failed")

    elif status == "Pending":
        st.info("⏱ Job Pending")

    else:
        st.info("Status Unknown")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Start Time")
        st.code(data.get("start_time"))

    with col2:
        st.write("Completion Time")
        st.code(data.get("completion_time"))

st.divider()

# ------------------------------
# Logs
# ------------------------------

st.header("Get Job Logs")

logs_job_name = st.text_input("Job Name for Logs", "test-job")

if st.button("Get Logs"):

    response = requests.get(
        f"{BASE_URL}/jobs/{logs_job_name}/logs",
        params={"namespace": namespace}
    )

    data = response.json()

    st.subheader("Logs")

    st.text_area(
        "Container Output",
        data.get("logs", "No logs available"),
        height=250
    )
    
st.header("All Submitted Jobs")

if st.button("Load Jobs"):

    response = requests.get(f"{BASE_URL}/jobs")

    if response.status_code == 200:

        jobs = response.json()

        if jobs:
            for job in jobs:

                st.write("Job ID:", job[0])
                st.write("Job Name:", job[1])
                st.write("Image:", job[2])
                st.write("Command:", job[3])
                st.write("Namespace:", job[4])
                st.write("Status:", job[5])
                st.write("Start Time:", job[6])
                st.write("Completion Time:", job[7])
                st.divider()

        else:
            st.info("No jobs found")