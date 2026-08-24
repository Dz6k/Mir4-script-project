# ADR-006: Configuração individual de cycle_delay

- Status: Aceito
- Data: 2026-08-24

## Contexto

Instâncias diferentes podem exigir intervalos distintos entre ciclos. Tratar o delay como configuração global impediria esse ajuste independente.

## Decisão

Armazenar `cycle_delay` em cada `FarmInstance`, expô-lo por propriedade e sincronizá-lo com o worker atual. A GUI valida valores não negativos e aplica a alteração ao confirmar o campo.

Referências: `src/mir4_auto_farm/features/instance/farm.py` e `src/mir4_auto_farm/features/canvas/canvas.py`.

## Consequências

Cada instância pode operar com seu próprio intervalo e a configuração é preservada quando o worker é recriado. Valores inválidos não alteram a configuração vigente.
