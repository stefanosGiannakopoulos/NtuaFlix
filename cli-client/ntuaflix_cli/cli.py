from typing import Annotated, Optional
import typer
from rich import print
import requests
import urllib
from .utils import load_config, store_config, authenticated, handle_request, print_response, Format
from .config import *

app = typer.Typer(help="ntuaFLIX CLI manager")

@app.command()
def login(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        passw:      Annotated[str, typer.Option(help="Password", show_default=False)]
        ):
    """Logs in and stores token to local storage."""
    store_config("api_key", None)
    try:
        response = requests.post(API_URL + "/login",
                                 data={'username': username, 'password': passw},
                                 headers={'content-type': 'application/x-www-form-urlencoded'})

        if response.status_code == 200:
            if "token" in response.json():
                store_config("api_key", response.json()["token"])
                print(":white_check_mark: [bold green]You have been successfully authenticated.[/bold green]")
            else:
                print(":no_good: [bold red]Server responded in an irregular manner (no token in response JSON). Please contact system administrator.[/bold red]")
        elif response.status_code == 401:
            print(":stop_sign: [bold orange1]Unfortunately you were not authenticated (possibly due to wrong credentials). Please try again.[/bold orange1]")
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
    except requests.JSONDecodeError:
        print(":no_good: [bold red]Server responded in an irregular manner (bad JSON). Please contact system administrator.[/bold red]")
    except requests.ConnectionError:
        print(":cross_mark: [bold bright_black]Server is down.[/bold bright_black]")

@app.command()
@authenticated
def logout():
    """Logs out and deletes token from local storage."""
    try:
        response = requests.post(API_URL + "/logout", headers={"X-OBSERVATORY-AUTH": api_key})
        if response.status_code == 200:
            print(":white_check_mark: [bold green]You have been successfully logged out")
        else:
            print(":no_good: [bold red]Server responded in an irregular manner (bad status code). Please contact system administrator.[/bold red]")
            print(":white_exclamation_mark: [bright_black]Although server probably failed, your authentication token has been deleted from local db.")
    except requests.ConnectionError:
        print(":cross_mark: [bright_black]Server is down.[/bright_black]")
        print(":white_exclamation_mark: [bright_black]Your authentication token will be deleted from local db, though the server will not become aware of this.") 
    store_config("api_key", None)

@app.command()
@authenticated
def adduser(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        passw:      Annotated[str, typer.Option(help="Password", show_default=False)] 
        ):
    """Adds user to system. Requires authentication."""
    response = handle_request(f"/admin/usermod/{urllib.parse.quote(username)}/{urllib.parse.quote(passw)}", api_key=api_key)
    if response is not None:
        print(":white_check_mark: [bold green]User successfully created/modified.[/bold green]")
    else:
        print(":cross_mark: [bold red]User creation failed for unknownr reason.[/bold red]")


@app.command()
@authenticated
def user(
        username:   Annotated[str, typer.Option(help="Username", show_default=False)],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Returns user details. Requires authentication."""
    response = handle_request(f"/admin/users/{urllib.parse.quote(username)}", api_key=api_key, method="GET", params={'format': format})
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]User found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]User not found.[/bold bright_black]"
                )


@app.command()
@authenticated
def healthcheck(
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Checks the health of the API. Requires authentication."""
    response = handle_request("/admin/healthcheck", method="GET", api_key=api_key, params={'format': format})
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The following health status was received.[/bold green]")

@app.command()
@authenticated
def resetall(
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Resets database to initial state. Requires authentication."""
    response = handle_request("/admin/resetall", api_key=api_key, params={'format': format})
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")


@app.command()
@authenticated
def newtitles(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Titles. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titlebasics", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newakas(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Aliases. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleakas", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newnames(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for People. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/namebasics", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newcrew(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Crews. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titlecrew", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newepisode(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Episodes. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleepisode", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newprincipals(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Title Principals. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleprincipals", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def newratings(
        filename: Annotated[str, typer.Option(help=".tsv filename")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Uploads data for Title Ratings. Requires authentication."""
    try:
        with open(filename, "rb") as f:
            response = handle_request("/admin/upload/titleratings", api_key=api_key, params={'format': format},
                    files = {'file': ('', f, 'text/csv')})
    except OSError:
        print(":cross_mark: [bold red]The file could not be opened.[/bold red]")
        return
    if response is not None:
        print_response(response, format=format, found_msg=":white_check_mark: [bold green]The server responded the following.[/bold green]")

@app.command()
@authenticated
def title(
        titleID: Annotated[str, typer.Option("--titleID", help="ID of title (tconst)")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Searches for title details based on title ID. Requires authentication."""
    response = handle_request(f"/title/{urllib.parse.quote(titleID)}", method="GET", params={'format': format})
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]Title found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]Title not found.[/bold bright_black]" 
                )

@app.command()
@authenticated
def searchtitle(
        titlepart: Annotated[str, typer.Option(help="Substring of primary title.")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Searches for titles that their primary title contains a given string. Requires authentication."""
    response = handle_request(f"/searchtitle", method="GET", params={'format': format}, json={"titlePart": titlepart})
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]Titles found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]No Title found.[/bold bright_black]" 
                )

@app.command()
@authenticated
def bygenre(
        genre: Annotated[str, typer.Option(help="Genre")],
        _min: Annotated[float, typer.Option("--min", help="Minimum rating (must be between 0 and 10).")],
        _from: Annotated[Optional[int], typer.Option("--from", help="Start year must be after this year. If defined '--to' must also be defined.")] = None,
        to: Annotated[Optional[int], typer.Option(help="Start year must be before this year. If defined '--from' must also be defined.")] = None,
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Searches for Titles using criteria. Requires authentication."""

    if (_from is None) != (to is None):
        print(":no_entry: [bold red]Options '--from', '--to' must either both be defined or neither.[/bold red]")
        return
    if _min < 0 or _min > 10:
        print(":no_entry: [bold red] Minimum rating must be between 0 and 10.")
        return 
    payload = {'qgenre': genre, 'minrating': f"{_min:.1f}"}
    if _from is not None:
        payload["yrFrom"] = str(_from)
        payload["yrTo"] = str(to)
    response = handle_request(f"/bygenre", method="GET", params={'format': format}, json=payload)
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]Titles found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]No Title found.[/bold bright_black]" 
                )


@app.command()
@authenticated
def name(
        nameid: Annotated[str, typer.Option(help="ID of person (nconst)")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Searches for Person details based on name ID. Requires authentication."""
    response = handle_request(f"/name/{urllib.parse.quote(nameid)}", method="GET", params={'format': format})
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]Person found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]Person not found.[/bold bright_black]" 
                )


@app.command()
@authenticated
def searchname(
        namepart: Annotated[str, typer.Option(help="Substring of name.")],
        format: Annotated[Format, typer.Option(help="Format to query")] = Format.json
        ):
    """Searches for People that their name contains a given string. Requires authentication."""
    response = handle_request(f"/searchname", method="GET", json={"namePart": namepart}, params={'format': format})
    if response is not None:
        print_response(response,
                format=format,
                found_msg=":white_check_mark: [bold green]People found with following details.[/bold green]",
                empty_msg=":magnifying_glass_tilted_right: [bold bright_black]No Person found.[/bold bright_black]" 
                )

if __name__ == '__main__':
    app()

