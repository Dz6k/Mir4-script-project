# Mir4 Auto Farm

Testado apenas para classes ranged e em resolução 1080p, ela de padrão vem com comando de ultar sempre que possível!
Em breve farei demais melhorias e/ou modificações.

!!!!!!
Algumas atualizações irão ser adiadas para a criação de uma versão demo e uma outra vesão paga, para isso, iniciarei a criação de uma interface gráfica amigável e a separação de algunas funções. Agradeço sua paciência,
At.te Dz6k.
!!!!!!

ATUALIZAÇÕES

Versão 1.13:

    1 - Mudança no início do código:
        1.1 Antes ele clicava em uma coordenada x,y que deveria ser coencidente à tela do jogo, agora ele mesmo busca o processo mir4G[1] e ja "seleciona" sem que você precise deixar ele em um canto específico da tela (é altamente recomendado que use em tela cheia na metade direita do seu monitor);
        1.2 Este comando serve ÚNICA e EXCLUSIVAMENTE para o processo de jogo 1 do Mir4(que será sempre a primeira tela do mir4 que tu vai executar).
    2 - Adicionada uma nova automação com possíveis grandes melhorias e implementaçoes de novas funções futuras:
        2.1 Agora você irá inicar o código e responder uma pergunta de qual é a instância do jogo(qual número do jogo), este número você consegue ver no nome da janela do mir4(vai estar semelhante a: "Mir4G[1]);
        2.2 Agora você pode utilizar normalmente seu computador e até deixar o jogo minimizado que o código irá continuar rodando.
        2.3 Esta nova funcao é simples e direta, apenas farmar de maneira "stealth". Nesta função não tem como saber se você morreu como no executável farm.py, use-a sabendo que poderá morrer e ficar afk dando "tiros ao ar" na base.


Versão 1.12.1:

    1 - Corrigida a linha de código de reconhecimento de imagem na detecção se o alt estiver morto.

Versão 1.12:

    1 - Atualizado o verificador de morte.
    2 - Atualizada a variável de ultimate.
        2.1 Para usar ultimate durante o farm, deixe "ultimate = True" e para nao usar ultimate durante o farm deixe "ultimate = False".


Versão 1.11:

    1 - Corrigido alguns erros gramaticais.
    2 - Implemementados comentários em inglês para caso alguém queira aprimorar o código.
    3 - Deixando mais amigável e retornando informação da hora em que morreu.


versão 1.1:

    1 - Adicionado um verificador caso o player esteja morto.
    2 - Removido do código a funcao auto_farm() e substituindo apenas por um loop while.
    3 - Para esta função funcionar, tem alguns requisitos:
        Local de recolha de energia no "Bosques Fantasmas"da "Área do Centro Espiritual" tem que estar marcadocomo a última area "favoritada" e a janela do mir4"completa" na segunda metade do monitor(ladoesquerdo do monitor) (win+rightkey).
    4 - Adicionados alguns arquivos .png com a finalidade de cooperar para o reconhecimento de imagem! Não alterar, apagar ou trocar caso não tenha conhecimendo de como funciona.


OBS: Todos os testes e modificações são visando uma resolução 1920x1080. Qualquer teste em outra resolução ocasionará erro caso nao altere as coordenadas.

Thanks for using, improving or looking at my code! 