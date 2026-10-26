# Toronto Talk

A study app for learning everyday and business English expressions commonly used in Toronto and Canada, through fill-in-the-blank practice with Korean translations.

**Try it now:** https://chaeeunlee227.github.io/toronto-talk/

## Features
- 1,200+ expressions across 11 lines (Everyday talk, Feelings & relationships, Restaurants & shopping, Travel & transit, Home, clinic & bank, Meetings & work, Email & messaging, Phrasal verbs, Idioms, Colours, flowers & nature, Taste & texture)
- Hints (first 1–2 letters), reveal answer, and a bonus challenge for alternative answers
- Spaced repetition that sets review intervals from answer time and number of mistakes
- Answer by speaking into the in-page microphone (word mode / sentence mode), and listen to example sentences
- Word list, study streak, 30-day activity, and per-line progress dashboard
- Study progress is saved in this browser. Use **Copy / paste backup code** on the dashboard to move or restore it.

## On iPhone
Open in Safari, then Share → **Add to Home Screen**. Allow the microphone the first time you tap it.

## Structure
- `index.html` and other top-level files: the app, served by GitHub Pages
- `source/`: expression data (`data/*.txt`), the template, and the build script. Run `python3 build.py` to regenerate `site/index.html`.
