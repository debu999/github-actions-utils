# wsgi.py
from github_actions_utils.calculator import app

if __name__ == '__main__':
  app.run()