---
title: Лок скила — визуальный ранбук v1
status: locked
tags: [skill-lock, visual-runbook, arc3]
date: 2026-09-23
source: gm-chat-arc3-session1-visuals + postmortem
---

# Лок — echo-dawn-visual-runbook v1

Зафиксировано по итогам пайплайна `campaign/prep/arc3-visual-book/` (2026-09).

## Продукт

1. Ранбук = markdown-книга для **ведения за столом**, не галерея assets.  
2. Эталон структуры: хаб → двери → галерея → справочник (карты / вставки / playbook / spine / локи).  
3. Одна дверь за вечер = один файл главы.

## Визуал и доставка

4. Тон хаба Лунного моста: **фестиваль-язык + траур**, не grimdark.  
5. Картинки в Preview только через **публичный HTTPS** (iili.io / freeimage.host проверено).  
6. Запрещены как основной путь: relative `assets/`, symlinks `media/`, data URI, «скачай локально», HTML INDEX-табы.  
7. На каждый кадр: изображение + **⬇ скачать** (тот же URL).  
8. Речь НПС — **под** его портретом.  
9. Исходники кадров остаются в `assets/images/`; реестр URL — `image-urls.json`.

## Текст за столом

10. Проверки по-русски: **Сл**, Внимательность, Проницательность, …  
11. Дочь Маэстро = **Милана**.  
12. Дневник без запроса на страницы = **только оглавление** (+ оболочка сессии).  
13. Вставки, жертва F, сжатые playbooks, spine после с.2 — **в книгу**, не «потом отдельно».

## Процесс

14. Сначала план визуала (NPC/локации) → ok порциями → генерация → хостинг → вшивка в биты.  
15. Источники скриптов — quest-ветка / `arcs/`; не выдумывать двери.  
16. Перед сдачей: HTTPS 200, оглавление = файлы, сказать мастеру закрыть старые вкладки Preview.

Скил: [`.cursor/skills/echo-dawn-visual-runbook/SKILL.md`](../.cursor/skills/echo-dawn-visual-runbook/SKILL.md).  
Postmortem: [`…/references/postmortem-arc3-session1.md`](../.cursor/skills/echo-dawn-visual-runbook/references/postmortem-arc3-session1.md).
