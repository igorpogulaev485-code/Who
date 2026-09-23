# Перенос скилов Who → DND-

Цель: ветка `cursor/dnd-worldbuilding-skills-95c7` в репо `igorpogulaev485-code/DND-`.

Источник (уже собрано): ветка Who `cursor/arc3-session1-visuals-8f36`

## Команда для агента / терминала внутри DND-

```bash
# на ветке cursor/dnd-worldbuilding-skills-95c7
git remote add who https://github.com/igorpogulaev485-code/Who.git 2>/dev/null || true
git fetch who cursor/arc3-session1-visuals-8f36
git checkout who/cursor/arc3-session1-visuals-8f36 -- \
  .cursor/skills \
  AGENTS.md \
  campaign/plot/skill-lock-artifact-v1.md \
  campaign/plot/skill-lock-book-chapter-v1.md \
  campaign/plot/skill-lock-orchestrator-v1.md \
  campaign/plot/skill-lock-visual-runbook-v1.md
git add .cursor/skills AGENTS.md campaign/plot/skill-lock-*.md
git commit -m "Import Echo Dawn skills from Who (visual-runbook + full set)"
git push -u origin HEAD
```

Либо архив: `who_echo_dawn_skills_bundle.tgz` (артефакт агента Who) → `tar -xzf … -C .`
