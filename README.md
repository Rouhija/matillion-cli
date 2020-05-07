# Description
CLI tool for running Matillion jobs. Names are case-sensitive. Prompts for instance address, api user and api key on the first run.

### Usage
Installation
```
pip install matillioncli
```

Run in interactive mode
```sh
matillioncli
```

Optional arguments
```sh
usage: matillioncli [-h] [-d] [-c] [-r RUN]

optional arguments:
  -h, --help           show this help message and exit
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
| **list** *search_pattern* | List jobs in current context |
| **env** | Switch group/project context |
| **exit** | Exit |
