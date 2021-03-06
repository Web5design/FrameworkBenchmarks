
import subprocess
import sys
import setup_util
import os
from zipfile import ZipFile

def start(args):
  setup_util.replace_text("play-java/conf/application.conf", "jdbc:mysql:\/\/.*:3306", "jdbc:mysql://" + args.database_host + ":3306")
  
  subprocess.check_call("play dist", shell=True, cwd="play-java")

  if os.name == 'nt':
    ZipFile("./play-java/dist/play-java-1.0-SNAPSHOT.zip").extractall("./play-java/dist")
    with open("./play-java/dist/play-java-1.0-SNAPSHOT/start.bat", "w+") as f:
      f.write("java %1 -cp \"./lib/*;\" play.core.server.NettyServer .")
    subprocess.Popen("start.bat", shell=True, cwd="play-java/dist/play-java-1.0-SNAPSHOT")
  else:
    subprocess.check_call("unzip play-java-1.0-SNAPSHOT.zip", shell=True, cwd="play-java/dist")
    subprocess.check_call("chmod +x start", shell=True, cwd="play-java/dist/play-java-1.0-SNAPSHOT")
    subprocess.Popen("./start", shell=True, cwd="play-java/dist/play-java-1.0-SNAPSHOT")

  return 0
def stop():
  if os.name == 'nt':
    with open("./play-java/dist/play-java-1.0-SNAPSHOT/RUNNING_PID") as f:
      pid = int(f.read())
      os.kill(pid, 9)
  else:
    p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
      if './start' in line or ('play' in line and 'java' in line):   
        pid = int(line.split(None, 2)[1])
        os.kill(pid, 9)

  try:
    os.remove("play-java/RUNNING_PID")
  except OSError:
    pass
    
  return 0
