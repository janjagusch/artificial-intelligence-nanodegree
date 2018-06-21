"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    # def setUp(self):
        # reload(game_agent)
        # self.player1 = "Player 1"
        # self.player2 = "Player 2"
        # self.game = isolation.Board(self.player1, self.player2)

    def test_minimax(self):
        self.minimax_player = game_agent.MinimaxPlayer(score_fn=sample_players.center_score, timeout=float("inf"))
        self.greedy_player = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.minimax_player, self.greedy_player)
        # self.game.play(time_limit=float("inf"))
        self.minimax_player.match_boards(self.game, self.game)




if __name__ == '__main__':
    unittest.main()
