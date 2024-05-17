# Chess WDL
Plot Stockfish and/or Leela Chess Zero win-draw-loss (WDL) rates of any lichess game.

# Setup
1. Install Python at https://www.python.org/downloads/.
2. Download repository.
3. Open Terminal in repository folder.
4. Enter `pip install chess`.
5. Enter `pip install lichesspy`.
6. Enter `pip install matplotlib`.
7. Enter `pip install numpy`.
8. Enter `python main.py`.

# Usage
Run *main.py* via `python main.py` in Terminal.
`Game:` will print.
Enter the lichess game to analyze.
After, Stockfish 16.1 or Leela Chess Zero will analyze the game.
Stockfish is the default engine.
To switch to Leela Chess Zero, open *main.py* and add a `#` in front of `stockfish-windows-x86-64-avx2.exe` and delete the `#` in front of `lc0.exe`.
Based on the user's home machine software and hardware, reinstalling Leela Chess Zero may be necessary for the script to run properly.
Leela Chess Zero is available at https://lczero.org/.
UPDATE: Leela Chess Zero files are too big to upload to GitHub.
To utilize Leela Chess Zero analysis, please install the engine at the link and replace `lc0.exe` with the proper path.

During analysis, the current position, move, nodes, and evaluation (centipawns) will print, alongside the win, draw, and loss rates.
Once analysis completes, the generated WDL plot will display.
If Stockfish was used, two more plots will appear after closing the WDL plot, displaying the number of nodes used to analyze each position in the game to depth 30.
If Leela Chess Zero was used, no more plots will be generated.
This is because in this script Leela Chess Zero is used to analyze positions using 1 node, making node analysis unnecessary.

In this script, `Threads` and `Hash` are both set to `1` for Stockfish analysis.
Threads are the number of CPU cores Stockfish uses to analyze.
Increasing threads increases the speed with which Stockfish analyzes.
However, to generate deterministic results, threads must be set to 1.
If the user is content with in-deterministic results, the user can increase threads assuming the user's CPU has an equivalent or greater number of cores.

Hash is the amount of random access memory (RAM) Stockfish uses to analyze.
Increasing hash will provide more-accurate evaluation at the expense of increased calculation time.
To minimize calculation time, hash is set to its minimum value of 1 in this script.

This script is inspired by Leela Chess Zero's Win-Draw-Loss evaluation blog, located at https://lczero.org/blog/2020/04/wdl-head/.
The purpose of this script is to enable anyone to generate WDL plots easily.

# Example
Suppose the user wants to analyze the 2021 World Chess Championship Game 6.
This game is available at https://lichess.org/GigY8gpa/.
`GigY8gpa` is the game tag.

Run *main.py* via `python main.py` in Terminal.
When `Game:` prints, enter the game, namely `GigY8gpa`.
After, the script will analyze the game with Stockfish at depth 30 or Leela Chess Zero at 1 node depending on user preference.
Stockfish analysis provides a long but accurate analysis of the game.
Leela Chess Zero analysis provides a quick and mostly accurate analysis of the game, occasionally missing tactical ideas.
During this process, the current position, move, nodes, and evaluation (centipawns) will print, as well as the win, draw, and loss rates.
For this example, both engines were used.

In the end, the average and the standard deviation of the nodes will print.
Then, the plots will show.
To cycle through the plots, simply close them.
These plots are the key result of this script.
For this example, the plots are named *Figure_0.png*, *Figure_1.png*, *Figure_2.png* and *Figure_3.png* in the repository.

*Figure_0.png* is the WDL graph generated via Stockfish at depth 30.
*Figure_1.png* displays the number of nodes Stockfish used to gather evaluation and WDL rates at depth 30.
*Figure_2.png* takes the logarithm of each point in *Figure_1.png* and plots them via a histogram, indicating a Gaussian distribution.
*Figure_3.png* is the WDL graph generated via Leela Chess Zero at 1 node.

# Errors
1. `lichesspy.api.ApiHttpError: 404`
Solution: Invalid game entered.
Enter the correct game tag.
If the game recently concluded, the lichess API may not have yet updated.

# Contact
For help, improvements, etc., feel free to contact **silveryystar** on Discord.
