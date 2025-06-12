import streamlit as st
import pandas as pd
import chess
import chess.svg

st.title("Chess Openings Dashboard")

st.markdown("""
Welcome to the Chess Openings Dashboard!
- Use the filters below to narrow down the list of openings.
- Select an opening from the table or the dropdown further down to see its details and visualize its moves.
- Use the 'Previous Move' and 'Next Move' buttons to navigate the opening sequence on the board.
""")
st.divider()

# Initialize session state variables if they don't exist
if 'selected_opening_name_key' not in st.session_state:
    st.session_state.selected_opening_name_key = ""
if 'current_opening_moves' not in st.session_state:
    st.session_state.current_opening_moves = []
if 'current_move_index' not in st.session_state:
    st.session_state.current_move_index = 0
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Load the chess openings data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("chess_openings.csv")
        return df
    except FileNotFoundError:
        st.error("ERROR: `chess_openings.csv` not found. Please ensure the file exists in the same directory as `dashboard.py`.")
        return pd.DataFrame(columns=['ECO', 'Name', 'Moves', 'Description'])

chess_df = load_data()

# Gracefully handle if chess_df is empty from the start
if chess_df.empty:
    st.warning("No chess openings data loaded. Dashboard functionality will be limited.")
    # Optionally, exit here if no data means nothing else can be done
    # st.stop()

# Display the dataframe
st.subheader("Chess Openings Data")

# Initialize filtered_df with the original DataFrame
# This check is important if chess_df could be empty due to load_data failure
if not chess_df.empty:
    filtered_df = chess_df
else:
    filtered_df = pd.DataFrame(columns=['ECO', 'Name', 'Moves', 'Description'])

# Filter by ECO code
eco_codes = ["All"] + sorted(chess_df["ECO"].unique().tolist())
selected_eco = st.selectbox("Filter by ECO Code:", eco_codes)

if selected_eco != "All":
    filtered_df = filtered_df[filtered_df["ECO"] == selected_eco]

# Filter by Name
name_query = st.text_input("Search by Name:", "")
if name_query:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name_query, case=False, na=False)]

st.dataframe(filtered_df)

st.divider()

if not filtered_df.empty:
    # Ensure opening_names is not created if filtered_df is empty
    opening_names = ["---"] + filtered_df["Name"].tolist() if not filtered_df.empty else ["---"]
    selected_opening_name = st.selectbox("Select Opening to View Details:", opening_names)

    if selected_opening_name != "---" and not filtered_df.empty: # Added check for filtered_df
        selected_opening_data = filtered_df[filtered_df["Name"] == selected_opening_name]
        if not selected_opening_data.empty:
            st.subheader(selected_opening_data['Name'].iloc[0])
            st.markdown(f"**ECO:** {selected_opening_data['ECO'].iloc[0]}")
            st.markdown(f"**Moves:** `{selected_opening_data['Moves'].iloc[0]}`")
            st.markdown(f"**Description:** {selected_opening_data['Description'].iloc[0]}")

            moves_str = selected_opening_data['Moves'].iloc[0]

            # Check if the selected opening has changed
            if selected_opening_name != st.session_state.selected_opening_name_key:
                st.session_state.selected_opening_name_key = selected_opening_name
                st.session_state.current_move_index = 0
                st.session_state.board = chess.Board()
                if moves_str:
                    st.session_state.current_opening_moves = [m for m in moves_str.split(' ') if m] # Filter out empty strings
                else:
                    st.session_state.current_opening_moves = []
                # No moves played yet, board is fresh for the new opening

            if st.session_state.current_opening_moves:
                st.subheader("Board Position:")

                # Navigation buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Previous Move", disabled=st.session_state.current_move_index == 0):
                        st.session_state.current_move_index -= 1
                        # Replay board from scratch
                        st.session_state.board = chess.Board()
                        for i in range(st.session_state.current_move_index):
                            try:
                                st.session_state.board.push_san(st.session_state.current_opening_moves[i])
                            except Exception as e: # Catch broad errors during replay
                                st.error(f"Error replaying move '{st.session_state.current_opening_moves[i]}': {e}")
                                # Potentially stop replay or handle error state
                                break

                with col2:
                    if st.button("Next Move", disabled=st.session_state.current_move_index == len(st.session_state.current_opening_moves)):
                        try:
                            move_to_play = st.session_state.current_opening_moves[st.session_state.current_move_index]
                            st.session_state.board.push_san(move_to_play)
                            st.session_state.current_move_index += 1
                        except (chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError) as e:
                            st.warning(f"Invalid move '{move_to_play}': {e}")
                        except IndexError:
                             st.warning("No more moves to play.")


                # Display board and move count
                st.image(chess.svg.board(board=st.session_state.board))
                st.write(f"Move: {st.session_state.current_move_index} / {len(st.session_state.current_opening_moves)}")

            elif moves_str and not filtered_df.empty : # Handles openings that might have moves but they are invalid from the start
                st.warning("This opening has moves listed, but they could not be processed to display a board.")
            # If filtered_df is empty, this whole detail section is skipped by selected_opening_name != "---" and not filtered_df.empty

st.sidebar.title("Summary Statistics") # Changed from st.sidebar.header
st.sidebar.metric("Total Openings Displayed", len(filtered_df)) # This will be 0 if data loading failed

if not filtered_df.empty:
    st.sidebar.subheader("Openings per ECO Code")
    eco_counts = filtered_df["ECO"].value_counts()
    st.sidebar.bar_chart(eco_counts)
else:
    st.sidebar.info("No data to display statistics for (or data file not found).")
