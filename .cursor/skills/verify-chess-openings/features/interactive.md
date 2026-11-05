# Interactive board and PGN
## Source
Session history/index/chess.Board, replay_interactive_board_to_index; make-move validates copied board before truncation, then reruns to reset input and control states. Upload hashes content, parses PGN before replacing history. Download builds full history from standard start.
## User route and sub-features
Interactive Chessboard -> enterSAN -> MakeMove; Previous/Next; new legal move in past replaces future, invalid one must preserve it. Upload localPGN -> board starts at0, Next moves through imported game. Download exports fullhistory (not just currentprefix).
## Driving
verify.py covers legal e4/e5/back/invalid preservesfuture/forward/c5 branch/unrelatedrerun. browser.mjs uses real fileinput and actual downloaded bytes at390/1365, examines board pixels. No internal state writes or fake UI. Generic fixturePGNs only.
## Limits
Imported nonstandard startingpositions/parsererrorgames are rejected. Malformed-upload, same-byte-length differentfile, castling/promotion/nonUTF8/largefile matrices remain unverified. A same-path replacement attempt did not reach expected readiness; remove/reupload and same-size replacement remain unverified. No persistent game or reset feature claimed.
