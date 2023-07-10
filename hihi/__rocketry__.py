from rocketry import Rocketry

from hihi.utils.ssi import SSI

app = Rocketry()


@app.task("every 1 hour")
def refresh_token():
    SSI()
