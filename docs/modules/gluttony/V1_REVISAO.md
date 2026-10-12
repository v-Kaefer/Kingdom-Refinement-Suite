# Gluttony Rebalanced: revisão de estabilidade e fechamento da V1 (11 out 2026)

> **Status date:** 2026-10-11 | **Kind:** review | **Trust:** static evidence plus in-game runs of 10 Oct 2026 | **Game version:** 1.9.8

**V1 fechada por ora em 11 out 2026** (ver a seção "Fechamento da V1" no fim). Revisão estática, sem abrir o jogo, para decidir se dá para fechar uma V1 mesmo sem todas as comprovações no jogo. Veredito: **estável o bastante para fechar como V1-candidata**, com as ressalvas abaixo. Base das medições: `ANALISE_BASE.html` (seção 6 e "Medido no jogo"); módulo: `modules/krs_skipcost`; ferramenta de teste: `tools/harness/skipcost/`.

## O que sustenta a V1
- `check_docs`, `check_patch_names` (krs_items, krs_skipcost, krs_exploration) e `check_ownership`: 0 problemas; `tools/build_module.py krs_skipcost` constrói.
- O módulo empacotado e a cópia testada no jogo são o mesmo código (entidade e `.ent` idênticos byte a byte; o script de partida difere só pela linha de configuração do builder de teste, com os mesmos padrões).
- Quatro execuções no jogo 1.9.8 (as duas últimas com `krs_items`): nenhum erro de Lua do `KRS_SC`; só avisos do próprio jogo. Duas trocas de dono da entidade por sessão (menu e jogo), sem falha de criação.
- `tools/lua_api_check.py`: todas as chamadas do script existem no jogo; `RPG.DigestionSpeed` aparece como constante desconhecida mas funcionou (`prior rate_per_h=3.2813`).
- Comprovado no jogo: Wait de 3,991 h custou 9,534 e de 1,993 h custou 4,761 (taxa x horas x 0,75); a fome lida de volta bateu com o alvo; postura em pé, deitado, sentado, em pé ao abrir e cancelar a cama; o Wait logo depois foi cobrado a 75%.
- O desenho falha para o lado seguro: erro do script é capturado e logado uma vez, o jogo segue como o vanilla; sem taxa medida o custo é zero.

## Riscos conhecidos (R1 a R3 tratados em 11 out 2026, ver o fim desta seção)
| # | Risco | Efeito | Correção prevista |
|---|---|---|---|
| R1 | Quadros de 0,15 s ou mais contam como pulo (`LONG_FRAME_MIN`) | abaixo de cerca de 6 quadros por segundo o jogo normal seria cobrado como Wait (75% a mais por cima da fome normal) | confirmar ao fim do pulo que andou mais de 100 s de mundo por segundo real (`os.time`) antes de cobrar |
| R2 | A partida recria a entidade a cada evento de interface se o contador de quadros não andou, com limite de 40 na sessão (`KRS_SC_Spawns`) | se a entidade parar de atualizar com o jogo pausado, o limite acaba e o mod para depois de uma troca de nível | trocar o limite por um intervalo mínimo entre recriações (por exemplo 10 s) |
| R3 | Sem verificador de Lua nesta máquina | uma correção de R1 ou R2 não é conferida por sintaxe | executar uma vez o jogo (com backup dos saves) e ver o log sem `ERR` |

**Tratamento (11 out 2026, módulo 0.1.1).** Instalado o Lua 5.1 do pacote `lupa` num venv à parte (só para isto; nada no sistema). R1: um pulo só conta se o relógio andou 100 s de mundo ou mais por segundo real (jogo normal anda 15). R2: recriação no máximo a cada 10 s, sem o limite de 40 (que só vale sem `os.time`). R3: `tools/harness/skipcost/test_skipcost.py` carrega os dois scripts com um jogo falso e roda 33 verificações, todas passando: sintaxe, taxa medida, Wait, sono, sentado, vigor subindo, jogo lento a 5 quadros por segundo, Wait depois de jogo lento, carga de save, engasgo, sem `os.time`, intervalo de recriação e troca de dono da entidade. Desligando o R1 de propósito o teste do jogo lento falha, então ele pega o defeito. A simulação prova a lógica e a sintaxe, não que o motor se comporte como o jogo falso; as duas mudanças não foram rodadas no jogo real.

## Decisões de balanceamento
Respostas do autor em 11 out 2026:
- **Fome em zero por pulo:** avisar o jogador (mensagem na tela depois do pulo, módulo 0.1.2), sem piso. O diálogo de Wait e de sono prevê a fome como se o pulo não custasse nada, então a mensagem diz o custo e se o jogador ficou com fome ou em inanição. Falta ver no jogo se o texto aparece (é texto simples, sem chave de localização).
- **Demanda diária:** manter a taxa do KRS Items (cerca de 65 pontos por dia, perto de 4.500 kcal pela mediana de 69 kcal por unidade; o consumo realista é 3.200 a 3.800 kcal).
- **Leitura longa: mantida** (11 out 2026). Com os livros do KRS Items em 10 a 25 h, um livro de 25 h custa cerca de 41 pontos a 50% (3,28 por hora x 25 x 0,5): quase meia barra por livro; o jogador é avisado pela mensagem.
- **Sentado = 50%:** confirmado (cobre ler num banco e também esperar numa cadeira; `--sit 0.75` o iguala ao Wait).

Em aberto:
- **Limites do que foi testado.** Sem teste com o mod: dormir de verdade, Wait sentado, ler livro, desmaiar, e as mensagens "(you are hungry)" e "(starving)".

## Execução no jogo (11 out 2026, módulo 0.1.3)
A primeira execução com as mudanças 0.1.x achou **dois defeitos que a simulação não pegou**, ambos corrigidos na 0.1.3:
1. O limiar do R1 (100 s de mundo por segundo real) era apertado: um Wait de 1 h levou uns 25 s num PC ocupado e foi descartado, sem cobrança. Agora 40 (jogo normal, mesmo a 5 quadros por segundo, anda 15), e o descarte é logado.
2. O intervalo de 10 s do R2 fazia a partida perder os eventos de interface logo depois de carregar um save, e não havia entidade no jogo. O intervalo saiu; o limite é 500 criações e as cópias extras se removem quando uma está trabalhando.
Depois da correção, no jogo 1.9.8 com `krs_items`: a entidade assume depois da carga, a taxa acordado foi medida (3,1848 por hora), um Wait em pé de 2,993 h custou 7,148 (taxa x horas x 0,75), a fome foi de 59,16 a 52,01 e **a mensagem "Waited 3.0 h: hunger -7" apareceu na tela** como notificação (o jogo a desenha em maiúsculas). Os saves foram copiados antes e comparados por hash depois: nenhuma diferença. Lição: a simulação prova a lógica, mas não o tempo dos eventos do motor; uma mudança no módulo precisa de uma execução curta no jogo.

## Fronteiras do pacote
- O `krs_items` ainda leva os livros (56 linhas de `document` e `ReadingXpPerHour`) e a poção de Aesop; pela divisão, livros são do Leech & Lore Reworked e poções do Realistic Potions. Enquanto não forem movidos, o Gluttony V1 os traz junto.
- Fora da V1 por não estarem decididos: apodrecimento por classe, nutrição e refresco, lanches (2011), serviços (1105).
- Conteúdo da V1: digestão x2,25 e efeitos de inanição (`krs_items`) e o custo de pular tempo (`krs_skipcost`).

## Para fechar a V1 "sólida"
1. ~~Decidir as questões de balanceamento~~ (todas respondidas em 11 out 2026).
2. ~~Aplicar R1 e R2~~ (feito, 0.1.1).
3. ~~Uma execução no jogo réplica~~ (feita em 11 out 2026, com backup e comparação por hash sem diferença; ver abaixo).
4. Opcional: dormir de verdade com o mod (grava um autosave e o jogo apaga o autosave mais antigo).

## Fechamento da V1 (11 out 2026)
Fechada por decisão do autor, "por enquanto": é uma V1 de partida, não a versão completa do pacote.

**O que a V1 contém**
| Peça | Módulo e versão | O que faz |
|---|---|---|
| Digestão e inanição | `krs_items` 2.0.0 | `DigestionSpeed` 0,000578704 -> 0,001302084 (x2,25); `StarvationPlayerEffectMinMin` 90 -> 95, `MaxMax` 75 -> 65, `MinMax` 45 -> 25 |
| Custo de pular tempo | `krs_skipcost` 0.1.3 | depois de Wait, sono, leitura ou desmaio, cobra fome = taxa acordado x horas x fator por postura (em pé 75%, sentado 50%, deitado 50%) e avisa o jogador na tela |

O `krs_items` ainda carrega, fora do escopo do pacote, os 56 livros, `ReadingXpPerHour` e a poção de Aesop (de Leech & Lore e Realistic Potions); as camas melhores ficam fora (guardadas em `krs_exploration/src/held/`) para o sono continuar como no jogo.

**Decisões do autor que a V1 fixa:** dia de 96 minutos (razão 15) e sono intocado; taxa de fome do KRS Items mantida; sentado 50%; sem piso para o custo, com aviso ao jogador; leitura longa mantida.

**Evidência:** `check_docs`, `check_patch_names` e `check_ownership` em 0 problemas; 36 verificações de simulação em Lua 5.1; execução no jogo 1.9.8 (saves copiados antes e comparados por hash depois, sem diferença): Wait em pé cobrado certo e mensagem na tela. Detalhes na seção "Execução no jogo".

**Fora da V1 (backlog para a V1.1 ou depois)**
- Sem teste no jogo com o módulo: dormir de verdade, Wait sentado, ler livro, desmaiar, as mensagens "(you are hungry)" e "(starving)". Dormir grava um autosave e o jogo apaga o mais antigo.
- Apodrecimento por classe de alimento (22 classes, valor escolhido vazio), nutrição e refresco, lanches com buffs (2011), serviços e banho (1105).
- Mover os livros e a poção de Aesop do `krs_items` para os pacotes Leech & Lore Reworked e Realistic Potions.
- Mensagem só em inglês (texto simples com números); chaves de tradução se for preciso.
- Opcional: piso para o custo, `--sit 0.75`, ajustes da taxa diária (cerca de 65 pontos por dia).
- O id técnico do pacote ainda não existe; os ids dos módulos não foram renomeados.
- Antes de qualquer mudança no `krs_skipcost`: simulação (`tools/harness/skipcost/test_skipcost.py`) e uma execução curta no jogo.
