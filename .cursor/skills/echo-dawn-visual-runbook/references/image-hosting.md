---
title: Image hosting for visual runbooks
status: reference
skill: echo-dawn-visual-runbook
---

# Хостинг картинок для ранбука

## Жёсткое правило

В markdown главах ранбука для Preview допустим **только** публичный URL вида:

```text
https://iili.io/<id>.jpg
```

(или другой стабильный HTTPS image host с прямым `Content-Type: image/*`).

Локальные пути, relative markdown links на `assets/`, raw GitHub blob без raw-content, data URI — **не использовать** в главах книги.

---

## Почему локальное не работает (проверено)

| Метод | Симптом | Причина |
|---|---|---|
| `![](../assets/images/x.png)` | Пустая рамка / broken | Preview sandbox ≠ cwd репо; глубина главы ломает относительные пути |
| Править на `../../../` | Иногда мелькнет, потом снова нет | Хрупко; разные главы на разной глубине |
| Symlink `chapters/media` → assets | Не видно | Игнор / не резолв в preview |
| `data:image/jpeg;base64,…` | Картинка исчезает из md | Рендерер/санитайзер вырезает data URI |
| `file://` / «открой скачанный png» | Мастер страдает | Нет второго экрана-потока; не git-friendly |
| GitHub `blob/…` HTML страница | Не картинка | Нужен raw URL; всё равно auth/CORS сюрпризы |
| Встроенный INDEX.html | Путаница вкладок | Расходится с md; «старый INDEX» |

---

## Рабочий пайплайн (Arc 3)

### 1. Исходник в репо

```text
assets/images/.../frame.png   # или .jpg
assets/maps/...-map.jpg
```

Хранить исходники в git **обязательно** (канон ассета). HTTPS — только delivery для Preview.

### 2. Починка формата

Если файл называется `.png`, а внутри JPEG:

```bash
python3 - <<'PY'
from PIL import Image
im = Image.open("in.png").convert("RGB")
im.save("out.jpg", quality=92)
PY
```

Или перезалить правильный MIME.

### 3. Заливка

Предпочтительно: **freeimage.host** → короткие ссылки `iili.io`.

В облачной среде:

- catbox / 0x0 иногда **blocked** — не застревать, сразу другой хост;  
- нужны прямые ссылки на байты картинки, не страница просмотра;  
- после upload проверить:

```bash
curl -sI "https://iili.io/XXXX.jpg" | head
# ждать HTTP/2 200 и content-type: image/jpeg (или png)
```

### 4. Реестр

`campaign/prep/<book>/image-urls.json`:

```json
{
  "media/funeral-a-city-establishing.png": "https://iili.io/nAC37st.jpg",
  "media/funeral-a-city-establishing.jpg": "https://iili.io/nAC37st.jpg"
}
```

- Ключ = стабильный логический путь (можно дублировать png/jpg на один URL).  
- Значение = **канонический** HTTPS для вставки в md.  
- Карты можно держать отдельно (`map-urls.json`) или в том же файле с префиксом `maps/`.

### 5. Вставка в главу

```markdown
![Утро в Кузнице Фиалки](https://iili.io/nACF49f.jpg)

> **Кадр:** Утро в Кузнице Фиалки · [⬇ скачать](https://iili.io/nACF49f.jpg)
```

- Alt и подпись **по-русски**, коротко.  
- URL в `![…]` и в ⬇ **идентичны**.  
- Не оборачивать в HTML `<img>` без нужды (md достаточно).

### 6. Портрет + речь

```markdown
#### Тандил

![Тандил](https://iili.io/…)

> **Кадр:** Тандил · [⬇ скачать](https://iili.io/…)

**Сказать:**

> Реплика этого НПС…
```

Не собирать все речи в конец главы.

---

## Массовая замена

Если URL переехали:

1. Обновить `image-urls.json`.  
2. Скриптом пройти `chapters/*.md` и заменить старые URL.  
3. Снова curl-проверить выборку (все или ≥1 на главу).

Не оставлять смесь старых local paths и новых HTTPS в одной главе.

---

## Второй экран (контракт UX)

1. Ноутбук: Cursor Preview главы.  
2. Клик **⬇ скачать** / открыть URL → планшет / второй монитор / TV.  
3. Игроки видят лицо/карту; мастер читает текст с Preview.

Поэтому ⬇ — не «nice to have», а **обязательный** элемент кадра.

---

## Кэш / вкладки

После смены URL или структуры книги:

> Закрой старые вкладки Preview и открой файл заново.

Иначе мастер смотрит закэшированный broken state и думает, что фикс не сработал.

---

## Что можно хранить только локально

- Сырьё генерации, отвергнутые варианты, PSD/исходники.  
- Промпты (`assets/prompts/`).  
- Планы визуала.

В **главах ранбука** — нет: только HTTPS из реестра.

---

## Запасные хосты

Если iili/freeimage падает:

1. Другой публичный image host с **прямым** URL.  
2. Обновить реестр + главы.  
3. Зафиксировать в коммите, какой хост каноничен сейчас.

Не плодить три хоста на одну книгу без миграции.

---

## Инцидент 2026-09-27 · CDN `iili.io` (весь ранбук)

Симптом: Preview / curl на `https://iili.io/<id>.jpg` — **таймаут**, 0 байт.  
Freeimage HTML жив, upload API — `Internal upload error`.

**Обход (весь Arc 3 visual book + UX-копия):** все кадры перезалиты на **litterbox**  
`https://litter.catbox.moe/…` (TTL **168h / 7 дней**). Реестр: `campaign/prep/arc3-visual-book/image-urls.json`.  
Исходники — `assets/images/**` и `assets/maps/**` (JPEG из git `a3b150b` восстановлены).

Пока iili мёртв — **не** возвращать URL на iili без свежего `curl` 200.  
До истечения TTL: перезалить на постоянный хост или снова на litterbox с assets.
