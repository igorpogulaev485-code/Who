---
title: "Побочные квесты — как устроено в репо"
status: prep
---

# Побочки «Эхо рассвета»

Скил: [`echo-dawn-quest-side`](../../../.cursor/skills/echo-dawn-quest-side/SKILL.md)

## Правило двух слоёв

| Слой | Где | Что |
|---|---|---|
| **Якорь** | `playbook.md` локации | id, крючок в 1 строку, кто выдаёт, ссылка на файл |
| **Полный текст** | `campaign/prep/locations/<slug>/quests/q-*.md` | hook, пути, DC, награды, liveliness |

**Основные** (`mq-*`) — отдельно: `campaign/prep/arcs/<arc>/quests/` · скил `echo-dawn-quest-main`.

## Статус по локациям арки 3 (сессия 2 · двери)

| Дверь / локация | Якоря side | Полные q-* | arc_link |
|---|---|---|---|
| **A** · Купель (ворота) | q-kupel-01…02 | [`lunnyy-most/quests/`](../locations/lunnyy-most/quests/) | standalone / soft-arc |
| **A** · Маяк душ | q-mayak-01…03 | [`mayak-dush/quests/`](../locations/mayak-dush/quests/) | standalone / soft-arc |
| **D** · Серебряный Порог | q-porog-01…03 | **есть** | soft-arc |
| **F** · Серый Причал | q-prichal-01…03 | **есть** | standalone / soft-arc |
| Лунный мост · камень | q-portal-stone | **есть** (вход mq-03) | hard-arc к двери D |

Все side сессии 2 (**кроме** q-portal-stone) **не** двигают основной spine соответствующего mq.

## За стол

Партия в локации → смотри якоря в playbook → при взятии открывай полный `q-*.md` (или `quests-bundle.md`).
