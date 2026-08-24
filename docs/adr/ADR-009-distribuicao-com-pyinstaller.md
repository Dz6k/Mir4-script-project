# ADR-009: Distribuição Windows com PyInstaller

- Status: Aceito
- Data: 2026-08-24

## Contexto

A aplicação desktop precisa ser executável fora do ambiente de desenvolvimento, sem exigir que o usuário final instale o pacote Python e suas dependências.

## Decisão

Usar PyInstaller para gerar um executável Windows em arquivo único e sem console, com `src/mir4_auto_farm/main.py` como entrada e `src` no caminho de análise. O comando de referência é:

```bash
uv run -- python -m PyInstaller --paths src --name MIR4AutoFarm --windowed --onefile src/mir4_auto_farm/main.py
```

Os artefatos intermediários ficam em `build` e o executável final esperado é `dist/MIR4AutoFarm.exe`. Esses diretórios permanecem ignorados pelo Git.

Referências: `pyproject.toml`, `MIR4AutoFarm.spec` e `src/mir4_auto_farm/main.py`.

## Consequências

A aplicação pode ser distribuída como um executável único e o entry point `mir4_auto_farm` continua disponível para desenvolvimento. O build depende do ambiente Windows e gera artefatos que precisam ser validados antes de uma versão distribuível.
