import os


def get_environment():
    env = os.environ.get('ENV')
    if env != "DEV" and env != "PROD":
        exit(" ENV must be PROD/DEV")
    return env


ENV = get_environment()
MOCK_DATA = "Hello for Devalore from Idan"


def environment_wrapper(func):
    def wrapper(*args, **kwargs):
        if ENV == "DEV":
            result = MOCK_DATA
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper


@environment_wrapper
def check():
    return 5


if _name_ == '_main_':
    print(check())