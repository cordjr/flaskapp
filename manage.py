from flask_script import Manager
from app import app, db

manager = Manager(app)


@manager.shell
def make_shell_context():
    """ Creates a REPL with several default imports
        in the context of app

    :return:
    """
    return dict(app=app, db=db)
if __name__ == '__main__':
    manager.run()


