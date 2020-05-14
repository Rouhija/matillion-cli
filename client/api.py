import requests
import urllib.parse

HDRS = {'Content-Type': 'application/json'}
PORT = 443

class Error(Exception):
    pass

class ApiError(Error):
    def __init__(self, message):
        self.message = message

def get_groups(addr, auth):
    r = requests.get(f'{addr}:{PORT}/rest/v1/group/', headers=HDRS, auth=auth, verify=False, timeout=5)
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_projects(addr, auth, group):
    r = requests.get(
        f'{addr}:{PORT}/rest/v1/group/name/{urllib.parse.quote(group)}/project/',
        headers=HDRS,
        auth=auth,
        verify=False
        )
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_jobs(addr, auth, group, project):
    r = requests.get(
        f'{addr}:{PORT}/rest/v1/group/name/{urllib.parse.quote(group)}/project/name/{urllib.parse.quote(project)}/version/name/default/job/',
        headers=HDRS,
        auth=auth,
        verify=False
        )
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def run_orchestration_job(addr, auth, group, project, job):
    r = requests.post(
        f'{addr}:{PORT}/rest/v1/group/name/{urllib.parse.quote(group)}/project/name/{urllib.parse.quote(project)}/version/name/default/job/name/{urllib.parse.quote(job)}/run?environmentName=SNOWFLAKE',
        headers=HDRS,
        auth=auth,
        verify=False
        )
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_running_tasks(addr, auth, group, project):
    r = requests.get(
        f'{addr}:{PORT}/rest/v1/group/name/{urllib.parse.quote(group)}/project/name/{urllib.parse.quote(project)}/task/running',
        headers=HDRS,
        auth=auth,
        verify=False
        )
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_task_status(addr, auth, group, project, task_id):
    r = requests.get(
        f'{addr}:{PORT}/rest/v1/group/name/{urllib.parse.quote(group)}/project/name/{urllib.parse.quote(project)}/task/id/{task_id}',
        headers=HDRS,
        auth=auth,
        verify=False
        )
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None