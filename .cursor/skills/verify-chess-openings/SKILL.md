---
name: verify-chess-openings
description: Exercise the actual Streamlit dashboard, all shipped opening sequences, literal filters, legal interactive moves and navigation, and browser PGN upload/download at mobile and desktop widths.
---
# Chess openings verification

## Launch and doctor
From repo root use Python3.10+ in an isolated venv; `python -m venv .venv`, `.venv/bin/pip install -r requirements.txt`. Browser helper needs Node22.12+, Chrome and `npm ci --ignore-scripts --prefix .cursor/skills/verify-chess-openings`. No accounts or external services needed. Requirements are upstream unpinned; executed baseline was Streamlit1.65.0. Do not claim lockfile reproducibility for Python.

`python -m py_compile dashboard.py` first. Then `.venv/bin/python .cursor/skills/verify-chess-openings/helpers/verify.py /tmp/chess-proof` runs actual Streamlit AppTest widgets. Browser helper owns loopback Streamlit port18764, checks /_stcore/health and actual move input readiness, then uses real buttons/upload/download: `VERIFY_PYTHON=$PWD/.venv/bin/python node .cursor/skills/verify-chess-openings/helpers/browser.mjs /tmp/chess-browser`. CHROME_PATH overrides Chrome. Do not run browser helpers concurrently on fixed port. Live manual entry: `streamlit run dashboard.py` from root so CSV/theme resolve.

## Drive and evidence
AppTest: all26shipped opening PGNs must parse without errors; select every opening and advance/back through every ply, assert endpoint-disabled controls and fresh board; ECO B20, case-insensitive literal Sicilian, unmatched query and literal `[` no exception; e4/e5/back/invalid preserves future/forward/back/c5 creates branch; unrelated filter rerun must not reset interactive board. The helper drives widgets, inspects existing session state read-only and never substitutes product logic.

Browser390/1365: actual e4 via input+button, real board rendered, upload controlled PGN d4/d5/c4, Next, download bytes contain the entire imported game. Replacing a selected upload without clearing is not accepted by this harness; a same-path replacement attempt did not reach expected0/3 readiness and is retained as a gap, not counted. Assert no Streamlit exception, no document overflow and actual board. Inspect named move/import screenshots at both widths. They cover board/contrast/layout, not the entire dashboard aesthetic or accessibility. Fixture games are not user records. CSV strategic descriptions/source attribution are not independently validated by legal move replay.

## Failure and cleanup
No health after surprising behavior: inspect app exception/log, reset AppTest/new browser session before continuing. Preserve resultJSON/screenshots after cleanup. Helpers close owned browser and terminate owned Streamlit process, never process-name kill; no provider calls, secrets, persisted user games or database. Stop after a failed run, fix harness or bounded source defect then repeat full relevant proof. Rerun on fetched default branch before completion. Read-only runtime assertions are evidence, not an alternative UI. No resource override experiment is used here.

## Coverage limits and maintenance
Live deployment/CI, screen-reader/keyboard-only/fullvisual acceptance, malformed upload/Unicode/castling/promotion/FENPGN matrix and very large uploads remain unverified unless explicitly added and run. Imports with parser errors or nonstandard start position are rejected rather than silently converting a partial/nonstandard game to standard history. Generated PGN uses full history, even when viewing earlier move. A future board-reset/persistence feature must be mapped before claiming it works. Follow /maintain-verification-skill for drift.
