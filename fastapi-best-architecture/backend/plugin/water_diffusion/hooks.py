from starlette.staticfiles import StaticFiles

from backend.common.log import log


def setup(app) -> None:
    """Mount water diffusion simulation sub-app with its own Socket.IO and static files."""
    from backend.plugin.water_diffusion.manager import socket_app

    app.mount("/simulations/water-diffusion", socket_app)
    log.info("Water diffusion simulation plugin mounted at /simulations/water-diffusion")
