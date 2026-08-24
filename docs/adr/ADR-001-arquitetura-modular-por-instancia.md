# ADR-001: Arquitetura modular por instância

- Status: Aceito
- Data: 2026-08-24

## Contexto

A aplicação evoluiu de uma organização concentrada em scripts para uma aplicação Python com GUI, execução de farm e infraestrutura de entrada. A concentração dessas responsabilidades dificultava a evolução independente e o controle de múltiplas instâncias do MIR4.

## Decisão

Organizar o sistema em módulos de aplicação, features e infraestrutura, tendo `FarmInstance` como unidade principal de execução. O fluxo adotado é:

`GUI -> FarmManager -> FarmInstance -> FarmWorker -> FarmCommands -> InputController`

A GUI interage com as abstrações de instância e gerenciamento, sem controlar diretamente os detalhes do worker ou do mecanismo de input.

Referências: `src/mir4_auto_farm/app`, `src/mir4_auto_farm/features` e `src/mir4_auto_farm/infrastructure`.

## Consequências

A lógica de negócio, a apresentação e a infraestrutura podem evoluir com menor acoplamento. Cada instância possui um ciclo de vida próprio e a estrutura fica preparada para execução concorrente. Em contrapartida, a aplicação passa a ter mais módulos e contratos internos a manter.
