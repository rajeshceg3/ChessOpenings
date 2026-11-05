#!/usr/bin/env python3
"""Drive actual Streamlit script widgets and validate shipped PGN data, never a replacement UI."""
import csv, io, json, pathlib, sys
import chess, chess.pgn
from streamlit.testing.v1 import AppTest
root=pathlib.Path(__file__).resolve().parents[4]
output=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/chess-proof');output.mkdir(parents=True,exist_ok=True)
import os
os.chdir(root)
result={'ok':False,'scope':'Actual Streamlit AppTest widgets plus shipped CSV legal replay; browser/upload/download separate'}
def clean(at):
 assert not at.exception,[e.message for e in at.exception]
try:
 rows=list(csv.DictReader(open('chess_openings.csv')))
 for row in rows:
  game=chess.pgn.read_game(io.StringIO(row['Moves']));assert game and not game.errors,row['Name']
 at=AppTest.from_file(str(root/'dashboard.py')).run();clean(at)
 assert len(at.dataframe[0].value)==len(rows)
 at.selectbox[0].select('B20').run();clean(at);assert set(at.dataframe[0].value.ECO)=={'B20'}
 at.text_input[0].set_value('zzznomatch').run();clean(at);assert at.dataframe[0].value.empty
 at.selectbox[0].select('All').run();at.text_input[0].set_value('[').run();clean(at);assert at.dataframe[0].value.empty
 at.text_input[0].set_value('sicilian').run();clean(at);assert len(at.dataframe[0].value)>0
 at.text_input[0].set_value('').run()
 for row in rows:
  at.selectbox[1].select(row['Name']).run();clean(at)
  count=len(at.session_state['current_opening_moves'])
  for _ in range(count):at.button[1].click().run();clean(at);assert not at.warning
  assert at.session_state['current_move_index']==count
  assert at.button[1].disabled
  for _ in range(count):at.button[0].click().run();clean(at)
  assert at.session_state['board']==chess.Board() and at.button[0].disabled
 def move(s):
  at.text_input[1].set_value(s);at.button(key='interactive_make_move_button_key').click().run();clean(at)
 move('e4');move('e5');assert not at.error
 history=list(at.session_state['interactive_moves_history'])
 at.button(key='interactive_prev_move').click().run();clean(at)
 move('invalid');assert at.error and at.session_state['interactive_moves_history']==history
 assert at.session_state['interactive_current_move_index']==1
 at.button(key='interactive_next_move').click().run();assert at.session_state['interactive_current_move_index']==2
 at.button(key='interactive_prev_move').click().run();move('c5');assert at.session_state['interactive_moves_history']==['e4','c5']
 at.text_input[0].set_value('French').run();clean(at);assert at.session_state['interactive_board'].peek()==chess.Move.from_uci('c7c5')
 result.update(ok=True,openings=len(rows),interactive='e4/e5/back/invalid preserves future/forward/back/c5 branch and unrelated rerun')
except Exception as e:
 import traceback;traceback.print_exc();result['error']=repr(e)
(output/'apptest.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(not result['ok'])
