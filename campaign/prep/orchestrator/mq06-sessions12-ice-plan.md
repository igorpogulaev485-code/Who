---
id: orch-mq06-sessions12-ice
title: "План — mq-06 дверь E: льды (сессия 2)"
status: wait-ok
source: gm-2026-09-22 («Дальше пошли во льда»)
---

# План — дверь E · льды

## Цель

Как A/F/D: **сессия 1 общая** уже есть → полный скрипт **сессии 2** для двери **E** (mq-06, старт с **Ледяного Союза / Лианэи / Доспехов смерти**), по методу «как раньше».

## Шаг 0 — canon

- Ветка: `cursor/quest-skill-arc3-bd87`
- Сессия 1: [`../arcs/arc-3/quests/mq-01-sessions-1-2-detail.md`](../arcs/arc-3/quests/mq-01-sessions-1-2-detail.md) (дверь E уже названа)
- mq-06 карточка: [`../arcs/arc-3/quests/mq-06-tri-na-zemle.md`](../arcs/arc-3/quests/mq-06-tri-na-zemle.md)
- Лианэя + видение: [`../../../world/npcs/lianeya.md`](../../../world/npcs/lianeya.md) · [`../briefs/elarion-vision-lianeya.md`](../briefs/elarion-vision-lianeya.md)
- L1+L2: Доспехи = антенна Кардиана; он причастен к воскрешению ([`../../plot/canon-lock-2026-09-22-mq04-dead-plane-be.md`](../../plot/canon-lock-2026-09-22-mq04-dead-plane-be.md))
- Готовы с.2: **A**, **F**, **D**. Нет: **B**, **C**, **E** ← берём E
- Дырки: клифф с.2; как едем; кто толкает; насколько рано Лианэя; только льды или меню тройки

## Маршрут (после ok + ответов опроса)

| # | Скил | Зачем | Статус |
|---|---|---|---|
| 1 | echo-dawn-quest-main | spine mq-06 акт A (~20 битов льдов) + скрипт `mq-06-sessions-2-door-e.md` | blocked-survey |
| 2 | echo-dawn-location | якорь первой ледяной локации (если опрос скажет «нужен playbook») | wait |
| 3 | echo-dawn-quest-side | побочки на границе льдов — только по запросу | skip-default |

## Опросы

[`../../plot/survey-mq06-sessions12-holes.md`](../../plot/survey-mq06-sessions12-holes.md) (**v2**) · HTML: [`../../plot/survey-mq06-sessions12-holes.html`](../../plot/survey-mq06-sessions12-holes.html)

## Файлы-результаты (после ответов)

- [ ] `campaign/plot/canon-lock-2026-09-22-next-path-mq06-ice.md` (лок выбора E)
- [ ] `campaign/prep/arcs/arc-3/quests/mq-06-ice-spine-20.md` (если depth = +spine)
- [ ] `campaign/prep/arcs/arc-3/quests/mq-06-sessions-2-door-e.md`
- [ ] sync `mains-overview` / open-threads

## Не делаем в этом плане

- Встреча-босс с Лианэей как финал с.2 (если опрос не выберет иное)
- Полные акты B/C (Хребет / Пыль) в той же сессии 2
- Спойлер «Кардиан воскресил» игрокам до стола
- Паспорт Ледяного Союза целиком

---

**Жду ok + ответы опроса** → пишем spine/скрипт с.2.
