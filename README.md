# notes

Here's some basic workflow

noblox -> nbx

apt-file search bin/nbx reveals nothing - nbx should have no collisions


```shell
$ cd mycode
$ noblox init
   created orange-dolphin/
   added git hooks
   no apikey found, generating...
   your api key 44168467-e4cd-4ca6-87ee-25fd052f573a has been added

then I do something like this
$ cat OPENAI_KEY=123abc > .env
$ nvim ... work work work ...
$ git commit -am "work for the day"
   noblox detected .env changes, encrypting and syncing
$ git push
```


```
┌──┬──┐                 __    __          
│  │  │    ____  ____  / /_  / /___  _  __
├──┼──┤   / __ \/ __ \/ __ \/ / __ \| |/_/
│  │  │  / / / / /_/ / /_/ / / /_/ />  <  
└──┴──┘ /_/ /_/\____/_.___/_/\____/_/|_|
usage: noblox-cli.py [-h] {getenv,request,update,share,login} ...

noblox CLI tool.

positional arguments:
  {getenv,request,update,share,login}
                        Available commands
    getenv              Fetch environment variables and populate .env file
    request             Request API keys from fly.io or together.ai
    update              Check for updated API keys
    share               Share a restricted set of environment variables
    login               Login with an API key

options:
  -h, --help            show this help message and exit
```
