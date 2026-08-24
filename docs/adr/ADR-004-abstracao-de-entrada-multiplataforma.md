# ADR-004: Abstração de entrada multiplataforma

- Status: Aceito
- Data: 2026-08-24

## Contexto

A automação precisa enviar comandos ao ambiente do jogo sem depender do mouse/teclado físico do usuário. Windows e Linux possuem mecanismos diferentes para descoberta de janelas e envio de input.

## Decisão

Manter `InputController` como contrato de infraestrutura e fornecer implementações específicas por plataforma. A lógica de `FarmCommands` depende dessa abstração, enquanto as implementações Windows e Linux encapsulam suas ferramentas e APIs locais.

Referências: `src/mir4_auto_farm/infrastructure/input` e `src/mir4_auto_farm/features/farm/commands.py`.

## Consequências

O farm permanece desacoplado do sistema operacional e pode executar sem mover o cursor do desktop. A implementação Linux, incluindo integração com `xdotool`, permanece disponível, mas sua evolução não é prioridade enquanto Windows for o ambiente principal.
