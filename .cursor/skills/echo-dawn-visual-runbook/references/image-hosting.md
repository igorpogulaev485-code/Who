---
title: Image hosting for visual runbooks
status: reference
skill: echo-dawn-visual-runbook
---

# Хостинг картинок для ранбука

## Жёсткое правило (2026-09-28)

Репозиторий **публичный**. В главах ранбука — только:

```text
https://raw.githubusercontent.com/igorpogulaev485-code/Who/<branch>/assets/...
```

+ строка **⬇ скачать** с тем же URL.

**Не использовать:** iili.io, litterbox, catbox, imgur и прочие сторонние хосты.

Локальные relative `../assets/…` в Preview Cursor по-прежнему часто ломаются — поэтому delivery = **raw GitHub HTTPS**, исходник лежит в `assets/`.

---

## Почему так

| Метод | Результат |
|---|---|
| Relative `../assets` | часто пусто в Preview |
| data URI | вырезаются |
| iili / litter | больше не нужны; ссылки протухают |
| **raw.githubusercontent.com** (public repo) | работает в Preview + ⬇ |

Пока файл только на feature-ветке — в URL указывай **эту ветку**. После merge в `main` — замени сегмент ветки на `main` (или перегенерируй `image-urls.json`).

---

## Пайплайн

1. Исходник в git: `assets/images/…` или `assets/maps/…` (для ранбука также зеркало `assets/images/runbook/`).  
2. Запись в `campaign/prep/arc3-visual-book/image-urls.json`: ключ → raw URL.  
3. В md главах — только raw URL.  
4. Проверка: `curl -sI "<url>"` → 200 + `content-type: image/*`.

### Обязательный блок кадра

```markdown
![Короткое имя](https://raw.githubusercontent.com/igorpogulaev485-code/Who/<branch>/assets/images/….jpg)

> **Кадр:** Короткое имя · [⬇ скачать](https://raw.githubusercontent.com/igorpogulaev485-code/Who/<branch>/assets/images/….jpg)
```
