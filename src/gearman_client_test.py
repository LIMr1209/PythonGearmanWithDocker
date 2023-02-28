from gearman import JOB_UNKNOWN
from gearman.client import GearmanClient


def check_request_status(job_request):
    if job_request.complete:
        print("Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result))
    elif job_request.timed_out:
        print("Job %s timed out!" % job_request.unique)
    elif job_request.state == JOB_UNKNOWN:
        print("Job %s connection failed!" % job_request.unique)


client = GearmanClient(['localhost:4730'])

completed_job_request = client.submit_job("reverse", "Hello World!")
check_request_status(completed_job_request)
