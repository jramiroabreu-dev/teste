# Reserva de Salas

Sistema de reserva de 4 salas com visual de calendário/planilha por sala e bloqueio de conflitos de horário.

## Regras

- Salas disponíveis: 1, 2, 3 e 4.
- Reservas apenas de segunda a sábado.
- Horários permitidos: 07:00 até 21:00.
- Horários em blocos de 1 hora (minutos `00`).
- Não permite reservar a mesma sala na mesma data e horário.
- Cada reserva exige valor (`R$`) maior que zero.

## Como executar localmente

```bash
python3 server.py
```

Acesse localmente: http://localhost:8000

## Acesso pela internet (link público)

Este projeto já está preparado para deploy com internet:

- `render.yaml` (deploy no Render)
- `Procfile` (compatível com plataformas PaaS)
- Suporte à porta dinâmica via variável `PORT` no `server.py`
- Endpoint de health check: `GET /health`

### Deploy rápido no Render

1. Suba este repositório para o GitHub.
2. No Render, clique em **New +** → **Blueprint**.
3. Selecione o repositório.
4. O Render usa o `render.yaml` automaticamente.
5. Após o deploy, você recebe um link público, por exemplo:
   - `https://reserva-salas.onrender.com`

## Organização visual

- A tela mostra um calendário/planilha separado para cada sala.
- Cada sala exibe Data, Hora, Nome e Valor.
- O total arrecadado por sala é mostrado no final do quadro.

## Arquivos de planilha gerados

Ao salvar reservas, o servidor exporta automaticamente:

- `reservas_planilha.csv` (todas as salas)
- `sala_1_calendario.csv`
- `sala_2_calendario.csv`
- `sala_3_calendario.csv`
- `sala_4_calendario.csv`

## Endpoints

- `GET /health`: health check para deploy.
- `GET /reservas`: lista todas as reservas ordenadas.
- `GET /calendario`: devolve reservas organizadas por sala.
- `POST /verificar`: verifica se sala/data/horário está disponível.
- `POST /reservar`: registra uma nova reserva com valor.
