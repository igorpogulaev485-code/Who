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
| **В / ЮВ** | Хозяйство Болот скорби | восток за границей = топи (не рисовать); залив не «открытый океан навсегда» |
| **Ю за заливом** | Империя Драконьего Хребта | юг за водой, не рисовать |

## Жёсткие следствия (где раньше «уезжало»)
1. **Пепельный Рубеж = ЗАПАД у хребта** (сторона Пепельных земель). **Запрещено** ставить его на юг у залива / к Драконьему Хребту.
2. **Силвания + Мировое Древо = глубина лесной суши** (центр западной половины). **Не** на берегу залива.
3. **Восточные Врата = восточный край МАТЕРИКОВОГО леса** (грязь/трава у воды, коридор к Элдеринской гавани). **Не** остров посреди залива, **не** открытая вода.
4. **Северная Заводь = северный берег залива** (сторона Ордена), пирс на суше.
5. **Серебряный Порог = запад леса** у гор (гостевой вход), отдельно от Рубежа.
6. **Снаружи пунктира:** только пергамент + западные горы у левого края. **Ноль** леса/воды/островов снаружи. Лес не должен «вылезать» за северный пунктир.
7. Острова залива — пейзаж (земля+деревья), без городских иконок.

---

# Решения мастера (лок)

| Тема | Решение |
|---|---|
| Процесс | База без текста → точные подписи |
| Соседи на карте | **Нет** |
| Регионы | Не обязательны (по умолчанию не подписывать) |
| Горы снаружи слева | Оставить |
| Топи | По удобству; без городов в океане |

## Whitelist текста (только это)
`Лес Хранителей` · `Силвания` · `Мировое Древо` · `Серебряный Порог` · `Северная Заводь` · `Восточные Врата` · `Пепельный Рубеж`

---

# Промпт B — GenerateImage (сверка с миром)

Reference images (must match silhouette):
1. `assets/maps/les-khraniteley-contour-locked.jpg` — dashed border shape; forest west / bay east
2. `assets/maps/les-khraniteley-borders-from-world.jpg` — world-map neighbor compass (geometry only)
3. `assets/maps/les-khraniteley-map-stage1-1-terrain-locked.jpg` — terrain fill style, parchment outside

```
Brand-new fantasy parchment state map of Лес Хранителей, 16:9, top-down classic RPG cartography, single clean pass.

WORLD-MAP SYNC (critical — do not invent a new country shape):
This state is the southeast mainland forest kingdom on the world map. Zoom map orientation:
• WEST + CENTER of the FRAME = dense evergreen FOREST mainland (country heart).
• EAST of the FRAME = large grey-blue BAY with ~5 small scenic forested islands (earth under trees).
• Red dashed border silhouette MUST match the contour-locked reference (forest west / bay east). Same outline, same bay bite. Do NOT redraw as Aelendor. Do NOT invent a new blob.
• Neighbor compass (geometry only, NO neighbor name labels anywhere):
  North→Orden (forest/river). West→Ash Lands beyond mountains. SW→Amirat beyond ridge.
  NE→Elderrin Harbor corridor. East/SE→Swamps of Sorrow beyond border. South across bay→Dragon Ridge.

HARD CLIP (prevent leaks):
• ALL forest, rivers, bay water, and islands STRICTLY INSIDE the red dashed border.
• ZERO trees/terrain spilling north, south, or east outside the dashed line.
• Outside the dashed border: aged parchment only, PLUS western mountains along the far-left edge (keep those mountains).
• Do NOT paint neighboring countries’ terrains. Do NOT paint swamp nation or harbor nation.

NO TEXT AT ALL (no Cyrillic, no Latin, no junk letters on compass). Labels added later. Compass rose decorative only, no letter glyphs.

Exactly SIX landmark icons, all ON MAINLAND LAND (never in open bay water, never on bay islands):

1) Силвания — CENTER of the forest mainland (western half of the map, deep in trees): large silver leaf-in-ring capital emblem. NOT on the bay shore.
2) Мировое Древо — immediately beside the capital, still deep in forest interior: giant sacred tree. NOT on the bay shore.
3) Серебряный Порог — WEST side of the forest near the mountains: stone temple/threshold gate (guest entrance from the west). Separate from the Ash fort.
4) Пепельный Рубеж — WESTERN foothills INSIDE the border, CLOSE TO THE MOUNTAIN RIDGE (toward Ash Lands / west). Stone mountain fort. FORBIDDEN: south shore of the bay, east, or Dragon-Ridge side.
5) Северная Заводь — NORTH shore where forest/river meets the bay (toward Orden): wooden pier on the BANK, feet on land.
6) Восточные Врата — EASTERN tip of the MAINLAND forest coast facing the bay (corridor toward Elderrin Harbor / NE): stone gate standing on dirt/grass shore at the rightmost edge of continuous forest land. NOT on an ocean island. NOT floating in open water. NOT at the far empty eastern water tip with no mainland.

Bay islands: trees + earth only — no city icons.
Optional slight marsh tint on southeast mainland fringe only — no swamp cities in water.
```

---

# Подписи после генерации (код)
Exact whitelist у иконок:
- Силвания → у листа в центре леса
- Мировое Древо → у древа рядом
- Серебряный Порог → запад у гор
- Пепельный Рубеж → запад у хребта (не юг!)
- Северная Заводь → северный берег залива на суше
- Восточные Врата → восточный материковый берег леса

Output: `assets/maps/les-khraniteley-map-v10.jpg`
