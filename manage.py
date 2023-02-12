import sys, subprocess, uvicorn

from game.config import MIGRATION_LOCATION, DEPLOYMENT_DETAILS

if __name__ == "__main__":
    if sys.argv == ["manage.py", "migrate", "first", "time"]:
        subprocess.run(["aerich", "init", "-t", "game.main.db_config", "--location", MIGRATION_LOCATION])
        subprocess.run(["aerich", "init-db"])
    
    if sys.argv == ["manage.py", "migrate"]:
        print("Please give migration a name.")
        migration_name = input()
        commands = [["aerich", "migrate", "--name", migration_name], ["aerich", "upgrade"]]
        for cmd in commands:
            subprocess.run(cmd)

    if sys.argv == ["manage.py", "runserver"]:
        uvicorn.run("game.main:app", port = DEPLOYMENT_DETAILS["PORT"], host=DEPLOYMENT_DETAILS["HOST"], reload=True, lifespan="on")
