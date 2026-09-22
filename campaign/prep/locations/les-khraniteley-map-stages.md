---
title: "Лес Хранителей — карта: этапы поверх locked-контура"
status: prep
contour_lock: campaign/plot/canon-lock-2026-09-22-les-khraniteley-contour.md
stage1_1_lock: campaign/plot/canon-lock-2026-09-22-les-khraniteley-stage1-1-terrain.md
---

# Этапы карты Леса

База: [`assets/maps/les-khraniteley-contour-locked.jpg`](../../assets/maps/les-khraniteley-contour-locked.jpg) — **не менять силуэт**.

| Этап | Файл | Статус | Что |
|---|---|---|---|
| 0 | `les-khraniteley-contour-locked.jpg` | **locked** | контур без подписей |
| 1 | `les-khraniteley-map-stage1-bg.jpg` | **wait-ok** | пергамент снаружи |
| 1.1 | `les-khraniteley-map-stage1-1-terrain-locked.jpg` | **draft / superseded** | старый патч-композит — не править; ждём rebuild |
| 1.1 prompt | [`les-khraniteley-map-prompt-1-1.md`](les-khraniteley-map-prompt-1-1.md) | **wait-ok** | **полный** промпт: рельеф + регионы + города + соседи + оформление |
| full map | `les-khraniteley-map.jpg` | pending | одна генерация после ok на промпт → lock |
| 2 / 3 | — | cancelled | не отдельными этапами: всё в одном промпте |

Промпт полной карты: [`les-khraniteley-map-prompt-1-1.md`](les-khraniteley-map-prompt-1-1.md).  
Старый патч 1.1: [`canon-lock-…-stage1-1-terrain.md`](../../plot/canon-lock-2026-09-22-les-khraniteley-stage1-1-terrain.md) — superseded.
