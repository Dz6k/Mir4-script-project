# ADR-007: Estratégia de testes e validação

- Status: Aceito
- Data: 2026-08-24

## Contexto

O refactor alterou a organização interna, o ciclo de vida das instâncias, a infraestrutura de input e a GUI. Era necessário preservar o comportamento do farm e detectar regressões sem depender apenas de testes manuais.

## Decisão

Manter testes unitários e testes específicos por plataforma com `pytest`, cobrindo workers, instâncias, manager, input e descoberta de janelas. Usar Ruff e mypy como verificações complementares e validar manualmente a GUI e o executável empacotado quando houver alterações nessas áreas.

Referências: `tests/unit`, `tests/windows`, `tests/linux` e `pyproject.toml`.

## Consequências

O refactor pode evoluir com uma rede de segurança automatizada e as diferenças de plataforma permanecem explícitas. Integrações externas, como `xdotool`, ainda podem falhar por limitações do ambiente gráfico e exigem validação no sistema correspondente.
