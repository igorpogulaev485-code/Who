---
id: orch-serebryanyy-porog-city
title: "План — регион Эллуэнар: город Серебряный Порог (полный)"
status: wait-ok
source: gm-2026-09-28
branch: cursor/serebryanyy-porog-city-bd87
survey: ../../plot/survey-serebryanyy-porog-city-v1.md
---

# План — Серебряный Порог (город) + дальше регион

## Цель

Подготовить **Эллуэнар** к сессии внутри региона. Старт — **город Серебряный Порог**: крупный хаб с плотными активностями, чтобы партия **захотела задержаться**, если зайдёт. Дальше (после города) — остальной регион по вилке Силвания / Древо / монастырь (Рубеж).

## Шаг 0 — canon

- Ветка: `cursor/serebryanyy-porog-city-bd87` ← `cursor/les-porozhe-region-bd87`
- Сейчас: партия у **Храма** Порога; репутация **−4**; тик — **порча/некромантия** у портала; вилка **Силвания / Малфурион / монастырь (слух, Рубеж)**
- Есть: карта Эллуэнар **LOCKED v11**; seed города [`../locations/gorod-serebryanyy-porog/`](../locations/gorod-serebryanyy-porog/); site Храма [`../locations/serebryanyy-porog/`](../locations/serebryanyy-porog/)
- Дырки → опрос [`../../plot/survey-serebryanyy-porog-city-v1.md`](../../plot/survey-serebryanyy-porog-city-v1.md)

## Маршрут (по порядку)

| # | Скил | Зачем | Статус |
|---|---|---|---|
| 1 | `echo-dawn-location` | Город Порог: seed → **полный** playbook (районы / места / НПС / 1к6 / якоря), ± карта города | `blocked-survey` |
| 2 | `echo-dawn-quest-side` | Порча у портала (+ другие якоря города по опросу) | `wait-ok` |
| 3 | `echo-dawn-location` | След. точки региона (Тириэлас / деревни / места / seed Силвании…) — **после** города, отдельный мини-план | `wait-ok` |
| 4 | `echo-dawn-location` / later | Древо · монастырь (Рубеж) — не в этой волне текста города | `wait-ok` |

## Опросы

Стыки масштаба/тона/−4/порчи/карты: [`survey-serebryanyy-porog-city-v1`](../../plot/survey-serebryanyy-porog-city-v1.md).

## Файлы-результаты (после ok + ответов)

- [ ] `campaign/prep/locations/gorod-serebryanyy-porog/playbook.md` (+ docx) — полная глубина
- [ ] `npc-registry.md` без дублей
- [ ] README масштаб обновлён
- [ ] опц. numbered map + каталог мест
- [ ] лок ответов опроса
- [ ] якоря квестов; полные side — шаг 2

## Не делаем в этом плане

- Полные тексты квестов до шага 2  
- Playbook Силвании / Древа / монастыря (только порядок в опросе G)  
- Перерисовка региональной карты v11  
- Канон «партия уже в городе» — они у Храма, пока не сыграли вход  

---

**Жду ok + ответы опроса** перед шагом 1.
