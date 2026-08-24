# ADR-005: Interface gráfica com PySide6

- Status: Aceito
- Data: 2026-08-24

## Contexto

A aplicação precisava de uma interface desktop capaz de representar instâncias individualmente, manter controles responsivos durante a execução e expor configurações por instância.

## Decisão

Adotar PySide6 para a GUI. `MainWindow` compõe a aplicação e `Canvas` representa as instâncias por meio de linhas individuais, com estado, controle Agro, Ultimate, `cycle_delay` e remoção.

Referências: `src/mir4_auto_farm/app/window.py` e `src/mir4_auto_farm/features/canvas/canvas.py`.

## Consequências

A aplicação possui uma interface desktop integrada ao ciclo de vida das instâncias e pode atualizar o estado a partir da thread associada. A GUI passa a depender do runtime Qt e deve manter operações bloqueantes fora do event loop.
