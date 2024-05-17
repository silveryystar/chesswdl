from f import config, get_game, get_analysis, get_plots

exe = "stockfish-windows-x86-64-avx2.exe"
# exe = "lc0.exe"

game = input("Game: ")

moves, board = get_game(game)
engine, limit, key, value = config(exe)
wins, draws, losses, evals, nodes = get_analysis(board, engine, limit, key, value, moves)
get_plots(wins, draws, losses, evals, nodes, exe)
