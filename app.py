# import streamlit as st
# import chess.pgn
# import io

# def parse_pgn(pgn_content):
#     pgn = io.StringIO(pgn_content)
#     game = chess.pgn.read_game(pgn)
#     return game

# def extract_game_info(game):
#     headers = game.headers
#     return {
#         "Event": headers.get("Event", "N/A"),
#         "Date": headers.get("Date", "N/A"),
#         "White": headers.get("White", "N/A"),
#         "Black": headers.get("Black", "N/A"),
#         "Result": headers.get("Result", "N/A"),
#     }

# def main():
#     st.title("PGN Summarizer")

#     uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")
#     if uploaded_file is not None:
#         pgn_content = uploaded_file.read().decode("utf-8")
        
#         # # Display the raw PGN content
#         # st.subheader("Raw PGN Content")
#         # st.text(pgn_content)
        
#         # Parse the PGN and extract game information
#         game = parse_pgn(pgn_content)
#         game_info = extract_game_info(game)
        
#         # Display game information
#         st.subheader("Game Information")
#         for key, value in game_info.items():
#             st.write(f"{key}: {value}")
        
#         # TODO: Add OpenAI API integration for summarization

# if __name__ == "__main__":
#     main()



# import streamlit as st
# import chess.pgn
# import io
# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# # Load environment variables
# load_dotenv()

# # Set up OpenAI API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# import os
# from dotenv import load_dotenv

# load_dotenv()
# print(f"API Key from environment: {os.getenv('OPENAI_API_KEY')}")



# def parse_pgn(pgn_content):
#     pgn = io.StringIO(pgn_content)
#     game = chess.pgn.read_game(pgn)
#     return game

# def extract_game_info(game):
#     headers = game.headers
#     return {
#         "Event": headers.get("Event", "N/A"),
#         "Date": headers.get("Date", "N/A"),
#         "White": headers.get("White", "N/A"),
#         "Black": headers.get("Black", "N/A"),
#         "Result": headers.get("Result", "N/A"),
#     }

# def generate_summary(game_info, moves):
#     prompt = f"""
#     Summarize the following chess game:
    
#     Event: {game_info['Event']}
#     Date: {game_info['Date']}
#     White: {game_info['White']}
#     Black: {game_info['Black']}
#     Result: {game_info['Result']}
    
#     Moves: {moves}
    
#     Please provide a summary in the following format:
#     1. Opening: Briefly describe the opening played.
#     2. Key Moments: Highlight 2-3 critical points in the game.
#     3. Conclusion: Summarize how the game ended.
    
#     Keep the summary concise, around 150 words.
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a chess expert providing game summaries."},
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.choices[0].message.content

# def main():
#     st.title("PGN Summarizer")

#     uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")
#     if uploaded_file is not None:
#         pgn_content = uploaded_file.read().decode("utf-8")
        
#         # # Display the raw PGN content
#         # st.subheader("Raw PGN Content")
#         # st.text(pgn_content)
        
#         # Parse the PGN and extract game information
#         game = parse_pgn(pgn_content)
#         game_info = extract_game_info(game)
        
#         # Display game information
#         st.subheader("Game Information")
#         for key, value in game_info.items():
#             st.write(f"{key}: {value}")
        
#         # Extract moves
#         moves = " ".join(move.uci() for move in game.mainline_moves())
        
#         # Generate summary
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 summary = generate_summary(game_info, moves)
#                 st.subheader("Game Summary")
#                 st.write(summary)

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import chess
# import chess.pgn
# import chess.svg
# import io
# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# # Load environment variables
# load_dotenv()

# # Set up OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def parse_pgn(pgn_content):
#     pgn = io.StringIO(pgn_content)
#     game = chess.pgn.read_game(pgn)
#     return game

# def get_board_svg(board):
#     return chess.svg.board(board=board)

# def generate_summary(game_info, moves):
#     prompt = f"""
#     Summarize the following chess game:
    
#     Event: {game_info.get('Event', 'N/A')}
#     Date: {game_info.get('Date', 'N/A')}
#     White: {game_info.get('White', 'N/A')}
#     Black: {game_info.get('Black', 'N/A')}
#     Result: {game_info.get('Result', 'N/A')}
    
#     Moves: {moves}
    
#     Please provide a summary in the following format:
#     1. Opening: Briefly describe the opening played.
#     2. Key Moments: Highlight 2-3 critical points in the game.
#     3. Conclusion: Summarize how the game ended.
    
#     Keep the summary concise, around 150 words.
#     """
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a chess expert providing game summaries."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error generating summary: {str(e)}")
#         return None

# def main():
#     st.title("PGN Summarizer and Visualizer")

#     uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")
#     if uploaded_file is not None:
#         pgn_content = uploaded_file.read().decode("utf-8")
        
#         # Parse the PGN
#         game = parse_pgn(pgn_content)
        
#         # Display game information
#         st.subheader("Game Information")
#         for key, value in game.headers.items():
#             st.write(f"{key}: {value}")
        
#         # Create a chess board
#         board = game.board()
        
#         # Create a slider for move selection
#         moves = list(game.mainline_moves())
#         move_slider = st.slider("Select move", 0, len(moves), 0)
        
#         # Apply moves up to the selected point
#         for move in moves[:move_slider]:
#             board.push(move)
        
#         # Generate and display the board SVG
#         board_svg = get_board_svg(board)
#         st.write(board_svg, unsafe_allow_html=True)
        
#         # Display current position in FEN
#         st.text(f"Current FEN: {board.fen()}")
        
#         # Generate summary button
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 moves_uci = " ".join(move.uci() for move in moves)
#                 summary = generate_summary(game.headers, moves_uci)
#                 if summary:
#                     st.subheader("Game Summary")
#                     st.write(summary)

# if __name__ == "__main__":
#     main()













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

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_pgn(pgn_content):
    pgn = io.StringIO(pgn_content)
    game = chess.pgn.read_game(pgn)
    return game

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


# import streamlit as st
# import chess
# import chess.pgn
# import chess.svg
# import io
# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# # Load environment variables
# load_dotenv()

# # Set up OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def parse_pgn(pgn_content):
#     pgn = io.StringIO(pgn_content)
#     game = chess.pgn.read_game(pgn)
#     return game

# def get_board_svg(board):
#     return chess.svg.board(board=board)

# def generate_summary(game_info, moves):
#     prompt = f"""
#     Summarize the following chess game:
    
#     Event: {game_info.get('Event', 'N/A')}
#     Date: {game_info.get('Date', 'N/A')}
#     White: {game_info.get('White', 'N/A')}
#     Black: {game_info.get('Black', 'N/A')}
#     Result: {game_info.get('Result', 'N/A')}
    
#     Moves: {moves}
    
#     Please provide a summary in the following format:
#     1. Opening: Briefly describe the opening played.
#     2. Key Moments: Highlight 2-3 critical points in the game.
#     3. Conclusion: Summarize how the game ended.
    
#     Keep the summary concise, around 150 words.
#     """
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a chess expert providing game summaries."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error generating summary: {str(e)}")
#         return None

# def main():
#     st.title("PGN Summarizer and Visualizer")

#     if 'current_move' not in st.session_state:
#         st.session_state.current_move = 0
#     if 'moves' not in st.session_state:
#         st.session_state.moves = []
#     if 'board' not in st.session_state:
#         st.session_state.board = chess.Board()

#     uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")
#     if uploaded_file is not None:
#         pgn_content = uploaded_file.read().decode("utf-8")
        
#         # Parse the PGN
#         game = parse_pgn(pgn_content)
        
#         # Display game information
#         st.subheader("Game Information")
#         for key, value in game.headers.items():
#             st.write(f"{key}: {value}")
        
#         # Update session state
#         st.session_state.moves = list(game.mainline_moves())
#         st.session_state.board = game.board()
        
#         # Keyboard input for navigation
#         st.write("Use the text input below for keyboard navigation:")
#         st.write("← (left arrow): Previous move")
#         st.write("→ (right arrow): Next move")
#         st.write("↑ (up arrow): First move")
#         st.write("↓ (down arrow): Last move")
#         key_input = st.text_input("Press a key and hit enter:", key="move_input")
        
#         if key_input:
#             if key_input == '←':
#                 st.session_state.current_move = max(0, st.session_state.current_move - 1)
#             elif key_input == '→':
#                 st.session_state.current_move = min(len(st.session_state.moves), st.session_state.current_move + 1)
#             elif key_input == '↑':
#                 st.session_state.current_move = 0
#             elif key_input == '↓':
#                 st.session_state.current_move = len(st.session_state.moves)
            
#             # Clear the input
#             st.session_state.move_input = ""
        
#         # Navigation buttons
#         col1, col2, col3, col4, col5 = st.columns(5)
#         with col1:
#             if st.button("⏮️ First"):
#                 st.session_state.current_move = 0
#         with col2:
#             if st.button("◀️ Previous"):
#                 st.session_state.current_move = max(0, st.session_state.current_move - 1)
#         with col3:
#             if st.button("Next ▶️"):
#                 st.session_state.current_move = min(len(st.session_state.moves), st.session_state.current_move + 1)
#         with col4:
#             if st.button("Last ⏭️"):
#                 st.session_state.current_move = len(st.session_state.moves)
#         with col5:
#             st.write(f"Move: {st.session_state.current_move}/{len(st.session_state.moves)}")
        
#         # Apply moves up to the current point
#         st.session_state.board = game.board()
#         for move in st.session_state.moves[:st.session_state.current_move]:
#             st.session_state.board.push(move)
        
#         # Generate and display the board SVG
#         board_svg = get_board_svg(st.session_state.board)
#         st.write(board_svg, unsafe_allow_html=True)
        
#         # Display current position in FEN
#         st.text(f"Current FEN: {st.session_state.board.fen()}")
        
#         # Generate summary button
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 moves_uci = " ".join(move.uci() for move in st.session_state.moves)
#                 summary = generate_summary(game.headers, moves_uci)
#                 if summary:
#                     st.subheader("Game Summary")
#                     st.write(summary)

# if __name__ == "__main__":
#     main()