# ADR-002: Ciclo de vida e concorrência por instância

- Status: Aceito
- Data: 2026-08-24

## Contexto

A execução direta do worker poderia bloquear a interface e não permitia operar várias instâncias simultaneamente. O farm também precisava ser interrompido sem aguardar passivamente delays longos.

## Decisão

Cada `FarmInstance` cria uma `threading.Thread` daemon para executar seu `FarmWorker`. O worker usa `threading.Event` como sinal de parada e também durante as esperas. `start` recria o worker com as configurações atuais, e `stop` sinaliza a parada e aguarda a thread por até um segundo.

Referências: `src/mir4_auto_farm/features/instance/farm.py` e `src/mir4_auto_farm/features/farm/worker.py`.

## Consequências

A GUI permanece responsiva e instâncias podem executar e parar de forma independente. O uso de `Thread` e `Event` mantém a solução pequena, mas exige cuidado com o ciclo de vida das threads e não substitui um modelo de cancelamento mais sofisticado caso a concorrência cresça.
