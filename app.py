# Description: Streamlit app for visualizing and summarizing PGN files.
import streamlit as st
import chess
import chess.pgn
import chess.svg
import io
import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from openai import OpenAIError
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_pgn(pgn_content):
    pgn = io.StringIO(pgn_content)
    game = chess.pgn.read_game(pgn)
    
    # Filter and modify the headers
    filtered_headers = {}
    for key, value in game.headers.items():
        if key not in ['ECO', 'Annotator']:
            if key == 'EventDate':
                # Extract only the year from the EventDate
                try:
                    date = datetime.strptime(value, "%Y.??.??")
                    filtered_headers[key] = str(date.year)
                except ValueError:
                    # If the date format is different, just use the first 4 characters (assuming it's the year)
                    filtered_headers[key] = value[:4]
            else:
                filtered_headers[key] = value
    
    # Create a new game object with the filtered headers
    new_game = chess.pgn.Game()
    new_game.headers = chess.pgn.Headers(filtered_headers)
    
    # Copy the moves from the original game
    node = new_game
    for move in game.mainline_moves():
        node = node.add_variation(move)
    
    return new_game

def get_board_svg(board):
    return chess.svg.board(board=board)

def generate_summary(game_info, moves):
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key is not set. Please check your .env file.")
        return None

    # Truncate moves if too long
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    max_tokens = 4096 - 500  # Reserve tokens for response and prompt
    moves_tokens = encoding.encode(moves)
    if len(moves_tokens) > max_tokens:
        moves = encoding.decode(moves_tokens[:max_tokens])
        st.warning("Game is very long. Summary might be incomplete.")

    prompt = f"""
    Summarize the following chess game:
    
    Event: {game_info.get('Event', 'N/A')}
    Date: {game_info.get('Date', 'N/A')}
    White: {game_info.get('White', 'N/A')}
    Black: {game_info.get('Black', 'N/A')}
    Result: {game_info.get('Result', 'N/A')}
    
    Moves: {moves}
    
    Please provide a summary in the following format:
    1. Opening: Briefly describe the opening played.
    2. Key Moments: Highlight 2-3 critical points in the game.
    3. Conclusion: Summarize how the game ended.
    
    Keep the summary concise, around 150 words.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chess expert providing game summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        if "Rate limit" in str(e):
            st.error("API rate limit exceeded. Please try again in a moment.")
        elif "Invalid authentication" in str(e):
            st.error("Invalid API key. Please check your OpenAI API key.")
        else:
            st.error(f"OpenAI API error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

def main():
    st.title("PGN Summarizer and Visualizer")

    if 'current_move' not in st.session_state:
        st.session_state.current_move = 0

    uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")
    if uploaded_file is not None:
        pgn_content = uploaded_file.read().decode("utf-8")
        
        # Parse the PGN
        game = parse_pgn(pgn_content)
        
        # Display game information
        st.subheader("Game Information")
        for key, value in game.headers.items():
            st.write(f"{key}: {value}")
        
        # Create a chess board
        board = game.board()
        moves = list(game.mainline_moves())
        
        # Navigation buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("⏮️ First"):
                st.session_state.current_move = 0
        with col2:
            if st.button("◀️ Previous"):
                st.session_state.current_move = max(0, st.session_state.current_move - 1)
        with col3:
            if st.button("Next ▶️"):
                st.session_state.current_move = min(len(moves), st.session_state.current_move + 1)
        with col4:
            if st.button("Last ⏭️"):
                st.session_state.current_move = len(moves)
        with col5:
            st.write(f"Move: {st.session_state.current_move}/{len(moves)}")
        
        # Apply moves up to the current point
        board = game.board()
        for move in moves[:st.session_state.current_move]:
            board.push(move)
        
        # Generate and display the board SVG
        board_svg = get_board_svg(board)
        st.write(board_svg, unsafe_allow_html=True)
        
        # Display current position in FEN
        st.text(f"Current FEN: {board.fen()}")
        
        # Generate summary button
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                moves_uci = " ".join(move.uci() for move in moves)
                summary = generate_summary(game.headers, moves_uci)
                if summary:
                    st.subheader("Game Summary")
                    st.write(summary)

if __name__ == "__main__":
    main()

