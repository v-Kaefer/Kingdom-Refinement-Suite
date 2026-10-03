Variáveis (colunas) da tabela food e seu efeito no jogo
Coluna	Tipo	O que controla no jogo
alcohol_content	real	Grau alcoólico (0-100). Quanto maior, mais rápido o medidor de embriaguez sobe, ativando buffs/debuffs de bêbado.
cooked_item_id / dried_item_id / smoked_item_id	uuid	Liga o item “cru” à versão cozida, seca ou defumada. Quando o jogador cozinha/seca a comida, o jogo troca o item pelo UUID indicado.
decay_time_hours	real	Horas (tempo de jogo) até o alimento começar a estragar. Afeta a cor do ícone e pode causar envenenamento alimentar.
food_type_id	integer	Agrupamento grosso (1 = Meal, 2 = Ingredient, 3 = Drink, etc.). Define filtros no inventário e quais perks interagem com o item.
food_subtype_id	integer	Sub-categoria opcional (ex.: 4 = herbal decoction, 8 = Saviour Schnapps).
health_benefit	real	Pontos de vida curados (positivo) ou dano direto (negativo) aplicados na hora de consumir.
nutrition_benefit	real	Pontos de Nutrição que entram na barra de Fome. Valores negativos reduzem saciedade (usado em laxantes/venenos).
short_term_nutrition_benefit_ratio	real	Multiplicador de “peso no estômago”. Um valor 0.5 faz a Nutrição temporária contar como o dobro, podendo levar a overeating rápido.
refresh_benefit	real	Pontos de Energia (fadiga). Positivo = desperta; negativo = sonífero.
max_status	integer	Durabilidade (0–100). Cada tick de deterioração reduz esse valor; quando chega a 0 o item estraga.
item_id	uuid	Identificador único do item (referenciado por inventário, recipes, loot-tables).