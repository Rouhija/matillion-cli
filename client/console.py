import sys
import json
import time
import logging
import urllib3
from time import sleep
from client.api import *
from client.utils import *
from client.config import Config
from requests import ConnectTimeout
from client.signals import listen_signals

LOG = logging.getLogger(__name__)


class Console:
    def __init__(self, config):
        self.config = config
        self.addr = config['addr']
        self.auth = (config['user'], config['password'])
        self.group = None
        self.project = None
        self.active_tasks = []
        self.keepalive = True

    def print_usage(self):
        print('\nusage:')
        print('\tlist <search pattern> (list jobs in current context)')
        print('\trun <job_name> (run job in current context)')
        print('\tenv (switch context)')
        print('\tstatus (display status or active programs)')
        print('\thelp (display this message)')
        print('\texit')
        print()

    def select_env(self):
        try:
            self.select_group()
            self.select_project()
        except ConnectTimeout:
            sys.exit('Connection timed out, check target instance firewall rules for port 443')
        except Exception as e:
            sys.exit(f'Something went wrong, {e}')

    def run(self):
        self.select_env()
        self.print_usage()
        try:
            while self.keepalive:
                print(f'{self.group}:{self.project}> ', end='', flush=True)
                user_in = sys.stdin.readline().replace('\n', '').strip()
                cmd = parse_command(user_in)
                if cmd[0] == 'list':
                    self.list_jobs(cmd)
                elif cmd[0] == 'run':
                    self.run_job(cmd[1])
                elif cmd[0] == 'env':
                    self.select_env()
                elif cmd[0] == 'status':
                    self.get_status()
                elif cmd[0] == 'help':
                    self.print_usage()
                elif cmd[0] == 'exit':
                    self.keepalive = False
        except Exception as e:
            LOG.error(e)
        finally:
            sys.exit('exit')

    def get_status(self):
        for task_id in self.active_tasks:
            try:
                raw_resp = get_task_status(self.addr, self.auth, self.group, self.project, task_id)
            except:
                continue
            resp = to_json(raw_resp)
            job_name = f"{resp['jobName']} ({resp['id']})"
            job_state = resp['state']
            if int(resp['endTime']) == 0:
                job_uptime = int(round(time.time() * 1000)) - int(resp['startTime'])
            else:
                job_uptime = int(resp['endTime']) - int(resp['startTime'])
            job_uptime = round(job_uptime / 1000, 1)
            print('{:{width}}'.format(job_name, width=30), end='', flush=True)
            print('{:{width}}'.format(job_state, width=10), end='', flush=True)
            print(f'uptime: {job_uptime} seconds')

    def run_job(self, job, poll=False):
        if not self.is_running(job):
            print(f'calling job {self.group}.{self.project}.{job}')
            raw_resp = run_orchestration_job(self.addr, self.auth, self.group, self.project, job)
            print(raw_resp)
            task_id = to_json(raw_resp)['id']
            self.active_tasks.append(task_id)
            if poll:
                self.poll_job(job, task_id)
        else:
            print(f'job {job} is already running!')

    def poll_job(self, job, task_id):
        print(f'polling {job} ({task_id}) status...')
        state = None
        start_time = time.time()
        while 1:
            try:
                raw_resp = get_task_status(self.addr, self.auth, self.group, self.project, task_id)
            except Exception as e:
                print(e)
                state = 'NOT RUNNING'
                break
            resp = to_json(raw_resp)
            state = resp['state']
            if state != 'RUNNING':
                break
            else:
                elapsed = time.time() - start_time
                print('\r', end='', flush=True)
                print(f'{job} is running... elapsed {round(elapsed, 1)} seconds', end='', flush=True)
                sleep(1)
        print(f'\n{job} finished. State: {state}')
        self.task_id = None

    def run_from_argument(self, arg):
        err = 'arguments needs to be formatted as <group>.<project>.<job> (case-sensitive)'
        try:
            args = arg.split('.')
            self.group = args[0]
            self.project = args[1]
            self.run_job(args[2], poll=True)
        except:
            sys.exit(err)

    def is_running(self, job):
        raw_resp = get_running_tasks(self.addr, self.auth, self.group, self.project)
        resp = json.loads(raw_resp)
        if not len(resp):
            return False 
        elif job in resp[0]['jobNames']:
            return True
        else:
            return False

    def list_jobs(self, cmd):
        raw_resp = get_jobs(self.addr, self.auth, self.group, self.project)
        jobs = format_resp(raw_resp)
        jobs = sorted(jobs)
        if len(cmd) == 2:
            enumerate_list(jobs, cmd[1])
        else:
            enumerate_list(jobs)

    def select_group(self):
        raw_resp = get_groups(self.addr, self.auth)
        groups = format_resp(raw_resp)
        groups = sorted(groups)
        if len(groups) == 1:
            self.group = groups[0]
            print(f'using group {groups[0]}')
        else:
            enumerate_list(groups)
            print('choose a project number: ', end='', flush=True)
            user_in = sys.stdin.readline().replace('\n', '').strip()
            self.group = groups[int(user_in)]

    def select_project(self):
        raw_resp = get_projects(self.addr, self.auth, self.group)
        projects = format_resp(raw_resp)
        projects = sorted(projects)
        if len(projects) == 1:
            self.project = projects[0]
            print(f'using project {projects[0]}')
        else:
            enumerate_list(projects)
            print('choose a project number: ', end='', flush=True)
            user_in = sys.stdin.readline().replace('\n', '').strip()
            self.project = projects[int(user_in)]


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    listen_signals()
    args = arg_parser()
    conf = Config()
    conf.write_config(args.configuration)
    logger_options(args.debug)
    c = Console(conf.read_config())
    if args.run:
        c.run_from_argument(args.run)
    else:
        c.run()


if __name__ == '__main__':
    main()
