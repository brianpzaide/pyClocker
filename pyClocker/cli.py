from pathlib import Path
from typing import Optional, List

from . import(
    SUCCESS, ERRORS, __app_name__, __version__, config, database, pyClocker
)

import typer
import matplotlib.pyplot as plt

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="pyClocker database location?",
    ),
) -> None:
    """Initialize the pyClocker database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating schema file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The pyClocker database is {db_path}", fg=typer.colors.GREEN)

def get_pyClocker() -> pyClocker.PyClocker:
    """Get pyClocker object"""
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "pyClocker init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return pyClocker.PyClocker(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "pyClocker init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command(name="start")
def start_session() -> None:
    """Start a new Session."""
    mpt = get_pyClocker()
    res = mpt.start()
    if res == SUCCESS:
        typer.secho(
            'New work session started', fg=typer.colors.GREEN
        )
        return
    else:
        typer.secho(
            f'{ERRORS[res]}', fg=typer.colors.RED
        )
        return

@app.command(name="stop")
def end_session() -> None:
    """End the current session."""
    mpt = get_pyClocker()
    res = mpt.stop()
    if res == SUCCESS:
        typer.secho(
            'current session stopped', fg=typer.colors.GREEN
        )
        return
    else:
        typer.secho(
            f'{ERRORS[res]}', fg=typer.colors.RED
        )
        return
        

@app.command(name="today")
def hours_today() -> None:
    """Number of hours put in today."""
    mpt = get_pyClocker()
    res = mpt.hours_put_in_today()
    typer.secho(
            res, fg=typer.colors.BLUE
        )
    return

@app.command(name="daily")
def daily_stats() -> None:
    """Get number of hours put in everyday."""
    mpt = get_pyClocker()
    res = mpt.hours_put_in_daily()
    days = []
    hours = []
    for dwh in res:
        days.append(dwh.date)
        hours.append(dwh.hours)
    
    # plotting a line graph x-axis: days, y-xis: hours
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    ax.plot(days, hours, linewidth=2.0)
    ax.set_xlabel("day->")
    ax.set_ylabel("hours->")
    plt.show()


def _version_callback(value:bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True, 
    )
) -> None:
    return