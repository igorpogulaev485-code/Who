---
title: "Лес Хранителей — бриф + промпт карты (сверка с картой мира)"
status: prep
date: 2026-09-22
source: gm-answers + world-map-echo-dawn + borders-from-world + passport
contour_lock: campaign/plot/canon-lock-2026-09-22-les-khraniteley-contour.md
world_map: assets/maps/world-map-echo-dawn.jpg
borders_ref: assets/maps/les-khraniteley-borders-from-world.jpg
contour_ref: assets/maps/les-khraniteley-contour-locked.jpg
terrain_ref: assets/maps/les-khraniteley-map-stage1-1-terrain-locked.jpg
---

# Сверка с картой мира (обязательно)

## Где Лес на карте мира
- **ЮВ материка**, отдельное государство (не Аэлендор, не «Сильванион»).
- На обводке GM (`borders-from-world`): густой лес + **залив с островами** внутри границ; силуэт ≈ «подкова» вокруг залива.
- На zoom-контуре (`contour-locked`): **лес = запад+центр кадра**, **залив = восток** — это мастер-силуэт, не перерисовывать.

Соседи по миру/паспорту (**подписи соседей на карте государства НЕ ставить**):

| Сторона от Леса | Государство на карте мира | Что это значит для геометрии |
|---|---|---|
| **С** | Орден пламенеющей стали | северная кромка = лес/река к Ордену |
| **З** | Королевство Пепельных земель | запад = горы/пепел → **Пепельный Рубеж только здесь** |
| **ЮЗ** | Амират (за хребтом) | юго-запад за горами, не рисовать |
| **СВ** | Элдеринская гавань | коридор гавани → **Восточные Врата** на В/СВ материковом берегу |
| **В / ЮВ** | Хозяйство Болот скорби | восток за границей = топи (не рисовать) |
| **Ю за заливом** | Империя Драконьего Хребта | юг за водой, не рисовать |

## Жёсткие следствия
1. **Пепельный Рубеж = ЗАПАД у хребта**. Не юг у залива.
2. **Силвания + Мировое Древо = глубина лесной суши**. Не на берегу залива.
3. **Восточные Врата = правый край того же материкового леса** у залива. Не через залив, не остров.
4. **Северная Заводь = северный берег залива**, пирс на суше — **отдельная** иконка от Врат.
5. **Серебряный Порог = запад** у гор, отдельно от Рубежа.
6. Снаружи пунктира: пергамент + западные горы слева. Лес не вылезает за пунктир.
7. Острова залива — пейзаж без городских иконок.

---

# Решения мастера (лок)

| Тема | Решение |
|---|---|
| Процесс | База без текста → точные подписи |
| Соседи на карте | **Нет** |
| Регионы | Не обязательны |
| Горы снаружи слева | Оставить |
| Топи | По удобству; без городов в океане |
| Иконки городов | Крупные, читаемые, разные силуэты |
| Атмосфера | Живая карта: тропы, туман, детали берега, не «сухой» плоский лес |

## Whitelist текста (только это)
`Лес Хранителей` · `Силвания` · `Мировое Древо` · `Серебряный Порог` · `Северная Заводь` · `Восточные Врата` · `Пепельный Рубеж`

---

# Промпт B — GenerateImage (атмосфера + крупные иконки)

Reference images:
1. `assets/maps/les-khraniteley-contour-locked.jpg` — silhouette
2. `assets/maps/les-khraniteley-borders-from-world.jpg` — neighbor compass (geometry only)
3. `assets/maps/les-khraniteley-map-stage1-1-terrain-locked.jpg` — terrain fill + parchment outside

```
Hand-painted fantasy parchment STATE MAP of Лес Хранителей, 16:9, classic RPG cartography, rich atmospheric illustration — NOT a dry flat diagram.

WORLD-MAP SILHOUETTE (critical):
• Match contour-locked red dashed border exactly: dense FOREST mainland = west+center; grey-blue BAY with ~5 small forested islands = east.
• Outside dashed border: aged parchment + western mountains on far-left edge only. ZERO forest/water leaking outside. No neighbor countries drawn. No neighbor name labels.
• Neighbor geometry only: N→Orden, W→Ash Lands, SW→Amirat, NE→Elderrin corridor, E/SE→Swamps beyond border, S across bay→Dragon Ridge.

ATMOSPHERE & DETAIL (make it feel alive — this is mandatory):
• Varied evergreen canopy: mixed pine heights, mossy clearings, soft mist pockets in hollows, dappled warm light on crowns.
• Winding silver rivers with tiny fords and fern banks; faint dirt pilgrim paths linking the six landmarks.
• Bay: layered shoreline ripples, reed beds, a few tiny fishing skiffs near the northern pier, rocky islets with wind-bent trees, gentle foam.
• Subtle ash dust and warm ochre on western foothills near the mountain fort; cool blue shadow under northern forest.
• Small wildlife hints only (a deer silhouette in a clearing, distant birds over the bay) — no clutter stickers.
• Ornate but glyph-free compass rose; soft parchment grain; painterly ink edges. Mood: sacred living forest kingdom, quiet wonder, not empty.
• Fill ALL interior of the dashed border (forest, river, or bay) — no blank parchment holes inside.

NO TEXT AT ALL: no Cyrillic, Latin, digits, numbered badges, callout circles, or compass letters. Labels added later.

Exactly SIX LARGE, DISTINCT city/landmark ICONS on mainland land only (icons must be obvious settlement marks, big enough to read at a glance; never on bay islands; never floating in open water):

• Силвания — deep CENTER of forest mainland: CAPITAL town cluster — elven wooden halls + silver leaf-in-ring banner above a small plaza clearing. NOT only a tiny seal; show buildings. Not on bay shore.
• Мировое Древо — immediately beside the capital inland: colossal sacred glowing-canopy world tree with visible roots and a ring of standing stones. Distinct from Silvania.
• Серебряный Порог — WEST near mountains: grand silver-stone temple threshold gate with lanterns and a guest road. Separate from the ash fort.
• Пепельный Рубеж — WESTERN foothills INSIDE border against the mountain ridge (toward Ash Lands): stout ash-stained stone keep/fort with watch fire. FORBIDDEN on south bay shore or east.
• Северная Заводь — NORTH bay shore on land: riverside quay town — wooden pier, boats, low warehouses, smoke from a hearth. Separate icon from Eastern Gates.
• Восточные Врата — RIGHTMOST edge of the SAME continuous mainland forest where trees meet the bay (NE corridor toward Elderrin): twin stone gate towers on dirt/grass shore with a road inland. FORBIDDEN: far shore across the bay; islands; inventing a separate eastern peninsula.

Bay islands = scenery trees+earth only, no city icons.
```

---

# Подписи после генерации (код)
Exact whitelist у каждой иконки (не сливать Заводь и Врата):
- Силвания → у столичного кластера
- Мировое Древо → у древа
- Серебряный Порог → западный храм-порог
- Пепельный Рубеж → западный форт у хребта
- Северная Заводь → северный пирс/пристань
- Восточные Врата → восточные башни на материковом берегу

Output: `assets/maps/les-khraniteley-map-v12.jpg`
