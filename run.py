import subprocess, os

cmd_scheduler = "./scheduler.sh"
scheduler_proc = subprocess.Popen([cmd_scheduler], shell=True,
                        stdin=None, stdout=None, stderr=None, close_fds=True)

cmd_webserver = "./webserver.sh"
webserver_proc = os.system(cmd_webserver)
scheduler_proc.kill()