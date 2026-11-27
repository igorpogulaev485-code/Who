---
id: orch-arc3-quests
title: "План оркестратора — пакет квестов арки 3"
status: in-progress
source: gm-request-2026-09-07
---

# План — квесты арки 3

## Цель

Вызван оркестратор. Старт подготовки 3-й арки через квестовые скилы.

## Шаг 0 — canon

- Ветка: `cursor/quest-skill-arc3-bd87`
- Якоря: арка 3 старт; Лунный мост; оба пути Лес/Разлом; Маэстро мёртв
- Опрос приоритетов: **без ответов** → defaults из канона (волна 5: Разлом×2, Лес, Велиан, похороны)

## Маршрут (по порядку)

| # | Скил | Зачем | Статус |
|---|---|---|---|
| 0 | echo-dawn-canon | Ритуал | done |
| 1 | опрос оркестратора | Приоритеты | **skipped** (ok без ответов → канон-defaults) |
| 2 | echo-dawn-quest-main | Пакет `arc-3` | **done** |
| 3 | echo-dawn-location | Playbook Лунного моста + якоря | **done** (seed) |
| 4 | echo-dawn-quest-side | Побочки хаба | **deferred** (после mains) |
| 5 | правка prep | stale-баннер `arc3-session-01` | **done** |

## Опросы

Пропущены по ok мастера без заполнения HTML. Defaults зафиксированы в `mains-overview.md`.

## Файлы-результаты

- [x] `campaign/prep/arcs/arc-3/mains-overview.md`
- [x] `campaign/prep/arcs/arc-3/quests/mq-01…05-*.md`
- [x] `campaign/prep/locations/lunnyy-most/playbook.md` (якоря)
- [ ] побочки `lunnyy-most/quests/` — позже
- [x] stale-баннер `arc3-session-01-lunnyy-most.md`
- [ ] docx overview — по запросу

## Не делаем в этом плане

- Новый квестовый скил
- Полный A–T
- Побочки (шаг 4 отложен)
- Канон внутренности Разлома без отдельных фактов мастера

---

Следующий ok: побочки хаба / docx / углубить один mq под ближайшую сессию.
