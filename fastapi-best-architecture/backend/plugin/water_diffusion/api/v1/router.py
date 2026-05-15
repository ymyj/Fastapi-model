from fastapi import APIRouter
from fastapi.responses import JSONResponse

v1 = APIRouter(prefix="/water-diffusion", tags=["地下水污染垂向扩散模拟"])


@v1.get("/info")
async def get_plugin_info():
    return JSONResponse(content={
        "name": "地下水污染垂向扩散模拟",
        "version": "1.0.0",
        "description": "模拟地下水污染物的垂向扩散过程",
        "simulation_ui": "/simulations/water-diffusion/",
        "api_docs": "/simulations/water-diffusion/docs"
    })
