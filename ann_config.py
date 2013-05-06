import os

from apiclient.discovery import build
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

oauth_decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
  'https://www.googleapis.com/auth/cloudprint')
