# CLI

ntuaFLIX CLI manager

**Usage**:

```console
$ ntuaflix-cli [OPTIONS] COMMAND [ARGS]...
$ python3 -m ntuaflix_cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `adduser`: Adds user to system.
* `bygenre`: Searches for Titles using criteria.
* `healthcheck`: Checks the health of the API.
* `login`: Logs in and stores token to local storage.
* `logout`: Logs out and deletes token from local...
* `name`: Searches for Person details based on name ID.
* `newakas`: Uploads data for Aliases.
* `newcrew`: Uploads data for Crews.
* `newepisode`: Uploads data for Episodes.
* `newnames`: Uploads data for People.
* `newprincipals`: Uploads data for Title Principals.
* `newratings`: Uploads data for Title Ratings.
* `newtitles`: Uploads data for Titles.
* `resetall`: Resets database to initial state.
* `searchname`: Searches for People that their name...
* `searchtitle`: Searches for titles that their primary...
* `title`: Searches for title details based on title ID.
* `user`: Returns user details.

## `adduser`

Adds user to system. Requires authentication.

**Usage**:

```console
$ adduser [OPTIONS]
```

**Options**:

* `--username TEXT`: Username  [required]
* `--passw TEXT`: Password  [required]
* `--help`: Show this message and exit.

## `bygenre`

Searches for Titles using criteria. Requires authentication.

**Usage**:

```console
$ bygenre [OPTIONS]
```

**Options**:

* `--genre TEXT`: Genre  [required]
* `--min FLOAT`: Minimum rating (must be between 0 and 10).  [required]
* `--from INTEGER`: Start year must be after this year. If defined '--to' must also be defined.
* `--to INTEGER`: Start year must be before this year. If defined '--from' must also be defined.
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `healthcheck`

Checks the health of the API. Requires authentication.

**Usage**:

```console
$ healthcheck [OPTIONS]
```

**Options**:

* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `login`

Logs in and stores token to local storage.

**Usage**:

```console
$ login [OPTIONS]
```

**Options**:

* `--username TEXT`: Username  [required]
* `--passw TEXT`: Password  [required]
* `--help`: Show this message and exit.

## `logout`

Logs out and deletes token from local storage.

**Usage**:

```console
$ logout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `name`

Searches for Person details based on name ID. Requires authentication.

**Usage**:

```console
$ name [OPTIONS]
```

**Options**:

* `--nameid TEXT`: ID of person (nconst)  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newakas`

Uploads data for Aliases. Requires authentication.

**Usage**:

```console
$ newakas [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newcrew`

Uploads data for Crews. Requires authentication.

**Usage**:

```console
$ newcrew [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newepisode`

Uploads data for Episodes. Requires authentication.

**Usage**:

```console
$ newepisode [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newnames`

Uploads data for People. Requires authentication.

**Usage**:

```console
$ newnames [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newprincipals`

Uploads data for Title Principals. Requires authentication.

**Usage**:

```console
$ newprincipals [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newratings`

Uploads data for Title Ratings. Requires authentication.

**Usage**:

```console
$ newratings [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `newtitles`

Uploads data for Titles. Requires authentication.

**Usage**:

```console
$ newtitles [OPTIONS]
```

**Options**:

* `--filename TEXT`: .tsv filename  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `resetall`

Resets database to initial state. Requires authentication.

**Usage**:

```console
$ resetall [OPTIONS]
```

**Options**:

* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `searchname`

Searches for People that their name contains a given string. Requires authentication.

**Usage**:

```console
$ searchname [OPTIONS]
```

**Options**:

* `--namepart TEXT`: Substring of name.  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `searchtitle`

Searches for titles that their primary title contains a given string. Requires authentication.

**Usage**:

```console
$ searchtitle [OPTIONS]
```

**Options**:

* `--titlepart TEXT`: Substring of primary title.  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `title`

Searches for title details based on title ID. Requires authentication.

**Usage**:

```console
$ title [OPTIONS]
```

**Options**:

* `--titleID TEXT`: ID of title (tconst)  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

## `user`

Returns user details. Requires authentication.

**Usage**:

```console
$ user [OPTIONS]
```

**Options**:

* `--username TEXT`: Username  [required]
* `--format [json|csv]`: Format to query  [default: json]
* `--help`: Show this message and exit.

