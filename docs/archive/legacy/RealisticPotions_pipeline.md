## Pipeline – Realistic Potions (KCD)

```mermaid
flowchart LR
  %% ==== Inputs (vanilla XML) ====
  subgraph IN["Inputs (Tables/Tables/item)"]
    item["item.xml (item_id → item_name)"]
    herb["herb.xml (is_poisonous, ...)"]
    amat["alchemy_material.xml (type/subtype)"]
    rcpd["recipe.xml (product_item_id, base_material_id)"]
    rcing["recipe_ingredient.xml (recipe_id → item_id, qty)"]
    abase["alchemy_base.xml (base item_id → name)"]
    food["food.xml (tabela food)"]
  end

  %% ==== Etapa A: build_ingredients_json.py ====
  subgraph BUILD["Etapa A · build_ingredients_json.py"]
    A1["Join: item + herb + alchemy_material"]
    A2["Regras: venenoso / amargo / medicinal / calmante / proteína"]
    A3["Emitir ingredients.json"]
  end

  %% ==== Etapa B: XmlFilesAnalyzer_auto.py ====
  subgraph ANALYZE["Etapa B · XmlFilesAnalyzer_auto.py"]
    B1["Detectar base: recipe + alchemy_base"]
    B2["Poção → ingredientes: recipe_ingredient (+ qty)"]
    B3["Somar contributions (ingredients.json)"]
    B4["Aplicar fatores da base: fac, ratio, alc, nut_base, ene_base, weight"]
    B5["Gerar linhas <row ...> (patch)"]
  end

  %% ==== Opcional: Visualizações ====
  subgraph VIZ["Opcional · Visualizações"]
    pjson["potion_ingredients.json (poção → ingredientes)"]
    pmd["potion_ingredients_mermaid.md (diagrama)"]
  end

  OUT["food_potions.xml · PTF"]
  PACK["Empacotar em Mods/SeuMod/Data/Tables.pak"]

  %% ==== Conexões ====
  item --> A1
  herb --> A1
  amat --> A1
  A1 --> A2 --> A3

  rcpd --> B1
  abase --> B1
  rcing --> B2
  A3 --> B3
  B2 --> B3
  B1 --> B4
  B3 --> B4
  food --> B5
  B4 --> B5 --> OUT --> PACK

  rcing --> pjson
  item --> pjson
  pjson --> pmd
```
---

## Passo-a-passo (resumo)

Entradas (XML vanilla)

item.xml: nomes legíveis de cada item_id.

herb.xml: flags e metadados (ex.: is_poisonous).

alchemy_material.xml: classifica partes animais etc.

recipe.xml: liga poção → base_material_id (e product_item_id).

alchemy_base.xml: traduz base_material_id → Spirits/Wine/Water/Oil.

recipe_ingredient.xml: lista ingredientes (e quantidades) de cada receita.

food.xml: é a tabela que receberá o patch (PTF).

Etapa A — build_ingredients_json.py

Faz join de item.xml + herb.xml (+ alchemy_material.xml).

Aplica regras realistas (veneno forte/leves, amargo, medicinal, calmante, proteína).

Emite ingredients.json com:

name (facilita revisar),

nutrition, energy, health,

opcionais: absorption (ratio do ingrediente), element (aqua/ignis…).

Etapa B — XmlFilesAnalyzer_auto.py

Descobre a base de cada poção via recipe.xml + alchemy_base.xml.

Junta os ingredientes (e quantidades) via recipe_ingredient.xml.

Marca venenos via herb.xml.

Soma contribuições do ingredients.json e aplica fatores da base:

fac (diluição), ratio (short-term), alc, nut_base, ene_base, weight.

Gera food_potions.xml (PTF minimalista, só as linhas <row> alteradas).

Saída

food_potions.xml → empacotar em Mods\<SeuMod>\Data\Tables.pak e testar.

(Opcional) Visualização

potion_ingredients.json + potion_ingredients_mermaid.md para inspecionar rapidamente poções e dependências.

Comandos (relembrando)

# Regerar contribuições (se quiser atualizar regras)
python build_ingredients_json.py

# Gerar o patch PTF
python XmlFilesAnalyzer_auto.py
