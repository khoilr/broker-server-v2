import rocketry

from server.utils.ssi import SSI

app = rocketry.Rocketry()


@app.task("every 1 hour")
def refresh_token():
    """Refresh SSI token by initializing it."""
    SSI()
