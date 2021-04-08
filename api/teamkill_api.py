from aiohttp.server import Sever
from functions.teamkill_leaderboard import main


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(
            str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).encode())
        return
