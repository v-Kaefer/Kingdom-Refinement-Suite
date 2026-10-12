# Grade B mods: first-pass review

> **Status date:** 2026-10-08 | **Kind:** review | **Trust:** measured (files, game tables, 2020 reference tables) and derived (counts, readings of values) | **Game version:** 1.9.8

The 21 mods graded B ("large") in [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md), opened file by file and compared cell by cell with the 1.9.8 install. First pass only: what each mod really changes, how they relate, what looks wrong, what is worth keeping later. No balance decision is taken, nothing is moved to `Reviewed_Mods`, and nothing was run.

The full review is the page [`GRADE_B_REVIEW.html`](GRADE_B_REVIEW.html) (Portuguese, the author's display standard: before-and-after tables, a glossary with evidence and a confidence mark on every claim). It is built by `tools/build_grade_b_page.py` from `grade_b_*.csv/json` (written by `tools/grade_b_extract.py`) and the curated text in `tools/grade_b_data*.py`. [`grade_b_intersections.csv`](grade_b_intersections.csv) has every pair of mods that write the same row, and [`grade_b_overview.csv`](grade_b_overview.csv) one line per mod.

## Sub-categories and ranking

| Sub-category | Ranking (best made first) |
|---|---|
| Comida, bebida e apodrecimento | 1483 (1), 2011 (2), 2345 (3), 1639 (4) |
| Perks: a linha Perkaholic | 1009 (1), 770 (2), 85 (3) |
| Combate: ritmo da IA, bloqueio e vigor | 2179 (1), 1384 (2), 1112 (3) |
| Armas e munição: estatísticas | 2045 (1), 2035 (2) |
| Equipamento: conteúdo, manutenção e visual | 2173 (1), 1380 (2), 2209 (3), 2343 (4) |
| Economia de serviços e acampamento | 1062 (1), 1105 (2) |
| Regras globais: o pacote de parâmetros | 1558 (1) |
| Auxiliares de interface e de script (Lua) | 2318 (1), 2323 (2) |

## What stands out

- **Três pacotes não carregam como empacotados.** **85** (manifest só lista 1.3 e 1.3.1, o motor o desativa), **1639** (o id derivado do nome, `AlternateFoodSpoil2X`, tem dígito: pela regra 4 o patch provavelmente é ignorado) e **1384** (sem manifest: pak solto, aplicação por patch não medida). O 770 está em quarentena por caminhos `../` no pak.
- **Erros de digitação e de empacotamento reais.** 1639: Dead Chicken 24 → **2400** (era 48). 2011: atributo `decay_ime_hours`, cabeçalho `Weight` com W maiúsculo (provável peso vazio em 44 itens), zeros em carne crua. 1558: **14 chaves de XP de escudo** que nenhuma lista conhece, e `ShoeHealthDecrease` 10x maior contra o leia-me ('botas gastam mais devagar'). 85: cabeçalho de `perk.xml` sem duas colunas do jogo.
- **Os quatro mods de combate se contradizem.** `CombatAutoMaxAttackDelay`: jogo 6, 1112 e 1384 **0,01**, 2179 **3**, 1558 **1,5**. `SkillToDmgConstA`: jogo 250, 1384 **700**, 1558 **100**. `SkillToDefense`: jogo 0,02857, 2179 **0,2857**, 1558 **0,01**. Cada um escreve a mesma linha: vale o último na ordem.
- **Mudanças fora do escopo declarado.** 2045 liga a tecla **3** a um comando de depuração; 2011 reescreve itens de teste e 'Generic potion' vira veneno (`doomsday_poison`); 85 regrava 63 buffs e 19 habilidades do jogo com valores de 2018; 1112 muda o NPC `rat_bernard`; 2323 deixa o comando `alchemy_give_all`; 2343 e 2318 substituem arquivos de interface do inventário; 2173 apaga colunas de editor.
- **Tabelas substituídas inteiras.** 85, 770 (perks), 2345 (`food`) e 1062 (`sleeping_spot_type`). Uma tabela inteira vence qualquer patch de outro mod e desfaz as mudanças do 1.9.7/1.9.8 nela.
- **Perkaholic: três empacotamentos das mesmas 56 perks.** 85, 770 e 1009 trazem as mesmas perks e os mesmos buffs: 85 e 770 são idênticos entre si nas 186 linhas em comum; o 1009 difere em 15 a 16 linhas (campos de interface do buff e `mst*1.1`). Só o **1009** (patch, 13 idiomas, código correto) é utilizável.
- **Valores extremos a testar antes de qualquer decisão.** Atraso entre ataques 0,01 (1112, 1384); alcance do arco 3,3x (2035); quarto 10 a 25x mais caro (1105); `RepairKitCapacity` 8000 e sujeira desligada (1558); `MaxDamage` 100 em quatro mods (em acordo).
- **Ideias únicas do grau B.** Buffs de lanche e textos de efeito (2011); estado do equipamento e moral dos NPCs (2179); linhas de bloqueio perfeito por direção (1112/1384); armas de haste (2045); acampamento (1062); ligar ingredientes de estoques e cavalo à alquimia (2323); 56 perks (1009).

## Open questions

18 questions with a way to confirm each are in the page (section "Perguntas").

## Safety and scope

The archives were listed before extraction, extracted to a scratch folder, read and deleted; nothing was run, installed or loaded by the game. Mod 770 is in quarantine and was read the same way. The comparison used the replica install (`Mods WIP folder/KingdomComeDeliverance`, read only).
