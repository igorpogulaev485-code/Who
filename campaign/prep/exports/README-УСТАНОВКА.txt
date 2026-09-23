УСТАНОВКА СКИЛОВ В РЕПО DND-
============================

1. Скачай этот архив.
2. Открой репозиторий DND- (ветка cursor/dnd-worldbuilding-skills-95c7 или любая рабочая).
3. Распакуй архив В КОРЕНЬ репозитория (рядом с уже существующими папками).

   В Finder / Explorer: «Извлечь сюда» в папку клона DND-.
   Или в терминале:

   cd /путь/к/DND-
   unzip echo-dawn-skills-for-dnd.zip

4. Должны появиться:
   - .cursor/skills/echo-dawn-*   (9 скилов)
   - AGENTS.md
   - campaign/plot/skill-lock-*.md
   - README-УСТАНОВКА.txt (этот файл — можно удалить)

5. Закоммить и запушь:

   git add .cursor/skills AGENTS.md campaign/plot/skill-lock-*.md
   git commit -m "Import Echo Dawn skills from Who"
   git push

Скилы ссылаются на структуру Who (CANON.md, world/, campaign/, templates/).
Если в DND- другие пути — поправь ссылки в .cursor/skills/*/SKILL.md позже.
