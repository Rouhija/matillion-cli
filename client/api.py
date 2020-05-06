import requests

HDR = {'Content-Type': 'application/json'}

class Error(Exception):
    pass

class ApiError(Error):
    def __init__(self, message):
        self.message = message

def get_groups(addr, auth):
    r = requests.get(f'{addr}/rest/v1/group/', headers=HDR, auth=auth)
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_projects(addr, auth, group):
    r = requests.get(f'{addr}/rest/v1/group/name/{group}/project/', headers=HDR, auth=auth)
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def get_jobs(addr, auth, group, project):
    r = requests.get(f'{addr}/rest/v1/group/name/{group}/project/name/{project}/version/name/default/job/', headers=HDR, auth=auth)
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None

def run_orchestration_job(addr, auth, group, project, job):
    r = requests.post(f'{addr}/rest/v1/group/name/{group}/project/name/{project}/version/name/default/job/name/{job}/run?environmentName=SNOWFLAKE', headers=HDR, auth=auth)
    if r.status_code == 200:
        return r.text
    else:
        raise ApiError(r.text)
        return None