import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8000
DATA_FILE = Path("reservas.json")


def load_reservas():
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_reservas(reservas):
    DATA_FILE.write_text(json.dumps(reservas, ensure_ascii=False, indent=2), encoding="utf-8")


def validar_data_horario(data, horario):
    try:
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        horario_obj = datetime.strptime(horario, "%H:%M")
    except ValueError:
        return False, "Data ou horário inválido."

    dia_semana = data_obj.weekday()  # segunda=0 ... domingo=6
    if dia_semana == 6:
        return False, "Reservas são permitidas apenas de segunda a sábado."

    if horario_obj.hour < 7 or horario_obj.hour > 21:
        return False, "Horário precisa estar entre 07:00 e 21:00."

    if horario_obj.minute != 0:
        return False, "Use horários em blocos de 1 hora (minutos 00)."

    return True, ""


def verificar_disponibilidade(reservas, sala, data, horario):
    valido, motivo = validar_data_horario(data, horario)
    if not valido:
        return False, motivo

    conflito = any(
        r["sala"] == sala and r["data"] == data and r["horario"] == horario for r in reservas
    )

    if conflito:
        return False, "Horário já ocupado para essa sala nesta data."

    return True, ""


class ReservationHandler(BaseHTTPRequestHandler):
    def _json_response(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _text_response(self, content, content_type="text/html; charset=utf-8", status=200):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        if self.path == "/":
            html = Path("index.html").read_text(encoding="utf-8")
            self._text_response(html)
            return

        if self.path == "/reservas":
            reservas = load_reservas()
            reservas_ordenadas = sorted(reservas, key=lambda r: (r["data"], r["horario"], r["sala"]))
            self._json_response(reservas_ordenadas)
            return

        self._json_response({"erro": "Rota não encontrada."}, status=404)

    def do_POST(self):
        if self.path not in ["/verificar", "/reservar"]:
            self._json_response({"erro": "Rota não encontrada."}, status=404)
            return

        payload = self._read_json()
        if payload is None:
            self._json_response({"erro": "JSON inválido."}, status=400)
            return

        sala = str(payload.get("sala", "")).strip()
        data = str(payload.get("data", "")).strip()
        horario = str(payload.get("horario", "")).strip()
        nome = str(payload.get("nome", "")).strip()

        if sala not in {"1", "2", "3", "4"}:
            self._json_response({"disponivel": False, "motivo": "Sala inválida."}, status=400)
            return

        reservas = load_reservas()
        disponivel, motivo = verificar_disponibilidade(reservas, sala, data, horario)

        if self.path == "/verificar":
            self._json_response({"disponivel": disponivel, "motivo": motivo})
            return

        if not nome:
            self._json_response({"erro": "Nome é obrigatório."}, status=400)
            return

        if not disponivel:
            self._json_response({"erro": motivo}, status=409)
            return

        reservas.append({"nome": nome, "sala": sala, "data": data, "horario": horario})
        save_reservas(reservas)
        self._json_response({"ok": True}, status=201)


if __name__ == "__main__":
    print(f"Servidor rodando em http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), ReservationHandler)
    server.serve_forever()
