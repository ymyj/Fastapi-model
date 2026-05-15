"""Water diffusion simulation manager - holds the sub-app and simulator state."""

import asyncio
import base64
import concurrent.futures
import io
import os
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from PIL import Image
import socketio

from backend.plugin.water_diffusion.core.simulation import SoilPollutionSimulator

sub_app = FastAPI(title="Water Diffusion Simulation")

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, sub_app, socketio_path='/simulations/water-diffusion/socket.io')

simulator = None
is_running = False
frames_store = []


def _get_index_path():
    return os.path.join(os.path.dirname(__file__), "templates", "index.html")


@sub_app.get("/")
async def index():
    file_path = _get_index_path()
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={
        "message": "地下水污染垂向扩散模拟插件已加载",
        "api_docs": "/api/v1/water-diffusion/docs",
        "simulation_ui": "/simulations/water-diffusion/"
    })


@sub_app.post("/api/simulate")
async def start_simulation(request: Request):
    global simulator, is_running

    if is_running:
        return JSONResponse(content={"error": "Simulation already running"}, status_code=400)

    params = await request.json()
    simulator = SoilPollutionSimulator(params)
    is_running = True

    asyncio.create_task(_run_simulation_wrapper())

    return JSONResponse(content={"status": "started"})


@sub_app.post("/api/stop")
async def stop_simulation():
    global is_running
    is_running = False
    return JSONResponse(content={"status": "stopped"})


@sub_app.post("/api/reset")
async def reset_simulation():
    global simulator, is_running, frames_store
    is_running = False
    frames_store = []
    if simulator:
        simulator.reset()
        initial_frame = simulator.render_frame(simulator.c, 0)
        stats = simulator.calculate_stats()
        depth_data, concentration_data = simulator.get_depth_profile()
        await sio.emit("frame", {
            "image": initial_frame,
            "step": 0,
            "time": 0,
            "total_steps": simulator.steps,
            "stats": stats,
            "depth_data": depth_data,
            "concentration_data": concentration_data
        })
    return JSONResponse(content={"status": "reset"})


@sub_app.get("/api/export-animation")
async def export_animation():
    global frames_store
    if not frames_store:
        return JSONResponse(content={"error": "No frames to export"}, status_code=400)

    try:
        images = []
        for frame_data in frames_store:
            img_data = base64.b64decode(frame_data)
            img = Image.open(io.BytesIO(img_data))
            img = img.convert("RGB")
            images.append(img)

        output = io.BytesIO()
        images[0].save(
            output,
            format="GIF",
            append_images=images[1:],
            save_all=True,
            duration=80,
            loop=0,
            optimize=False
        )
        output.seek(0)

        return StreamingResponse(output, media_type="image/gif",
                                 headers={"Content-Disposition": 'attachment; filename="simulation.gif"'})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@sub_app.get("/api/params")
async def get_default_params():
    temp_sim = SoilPollutionSimulator()
    return JSONResponse(content=temp_sim.default_params)


@sio.on("connect")
async def handle_connect(sid, environ):
    global simulator
    if simulator:
        initial_frame = simulator.render_frame(simulator.c, 0)
        stats = simulator.calculate_stats()
        depth_data, concentration_data = simulator.get_depth_profile()
        await sio.emit("frame", {
            "image": initial_frame,
            "step": 0,
            "time": 0,
            "total_steps": simulator.steps,
            "stats": stats,
            "depth_data": depth_data,
            "concentration_data": concentration_data
        }, room=sid)


@sio.on("disconnect")
async def handle_disconnect(sid):
    pass


async def _run_simulation_wrapper():
    try:
        await _run_simulation()
    except Exception as e:
        traceback.print_exc()
        global is_running
        is_running = False


async def _run_simulation():
    global is_running, simulator, frames_store

    if not simulator:
        return

    frames_store = []
    steps = simulator.steps
    frame_interval = 25

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    try:
        for step in range(steps):
            if not is_running:
                break

            result = await asyncio.get_running_loop().run_in_executor(
                executor,
                lambda s=step: simulator.solve_step(simulator.c, s)
            )
            simulator.c = result

            if step % frame_interval == 0:
                frame_image = await asyncio.get_running_loop().run_in_executor(
                    executor,
                    lambda: simulator.render_frame(simulator.c, step)
                )
                time_days = step * simulator.dt
                stats = await asyncio.get_running_loop().run_in_executor(
                    executor,
                    lambda: simulator.calculate_stats()
                )
                depth_data, concentration_data = await asyncio.get_running_loop().run_in_executor(
                    executor,
                    lambda: simulator.get_depth_profile()
                )

                frames_store.append(frame_image)

                await sio.emit("frame", {
                    "image": frame_image,
                    "step": step,
                    "time": time_days,
                    "total_steps": steps,
                    "stats": stats,
                    "depth_data": depth_data,
                    "concentration_data": concentration_data
                })

        await sio.emit("simulation_complete")
    finally:
        executor.shutdown(wait=False)
        is_running = False
