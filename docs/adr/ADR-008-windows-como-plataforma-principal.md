# ADR-008: Windows como plataforma principal

- Status: Aceito
- Data: 2026-08-24

## Contexto

O projeto mantém implementações para Linux, mas o desenvolvimento, os testes manuais, a GUI e a distribuição atuais estão concentrados em Windows.

## Decisão

Priorizar Windows como ambiente principal sem remover o suporte Linux existente. Dependências específicas de Windows, como `pywin32`, permanecem condicionadas à plataforma no `pyproject.toml`.

Referências: `src/mir4_auto_farm/infrastructure`, `tests/windows`, `tests/linux` e `pyproject.toml`.

## Consequências

A entrega principal pode ser validada e distribuída de forma consistente para Windows, enquanto a separação por implementações preserva a possibilidade de retomar Linux. A cobertura e a experiência entre plataformas podem permanecer assimétricas.
