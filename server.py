from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from pathlib import Path
import mimetypes


class MyServer(BaseHTTPRequestHandler):
    BASE_DIR = Path(__file__).parent

    def do_GET(self):
        """Обработка GET-запросов для разных типов файлов"""
        # Определяем путь к файлу
        if self.path == '/' or self.path == '/index.html':
            file_path = self.BASE_DIR / 'index.html'
        else:
            file_path = self.BASE_DIR / self.path[1:]  # Убираем первый /

        # Проверяем существование файла
        if not file_path.exists():
            self.send_error(404, "File not found")
            return

        # Определяем MIME-тип
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Отправляем успешный ответ
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()

        # Читаем и отправляем файл
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())


def run_server():
    hostName = "localhost"
    serverPort = 8080

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    print("Available pages:")
    print("- http://localhost:8080/")
    print("- http://localhost:8080/catalog.html")
    print("- http://localhost:8080/contacts.html")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    run_server()