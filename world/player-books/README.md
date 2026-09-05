---
title: Книги для игроков
status: active
---

# Книги для игроков

Собраны мастером для выдачи за столом.  
Скил глав: [`.cursor/skills/echo-dawn-book-chapter/SKILL.md`](../../.cursor/skills/echo-dawn-book-chapter/SKILL.md) · лок: [`skill-lock-book-chapter-v1.md`](../../campaign/plot/skill-lock-book-chapter-v1.md).

## Правило канона

В оглавлении Telegraph открытая глава помечена фразой **«Вы изучили эту главу»** (ссылка).  
Текст по этой ссылке = **жёсткий канон**. Закрытые пункты без ссылки — **не канон** (prep только по запросу).

Изучение за столом: партия **тратит время** на прочтение.

## Структура (канон скила)

```
world/player-books/<book>/
  README.md          # индекс книги
  chapters/          # главы этой книги
gm-codex/            # скрытый лор мастера
```

| Книга | Папка | Голос |
|---|---|---|
| Зеркало Памяти | [`zerkalo-pamyati/`](zerkalo-pamyati/) | хроника |
| Трактат о флоре | [`traktat-o-flore/`](traktat-o-flore/) | травник/алхимик |
| Энциклопедия драконов | [`entsiklopediya-drakonov/`](entsiklopediya-drakonov/) | зоологический справочник |
| GM-кодексы | [`gm-codex/`](gm-codex/) | только мастер |

**Наследие:** общие [`chapters/`](chapters/) и корневые индексы (`zerkalo-pamyati.md` и т.д.) ещё живут; при правке главы — мигрировать в папку книги.

## Сборники (Telegraph)

| Книга | Оглавление | Индекс открытых |
|---|---|---|
| **Зеркало Памяти** | https://telegra.ph/ZERKALO-PAMYATI-HRONIKI-RAZORVANNOGO-MIRA-12-05-3 | [`zerkalo-pamyati.md`](zerkalo-pamyati.md) |
| **Трактат о флоре** | https://telegra.ph/Traktat-o-Flore-Planov-i-Predelov-12-08 | [`traktat-o-flore-planov.md`](traktat-o-flore-planov.md) |
| **Энциклопедия драконов** | https://telegra.ph/EHNCIKLOPEDIYA-DRAKONOV-POLNYJ-ZOOLOGICHESKIJ-SPRAVOCHNIK-05-14 | [`entsiklopediya-drakonov.md`](entsiklopediya-drakonov.md) |

Сырой HTML: [`telegra-raw/`](telegra-raw/)
