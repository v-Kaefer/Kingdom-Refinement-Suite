# Real-world sources for the potion rebalance

Companion to `ANALYSIS.md` (evidence class B). It supports the workflow you described:

1. Read the ingredient description (in-game herbarium text or the wiki).
2. Turn each statement into a **claim** and compare it with what is known about the real plant, substance or
   consumption effect.
3. Record the verdict and let it justify, limit or veto a rule.

`claims_ledger.csv` holds the claims (29 so far, one row per claim) and this file holds the sources. A rule in the
rebalance should cite a ledger row, and a ledger row cites source ids (`S01`...).

## How much to trust this

- **[F]** = I opened the page and read it. **[S]** = I only saw it in a search result summary. Open an [S] page before a
  rule depends on it.
- Tiers: **T1** regulator or government resource (EMA, NIH, NCBI Bookshelf, Cochrane); **T2** peer-reviewed paper;
  **T3** encyclopaedia or plant database, for context only.
- Paraphrased, not quoted. Numbers are as the source states them.
- Nothing here is medical advice; it only records what the sources say about the real plant.

## Where the in-game text comes from

The game's own herb descriptions are in `Localization/English_xml.pak` (`herb_<name>_desc`, `_effect`) and are
extracted into `docs/potions/ingredient_dataset.csv` (`in_game_effect_text`). The community wiki shows the same
descriptions per herb and the potion recipes:
[Herbarium](https://kingdom-come-deliverance.fandom.com/wiki/Herbarium) ·
[Ingredients](https://kingdom-come-deliverance.fandom.com/wiki/Ingredients) ·
[Belladonna](https://kingdom-come-deliverance.fandom.com/wiki/Belladonna) ·
[Herbarium on wiki.gg](https://kingdomcomedeliverance.wiki.gg/wiki/Herbarium) [S, T3].

## Sources

| Id | Subject | Source | Tier | Read |
|---|---|---|---|---|
| S01 | Wormwood: traditional use for appetite and mild digestive complaints, adults, liver/bile-duct caution | [EMA Absinthii herba](https://www.ema.europa.eu/en/medicines/herbal/absinthii-herba) | T1 | F |
| S02 | Thujone neurotoxicity and daily limits (wormwood, sage) | [EMA public statement on thujone](https://www.ema.europa.eu/en/documents/scientific-guideline/public-statement-use-herbal-medicinal-products-containing-thujone-revision-1_en.pdf) | T1 | S |
| S03 | Belladonna / tropane alkaloid poisoning: mechanism, symptoms, onset 1-4 h | [StatPearls, Plant Alkaloids Toxicity](https://www.ncbi.nlm.nih.gov/sites/books/NBK587364/) | T1 | F |
| S04 | Belladonna intoxication case report | [PMC3361210](https://pmc.ncbi.nlm.nih.gov/articles/PMC3361210/) | T2 | S |
| S05 | Chamomile: minor GI complaints, skin and mouth uses | [EMA Matricariae flos](https://www.ema.europa.eu/en/medicines/herbal/matricariae-flos) | T1 | S |
| S06 | Chamomile safety, interactions, evidence | [NCCIH Chamomile](https://www.nccih.nih.gov/health/chamomile) | T1 | F |
| S07 | Comfrey root: external use only, minor sprains and bruises, 10 days, adults, liver toxicity when taken by mouth | [EMA Symphyti radix](https://www.ema.europa.eu/en/medicines/herbal/symphyti-radix) | T1 | F |
| S08 | Pyrrolizidine alkaloids in herbal products | [EMA public statement on PAs](https://www.ema.europa.eu/en/use-herbal-medicinal-products-containing-toxic-unsaturated-pyrrolizidine-alkaloids-pas-scientific-guideline) | T1 | S |
| S09 | Dandelion: traditional diuretic and mild digestive use | [EMA Taraxaci radix cum herba](https://www.ema.europa.eu/en/medicines/herbal/taraxaci-radix-cum-herba) | T1 | S |
| S10 | Eyebright eye drops in conjunctivitis (prospective cohort) | [PubMed 11152054](https://pubmed.ncbi.nlm.nih.gov/11152054/) | T2 | S |
| S11 | Eyebright drops in preterm neonates (randomised trial) | [PMC7431947](https://pmc.ncbi.nlm.nih.gov/articles/PMC7431947/) | T2 | S |
| S12 | St John's wort: depression use, enzyme induction and drug interactions | [EMA assessment report](https://www.ema.europa.eu/en/documents/herbal-report/final-assessment-report-hypericum-perforatum-l-herba-revision-1_en.pdf) | T1 | S |
| S13 | St John's wort safety | [NCCIH St. John's Wort](https://www.nccih.nih.gov/health/st-johns-wort) | T1 | S |
| S14 | Calendula: topical minor wounds and skin inflammation | [EMA Calendulae flos](https://www.ema.europa.eu/en/medicines/herbal/calendulae-flos) | T1 | S |
| S15 | Peppermint leaf: dyspepsia and flatulence | [EMA Menthae piperitae folium](https://www.ema.europa.eu/en/medicines/herbal/menthae-piperitae-folium) | T1 | S |
| S16 | Hangover remedies: no compelling evidence for any intervention | [BMJ systematic review, PMC1322250](https://pmc.ncbi.nlm.nih.gov/articles/PMC1322250/) | T2 | S |
| S17 | Herb Paris: saponins, nausea and vomiting, toxicity of berries and roots | [Z. Naturforsch. C, chemical composition](https://doi.org/10.1515/znc-2012-11-1206); [PFAF](https://pfaf.org/user/Plant.aspx?LatinName=Paris+quadrifolia) | T2 / T3 | S |
| S18 | Opium poppy preparations and infant deaths | [Lethal Lullabies, PubMed 26163533](https://pubmed.ncbi.nlm.nih.gov/26163533/); [Poppy intoxication in infants, PubMed 34027872](https://pubmed.ncbi.nlm.nih.gov/34027872/) | T2 | S |
| S19 | Sage: dyspepsia and sweating, thujone limit | [EMA Salvia officinalis folium (draft monograph)](https://www.ema.europa.eu/en/documents/herbal-monograph/draft-community-herbal-monograph-salvia-officinalis-l-folium_en.pdf) | T1 | S |
| S20 | Blessed thistle: temporary loss of appetite, dyspepsia | [EMA Cnici benedicti herba](https://www.ema.europa.eu/en/medicines/herbal/cnici-benedicti-herba) | T1 | S |
| S21 | Nettle: haemostatic and wound-healing potential (animal and lab) | [PMC5672119](https://pmc.ncbi.nlm.nih.gov/articles/PMC5672119/) | T2 | S |
| S22 | Nettle: no clinically useful antibacterial evidence | [PubMed 35693473](https://pubmed.ncbi.nlm.nih.gov/35693473/) | T2 | S |
| S23 | Nettle leaf: traditional urinary flushing and minor joint pain | [EMA Urticae folium](https://www.ema.europa.eu/en/medicines/herbal/urticae-folium) | T1 | S |
| S24 | Valerian: mild nervous tension and sleep, slow onset | [EMA Valerianae radix](https://www.ema.europa.eu/en/medicines/herbal/valerianae-radix) | T1 | S |
| S25 | Valerian and chamomile for sleep: evidence unproven | [NCCIH Sleep Disorders](https://www.nccih.nih.gov/health/sleep-disorders-and-complementary-health-approaches) | T1 | F |
| S26 | Valerian: rare liver injury | [LiverTox, valerian](https://www.ncbi.nlm.nih.gov/books/NBK548255/) | T1 | S |
| S27 | Activated charcoal: time-dependent benefit (74 % / 47 % / 40 % / 16.5 %), poor binding of toxic alcohols and metals, not for routine use | [PMC4767212](https://pmc.ncbi.nlm.nih.gov/articles/PMC4767212/) | T2 | F |
| S28 | AACT/EAPCCT position statement on single-dose activated charcoal | [PubMed 9482427](https://pubmed.ncbi.nlm.nih.gov/9482427/) | T1 | S (page needs cookies) |
| S29 | Ethanol absorption is not significantly prevented by charcoal | [PubMed 6530700](https://pubmed.ncbi.nlm.nih.gov/6530700/) | T2 | S |
| S30 | Honey as a topical wound treatment (Cochrane) | [PMC9719456](https://pmc.ncbi.nlm.nih.gov/articles/PMC9719456/) | T1 | F |
| S31 | Amanita muscaria: ibotenic acid and muscimol syndrome | [PMC12737661](https://pmc.ncbi.nlm.nih.gov/articles/PMC12737661/); [PubMed 25173077](https://pubmed.ncbi.nlm.nih.gov/25173077/) | T2 | S |
| S32 | Alcohol strength: beer 2-8 %, wine 8-14 %, spirits 40-50 %; aqua vitae history | [Britannica, distilled spirit](https://www.britannica.com/topic/distilled-spirit); [Wikipedia, Aqua vitae](https://en.wikipedia.org/wiki/Aqua_vitae) | T3 | S |
| S33 | Food in the stomach slows alcohol absorption | [PubMed 7206717](https://pubmed.ncbi.nlm.nih.gov/7206717/); [PMC1705129](https://pmc.ncbi.nlm.nih.gov/articles/PMC1705129/) | T2 | S |

## What the comparison shows

1. **Real-world accepted uses are narrow and mostly digestive or topical.** Wormwood, thistle, mint, sage, chamomile and
   dandelion are accepted for appetite, digestion or urine flow; marigold, comfrey and nettle for the skin or bruises.
   The in-game stat effects (strength, agility, speech) have no real-world basis and should stay labelled as game design.
2. **Some in-game remedies are contradicted.** Mint or sage against intoxication or hangover (S15, S16, S19); comfrey as a
   drink, because the root is liver-toxic by mouth and is allowed externally only (S07).
3. **Some real dangers are not in the game text.** Wormwood and sage (thujone, S02), comfrey by mouth (S07), poppy for
   children (S18), St John's wort interactions (S12). Whether to model them is a design choice, not a given.
4. **The game already models one real effect.** The engine has `AlcoholDigestSpeedModfifOnFullStomache` (0.5) and
   `...OnEmptyStomache` (2); food slows alcohol absorption in real life (S33). A potion rule should not add a second one.
5. **Poisonous in the game is not poisonous in the lab.** `herb.poisonous` is set for nettle; the regulator treats nettle
   leaf as a tea (S23). Use the real toxicity (belladonna S03, Herb Paris S17, poppy S18, Amanita S31) when a rule needs
   "dangerous", not the flag.
6. **Charcoal has a time window (S27).** A realistic antidote rule would depend on how soon it is drunk; that needs the
   buff duration data, which is not analysed yet.

## Gaps

- No source for boar tooth, antlers, cobweb, cave mushroom, or "Attire" (game items without a clear real counterpart).
- The poppy species and the Amanita species are not stated in the game data (Papaver somniferum and A. muscaria are
  assumptions).
- Herb Paris and the alcohol-strength rows rest on weaker (T3) sources; a toxicology reference for Herb Paris and a
  historical source for medieval Bohemian drinks are still missing.
- The in-game claims for dandelion syrup against colds, St John's wort in wine, and thistle against plague were not
  checked and are marked `open` in the ledger.
- Pages marked [S] were not opened in full.

## Adding a claim

Add a row to `claims_ledger.csv`: the in-game claim and where you read it, the real-world finding with source ids,
a verdict (`supported`, `partly supported`, `not supported`, `contradicted`, `game fiction`), and the *direction* of the
rule it allows (never a number). Keep numbers for the rule table in `ANALYSIS.md` section 6.
