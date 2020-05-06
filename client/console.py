import sys
import logging
from client.api import *
from client.utils import *
from client.config import Config

LOG = logging.getLogger(__name__)


class Console:
    def __init__(self, config):
        self.config = config
        self.addr = config['addr']
        self.auth = (config['user'], config['password'])
        self.group = None
        self.project = None
        self.keepalive = True

    def select_env(self):
        self.select_group()
        self.select_project()
        pass

    def print_usage(self):
        print('\nusage:')
        print('\tlist <search pattern> (list jobs in context)')
        print('\trun <job_name>')
        print('\tenv (switch context)')
        print('\thelp (display this message)')
        print()

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
                elif cmd[0] == 'help':
                    self.print_usage()
        except Exception as e:
            LOG.error(e)
        finally:
            sys.exit()

    def run_job(self, job):
        raw_resp = run_orchestration_job(self.addr, self.auth, self.group, self.project, job)
        print(raw_resp)

    def list_jobs(self, cmd):
        raw_resp = get_jobs(self.addr, self.auth, self.group, self.project)
        jobs = format_resp(raw_resp)
        if len(cmd) == 2:
            enumerate_list(jobs, cmd[1])
        else:
            enumerate_list(jobs)

    def select_group(self):
        raw_resp = get_groups(self.addr, self.auth)
        groups = format_resp(raw_resp)
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
        if len(projects) == 1:
            self.project = projects[0]
            print(f'using project {projects[0]}')
        else:
            enumerate_list(projects)
            print('choose a project number: ', end='', flush=True)
            user_in = sys.stdin.readline().replace('\n', '').strip()
            self.project = projects[int(user_in)]


def main():
    args = arg_parser()
    conf = Config()
    conf.write_config(args.configuration)
    logger_options(args.debug)
    c = Console(conf.read_config())
    c.run()
    pass


if __name__ == '__main__':
    main()