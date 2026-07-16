from fastapi import FastAPI
from fastapi_mcp import FastApiMCP 
from app.routers import v1_media, v1_payment, v1_rbac, v1_student,v1_auth,v1_staff
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ERP Staff & Student Management API",
    description="A secure and comprehensive set of JWT-authenticated APIs for managing student and staff records.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_student.router, tags=["Student Management Version 1"])
app.include_router(v1_media.router, tags=["Student Media Creation Version 1"])
app.include_router(v1_rbac.router, tags=["Student and Staff RBAC Login Version 1"])
app.include_router(v1_payment.router, tags=["Student Online Payment Version 1"])
app.include_router(v1_auth.router, tags=["Student and Staff RBAC Login Version 1"])
app.include_router(v1_staff.router, tags=["Staff Management Version 1"])



# ------------------ MCP Mount ------------------
#mcp = FastApiMCP(app)
#mcp.mount_http()   # mounts MCP at /mcp


mcp = FastApiMCP(app)
mcp.mount_http(mount_path='/coreapi/mcp')
