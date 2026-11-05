# Opening library
## Source
CSV -> cached load_data -> ECO/name filters -> dataframe + selected detail + sidebar metrics. Opening sequence parsed as PGN and replayed in session board.
## User route and sub-features
Open dashboard from root, filter ECO or type literal name; table count/statistics update. Select opening, Next/Previous show board and ply count. All26CSV entries are legally replayed by actual widgets. Move numbers are not SAN moves; prior split-by-space attempted1. as a move.
## Driving
Run verify.py. It traverses every opening to both ends, tests B20/no-match/Sicilian/literal[. Browser covers actual board pixels. Names include a default---choice; filters can remove selector. No-match is not empty source. Missing CSV fallback exists but is not exercised here.
## Limits
Strategic/cultural descriptions and provenance claims not independently verified. Sidebar/chart/fulltable pixels and missing/malformed CSV fixture matrix not accepted by this limited browser proof. Session only, no saved user library.
