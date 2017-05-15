import os

value = os.getenv('env', None)
if value:
    print('The value received from the env is ', value)

