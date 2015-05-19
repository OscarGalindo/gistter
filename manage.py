from flask.ext.script import Manager, Server, Shell
from gistter import app, mongo
import sys
import os


def _make_context():
    return dict(app=app, mongo=mongo)


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'))

manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()