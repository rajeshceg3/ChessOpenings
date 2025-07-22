import streamlit as st
import pandas as pd
import chess
import chess.svg
import chess.pgn
import datetime
import io

# Set page config (including dark theme if directly supported, or use custom CSS)
# Streamlit's theming has evolved. Forcing a "dark" theme might be part of the theme object
# or might require custom CSS. We'll set the page config and then apply custom CSS
# that ensures a dark background and appropriate text colors if theme="dark" isn't sufficient.
st.set_page_config(
    layout="wide",
    page_title="Chess Openings Dashboard",
    page_icon=":chess_pawn:",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look and feel
custom_css = """
<style>
    /* Base theme colors - Assuming a dark theme is desired */
    body {
        font-family: 'Roboto', 'Open Sans', sans-serif;
        color: #E0E0E0; /* Light grey text for dark background */
        background-color: #1E1E1E; /* Dark background */
    }

    /* Primary color for accents, buttons, etc. */
    :root {
        --primary-color: #4A90E2; /* Modern Blue */
        --primary-color-hover: #357ABD; /* Darker blue for hover */
        --button-text-color: #FFFFFF;
        --table-header-bg: #2A2A2A;
        --table-row-bg: #252525;
        --table-row-hover-bg: #303030;
        --table-border-color: #353535;
    }

    /* General app styling */
    .stApp {
        background-color: #1E1E1E; /* Ensure app background is dark */
    }

    /* Title */
    h1 {
        color: var(--primary-color);
    }

    /* Buttons styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: var(--button-text-color);
        border: none;
        border-radius: 8px; /* Rounded corners */
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow */
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--primary-color-hover);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:disabled {
        background-color: #555;
        color: #AAA;
        box-shadow: none;
    }


    /* Table styling */
    .stDataFrame table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        color: #E0E0E0; /* Light text for table content */
    }
    .stDataFrame th {
        background-color: var(--table-header-bg); /* Darker header for tables */
        color: #F0F0F0; /* Lighter text for headers */
        text-align: left;
        padding: 12px 15px;
        border-bottom: 2px solid var(--primary-color);
    }
    .stDataFrame td {
        padding: 10px 15px;
        border-bottom: 1px solid var(--table-border-color); /* Subtle border for rows */
        background-color: var(--table-row-bg);
    }
    .stDataFrame tr:hover td {
        background-color: var(--table-row-hover-bg); /* Hover effect for rows */
    }
    /* Remove Streamlit's default table borders if they conflict */
    .stDataFrame .dataframe {
        border: none;
    }

    /* Selectbox and Text Input styling */
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput input {
        border-radius: 5px;
        border-color: #555; /* Darker border for inputs */
        background-color: #252525; /* Dark input background */
        color: #E0E0E0;
    }
    .stSelectbox div[data-baseweb="select"] > div:focus,
    .stTextInput input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25);
    }

    /* Markdown links */
    a {
        color: var(--primary-color);
    }
    a:hover {
        color: var(--primary-color-hover);
    }

    /* Sidebar styling */
    .css-1d391kg { /* Specific class for Streamlit sidebar; may need adjustment if Streamlit updates */
        background-color: #252525; /* Slightly lighter dark for sidebar */
    }

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Chess Openings Dashboard")

with st.expander("ℹ️ How to Use This Dashboard (Beginner's Guide)", expanded=False):
    st.markdown("""
    Welcome to the Chess Openings Dashboard! This guide will help you get started.

    **1. Exploring Chess Openings:**

    *   **Filtering by ECO Code:**
        *   The "🏷️ Filter by ECO Code" dropdown on the left allows you to see openings belonging to a specific ECO (Encyclopedia of Chess Openings) code.
        *   Select an ECO code (e.g., "A00", "B20") to narrow down the list. Select "All" to see all openings.
    *   **Searching by Name:**
        *   Use the "🔍 Search by Name" text box on the right to find openings containing specific words (e.g., "King's Gambit", "Sicilian").
        *   The table will update as you type.
    *   **Understanding the Openings Table:**
        *   The main table displays a list of chess openings. Each row shows:
            *   `ECO`: The ECO code for the opening.
            *   `Name`: The common name of the opening.
            *   `Moves`: The sequence of moves in Standard Algebraic Notation (SAN).
            *   `Description`: A brief description of the opening's strategy or characteristics.

    **2. Viewing Opening Details and Moves:**

    *   **Selecting an Opening:**
        *   Below the filters, you'll find a dropdown menu labeled "Select Opening to View Details:".
        *   Choose an opening name from this list.
        *   Once selected, its detailed information (ECO, Name, Moves, Description) will appear.
    *   **Visualizing on the Chessboard:**
        *   After selecting an opening, a chessboard will show its starting position.
        *   Use the "➡️ Next Move" button to play the next move in the opening sequence on the board.
        *   Use the "⬅️ Previous Move" button to go back one move.
        *   The text below the board (e.g., "Move: 1 / 5") tells you which move you are currently viewing out of the total moves in the sequence.

    **3. Trying Your Own Moves (Interactive Chessboard):**

    *   Scroll down to the "Interactive Chessboard" section.
    *   Here, you can input your own chess moves in the text box (e.g., "e4", "Nf3", "O-O" for castling).
    *   Click "▶️ Make Move" to see your move on the board.
    *   You can also navigate through the moves you've made using the "⏪ Previous Interactive Move" and "⏩ Next Interactive Move" buttons in this section.

    **4. Summary Statistics:**

    *   The sidebar on the left (you might need to expand it) shows "📊 Summary Statistics".
    *   This includes the "Total Openings Displayed" (based on your filters) and a chart of "Openings per ECO Code".

    **5. Importing and Exporting Games (PGN):**

    *   **Importing a Game (⬆️ Upload PGN File):**
        *   In the "Interactive Chessboard" section, click on "Browse files" under "⬆️ Upload PGN File".
        *   Select a PGN file (`.pgn`) from your computer.
        *   The game from the PGN file will be loaded onto the interactive chessboard, replacing any existing moves. You can then navigate through its moves.
    *   **Exporting a Game (⬇️ Download PGN):**
        *   After making moves on the "Interactive Chessboard", the "⬇️ Download PGN" button will appear.
        *   Click this button to save the sequence of moves you've played on the interactive board as a `.pgn` file to your computer.

    We hope this helps you explore the fascinating world of chess openings!
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

# For the interactive chessboard
if 'interactive_board' not in st.session_state:
    st.session_state.interactive_board = chess.Board()
if 'interactive_moves_history' not in st.session_state:
    st.session_state.interactive_moves_history = []
if 'interactive_current_move_index' not in st.session_state:
    st.session_state.interactive_current_move_index = 0
if 'pgn_file_id' not in st.session_state:
    st.session_state.pgn_file_id = None

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

# Filtering options in columns
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    eco_codes = ["All"] + sorted(chess_df["ECO"].unique().tolist())
    selected_eco = st.selectbox("🏷️ Filter by ECO Code:", eco_codes)
    if selected_eco != "All": # Apply ECO filter immediately if selected
        filtered_df = filtered_df[filtered_df["ECO"] == selected_eco]

with filter_col2:
    name_query = st.text_input("🔍 Search by Name:", "")
    if name_query: # Apply name filter if query exists
        filtered_df = filtered_df[filtered_df["Name"].str.contains(name_query, case=False, na=False)]

st.dataframe(filtered_df) # Display the possibly filtered dataframe

st.divider()

if not filtered_df.empty:
    # Ensure opening_names is not created if filtered_df is empty
    opening_names = ["---"] + filtered_df["Name"].tolist() if not filtered_df.empty else ["---"]
    selected_opening_name = st.selectbox("Select Opening to View Details:", opening_names)

    if selected_opening_name != "---" and not filtered_df.empty: # Added check for filtered_df
        selected_opening_data = filtered_df[filtered_df["Name"] == selected_opening_name]
        if not selected_opening_data.empty:
            with st.container(border=True): # Group opening details
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
                    col1_nav, col2_nav = st.columns(2) # Renamed to avoid conflict with filter columns
                    with col1_nav:
                        if st.button("⬅️ Previous Move", disabled=st.session_state.current_move_index == 0):
                            st.session_state.current_move_index -= 1
                            st.session_state.board.pop()

                    with col2_nav:
                        if st.button("➡️ Next Move", disabled=st.session_state.current_move_index == len(st.session_state.current_opening_moves)):
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
            st.markdown("<br>", unsafe_allow_html=True) # Add some space after the container

st.divider()
st.header("Interactive Chessboard")

with st.container(border=True): # Group interactive chessboard section
    # Helper function to replay interactive board to a specific move index
    def replay_interactive_board_to_index(move_idx):
        """
        Replays moves from st.session_state.interactive_moves_history up to move_idx
        and updates st.session_state.interactive_board.
        """
    board = chess.Board()
    # Only try to replay moves if there's history and index is valid
    if st.session_state.interactive_moves_history and move_idx > 0 :
        for i in range(move_idx):
            # Check if the move index is within the bounds of the history list
            if i < len(st.session_state.interactive_moves_history):
                try:
                    board.push_san(st.session_state.interactive_moves_history[i])
                except (chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError) as e:
                    st.error(f"Error replaying move '{st.session_state.interactive_moves_history[i]}' at index {i} (specific chess error): {e}")
                    break
                except Exception as e: # Fallback for other unexpected errors
                    st.error(f"An unexpected error occurred while replaying move '{st.session_state.interactive_moves_history[i]}' at index {i}: {e}")
                    break
            else: # Should not happen if move_idx is managed correctly
                st.warning(f"Attempted to replay move at index {i} beyond history length.")
                break
    st.session_state.interactive_board = board


    # UI for PGN Upload
    uploaded_pgn_file = st.file_uploader("⬆️ Upload PGN File", type=["pgn"], accept_multiple_files=False, key="pgn_uploader")

    if uploaded_pgn_file is not None:
        # Generate a unique ID for the uploaded file to detect new uploads
        file_id = f"{uploaded_pgn_file.name}-{uploaded_pgn_file.size}"
        if st.session_state.pgn_file_id != file_id:
            st.session_state.pgn_file_id = file_id
            if 'pgn_processed' in st.session_state:
                del st.session_state.pgn_processed

    if uploaded_pgn_file is not None and 'pgn_processed' not in st.session_state:
        try:
            pgn_bytes = uploaded_pgn_file.getvalue()
            pgn_string = pgn_bytes.decode("utf-8")
            pgn_file_like = io.StringIO(pgn_string)
            game = chess.pgn.read_game(pgn_file_like)

            if game:
                # Clear existing interactive game state
                st.session_state.interactive_moves_history = []
                st.session_state.interactive_board = chess.Board() # Reset board
                st.session_state.interactive_current_move_index = 0

                temp_board_for_san = chess.Board()
                for move in game.mainline_moves():
                    san_move = temp_board_for_san.san(move)
                    st.session_state.interactive_moves_history.append(san_move)
                    temp_board_for_san.push(move)

                st.session_state.pgn_processed = True
                replay_interactive_board_to_index(st.session_state.interactive_current_move_index)
                st.success("PGN file uploaded and processed successfully. Board and history reset to PGN content.")
                # Board UI will be fresh as index is 0 and board is new.
                # replay_interactive_board_to_index(0) # Call this to be explicit if needed, but should be covered.
                # Clear the uploader after processing by rerunning with uploaded_pgn_file = None
                # This usually requires a more complex callback structure or session state trick
                # For now, the file will remain in the uploader widget until the user removes it or uploads another.
                # To allow re-uploading the same file, we can set key to a new value or use st.experimental_rerun
                # For simplicity, we'll leave it as is. The user can remove and re-upload.

            else:
                st.error("Error: Could not parse PGN file. Please ensure it's a valid PGN.")
        except Exception as e:
            st.error(f"An error occurred while processing the PGN file: {e}")
        # To prevent reprocessing on every script rerun after a successful upload,
        # you might want to clear uploaded_pgn_file from session_state or use a flag.
        # For now, this will reprocess if the user interacts with another widget.
        # A common pattern is to use st.session_state to store the "processed" state of the file.

    # UI for move input
    move_input = st.text_input("Enter your move (e.g., e4, Nf3):", key="interactive_move_input_key", help="Use Standard Algebraic Notation (e.g., e4, Nf3, O-O for castling).")
    # st.caption("Use Standard Algebraic Notation (e.g., e4, Nf3, O-O for castling).") # Alternative way to add help text
    make_move_button = st.button("▶️ Make Move", key="interactive_make_move_button_key")

    if make_move_button and move_input:
        try:
            # When a new move is made, it's on the current state of st.session_state.interactive_board
            # If interactive_current_move_index is not at the end of history (e.g., user went back, then made a new move),
            # this new move should effectively create a new branch of history.
            # For simplicity, let's assume new moves always append to the current board state,
            # and if the user was in the past, this new move truncates any "future" moves from old history.
            if st.session_state.interactive_current_move_index < len(st.session_state.interactive_moves_history):
                # User had navigated back, now making a new move. Truncate old future.
                st.session_state.interactive_moves_history = st.session_state.interactive_moves_history[:st.session_state.interactive_current_move_index]
                # The board should already be at interactive_current_move_index due to navigation.

            # board_to_update is st.session_state.interactive_board, which is either fresh or replayed to current_move_index
            st.session_state.interactive_board.push_san(move_input) # Apply new move

            st.session_state.interactive_moves_history.append(move_input)
            st.session_state.interactive_current_move_index = len(st.session_state.interactive_moves_history)

            st.session_state.interactive_move_input_key = ""
            st.success(f"Move '{move_input}' made successfully.")
            # The board is already up-to-date. No replay needed here.

        except (chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError) as e:
            st.error(f"Invalid move '{move_input}': {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while making move '{move_input}': {e}")

    # Navigation buttons for the interactive board
    col_prev_interactive, col_next_interactive = st.columns(2) # Renamed for clarity

    with col_prev_interactive:
        if st.button("⏪ Previous Interactive Move", key="interactive_prev_move",
                     disabled=st.session_state.interactive_current_move_index == 0):
            st.session_state.interactive_current_move_index -= 1
            replay_interactive_board_to_index(st.session_state.interactive_current_move_index)

    with col_next_interactive:
        if st.button("⏩ Next Interactive Move", key="interactive_next_move",
                     disabled=st.session_state.interactive_current_move_index >= len(st.session_state.interactive_moves_history)):
            st.session_state.interactive_current_move_index += 1
            replay_interactive_board_to_index(st.session_state.interactive_current_move_index)

    # Display the interactive chessboard and move count
    st.subheader("Current Interactive Board")
    # Ensure st.session_state.interactive_board is always up-to-date based on user actions
    if 'interactive_board' in st.session_state:
        st.image(chess.svg.board(board=st.session_state.interactive_board), caption="Interactive Board")
    else: # Should ideally not happen if initialized correctly
        st.warning("Interactive board is not available in session state.")

    if 'interactive_current_move_index' in st.session_state and 'interactive_moves_history' in st.session_state:
        st.write(f"Move: {st.session_state.interactive_current_move_index} / {len(st.session_state.interactive_moves_history)}")
    else: # Should ideally not happen
        st.warning("Interactive move history/index is not available in session state.")

    # PGN Download Button
    if st.session_state.interactive_moves_history:
        pgn_game = chess.pgn.Game()
        pgn_game.headers["Event"] = "Interactive Session"
        pgn_game.headers["Site"] = "Chess Openings Dashboard"
        pgn_game.headers["Date"] = datetime.date.today().strftime("%Y.%m.%d")
        pgn_game.headers["Round"] = "-"
        pgn_game.headers["White"] = "Player1"
        pgn_game.headers["Black"] = "Player2"
        pgn_game.headers["Result"] = "*" # Game is ongoing or result unknown

        # Create a temporary board to validate and add moves
        node = pgn_game
        for move_san in st.session_state.interactive_moves_history:
            try:
                move = node.board().parse_san(move_san)
                node = node.add_main_variation(move)
            except (chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError) as e:
                st.error(f"Error adding move {move_san} to PGN: {e}")
                # Optionally skip this move or stop PGN generation
                break

        pgn_string = str(pgn_game)

        st.download_button(
            label="⬇️ Download PGN",
            data=pgn_string,
            file_name="interactive_game.pgn",
            mime="application/x-chess-pgn"
        )
    st.markdown("<br>", unsafe_allow_html=True) # Add some space after the container


st.sidebar.title("📊 Summary Statistics") # Changed from st.sidebar.header
st.sidebar.metric("Total Openings Displayed", len(filtered_df)) # This will be 0 if data loading failed

if not filtered_df.empty:
    st.sidebar.subheader("Openings per ECO Code")
    eco_counts = filtered_df["ECO"].value_counts()
    st.sidebar.bar_chart(eco_counts)

    st.sidebar.divider() # Add a small divider

    st.sidebar.subheader("Name Insights")
    # Calculate number of gambit openings based on the original DataFrame
    # Ensure 'Name' column exists and is not empty before attempting string operations
    if 'Name' in chess_df.columns and not chess_df.empty:
        gambit_count = chess_df[chess_df['Name'].str.contains("Gambit", case=False, na=False)].shape[0]
    else:
        gambit_count = 0 # Default to 0 if 'Name' column is missing or df is empty
    st.sidebar.metric(label="Gambit Openings Found", value=gambit_count)

else:
    st.sidebar.info("No data to display statistics for (or data file not found).")
