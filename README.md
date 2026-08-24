# MIR4 Auto Farm

Aplicação desktop em Python para automatizar ciclos de farm do MIR4 em múltiplas instâncias, com interface PySide6 e execução concorrente por instância.

## Visão geral

O projeto separa a interface gráfica, o gerenciamento das instâncias, a execução do farm, os comandos de automação e a infraestrutura de entrada. A automação envia comandos à janela configurada sem depender do uso real do mouse/teclado do sistema.

O fluxo principal é:

`GUI -> FarmManager -> FarmInstance -> FarmWorker -> FarmCommands -> InputController`

Cada instância mantém seu próprio estado de execução, configuração de Ultimate e `cycle_delay`. A aplicação pode executar várias instâncias simultaneamente sem bloquear a interface.

## Funcionalidades

- Interface desktop com PySide6
- Criação de instâncias a partir dos índices informados
- Execução e parada individual de cada instância
- Execução concorrente usando threads daemon
- Controle individual de Ultimate
- `cycle_delay` configurável por instância
- Parada de todas as instâncias
- Implementações de input para Windows e Linux
- Remoção individual de instâncias
- Testes unitários e testes específicos por plataforma
- Empacotamento como executável Windows com PyInstaller

## Arquitetura

- `src/mir4_auto_farm/main.py`: ponto de entrada da aplicação
- `src/mir4_auto_farm/app/window.py`: janela principal e controles de criação
- `src/mir4_auto_farm/features/canvas`: representação visual das instâncias
- `src/mir4_auto_farm/features/instance`: modelo e ciclo de vida de `FarmInstance`
- `src/mir4_auto_farm/features/manager`: coordenação das instâncias
- `src/mir4_auto_farm/features/farm`: comandos e worker do farm
- `src/mir4_auto_farm/infrastructure/input`: abstrações e implementações de entrada
- `src/mir4_auto_farm/infrastructure/window`: descoberta e controle de janelas

As decisões estruturais estão registradas em [docs/adr](docs/adr):

- [ADR-001: Arquitetura modular por instância](docs/adr/ADR-001-arquitetura-modular-por-instancia.md)
- [ADR-002: Ciclo de vida e concorrência por instância](docs/adr/ADR-002-ciclo-de-vida-e-concorrencia-por-instancia.md)
- [ADR-003: Coordenação das instâncias com FarmManager](docs/adr/ADR-003-coordenacao-com-farm-manager.md)
- [ADR-004: Abstração de entrada multiplataforma](docs/adr/ADR-004-abstracao-de-entrada-multiplataforma.md)
- [ADR-005: Interface gráfica com PySide6](docs/adr/ADR-005-interface-grafica-com-pyside6.md)
- [ADR-006: Configuração individual de cycle_delay](docs/adr/ADR-006-cycle-delay-individual-por-instancia.md)
- [ADR-007: Estratégia de testes e validação](docs/adr/ADR-007-estrategia-de-testes-e-validacao.md)
- [ADR-008: Windows como plataforma principal](docs/adr/ADR-008-windows-como-plataforma-principal.md)
- [ADR-009: Distribuição Windows com PyInstaller](docs/adr/ADR-009-distribuicao-com-pyinstaller.md)
- [ADR-010: Regras de escrita para ADRs do projeto](docs/adr/ADR-010-regras-de-escrita-para-adrs-do-projeto.md)

## Requisitos

- Python 3.11 ou superior
- [uv](https://docs.astral.sh/uv/)
- Windows para a execução principal
- Dependências de input compatíveis com a plataforma utilizada

## Execução com uv

Instale as dependências e execute a aplicação pelo entry point registrado no projeto:

```bash
uv sync
uv run mir4_auto_farm
```

Na janela da aplicação, informe os índices das instâncias, separados por vírgula ou espaço, e o delay de ciclo. Cada instância criada começa sua execução de forma independente.

## Testes e qualidade

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Os testes estão organizados em `tests/unit`, `tests/windows` e `tests/linux`. A integração Linux depende do ambiente gráfico e de ferramentas disponíveis no sistema, como `xdotool`.

## Build Windows

O comando de referência para gerar o executável é:

```bash
uv run -- python -m PyInstaller --paths src --name MIR4AutoFarm --windowed --onefile src/mir4_auto_farm/main.py
```

O executável final será gerado em `dist/MIR4AutoFarm.exe`. O diretório `build` contém artefatos intermediários e não é o destino do executável distribuível.

## Estado do projeto

O refactor estrutural foi encerrado com a arquitetura modular, o gerenciamento individual de instâncias, a execução concorrente e o fluxo de build Windows estabelecidos. Novas alterações estruturais devem ser motivadas por uma necessidade concreta do produto.

## Licença

Este projeto é livre para uso, adaptação e experimentação.
