from functools import wraps
from pathlib import Path
import typer
import json
from rich import print, print_json
from rich.table import Table
import io
import csv
import requests

from .config import *

from enum import Enum

class Format(str, Enum):
    json = "json"
    csv = "csv"

def load_config(var):
    app_dir = Path(typer.get_app_dir(APP_NAME))
    config_path = app_dir / "config.json"
    if config_path.is_file():
        try:
            with open(config_path, "r") as config_f:
                config = json.load(config_f)
            if var in config:
                return config[var]
        except: pass
    return None

def store_config(var, value):
    app_dir = Path(typer.get_app_dir(APP_NAME))
    config_path = app_dir / "config.json"
    config = {}
    if config_path.is_file():
        try:
            with open(config_path, "r") as config_f:
                config = json.load(config_f)
        except: pass
    
    if value is not None: config[var] = value
    else:
        config.pop(var, None)

    app_dir.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as config_f:
        json.dump(config, config_f)

def call_inject_variable(func, variables, args, kwargs):
    sentinels = [object() for _ in range(len(variables))]
    olds = [func.__globals__.get(name, sentinel) for name, sentinel in zip(variables.keys(), sentinels)]
    func.__globals__.update(variables)
    ret = func(*args, **kwargs)
    for name, old, sentinel in zip(variables.keys(), olds, sentinels):
        if old is sentinel: func.__globals__.pop(name)
        else: func.__globals__[name] = old
    return ret

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = load_config("api_key")
        if api_key is not None:
            return call_inject_variable(func, {'api_key':api_key}, args, kwargs)
        else:
            print(":locked_with_key: [bold red]You are not authenticated. Please login first.[/bold red]")
    return wrapper

def handle_request(path, *, method="POST", api_key=None, **kwargs):
    try:
        if api_key is not None:
            if 'headers' not in kwargs: kwargs['headers'] = {}
            kwargs['headers']["X-OBSERVATORY-AUTH"] = api_key
        response = requests.request(method, API_URL + path,
                **kwargs
                )
        if response.status_code == 200:
            return response
        elif response.status_code == 401:
            print(response.text)
            print(":stop_sign: [bold red]Your token appears to be outdated. Please logout and relogin. [/bold red]")
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
    except requests.ConnectionError:
        print(":cross_mark: [bright_black]Server is down.[/bright_black]")
    return None

def print_csv(text, *, found_msg=None, empty_msg=None):
    csv_data = io.StringIO(text)
    csv_reader = csv.reader(csv_data)
    table = Table(show_header=True)
    try:
        headers = next(csv_reader, None)
        if headers is None:
            if empty_msg is not None: print(empty_msg)
            return
        for header in headers:
            table.add_column(header)
        first_row = next(csv_reader, None)
        if first_row is None:
            print(":no_good: [bold red]Server responded in an irregular manner (bad CSV). Please contact system administrator.[/bold red]")
            return
        table.add_row(*first_row)
        for row in csv_reader:
            table.add_row(*row)
    except csv.Error:
        print(":no_good: [bold red]Server responded in an irregular manner (bad CSV). Please contact system administrator.[/bold red]")
        return
    if found_msg is not None: print(found_msg)
    print(table)


def print_response(response, *, format, found_msg=None, empty_msg=None):
    if format == Format.json:
        try:
            response = response.json()
        except requests.JSONDecodeError:
            print(":no_good: [bold red]Server responded in an irregular manner (bad JSON). Please contact system administrator.[/bold red]") 
            return
        if response == {} or response == [] or response == None:
            if empty_msg is not None: print(empty_msg)
        else:
            if found_msg is not None: print(found_msg)
            print_json(data=response)
    elif format == Format.csv:
        print_csv(response.text, found_msg=found_msg, empty_msg=empty_msg)

