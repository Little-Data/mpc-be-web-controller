import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError

TARGET = 'http://127.0.0.1:13579'
PORT   = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class PlainCorsProxy(BaseHTTPRequestHandler):
    def do_GET(self):
        self._proxy('GET')

    def do_POST(self):
        self._proxy('POST')

    def _proxy(self, method):
        # 1. 拼装目标 URL
        url = TARGET + self.path
        body = None
        if method == 'POST':
            cl = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(cl)

        req = Request(url, data=body, method=method)
        # 2. 把浏览器原始头带过去
        for h in self.headers:
            if h.lower() not in ('host', 'content-length'):
                req.add_header(h, self.headers[h])

        # 3. 转发请求
        try:
            with urlopen(req) as res:
                code, headers, content = res.getcode(), res.headers, res.read()
        except HTTPError as e:
            code, headers, content = e.code, e.headers, e.read()

        # 4. 返回浏览器，顺手注入 CORS
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt, *args):
        # 可选：简化日志
        print(f"[{self.address_string()}] {fmt % args}")


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), PlainCorsProxy)
    print(f'MPC-BE CORS 代理已启动')
    print(f'端口为', PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nBye~')