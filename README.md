# Description
CLI tool for running Matillion jobs. Names are case-sensitive. Prompts for instance address, api user and api key on the first run.

### Usage

Make sure you have python3 on your machine (3.6 < 3.9)

Installation
```
pip install matillioncli            # install
pip install matillioncli --upgrade  # update
```

Run from commandline
```sh
matillioncli -r <group>.<project>.<job>
```

Run in interactive mode
```sh
matillioncli
```

First you will select your environment (dev/test/prod, for example). You can search jobs using `list <search pattern>` and run your recent search using `run list`, or you can run a specific job using `run <job name>`. Running jobs and their states can be displayed with `status` command.

Optional arguments
```sh
usage: matillioncli [-h] [-v] [-d] [-c] [-r RUN]

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        display package version
  -d, --debug          log to console
  -c, --configuration  re-input configuration values
  -r RUN, --run RUN    start orchestration job without interactive mode
                       (<group>.<project>.<job>)
```

### Commands
| CMD | ACTION |
|---------|---------|
| **help** | Display help |
| **status** | Display status or queued jobs |
| **run** *job_name* | Run job in current context |
| **run list** | Run recently listed jobs |
| **list** *search_pattern* | List jobs in current context |
| **env** | Switch group/project context |
| **exit** | Exit |

### References
- [APImap](https://snowflake-support.matillion.com/s/article/2920263)
