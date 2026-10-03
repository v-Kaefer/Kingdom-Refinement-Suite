# Potion base Shelf – bases (aqua, vinum, oleum, spiritus)

## Critério rápido para parâmetros
| Atributo                     | Como calcular                                                            |
|------------------------------|---------------------------------------------------------------------------|
| **Nourishment**              | 0 – 3 se venenosa / 4 – 6 se à base de vinho / ≤ 10 se decoction doce    |
| **short_term_ratio**         | 0.5 p/ poções destiladas, 0.3 p/ vinhos, 0.15 p/ água/óleo              |
| **Energy**                   | +1 a +4 se conter caféina/álcool leve / 0 se sedativa / -? se sonífera  |
| **Alcohol** (%)*             | 0 em aqua | 3 % em wine | 7 % spirits destilado |0 em óleo               |
| **Weight**                   | 0.25 spirits (frascos pequenos) | 0.4 wine | 0.5 decoctions            |
| **Health benefit**           | +X se curativa, -X se venenosa (Belladonna, Henbane etc.)               |

\*O jogo usa 0 – 100; % aqui é a divisão direta (7% → valor 7).

---

## Modelo a preencher

### ⬛ NOME DA POÇÃO
- **Base:** (Water / Wine / Spirits / Oil)  
- **Ingredientes:**  …  
- **Resumo lore:**  …  
- **Riscos/toxinas:**  …  

*Receives:*  
| Atributo   | Valor Vanilla | Novo Valor |
|------------|---------------|------------|
| Nourishment|               |            |
| Energy     |               |            |
| Weight     |               |            |
| Alcohol    |               |            |
| Health     |               |            |
| Observação |               |            |

---

## ☑️ POÇÕES JÁ AJUSTADAS

### Aesop Potion
- **Base:** Spirits  
- **Ingredientes:** Belladonna (veneno), Wormwood (amargo, força), Wild Boar Tusk (neutro), Comfrey (cura)  
- **Justificativa:** destilado forte, baixo valor nutritivo; contém Belladonna → dano; sem carvão neutralizador.  

*Receives:*  
| Atributo   | Vanilla | Novo |
|------------|---------|------|
| Nourishment| 10      | **2.5** |
| short_term_ratio | 0.1 | **0.5** |
| Energy     | 4       | 4 (mantido) |
| Weight     | 0.5     | 0.25 |
| Alcohol    | 10      | 10 (destilado) |
| Health     | 0       | **-15** |
| Obs.       | Cura cães/cavalos, mas causa leve intoxicação humana |

---

### Amor Potion
- **Base:** Wine  
- **Ingredientes:** Antlers (proteínas), Chamomile (sedativa leve, +Speech), Marigold (cura, leve nutritiva), Wormwood (força, amargo)  
- **Justificativa:** bebida afrodisíaca à base de vinho; ervas aumentam carisma; amargor reduz leve energia pós-efeito.  

*Receives:*  
| Atributo   | Vanilla | Novo |
|------------|---------|------|
| Nourishment| 7       | **5.0** |
| short_term_ratio | 0.3 | 0.3 (vinho) |
| Energy     | 4       | **3** |
| Weight     | 0.5     | **0.4** |
| Alcohol    | 7       | 7 (coerente) |
| Health     | 0       | 0 |
| Obs.       | Carisma +5 continua; nutrição reduzida pq vinho + ervas leves |

---

## ➡️ PRÓXIMOS (rótulos criados, valores a decidir)

Copie o modelo acima para cada um:

- Artemisia Potion (Spirits + Wormwood x2 + Valerian)  
- Bard Potion (Wine + Chamomile + Belladonna)  
- Bane Potion (Oil + Henbane + Belladonna)  
- Bivoj’s Rage (Spirits + St. John’s Wort x2 + Wormwood)  
- Buck’s Blood (Spirits + Sage + Wild Boar’s Tusk)  
- Chamomile Brew (Water + Chamomile x2)  
- … (restante da lista de 32)

Preencha **Nourishment/Energy/Weight/Health/Alcohol** usando a tabela-guia. Depois coloque apenas as linhas `<row …>` alteradas em `food_potions.xml`.

---

### Como gerar o XML PTF

Quando terminar cada ficha:

```xml
<row item_id="•••GUID•••"
     nutrition_benefit="5"
     short_term_nutrition_benefit_ratio="0.3"
     energy_benefit="3"
     alcohol="7"
     health_benefit="0"
     weight="0.4"/>


Segue abaixo a continuação do Potions.md, já preenchida para todas as poções vanilla de Kingdom Come: Deliverance (v 1.9.6).
Mantive o mesmo formato que você começou:

resumo dos ingredientes

lógica de base → efeito

tabela “Receives” com os valores vanilla e os novos valores sugeridos

observações de balanceamento

Escala numérica adotada (igual às duas primeiras poções que já definimos)

Atributo	Regra-guia
Nourishment	0–3 (venenosa) • 4–6 (wine) • até 10 (decoction doce)
short_term_ratio	0.5 (spirits) • 0.3 (wine) • 0.15 (water/ou oil)
Energy	+3 / +4 (estimulante) • 0 (neutro) • −? (sedativo)
Alcohol	0 (aqua) • 3 (wine) • 7 (strong wine) • 10 (spirits)
Health benefit	+X (cura) • −X (veneno)
Weight	0.25 (frasco spirits) • 0.4 (garrafa wine) • 0.5 (decoction)

☑️ Poções revisadas (lista completa)
Valores vanilla retirados do wiki em 01 ago 2025; “Novo” segue o guia acima.

Aesop Potion (já revisada)
(…mantido da sua versão)

Amor (Love) Potion (já revisada)
(…mantido da sua versão)

Antidote Potion
Base: Water

Ingredientes: Charcoal (neutraliza toxinas) + Valerian (calmante) + Thistle (sangue)

Justificativa: baixa nutrição; remove veneno ⇒ health_benefit +5.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 4 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | 0 | 0 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | +0 | +5 |
| Obs. | Cura veneno, leve nutrição |

Artemisia Potion
Base: Spirits

Ingredientes: Wormwood ×2 (amargo, força) + Valerian (calmante)

Justificativa: bebida estimulante/amarga → +Strength & −Speech.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 7 | 3 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 3 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | -2 (amargor tóxico leve) |
| Obs. | Reduz fala, aumenta força |

Bard’s Potion
Base: Wine

Ingredientes: Chamomile, Belladonna, Mint

Justificativa: aumenta Speech, contém Belladonna (leves náuseas).
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 7 | 5 |
| short_term_ratio | 0.3 | 0.3 |
| Energy | 4 | 2 |
| Weight | 0.4 | 0.4 |
| Alcohol | 7 | 7 |
| Health | 0 | -5 |
| Obs. | Debuff leve de saúde (toxina) |

Bane Potion
Base: Oil

Ingredientes: Henbane + Belladonna (venenosas)

Justificativa: veneno não letal; zero nutrição, dano à saúde.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 0 | 0 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -2 | -2 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | -15 | -15 |
| Obs. | Mantido como veneno fraco |

Bivoj’s Rage
Base: Spirits

Ingredientes: St John’s Wort ×2 (cura) + Wormwood (força)

Justificativa: tônica de força; alta energia; alcoólica.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 10 | 4 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 4 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | +0 | +2 |
| Obs. | Debuff de fala permanece |

Buck’s Blood
Base: Spirits

Ingredientes: Sage (vigor) + Wild Boar’s Tusk (proteína)

Justificativa: bebida forte de caça; leve cura, alto álcool.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 10 | 5 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 3 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | +2 |
| Obs. | Aumenta Vitalidade, cura pequena |

Chamomile Brew
Base: Water

Ingredientes: Chamomile ×2

Justificativa: calmante, induz fome.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 4 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -2 | -2 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | +0 | +1 |
| Obs. | Sedativo; aumenta fome |

Cockerel Potion
Base: Spirits

Ingredientes: Mint (estimulante) + Valerian (contrasta)

Justificativa: desperta; alta energia, baixo nutrição.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 2 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 4 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | 0 |
| Obs. | Remove fatiga, energia alta |

Dollmaker Potion
Base: Oil

Ingredientes: Belladonna + Poppy (sonífera)

Justificativa: veneno/paralisante; dano saúde, sedação.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 0 | 0 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -4 | -4 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | -20 | -20 |
| Obs. | Variação de Poison forte |

Embrocation (Horse)
Base: Oil

Ingredientes: St John’s Wort ×2 + Valerian (calma)

Justificativa: tratamento p/ cavalo; sem nutrição humana.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 0 | 0 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | 0 | 0 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | +0 | +0 |
| Obs. | Só uso em cavalo (unchanged) |

Faint-Heart Potion
Base: Spirits

Ingredientes: Valerian + Poppy (sedativo)

Justificativa: reduz coragem; nutrição baixa; sedação.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 2 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | -3 | -3 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | -2 |
| Obs. | Debuff coragem |

Lazarus Potion
Base: Spirits

Ingredientes: St John’s Wort + Valerian + Chamomile

Justificativa: cura total; moderada nutrição; alta energia.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 10 | 6 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 4 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | +0 | +15 |
| Obs. | Cura 100% saúde, cansaço reduzido |

Lethal Poison
Base: Oil

Ingredientes: Henbane + Belladonna + Wormwood

Justificativa: veneno letal; dano muito alto.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 0 | 0 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -5 | -5 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | -40 | -40 |
| Obs. | Mata NPC |

Lullaby Potion
Base: Water

Ingredientes: Poppy + Chamomile + Herb Paris

Justificativa: sedativo forte; reduz energia.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 3 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -4 | -4 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | 0 | 0 |
| Obs. | Faz alvo dormir |

Marigold Decoction
Base: Water

Ingredientes: Marigold ×2

Justificativa: cura leve; decoction herbal.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 4 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | 0 | 0 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | +0 | +5 |
| Obs. | Pequena cura |

Nighthawk Potion
Base: Spirits

Ingredientes: Eyebright + Belladonna

Justificativa: visão noturna; toxina leve; energia +2.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 5 | 2 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 2 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | -5 |
| Obs. | Debuff saúde leve (Belladonna) |

Poison (standard)
Base: Oil

Ingredientes: Henbane + Herb Paris

Justificativa: dano médio; sem nutrição.
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 0 | 0 |
| short_term_ratio | 0.15 | 0.15 |
| Energy | -2 | -2 |
| Weight | 0.5 | 0.5 |
| Alcohol | 0 | 0 |
| Health | -25 | -25 |
| Obs. | Veneno comum |

Savior Schnapps
Base: Spirits (destilado forte)

Ingredientes: Nettle + Belladonna + Mint

Justificativa: bebida alcoólica que salva; alta nutrição? (reduz)
| Atributo | Vanilla | Novo |
|----------|---------|------|
| Nourishment | 10 | 4 |
| short_term_ratio | 0.5 | 0.5 |
| Energy | 4 | 3 |
| Weight | 0.25 | 0.25 |
| Alcohol | 10 | 10 |
| Health | 0 | 0 |
| Obs. | Continua salvando, menos comida “grátis” |