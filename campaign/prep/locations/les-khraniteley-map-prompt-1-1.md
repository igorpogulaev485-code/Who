---
title: "Лес Хранителей — промпт единой карты (этап 1.1 rebuild)"
status: prep
wait: gm-ok-on-prompt
contour_lock: campaign/plot/canon-lock-2026-09-22-les-khraniteley-contour.md
date: 2026-09-22
note: "Картинку НЕ генерировать, пока мастер не окнет промпт."
---

# Промпт → одна верная картинка (без патчей)

## Зачем

Предыдущий 1.1 собирался правками уже готового JPG → швы, острова без земли, утечки рельефа наружу.  
Новый путь: **один промпт + reference (locked contour) → одна цельная карта → ok → lock**.

Старый `les-khraniteley-map-stage1-1-terrain-locked.jpg` считать **черновиком**; не патчить. После ok на промпт и генерацию — новый lock.

## Reference (обязательно приложить)

| # | Файл | Роль в промпте |
|---|---|---|
| 1 | `assets/maps/les-khraniteley-contour-locked.jpg` | **Жёсткий эталон силуэта** — красный пунктир, лес З / залив В, острова, реки, кадр 16:9 |
| 2 | `assets/maps/les-khraniteley-map-stage1-bg.jpg` | Эталон **пергамента снаружи** (текстура бумаги; западные горы у края — как на этом файле, не размазывать по всему фону) |
| 3 | *(опц.)* `assets/maps/les-khraniteley-borders-from-world.jpg` | Только если силуэт «плывёт» — напоминание формы с карты мира |

Не прикладывать: старый `…-terrain-locked.jpg`, `…-gaps-marked.jpg` — они учат модель неправильным артефактам.

## Чеклист проверки промпта (до генерации)

- [ ] Силуэт = locked, не Аэлендор, не новая клякса  
- [ ] 16:9, государство крупно  
- [ ] Снаружи — пергамент (не залитый лес/вода/земля по всему фону)  
- [ ] Внутри — рельеф **вплотную** к пунктиру (нет полос пергамента внутри)  
- [ ] Запад/север — лес; восток/юг — залив; острова **с землёй** под кронами  
- [ ] Реки как на locked  
- [ ] Без подписей соседей / городов / UI  
- [ ] Стиль: fantasy cartography на пергаменте (иконки сосен, рябь у берега)

---

## Промпт A — русский (для чтения / правки мастером)

```
Фэнтезийная карта государства «Лес Хранителей», вид сверху, кадр 16:9, государство занимает почти весь кадр.

ЖЁСТКОЕ ПРАВИЛО СИЛУЭТА: повтори ТОЧНО красный пунктирный контур и композицию с reference «contour-locked». Не меняй форму границы, не сглаживай, не рисуй силуэт Аэлендора, не сдвигай острова и устья рек. Красный пунктир остаётся верхней обводкой государства.

СНАРУЖИ красного пунктира: только текстурированный пергамент / старая бумага (как на reference stage1-bg). Не заливай снаружи лесом, водой или землёй. Допустимы лишь западные горы у самого левого края, как на stage1-bg — они не должны расползаться по всему фону.

ВНУТРИ красного пунктира — единый цельный рельеф без дыр пергамента:
• запад и север: густой хвойный лес (иконки елей), рельеф доходит вплотную до пунктира;
• западный край у границы: предгорья, согласованные с locked;
• восток и юг: большой залив серо-голубой воды с лёгкой рябью у берегов; вода доходит вплотную до пунктира (без песчаной «дыры» пергамента между водой и границей);
• острова в заливе: у каждого видна ЗЕМЛЯ (коричневый/песчаный берег и грунт), а зелёные кроны сидят НА земле, не парят на воде;
• реки через лес — как на locked, впадают в залив.

Стиль: классическая fantasy cartography на пергаменте, единый проход, без швов, без коллажа, без UI, без текста, без названий соседей и городов.
```

---

## Промпт B — English (для GenerateImage / той же модели)

```
Fantasy RPG regional state map, top-down cartography, 16:9, the state fills most of the frame.

HARD SILHOUETTE LOCK: match EXACTLY the red dashed border shape and layout from the contour-locked reference. Do not reshape, smooth, or redraw the border. Do not use an Aelendor-like silhouette. Keep the same island positions and river mouths. Keep the red dashed line as the top border stroke of the state.

OUTSIDE the red dashed border: only aged parchment / paper texture (like stage1-bg reference). No forest, water, or ground fill outside the border. Western mountains may appear only at the far-left edge as in stage1-bg — do not spread terrain across the whole outside.

INSIDE the red dashed border — one continuous terrain fill with ZERO parchment holes:
• west and north: dense evergreen forest (pine icons), terrain flush to the dashed line;
• western edge: foothills matching the locked reference;
• east and south: large grey-blue bay with subtle shoreline ripples; water flush to the dashed line (no parchment strip between water and border);
• bay islands: each has visible EARTH (brown/tan soil and a thin sandy shore) with green tree canopy ON TOP of the land — not floating green blobs on water;
• rivers through the forest as in the locked reference, emptying into the bay.

Style: classic fantasy parchment cartography, single coherent pass, no seams, no collage, no UI, no text, no neighbor or city labels.
```

---

## Как генерировать после ok (не раньше)

1. Reference: `contour-locked` + `stage1-bg`.  
2. Aspect: **16:9**.  
3. Промпт: **B** (или A, если модель лучше на RU).  
4. Сохранить как новый файл, например `les-khraniteley-map-stage1-1-terrain-v2.jpg` — **не** перезаписывать contour-locked.  
5. Мастер смотрит; при ok → новый canon-lock 1.1 на v2 (старый terrain-locked пометить superseded).

## Открытые решения для мастера (в промпте уже заложено default)

| Вопрос | Default в промпте | Если иначе — правим промпт до генерации |
|---|---|---|
| Западные горы снаружи | только у левого края, как stage1-bg | «снаружи вообще только пергамент, без гор» |
| Песчаные пляжи у материкового берега залива | тонкая кромка ок, но не полоса пергамента до пунктира | вода/лес строго flush без пляжа |
| Число/форма островов | как на contour-locked | — |
