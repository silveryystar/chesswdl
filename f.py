import chess.engine
import lichesspy.api
from lichesspy.format import PYCHESS
import matplotlib.pyplot as plt
import numpy as np


def config(exe):
    engine = chess.engine.SimpleEngine.popen_uci(exe)

    if exe == "lc0.exe":
        value = 1
        limit = chess.engine.Limit(nodes=value)
        key = "nodes"

    else:
        value = 30
        limit = chess.engine.Limit(depth=value)
        key = "depth"
        engine.configure({"Threads": 1,
                          "Hash": 1})

    return engine, limit, key, value


def get_eval(score):
    raw_eval = str(score).removeprefix("PovScore(Cp(")

    if "WHITE" in raw_eval:
        evaluation = raw_eval.removesuffix("), WHITE)")

        try:
            evaluation = int(evaluation)

        except ValueError:
            if "+" in evaluation:
                evaluation = "M+"
            else:
                evaluation = "M-"
    else:
        evaluation = raw_eval.removesuffix("), BLACK)")

        try:
            evaluation = -int(evaluation)

        except ValueError:
            if "-" in evaluation:
                evaluation = "M+"
            else:
                evaluation = "M-"

    return evaluation


def get_wdl(score, stm):
    wdl = score.wdl()
    win_rate, draw_rate, loss_rate = wdl[0]/1000, wdl[1]/1000, wdl[2]/1000

    if stm is False:  # wtm True, btm False
        win_rate, loss_rate = loss_rate, win_rate

    return win_rate, draw_rate, loss_rate


def analyze(board, engine, limit, key, value):
    stm = board.turn

    with engine.analysis(board, limit=limit) as i:
        for j in i:
            try:
                if j[key] == value:
                    nodes = j["nodes"]
                    score = j["score"]

                    evaluation = get_eval(score)
                    win_rate, draw_rate, loss_rate = get_wdl(score, stm)

            except KeyError:
                pass

    return win_rate, draw_rate, loss_rate, evaluation, nodes


def get_game(lichess_game):
    game = lichesspy.api.game(lichess_game)
    moves = game["moves"]
    move_list = list(moves.split(" "))

    game = lichesspy.api.game(lichess_game, format=PYCHESS)
    board = game.board()
    return move_list, board


def get_analysis(board, engine, limit, key, value, moves):
    wins, draws, losses, evals, nodes = [], [], [], [], []
    w, d, l, e, n = analyze(board, engine, limit, key, value)

    wins.append(w)
    draws.append(d)
    losses.append(l)
    evals.append(e)
    nodes.append(n)

    print(f"{board}\n"
          f"Move:  Starting Position\n"
          f"Nodes: {n}\n"
          f"Eval:  {e}\n"
          f"Win:   {w}\n"
          f"Draw:  {d}\n"
          f"Loss:  {l}\n")

    for i in moves:
        board.push_san(i)
        if "#" not in i:
            w, d, l, e, n = analyze(board, engine, limit, key, value)

            wins.append(w)
            draws.append(d)
            losses.append(l)
            evals.append(e)
            nodes.append(n)

            print(f"{board}\n"
                  f"Move:  {i}\n"
                  f"Nodes: {n}\n"
                  f"Eval:  {e}\n"
                  f"Win:   {w}\n"
                  f"Draw:  {d}\n"
                  f"Loss:  {l}\n")

    return wins, draws, losses, evals, nodes


def normalize_evals(evals):
    while "M+" in evals:
        loc = evals.index("M+")
        evals[loc] = 1000
    while "M-" in evals:
        loc = evals.index("M-")
        evals[loc] = -1000
    for i in evals:
        if i > 1000:
            loc = evals.index(i)
            evals[loc] = 1000
        if i < -1000:
            loc = evals.index(i)
            evals[loc] = -1000
    evals = [i/(2*max(evals))+0.5 for i in evals]
    return evals


def get_plots(wins, draws, losses, evals, nodes, exe):
    length = range(0, len(wins))
    evals = normalize_evals(evals)

    plt.stackplot(length, [wins, draws, losses], labels=["Win Rate", "Draw Rate", "Loss Rate"])
    plt.plot(length, evals, color="black", label="Normalized Evaluation")
    plt.plot(length, len(wins)*[0.5], color="black", linestyle="--")

    plt.xlim(0, len(wins)-1)
    plt.ylim(0, 1)
    plt.xlabel("Move (#)")
    plt.ylabel("WDL (%/100)")
    plt.title("Win Draw Loss (WDL) Plot")
    plt.legend()
    plt.tight_layout()
    plt.show()

    if exe == "stockfish-windows-x86-64-avx2.exe":
        node_avg = np.average(nodes)
        node_std = np.std(nodes)
        print(f"Node Average:            {node_avg}\n"
              f"Node Standard Deviation: {node_std}")

        plt.fill_between(length, node_avg-node_std, node_avg+node_std, color="bisque", label="Node Standard Deviation")
        plt.plot(length, nodes, color="blue", label="Nodes")
        plt.plot(length, len(wins)*[node_avg], color="orange", label="Node Average")

        plt.yscale("log")
        plt.xlim(0, len(wins))
        plt.xlabel("Move")
        plt.ylabel("Nodes")
        plt.title("Nodes per Move")
        plt.legend()
        plt.tight_layout()
        plt.show()

        nodes = [np.log10(i) for i in nodes]
        node_avg = np.average(nodes)
        node_std = np.std(nodes)

        q1 = np.quantile(nodes, 0.25)
        q3 = np.quantile(nodes, 0.75)
        width = 2*(q3-q1)/len(nodes)**(1/3)
        bins = int(np.ceil((max(nodes)-min(nodes))/width))

        ys, xs, _ = plt.hist(nodes, bins=bins, color="blue", density=True)

        def f(x):
            return 1/(node_std*np.sqrt(2*np.pi))*np.e**(-1/2*((x-node_avg)/node_std)**2)

        x = np.linspace(min(nodes), max(nodes), 1000000)
        plt.plot(x, f(x), color="green", label="Gaussian Distribution")
        plt.fill_betweenx([0, max(ys)], node_avg-node_std, node_avg+node_std, color="bisque", label="Node Standard Deviation")
        plt.axvline(node_avg, color="orange", label="Node Average")
        plt.hist(nodes, bins=bins, color="blue", density=True, label="Nodes")

        plt.ylim(0, max(ys))
        plt.xlabel("Logarithm Node Bins")
        plt.ylabel("Node Probability Density")
        plt.title("Gaussian Distribution of Logarithm Nodes")
        plt.legend()
        plt.tight_layout()
        plt.show()
