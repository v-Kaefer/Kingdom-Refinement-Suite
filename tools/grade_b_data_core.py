"""
grade_b_data_core.py - curated text of the Grade B review (Portuguese): sub-categories, rankings, feature tables, glossary, questions and the
hand-written intersection notes. Machine-derived facts (files, rows, values, overlaps) are NOT here: they come from grade_b_files.csv,
grade_b_cells.csv, grade_b_text.csv, grade_b_newrows.json and grade_b_scripts.json, written by tools/grade_b_extract.py.

Markup in the strings: `code`, **bold**, and the confidence marks ^c (confirmado: lido nos arquivos, no jogo ou no log), ^d (deduzido), ^n (nao verificado).
"""

STATUS = "Primeira passada concluída (só leitura); aguarda decisão do autor"

# (id, name, blurb, [mod ids])
SUBCATS = [
    ("food", "Comida, bebida e apodrecimento", "Quatro mods que mexem na tabela `food` (e, o 2011, em todo um sistema de buffs): quanto tempo a comida dura, quanto ela alimenta e se ela dá efeitos. É o grupo com mais choque de valores: três deles escrevem nas mesmas linhas.", ["1483", "1639", "2011", "2345"]),
    ("perks", "Perks: a linha Perkaholic", "Três empacotamentos do mesmo mod (Xylozi, 2018): as mesmas 56 perks e os mesmos 56 buffs, em versões de 2018 (tabela inteira), 2019 (tabela inteira) e 2024 (patch PTF). São alternativas estritas: só uma pode valer.", ["1009", "770", "85"]),
    ("combat", "Combate: ritmo da IA, bloqueio e vigor", "Três mods que reescrevem os parâmetros `CombatAuto*` (a IA dos inimigos), as janelas de bloqueio perfeito e a economia de vigor. Os dois menores (1112 e 1384) compartilham 130 linhas idênticas de bloqueio perfeito.", ["2179", "1384", "1112"]),
    ("weapons", "Armas e munição: estatísticas", "Dois mods de armas: as armas de haste (2045) e o arco, flechas e alcance (2035). Não mexem nas mesmas linhas; ambos mexem em `pickable_item` (preço e peso).", ["2045", "2035"]),
    ("equipment", "Equipamento: conteúdo, manutenção e visual", "Roupas e armaduras novas (1380, 2209), a economia do reparo (2173) e o cabelo dos cavalos (2343). Sem concorrência direta entre si; todos acrescentam entradas em lojas ou substituem arquivos de interface.", ["2173", "1380", "2209", "2343"]),
    ("economy", "Economia de serviços e acampamento", "Preços de serviços (banho, quarto, treinador, cavalo) e um sistema de acampamento com itens novos, perks de local e entidades criadas por script.", ["1105", "1062"]),
    ("rules", "Regras globais: o pacote de parâmetros", "Um único mod, mas o que mais parâmetros globais troca (101 linhas de `rpg_param`, 16 sobrescritas do modo Hardcore, 40 linhas de XP de livros). Cruza com os três do grupo de combate.", ["1558"]),
    ("lua", "Auxiliares de interface e de script (Lua)", "Dois mods sem tabela alguma: um mostra combos na tela, o outro liga estoques e cavalo à mesa de alquimia. Ambos trazem script grande e arquivos de interface ou comandos de console.", ["2318", "2323"]),
]

# subcategory -> [(mod id, position, why)]
RANK = {
    "food": [
        ("1483", 1, "O mais limpo: um único arquivo de tabela por opção (2X, 3X, 5X), 111 linhas completas, sufixo igual ao id, leia-me claro, nenhuma coluna fora do lugar. Faz uma coisa só (tempo de apodrecimento) e a faz sem erro. ^c"),
        ("2011", 2, "O mais ambicioso e o único que cria um sistema novo (42 buffs de lanche em 9 classes novas, 38 itens ligados a eles, 94 textos alterados). Perde posição por erros reais: o atributo `decay_ime_hours` (digitado errado), o cabeçalho `Weight` com W maiúsculo, matérias-primas e linguiça com apodrecimento 0 (nunca apodrecem), e mexer em itens de teste e poções que nada têm a ver com comida. ^c"),
        ("2345", 3, "Tabela inteira sem sufixo (substitui `food` e desfaz qualquer patch de outro mod nessa tabela), mas as linhas são completas e a intenção é clara: rebalancear nutrição e refresco. Só 24 linhas de apodrecimento. Sem leia-me. ^c"),
        ("1639", 4, "Repete exatamente o 1483 (2X) em 110 de 111 linhas, e perde: o id derivado do nome (`AlternateFoodSpoil2X`) tem dígito e maiúsculas (regra 4: provável patch ignorado), traz um `food.tbl` vazio e uma linha com erro de 100x (Dead Chicken 24 → 2400 em vez de 48). ^c"),
    ],
    "perks": [
        ("1009", 1, "A versão viva: patch PTF com sufixo `perkaholic`, carrega no 1.9.8 e corrige o código `rst*1.1` para `mst*1.1` (Proficiency). Não substitui tabelas do jogo. ^c"),
        ("770", 2, "Mesmas 56 perks e 56 buffs, mas substitui as 5 tabelas inteiras (herda o estado do jogo de 2019) e o pak guarda os arquivos com caminho `../../../Data/...` e extensão `.tbl`; já está em quarentena por isso. ^c"),
        ("85", 3, "A mais antiga: manifest que só lista as versões 1.3 e 1.3.1 (o motor desativa), 6 tabelas inteiras com colunas faltando no cabeçalho (`autolearnable`, `exclude_in_game_mode`) e 63 buffs e 19 habilidades do jogo regravados com valores velhos. Redundante com as duas acima. ^c"),
    ],
    "combat": [
        ("2179", 1, "O mais completo e coerente: textos das perks alterados para bater com os novos números, nenhuma linha duplicada com os outros dois, cobre IA, vigor, morale, equipamento dos NPCs e arco. Contras: 71 linhas novas de `rpg_param` (uma chave desconhecida), `.tbl` ao lado de cada `.xml` e escopo muito largo. ^c"),
        ("1384", 2, "Propósito estreito e documentado (Mestre/Bloqueio por direção): 150 linhas de bloqueio perfeito, 8 perks reduzidas, 18 parâmetros. Sem manifest (pak solto), mas os valores são moderados, exceto `CombatAutoMaxAttackDelay` 0,01. ^c"),
        ("1112", 3, "Irmão mais velho do 1384: 130 das 150 linhas de bloqueio perfeito são idênticas, repete as mesmas 5 mudanças de IA e acrescenta 29 parâmetros novos mais a cópia de 41 deles no modo Hardcore. Muda também a alma `rat_bernard` (nível de combate 3 → 6), algo sem relação com o resto. ^c"),
    ],
    "weapons": [
        ("2045", 1, "Trabalho de mais fôlego e mais bem acabado: 12 armas de haste reequilibradas, habilidade `weapon_large` visível, 30 entradas de loja, 4 `blendSpace` de alabarda e banco de animações. Contra: substitui o banco de animações inteiro (6,3 MB), liga a tecla `3` a um comando de depuração e multiplica preços por quase 3. ^c"),
        ("2035", 2, "Muda o dano das flechas (de perfurante para cortante e contundente), o alcance do arco (3,3x) e cria 2 flechas novas, em arquivos com sufixo correto. Contra: manifest só `*`, atributos de outra tabela copiados em `pickable_item`, e valores de alcance e dano extremos sem explicação. ^c"),
    ],
    "equipment": [
        ("2173", 1, "Pacote coerente de economia de reparo: kits, preços, durabilidade de selas, perks. Falhas pequenas: apaga colunas de editor (`computer_name`, `timestamp`) em 20 linhas e usa uma chave de `rpg_param` que nenhuma lista conhece. ^c"),
        ("1380", 2, "Conteúdo novo limpo: 6 peças pretas, texturas (8,4 MB) e 17 entradas de loja, 3 idiomas. Renomeia 5 itens do jogo (corrige nomes), o que é útil. Poucas colunas conferidas por teste. ^c"),
        ("2209", 3, "Remendo de compatibilidade: depende do mod 1807 (Poisonous Enemies) e traz a própria `PoisonousUtils.lua` (464 linhas) e 26 entradas de loja com quantidade 0. Só faz sentido com o 1807 instalado. ^c"),
        ("2343", 4, "Mais arriscado do grupo: 1215 linhas de Lua de teste (rótulos `TEST53B`), substitui `IGM_Inventory.xml` do jogo (interface do inventário), troca o cabelo de 4 cavalos e cria um token de jogo. Grande superfície para conflito. ^c"),
    ],
    "economy": [
        ("1062", 1, "Sistema próprio e bem completo (itens, perks de local, buffs, textos em 4 idiomas, 54 KB de Lua), mas cria entidades por script, substitui `Bed.lua` do jogo e a tabela `sleeping_spot_type` inteira. ^c"),
        ("1105", 2, "Simples e claro nos números (preços de quarto, treinador, banho e a fórmula do preço de cavalos), mas substitui três scripts inteiros do jogo para mudar linhas de preço. ^c"),
    ],
    "rules": [("1558", 1, "Único do grupo; é o cruzamento de quase todo parâmetro global. Ver as tabelas de balanceamento B5, B6, B8, B9 e B16: ele contradiz os outros três em vários valores. ^c")],
    "lua": [
        ("2318", 1, "Mod informativo (não muda regra), código grande mas bem escopado, README e CHANGELOG. Contra: substitui `Inventory.gfx` do jogo (209 KB). ^c"),
        ("2323", 2, "Útil e simples de entender, mas deixa comandos de teste (`alchemy_give_all`) e um laço de temporizador a cada 1 s para sempre. ^c"),
    ],
}

# subcategory -> (lead, [(feature, strongest, also, note)])
FEATURES = {
    "food": ("Quatro implementações do mesmo tema. Só o apodrecimento tem quatro concorrentes; o resto é de um ou dois mods.", [
        ("Prolongar o apodrecimento (todos os alimentos)", "1483", "1639", "1483 oferece 2X, 3X e 5X; 1639 é o 2X do 1483 com um erro. 2011 e 2345 usam valores próprios."),
        ("Apodrecimento seletivo e realista", "2345", "2011", "2345: só 24 linhas (cozidos 48 → 60 h). 2011: 71 linhas, com carnes cozidas 48 → 81 h e defumadas 120 → 220 h."),
        ("Nutrição, refresco e saúde por alimento", "2345", "2011", "Mexem em 143 das mesmas linhas, com valores diferentes em 231 de 237 células: são alternativas, não somam."),
        ("Efeitos de lanche (buffs temporários)", "2011", "-", "Único. 42 buffs novos, 38 itens ligados. Inclui itens de teste."),
        ("Segurança de aplicação (sufixo e id)", "1483", "2011", "1483 e 2011 têm sufixo igual ao id; 1639 tem dígito no id; 2345 não tem sufixo (tabela inteira)."),
    ]),
    "perks": ("Mesmas 56 perks nos três; a diferença está em como são empacotadas e no que mais vai junto.", [
        ("Empacotamento correto para o 1.9.8", "1009", "-", "Único com sufixo, `Libs/Tables` no caminho e versão 1.9.8 no manifest."),
        ("Código de buff de Proficiency (`mst`)", "1009", "-", "85 e 770 têm `rst*1.1` (código que o jogo não usa para vigor máximo)."),
        ("Tabelas do jogo preservadas", "1009", "-", "85 e 770 regravam tabelas inteiras."),
        ("Idiomas", "1009", "-", "1009: 13 pacotes (10 textos alterados e 114 novos em cada). 85 e 770: só inglês (85: 226 alterados e 685 novos; 770: 78 e 134)."),
    ]),
    "combat": ("Todos usam a mesma técnica (`rpg_param` novo ou alterado, `perk_rpg_param_override` para o modo Hardcore) nos mesmos parâmetros.", [
        ("Atraso entre ataques da IA (`CombatAutoMaxAttackDelay`)", "2179", "1384, 1112", "1384 e 1112 põem 0,01 (ataque imediato); 2179 põe 3 (metade do jogo)."),
        ("Pesos de bloqueio da IA", "2179", "1384, 1112", "Valores diferentes em todos: ver B6."),
        ("Linhas de bloqueio perfeito por direção", "1384", "1112", "130 de 150 idênticas; o 1112 tem 24 linhas a mais."),
        ("Economia de vigor", "2179", "1112, 1384, 1558", "Cada um com valores próprios; 2179 muda menos."),
        ("Ajustes das perks e dos buffs de poção", "2179", "1384", "2179 mexe em 35 buffs e atualiza 36 textos; 1384 mexe em 8 buffs sem atualizar os textos."),
        ("Equipamento e moral dos NPCs, arco, movimento", "2179", "-", "Único."),
    ]),
    "weapons": ("Sem concorrência: armas de haste contra arco.", [
        ("Armas de haste", "2045", "-", "Único: 12 armas, habilidade visível, animações."),
        ("Flechas e arco", "2035", "2179 (parcial)", "2179 também muda 14 linhas de `ammo`; 24 células em comum, todas com valores diferentes."),
    ]),
    "equipment": ("Quatro mods independentes entre si.", [
        ("Economia do reparo", "2173", "1558", "1558 também mexe em `RepairKitCapacity` (8000), `RepairKitItemHealth*` e preço de reparo."),
        ("Itens novos", "1380", "2209", "1380: 6 peças pretas; 2209: capuz e luvas de envenenador."),
        ("Cavalos", "2343", "-", "Único."),
    ]),
    "economy": ("Não se sobrepõem em arquivo; ambos mexem em preços e em lojas.", [
        ("Preços de serviço", "1105", "-", "Quarto, banho, treinadores, cavalos."),
        ("Acampamento e dormir fora", "1062", "-", "Único."),
    ]),
    "rules": ("Só um mod, mas com sobreposição com outros grupos.", [
        ("Parâmetros globais de combate", "2179", "1558, 1112, 1384", "Os quatro escrevem `MaxDamage` e `CombatAuto*` com valores diferentes."),
        ("XP e progressão", "1558", "-", "Único neste conjunto B (outros graus têm mods de XP)."),
    ]),
    "lua": ("Sem concorrência.", [
        ("Mostrar combos na tela", "2318", "-", "Único."),
        ("Ligar estoques e cavalo ao banco de alquimia", "2323", "-", "Único."),
    ]),
}

GLOSSARY = [
    ("PTF e sufixo `__id`", "Patch de tabela: um arquivo `tabela__idDoMod.xml` dentro do pak do mod. O motor só aplica se o sufixo for igual ao id do mod (sem diferença entre maiúsculas e minúsculas).", "docs/engine/ptf-rules.md regra 1; maiúsculas conferidas no log (`potion__DrinkSoundEffects`).", "c"),
    ("Id do mod com dígito", "O id só aceita letras minúsculas e sublinhado; um id com dígito (ex.: `krs_harness2`) não foi aplicado nos testes.", "ptf-rules.md regra 4, medido no jogo; para o 1639 é inferência (nome `AlternateFoodSpoil2X`).", "d"),
    ("Linha completa (regra 5)", "Se uma linha de patch lista só algumas colunas, as outras viram vazio. As linhas precisam trazer todas as colunas.", "ptf-rules.md regra 5, medido com Aqua Vitalis.", "c"),
    ("Último vence (regra 6)", "Quando dois mods escrevem a mesma linha, a do último mod em `mod_order.txt` substitui a linha inteira.", "ptf-rules.md regra 6, medido.", "c"),
    ("Tabela inteira (sem sufixo)", "Um arquivo `food.xml` (sem `__`) substitui a tabela do jogo inteira e passa por cima de patches de outros mods nessa tabela; também desfaz as mudanças do 1.9.7/1.9.8 nela.", "MOD_INTERSECTIONS.md (como o jogo trata); efeito sobre o 1.9.8 deduzido da comparação.", "d"),
    ("Referência de 2020", "`Data/Tables_reference.pak` (20/jan/2020) guarda as tabelas de uma versão antiga. Serve para saber se um valor do mod é só o valor antigo do jogo ('obsoleto') ou uma mudança deliberada.", "Arquivo do jogo; usado por `tools/grade_b_extract.py`.", "c"),
    ("`decay_time_hours`", "Horas de jogo até a comida estragar (24 = 1 dia). Zero significa que não estraga: 91 das 202 linhas de `food` têm 0 (poções, vinho, cerveja, itens de teste).", "Tabela `food` do 1.9.8 e leia-me do 1483 (maçã: 5 dias).", "c"),
    ("`nutrition_benefit` / `refresh_benefit` / `health_benefit`", "Quanto o alimento sacia a fome, quanto muda a sede/refresco e quanto cura. Valores negativos pioram.", "Nome das colunas e comportamento de poções no jogo; descrição exata deduzida.", "d"),
    ("`CombatAuto*`", "Constantes da IA de combate: atraso entre ataques, peso de cada tipo de bloqueio, probabilidade de truques, passos de combo.", "Params Reference.md (comentários do próprio jogo) e rpg_constants_runtime.csv (valores lidos no jogo).", "c"),
    ("`CombatAutoMaxAttackDelay`", "Tempo máximo (s) que a IA espera entre ataques. 6 no jogo; 0,01 nos mods 1112 e 1384 significa praticamente sem espera.", "Valor do jogo lido na tabela; efeito deduzido do nome e da referência.", "d"),
    ("`MaxDamage`", "Teto de todo dano de vigor e de vida (200 no jogo; 100 em quatro mods).", "Params Reference.md: 'all stam and health damages are clamped'.", "c"),
    ("Bloqueio perfeito e `combat_action_perfect_block`", "Tabela com 358 linhas que sincroniza a animação do bloqueio perfeito com o golpe do adversário por tipo de ação, zona de ataque, zona de bloqueio e armas. Linhas novas = combinações novas.", "Colunas da tabela no jogo; significado das linhas novas deduzido das descrições dos mods.", "d"),
    ("Códigos de `buff.params`", "`wat` dano de arma, `wac` custo de vigor do ataque, `hlh`/`slh` dano sofrido na vida/vigor, `srg` regeneração de vigor, `mst` vigor máximo, `ade` eficácia da armadura, `dee` dano ao equipamento do adversário, `bad` ameaça (inimigo foge), `hko` nocaute na cabeça, `ain` sangramento, `pac` envenenamento, `was` precisão, `asp` velocidade do golpe, `cli` clinch, `osb` custo de bloqueio ao adversário, `spc` fala, `str`/`agi`/`vit` atributos.", "Cada código aparece ao lado da descrição em inglês de uma perk do mod 1009 (ex.: `wat*1.05` = 'You deal 5% more damage').", "c"),
    ("`perk_rpg_param_override` e 'Hardcore Mode - Constants'", "Tabela que troca constantes por perk; a pseudo-perk 'Hardcore Mode - Constants' (`01c3b32a`) vale só no modo Hardcore. Os mods 1112, 1384, 1558, 2173 e 2179 escrevem aqui os mesmos valores que em `rpg_param`.", "ptf-rules.md e STATUS (valores do modo Hardcore só valem nele).", "c"),
    ("`.tbl` ao lado de `.xml`", "Versão binária da tabela. O 2179 traz um `.tbl` para cada patch; o 1639 e o 2345 trazem um `food.tbl` de 0 byte. Não sabemos qual dos dois formatos o motor prefere.", "Presença no pak (lido); comportamento não testado.", "n"),
    ("Cabeçalho incompleto", "As colunas declaradas no `<header>` da tabela. Coluna do jogo que falta no cabeçalho é esvaziada nas linhas do patch (regra 5).", "Comparação do cabeçalho com o do jogo, feita por `tools/grade_b_extract.py`.", "c"),
    ("Grau B", "Classificação da análise automática (`MOD_ANALYSIS.md`): 100 ou mais linhas, 6 ou mais tabelas, ou 600 ou mais linhas de Lua. É sobre tamanho, não sobre qualidade.", "MOD_ANALYSIS.md.", "c"),
]

# number, mods, question, how to confirm
QUESTIONS = [
    ("Q1", "2179", "O motor usa o `.tbl` ou o `.xml` quando o pak traz os dois lado a lado? Se usar o `.tbl`, os valores lidos aqui (XML) podem não ser os aplicados.", "Instalar só o 2179 na réplica e ler de volta 3 linhas por `Database` e `RPG.<chave>`; comparar com o XML. Log `Table ... is patched by`."),
    ("Q2", "1639, 2345", "O `food.tbl` de 0 byte (no mesmo caminho da tabela do jogo) atrapalha a leitura de `food`?", "Rodar o 1639 e o 2345 no menu da réplica e ler `food` de volta."),
    ("Q3", "1639", "O id derivado `AlternateFoodSpoil2X` (dígito e maiúsculas) é rejeitado pelo motor?", "Procurar no log `mod id` com aviso e `Table 'food' is patched by`; renomear o suffix para `alternatefoodspoil` e repetir."),
    ("Q4", "2011", "`decay_time_hours = 0` realmente significa 'nunca apodrece' para carnes cruas? (O mod põe 0 em 5 carnes cruas, linguiça defumada e banha.)", "Ler `food` de volta e observar um item no jogo ao longo de dias; comparar com poções (0 no jogo)."),
    ("Q5", "2011", "A coluna `Weight` (W maiúsculo) do `pickable_item` é lida como `weight`? Se não for, o peso das 44 linhas fica vazio (regra 5).", "Ler `pickable_item.weight` de volta para 3 itens do patch."),
    ("Q6", "85", "As colunas `autolearnable` e `exclude_in_game_mode` faltando no cabeçalho de `perk.xml` esvaziam esses campos em todas as 600 perks?", "Instalar o 85 e ler `perk` de volta (3 perks comuns). Já foi dado como redundante: só confirmar se for usar."),
    ("Q7", "1112, 1384", "Com `CombatAutoMaxAttackDelay` 0,01 os inimigos atacam sem pausa? Fica jogável?", "Teste de combate na réplica (duelo na arena), comparando com o valor do jogo (6) e do 2179 (3)."),
    ("Q8", "1558", "As 14 chaves de XP de escudo (`ShieldXP...`) existem no motor?", "Ler `RPG.ShieldXP` etc. na réplica; o autor do mod avisa 'MAY NOT WORK'."),
    ("Q9", "2045", "A tecla `3` fica presa ao comando de depuração `unequipitem`? Conflita com os atalhos do autor?", "Ler `Mods/PURLE/.../polearm_startup.lua` (já lido) e olhar `bind` em jogo."),
    ("Q10", "2343, 2318", "`IGM_Inventory.xml` (2343) e `Inventory.gfx` (2318) convivem entre si e com os mods de inventário ordenado (2203, 2204)?", "Instalar pares na réplica e abrir o inventário; ver erros de UI no log."),
    ("Q11", "2209", "O `PoisonousUtils.lua` do 2209 está no mesmo caminho do script do mod 1807 (Poisonous Enemies)? Qual vence?", "Listar os dois paks e comparar os caminhos; o 1807 está em `_unmatched`."),
    ("Q12", "2179, 2173", "As chaves `UnarmedHitArmorDamageCoef` (2179) e `DamageToArmorStatusHigherLayers` (2173) existem no motor?", "Ler `RPG.<chave>` na réplica; não estão na lista de constantes lida em 1.9.6."),
    ("Q13", "1558, 2179, 1112, 1384, 2173", "No modo normal (não Hardcore) valem só as linhas de `rpg_param`; no Hardcore, as de `perk_rpg_param_override`? Ou as duas se somam?", "Já medido para `RepairPriceModif` (ptf-rules/STATUS); repetir para um parâmetro de combate."),
    ("Q14", "2173", "O `max_status` das selas (30 a 60) exige a categoria de reparo `armor.horse_saddle.*`? O 2173 acrescenta essas duas linhas em `skill2item_category`.", "Ler `skill2item_category` de volta; abrir o reparo no jogo com uma sela."),
    ("Q15", "1062", "A substituição de `Bed.lua` conflita com outros mods que também substituem `Bed.lua`?", "Procurar `Bed.lua` nos paks do conjunto A–E (a análise de arquivos já faz isso)."),
    ("Q16", "1105", "A fórmula `sum² x 6 + 2500` dá preços aceitáveis para cavalos de todos os níveis (sem o piso `HorseMinFinalPrice`)?", "Simular com os atributos dos cavalos do jogo ou ler `Horsetraders.getHorsePrice` na réplica."),
    ("Q17", "2323", "O comando de console `alchemy_give_all` depende do mod Cheat (`cheat_add_item`)? Sem ele, falha em silêncio?", "Ler o código (feito): chama `cheat_add_item` e `cheat_unlock_recipes`, que são comandos do mod Cheat (106)."),
    ("Q18", "2011", "Os buffs de lanche (42) são visíveis e fazem sentido na interface? Os 94 textos trocados usam 'Snacky Snack' no nome do item.", "Jogar com o 2011 e olhar o inventário e as dicas; confere com a lista de textos."),
]

# curated intersections (a, b, kind, text); machine-found ones are added by the builder
INTERS = [
    ("1483", "1639", "Redundante", "Mesmas 111 linhas de `food`, mesma coluna: 110 linhas idênticas (2X) e 1 diferente, a Dead Chicken (1639: 2400). Usar um dos dois, nunca os dois."),
    ("1483", "2011", "Conflito direto", "102 linhas de `food` em comum; nas 68 células de `decay_time_hours` que os dois alteram só 1 tem o mesmo valor (1483 2X: 96; 2011: 81 ou 54). O último na ordem vence a linha inteira."),
    ("1483", "2345", "Conflito direto", "102 linhas em comum, 24 células de apodrecimento (2 iguais, 22 diferentes). O 2345 é tabela inteira: cada linha dele traz TODAS as colunas, então ele sobrepõe a linha inteira do 1483, inclusive o apodrecimento que o 2345 deixou como no jogo."),
    ("1639", "2345", "Conflito direto", "Mesma situação do 1483 x 2345."),
    ("1639", "2011", "Conflito direto", "102 linhas em comum; nas 68 células de apodrecimento só 1 igual."),
    ("2011", "2345", "Conflito direto", "143 linhas de `food` em comum (140 em conflito, 2 idênticas, 1 em colunas diferentes) e 237 células, 6 com o mesmo valor. São duas filosofias de rebalanceamento da mesma coisa (nutrição, refresco, saúde); não se somam."),
    ("2011", "2179", "Conflito direto", "6 linhas de `food` em comum (12 células), todas diferentes; o 2179 também mexe em `buff` e `pickable_item` fora do tema alimento."),
    ("2179", "2345", "Funcional leve", "1 célula em comum em `food`."),
    ("85", "770", "Redundante", "186 linhas em comum e as 186 idênticas: as mesmas 56 perks e os mesmos 56 buffs, ponto a ponto."),
    ("85", "1009", "Redundante", "192 linhas em comum: 175 idênticas e 16 que diferem em colunas de interface do buff (`buff_desc`, `buff_ui_name`, `icon_id`...) e em Proficiency (`rst*1.1` contra `mst*1.1`). O 1009 é o único que corrige o código."),
    ("770", "1009", "Redundante", "186 linhas em comum: 171 idênticas e 15 diferentes (os mesmos campos de interface do buff e `mst*1.1`)."),
    ("85", "2179", "Conflito direto", "12 linhas em `buff`/`perk2perk_exclusivity` (1 idêntica, 2 em conflito, 9 em colunas diferentes). O 85 regrava buffs com valores de 2018 (tabela inteira) e o 2179 ajusta os mesmos buffs de combate: o 85, por ser tabela inteira, vence."),
    ("1009", "2179", "Funcional leve", "2 linhas: 1 `perk2perk_exclusivity` e 1 `buff` (1 em conflito, 1 em colunas diferentes)."),
    ("1112", "1384", "Redundante", "141 linhas em comum: 130 linhas idênticas de bloqueio perfeito e as mesmas 11 constantes, 7 delas com valor diferente (`CombatAutoPBWeight` 3,85 contra 2; `CombatAutoNormalBWeight` 3,475 contra 3; os quatro `CombatAutoZoneChangeDelay*`; `MaxPerfectBlockSlotModifier` do Hardcore 0,5 contra 0,782). O 1384 é a versão 'Lite' do mesmo sistema de bloqueio por direção."),
    ("1112", "2179", "Conflito direto", "31 linhas de `rpg_param` e `perk_rpg_param_override` em comum: 4 idênticas e 27 em conflito (ex.: `CombatAutoPBWeight` 3,85 contra 1,8; `CombatAutoMaxAttackDelay` 0,01 contra 3)."),
    ("1384", "2179", "Conflito direto", "29 linhas em comum (`buff`, `perk_rpg_param_override`, `rpg_param`): 5 idênticas e 24 em conflito (ex.: `CombatAutoPBWeight` 2 contra 1,8; `MaxDamage` igual nos dois)."),
    ("1112", "1558", "Conflito direto", "14 linhas em comum: 1 idêntica e 13 em conflito (`CombatAutoMaxAttackDelay` 0,01 contra 1,5)."),
    ("1384", "1558", "Conflito direto", "14 linhas em comum: 1 idêntica e 13 em conflito (`SkillToDmgConstA` 700 contra 100)."),
    ("2179", "1558", "Conflito direto", "21 linhas em comum: 3 idênticas e 18 em conflito (`SkillToDefense` 0,2857 contra 0,01)."),
    ("1558", "2173", "Conflito direto", "6 linhas de reparo em comum, todas em conflito: `RepairKitCapacity` 8000 contra 600; `RepairKitItemHealth*` 0 e 0,1 contra 0,1 e 0,9."),
    ("2035", "2179", "Conflito direto", "25 linhas de munição em comum (`ammo` 12, `pickable_item` 13): 17 em conflito e 8 em colunas diferentes; das 24 células em comum nenhuma é igual. O 2035 redistribui o dano das flechas e o 2179 ajusta `power_mod` e ataque das mesmas flechas."),
    ("2173", "2179", "Funcional leve", "1 linha em comum (um buff de perk): `perk_weapon_cruncher` +0,15 → +0,05 no 2173 e também reduzida pelo 2179."),
    ("1062", "2011", "Independente", "Mesmas tabelas (`buff`, `food`, `item`, `pickable_item`) mas nenhuma linha em comum."),
    ("2209", "1380", "Independente", "Ambos adicionam itens e entradas de loja, linhas diferentes."),
    ("2318", "2343", "Conflito potencial (arquivo)", "O 2318 substitui `Libs/UI/Inventory.gfx` e o 2343 substitui `Libs/UI/UIActions/IGM_Inventory.xml`: são arquivos diferentes da mesma interface do inventário; a convivência não foi testada."),
    ("2045", "2343", "Conflito potencial (arquivo)", "Ambos trazem arquivos de animação/estado de personagem; o 2045 substitui `kcd_male_database.adb`. O 2343 não toca esse banco, mas hooka `OnBedStop` do jogador."),
    ("2045", "2318", "Funcional leve", "O 2318 lê as perks de combo (armas e combos aprendidos); o 2045 muda o que 'weapon_large' mostra. Sem conflito de arquivo."),
    ("2173", "2209", "Independente", "Mesma família True Hardcore e mesma tabela `armor`, mas linhas diferentes."),
]
