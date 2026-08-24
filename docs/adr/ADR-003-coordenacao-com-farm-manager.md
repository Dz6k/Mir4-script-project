# ADR-003: Coordenação das instâncias com FarmManager

- Status: Aceito
- Data: 2026-08-24

## Contexto

A interface precisava adicionar, iniciar, parar e remover instâncias sem assumir a implementação do ciclo de execução de cada farm.

## Decisão

Adotar `FarmManager` como coordenador das `FarmInstance`. O manager mantém um dicionário indexado pelo título da instância e oferece operações para adicionar, iniciar, parar, remover e parar todas as instâncias.

Referências: `src/mir4_auto_farm/features/manager/farm_manager.py` e `src/mir4_auto_farm/app/window.py`.

## Consequências

O gerenciamento central reduz a responsabilidade da GUI e permite parar todas as instâncias em uma única operação. O título da `Instance` passa a ser a identidade usada pelo manager, portanto deve ser único dentro da aplicação.
