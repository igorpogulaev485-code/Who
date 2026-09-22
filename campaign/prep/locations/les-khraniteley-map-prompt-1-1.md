---
title: "Лес Хранителей — промпт ПОЛНОЙ карты (один проход)"
status: prep
wait: gm-ok-on-image
contour_lock: campaign/plot/canon-lock-2026-09-22-les-khraniteley-contour.md
passport: world/locations/states/les-khraniteley.md
date: 2026-09-22
note: "Промпт дополнен exact-именами и сторонами света соседей. Генерация v8 — с нуля по этому промпту."
---

# Промпт → одна полная карта государства

## Reference

| # | Файл | Роль |
|---|---|---|
| 1 | `assets/maps/les-khraniteley-contour-locked.jpg` | Жёсткий силуэт: красный пунктир, лес ЗАПАД / залив ВОСТОК, острова, реки, 16:9 |
| 2 | `assets/maps/les-khraniteley-map-stage1-bg.jpg` | Пергамент снаружи; западные горы только у левого края |

Не использовать старые v2–v7 как reference (учат ошибкам подписей и городов в воде).

## Whitelist подписей (ТОЛЬКО эти строки, буква в букву)

### Заголовок
`Лес Хранителей`

### Соседи — снаружи пунктира на пергаменте

| Сторона света | Где на кадре | Точная подпись |
|---|---|---|
| **Север** | над государством, верх кадра | `Орден` |
| **Северо-восток** | верх-право, снаружи | `Элдеринская гавань` |
| **Восток** | право, снаружи | `Болота скорби` |
| **Юг** | под заливом, низ кадра, снаружи | `Драконий Хребет` |
| **Запад** | лево, снаружи | `Пепельные земли` |
| **Юго-запад** | лево-низ за горами, снаружи | `Амират` |

Запрещены любые другие внешние имена (нет «Палевые…», нет выдуманных слов).

### Города / места — ВНУТРИ, только на СУШЕ (иконка + подпись)

| Точная подпись | Где | Иконка |
|---|---|---|
| `Силвания` | север–центр леса (столица) | серебряный лист в кольце, самая крупная |
| `Мировое Древо` | сердце леса | великое древо |
| `Серебряный Порог` | юг леса / входные тропы | храм-порог |
| `Северная Заводь` | север у реки на берегу | пристань |
| `Восточные Врата` | **материковый** берег: где лес слева встречает залив; ноги иконки на земле | каменные ворота |
| `Пепельный Рубеж` | запад у предгорий | форт |

Запрещено: `Сильвания`, `Сильванор`, `Сильванарион`, любые кривые/смешанные написания.

### Регионы — мягкие подписи только на СУШЕ (опционально)

`Сердце Древа` · `Гостевой Порог` · `Круги Бури` · `Зелёные Топи`

`Зелёные Топи` = **ЮВ материковая топь** (влажная суша у берега залива). Не писать на открытой воде. Не ставить города в залив. Острова залива — только пейзаж (земля+деревья), без столиц/ворот.

---

## Промпт A — русский

```
Полная фэнтезийная карта государства, вид сверху, 16:9, государство крупно. Стиль: классическая parchment fantasy cartography, один цельный рисунок.

ЗАГОЛОВОК (точно): Лес Хранителей

СИЛУЭТ: точно как reference contour-locked — красный пунктир; лес на ЗАПАДЕ; большой залив на ВОСТОКЕ; острова в заливе; реки из леса в залив. Не Аэлендор. Не меняй форму границы.

СНАРУЖИ пунктира: пергамент. Горы только у левого края. Ровно шесть подписей соседей на пергаменте, точно так и только так:
• СЕВЕР (верх): Орден
• СЕВЕРО-ВОСТОК (верх-право): Элдеринская гавань
• ВОСТОК (право): Болота скорби
• ЮГ (низ, за заливом): Драконий Хребет
• ЗАПАД (лево): Пепельные земли
• ЮГО-ЗАПАД (лево-низ): Амират
Никаких других внешних названий.

ВНУТРИ: рельеф вплотную к пунктиру; лес З/С; залив В/Ю; острова с землёй под кронами; ЮВ — материковые топи (суша), не океан.

ГОРОДА — шесть иконок ТОЛЬКО НА СУШЕ, подписи точно:
1) Силвания — столица, лист в кольце, север–центр леса
2) Мировое Древо — великое древо, сердце леса
3) Серебряный Порог — храм-порог, юг леса
4) Северная Заводь — пристань на северном берегу реки
5) Восточные Врата — ворота на материковом берегу (лес слева у залива), НЕ в воде
6) Пепельный Рубеж — форт на западе у гор
Мягко на суше: Сердце Древа, Гостевой Порог, Круги Бури, Зелёные Топи (только суша ЮВ).

Подписи не наезжают. Без UI. Компас уместен.
```

---

## Промпт B — English (GenerateImage)

```
Brand-new complete fantasy parchment state map, 16:9, top-down classic RPG cartography, single coherent pass. State large in frame.

TITLE (exact Cyrillic only): Лес Хранителей

HARD SILHOUETTE: match contour-locked reference exactly — red dashed border; dense evergreen FOREST on the WEST; large grey-blue BAY on the EAST with small forested islands that have visible earth; rivers from forest into bay. Not Aelendor. Do not reshape the border.

OUTSIDE the dashed border: aged parchment only. Western mountains only at the far-left edge. Place EXACTLY these six neighbor labels on outside parchment at these compass positions — and NO other outside names at all:
• NORTH (top of frame): Орден
• NORTHEAST (top-right): Элдеринская гавань
• EAST (right): Болота скорби
• SOUTH (bottom, beyond the bay): Драконий Хребет
• WEST (left): Пепельные земли
• SOUTHWEST (bottom-left beyond mountains): Амират
Forbidden outside junk names (do not invent any).

INSIDE: terrain flush to the dashed line; forest W/N; bay E/S; islands = earth + trees scenery only (no capital/gate cities on open water). Southeast = contiguous mainland MARSH LAND (Зелёные Топи) beside the bay shore — NOT a label on open ocean.

EXACTLY SIX settlement icons, ALL ON LAND, exact Cyrillic labels (each once, no overlap):
1) Силвания — CAPITAL, largest, silver leaf-in-ring icon, north-central forest land
2) Мировое Древо — giant sacred tree, forest heart land
3) Серебряный Порог — temple/threshold gate, southern forest land
4) Северная Заводь — pier on northern riverbank land
5) Восточные Врата — stone gate on MAINLAND forest shore where land meets bay from the west — feet on dirt, NEVER standing in open water, NEVER on the far-right open bay
6) Пепельный Рубеж — fort in western foothills land

Optional soft land-only region labels (exact): Сердце Древа, Гостевой Порог, Круги Бури, Зелёные Топи (SE mainland marsh only).
Forbidden spellings: Сильвания, Сильванор, Сильванарион; any garbled Cyrillic; any extra country/city names.
No overlapping text. Compass rose OK. No UI, no watermark, no Latin replacing Russian names.
```

---

## Генерация

1. Reference: **только** `contour-locked` + `stage1-bg`.  
2. Aspect **16:9**.  
3. Промпт B.  
4. Файл: `assets/maps/les-khraniteley-map-v8.jpg`.  
5. Ok мастера → `les-khraniteley-map.jpg` + lock.
