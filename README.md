# Эхо рассвета

Кампания и мир D&D. Этот репозиторий — единый источник правды: лор, локации, NPC, сессии, сюжет и хоумбрю.

## Агенты и скилы

Полный порядок и пути: **[`AGENTS.md`](AGENTS.md)**.

| # | Скил | Папка |
|---|---|---|
| 0 | Оркестратор (entrypoint) | `.cursor/skills/echo-dawn-orchestrator/` |
| 1 | Канон | `.cursor/skills/echo-dawn-canon/` |
| 2 | Локации | `.cursor/skills/echo-dawn-location/` |
| 3 | Побочные квесты | `.cursor/skills/echo-dawn-quest-side/` |
| 4 | Основные квесты | `.cursor/skills/echo-dawn-quest-main/` |
| 5 | Государства | `.cursor/skills/echo-dawn-state/` |
| 6 | Артефакты | `.cursor/skills/echo-dawn-artifact/` |
| 7 | Главы книг | `.cursor/skills/echo-dawn-book-chapter/` |

Оркестратор по умолчанию первый: ритуал канона → `campaign/prep/orchestrator/<slug>-plan.md` → **ok мастера** → узкие скилы.

Скилы **не включаются сами по кнопке**: агент выбирает их по `description` в `SKILL.md` и по `AGENTS.md`. Чтобы отрабатывали стабильно — пиши задачу через оркестратор / «по AGENTS» / называй скил.

## Как пользоваться

1. **Канон** — то, что уже произошло или установлено в мире, лежит в `world/` и `campaign/`.
2. **Черновики** — идеи, варианты, «может быть» — в `drafts/`.
3. **Сессии** — отчёты и заметки после игры — в `campaign/sessions/`.
4. При конфликте версий побеждает запись в каноне; черновик не перетирает канон молча.

## Структура

```
.cursor/skills/ # скилы агента (см. AGENTS.md)
world/          # мир как таковой
  lore/         # космология, магия, народы, культура
  history/      # хронология и эпохи
  locations/    # места, регионы, города + states/
  artifacts/    # карточки/сеты/roster
  player-books/ # книги игроков + gm-codex
  factions/     # организации и силы
  npcs/         # важные персонажи мира
campaign/       # то, что связано с партией и игрой
  party/        # персонажи игроков
  plot/         # арки, крючки, тайны, локи/опросы
  prep/         # заготовки (locations, arcs, orchestrator…)
  sessions/     # лог сессий
rules/          # хоумбрю и дом. правила
drafts/         # незафиксированные идеи
templates/      # шаблоны новых записей
```

## Соглашения

- Один файл — одна сущность (локация, NPC, фракция, сессия).
- Имена файлов: `kebab-case.md` (латиница или транслит).
- В начале файла — короткий YAML front matter (`status`, `tags`, ссылки).
- Ссылки между сущностями — относительные markdown-ссылки.
- Статусы: `canon` | `active` | `draft` | `secret` | `retired`.

## Быстрый старт

Новые записи копируй из `templates/`. Канон правим осознанно; сомнения — сначала в `drafts/`.

Оглавление канона: [`CANON.md`](CANON.md).  
Агенты/скилы: [`AGENTS.md`](AGENTS.md).  
Правила импорта из Qwen: [`SOURCES.md`](SOURCES.md).  
Полные тексты шарингов лежат в `drafts/imports/` — на ссылки не опираемся.
