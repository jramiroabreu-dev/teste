# Reserva de Salas

Sistema de reserva de 4 salas com visual de calendário/planilha por sala e bloqueio de conflitos de horário.

## Regras

- Salas disponíveis: 1, 2, 3 e 4.
- Reservas apenas de segunda a sábado.
- Horários permitidos: 07:00 até 21:00.
- Horários em blocos de 1 hora (minutos `00`).
- Não permite reservar a mesma sala na mesma data e horário.
- Cada reserva exige valor (`R$`) maior que zero.

## Como executar

```bash
python3 server.py
```

Acesse: http://localhost:8000

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

- `GET /reservas`: lista todas as reservas ordenadas.
- `GET /calendario`: devolve reservas organizadas por sala.
- `POST /verificar`: verifica se sala/data/horário está disponível.
- `POST /reservar`: registra uma nova reserva com valor.
