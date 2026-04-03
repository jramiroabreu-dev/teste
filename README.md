# Reserva de Salas

Sistema simples de reserva de 4 salas, com front-end em HTML e back-end em Python (sem dependências externas).

## Regras

- Salas disponíveis: 1, 2, 3 e 4.
- Reservas apenas de segunda a sábado.
- Horários permitidos: 07:00 até 21:00.
- Horários em blocos de 1 hora (minutos `00`).
- Não permite reservar a mesma sala na mesma data e horário.

## Como executar

```bash
python3 server.py
```

Acesse no navegador:

- http://localhost:8000

## Endpoints

- `GET /reservas`: lista todas as reservas.
- `POST /verificar`: verifica se sala/data/horário está disponível.
- `POST /reservar`: registra uma nova reserva.
