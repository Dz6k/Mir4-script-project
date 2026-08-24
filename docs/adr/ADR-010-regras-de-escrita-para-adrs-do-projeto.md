# ADR-010: Regras de escrita para ADRs do projeto

- Status: Aceito
- Data: 2026-08-24

## Contexto

O projeto utiliza ADRs como documentação técnica de mudanças, e não como tutoriais. É essencial que cada novo registro siga um padrão consistente para permitir a compreensão rápida da decisão, da motivação e da sua relação com a arquitetura existente.

## Decisão

Adotar as seguintes regras para a escrita de ADRs neste repositório:

- O nome do arquivo deve ser numerado e descritivo, usando hífens no lugar de caracteres incompatíveis com o sistema de arquivos. O documento deve conter um título no formato `ADR-XXX: Descrição da decisão`.
- O documento deve começar com um único título em `#`.
- Usar apenas os cabeçalhos `##` para as seções principais: `Contexto`, `Decisão` e `Consequências`.
- Usar `###` somente para subtópicos dentro dessas seções, quando necessário.
- Evitar `####` ou níveis adicionais em ADRs normais. Exceções devem ser justificadas por uma necessidade documental específica.
- Registrar informações técnicas de mudança e motivação, evitando linguagem de tutorial ou descrição passo a passo do fluxo de usuário.
- Incluir, quando apropriado, referências a arquivos implementados, commits relevantes e outras ADRs relacionadas.
- Manter o texto conciso e orientado a decisão, respondendo principalmente: por quê, o que mudou e qual foi o impacto.

A `ADR-010` também deve ser usada como referência para revisar ADRs existentes que não sigam esse padrão, especialmente quando forem atualizadas ou quando uma decisão arquitetural relacionada for registrada.

## Consequências

A leitura das ADRs fica mais rápida e previsível, e as decisões passam a ter maior rastreabilidade com a implementação. Novos documentos terão uma estrutura consistente, reduzindo divergências de estilo e facilitando a manutenção da documentação. ADRs antigas podem precisar de normalização quando forem revisadas.
