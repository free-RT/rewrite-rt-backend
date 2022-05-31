from sanic import Blueprint, response
from sanic_mysql import cursor


bp = Blueprint("api_STATUS", url_prefix="/api")


@bp.get("/status")
@cursor()
async def status(request, conn, cur):
    await cur.execute("SELECT * FROM status")
    cpus = []
    disks = []
    labels = []
    memorys = []
    pings = []
    servers = []
    users = []
    for cpu, disk, label, memory, ping, server, user in await cur.fetchall():
        cpus.append(cpu)
        disks.append(disk)
        labels.append(label)
        memorys.append(memory)
        pings.append(ping)
        servers.append(server)
        users.append(user)
    return response.json(
        {
            "cpu": cpus,
            "disk": disks,
            "labels": labels,
            "memory": memorys,
            "ping": pings,
            "server": servers,
            "user": users
        }
    )