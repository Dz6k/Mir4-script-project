# Mir4 Auto Farm


ATUALIZAÇÕES

Versão 3.0.170824:

    1 - Alterada levemente a interface
    2 - União das 2 interfaces/modos
    3 - Correção/Mudança na maneira de atualizacao do script 
        3.1 Agora voce nao é "obrigado" a atualizar, ficou facultativo e mais simples a atualização
    4 - Mudança na maneira de encontrar processos e inicia-los
        4.1 Antes para o modo manual, para aplicativos com índice maior que 9 (10 em diante)
        4.2 Aumentada a velocidade da ativação do script: agora a cada instancia que ele acha, ele ja inicia na hora // Antes ele procurava todas e apos procurar por um numero X de vezes, ele iniciava as instânscias, agora ele inicia a partir do momento que encontra a aplicação
        4.3 Agora enquanto ele procura as instânscias abertas para iniciar o script, ele nao fica com a interface travada.
    5 - Remoção de opções: 
        5.1 Modo Simples
        5.2 Modo Safe
        - Motivo: Não estão otimizados e são redundantes, parecem muito mais funções para "encher linguiça" do que funções que de fato acrescentam alguma funcionalidade.
    
    OBS: Funcionalidades como teleporte e script de mineração estão, indeterminadamente, fora de questão por limitações da linguagem.
    -> limitações como: Enviar clicks em coordenadas diretamente sem que bloqueie o uso do mouse do usuario, sobre o script de mineração, ele até é viável mas será bem longo, alem de implementar IA no reconhecimento de imágem eu preciso ainda pegar muitos pontos no mapa para me locomover e com python e sem acessar diretamente a memoria do jogo, fica como uma movimentacao cega, posso ate me movimentar mas 100% de certeza que vou ate o ponto especifíco. 

Versão 2.2:

    1 - Arrumado o seletor de indices Mir4: antes ele funcionava corretamente ate Mir4[9] no modo seletor
    
Versão 2.1:

    1 - Modo Simples com verificação de morte agora funciona em segundo plano;
    2 - Mudança na função do click, agora está mais realista.

Versão 2.0:

    1 - Adicionado outra interface gráfica que tem a possibilidade de você escolher qual ou quais janelas voce quer que o script seja executado e ainda podendo escolher o tempo de mudança de alvo;
    2 - Bug encontrado não resolvido(ainda):
        2.1 O reconhecimento de imagem de quando você esta morrendo ou sendo atacado ta dando conflito com algumas skils de exposão dando TP em falsos positivos;
        2.2 Mal otimização nas funções "Safe".
    3 - Atualizações no funcionamento das funções;
    4 - Alteração do icone;
    5 - Criação de um ambiente virtual venv;
    6 - Criação de uma nova função:
        6.1 Funções "Stops" para parar o script sem a necessidade de apertar a hotkey "CTRL+E", podendo ser executado e "pausado" quando bem quiser;
    7 - Mudança do limite de procura de processos "Mir4G[]" para até 15 instâncias.

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


Thanks for using, improving or looking at my code! 
