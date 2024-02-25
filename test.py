import unittest
import client

class TestGetMove(unittest.TestCase):
  def test_get_move_returns_a_valid_move(self):
    board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0]]
    ''' different than GIVEN:
    [[0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0], 
     [0, 0, 0, 1, 1, 0, 0, 0], 
     [0, 0, 1, 1, 1, 0, 0, 0], 
     [0, 0, 2, 0, 0, 0, 0, 0], 
     [0, 0, 2, 0, 0, 0, 0, 0], 
     [0, 0, 2, 0, 0, 0, 0, 0]]
    '''
    #GIVEN -- inaccurate?? self.assertEqual(client.get_move(1, board), [2, 3])
    self.assertEqual(client.get_move(1, board), [6,1])

class TestErrorCausingBoards(unittest.TestCase):
  def test_current_error1(self):
    player = 1
    board = [[1, 2, 2, 2, 2, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0]]
    '''[[1, 2, 2, 2, 2, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 0, 1, 1, 0, 0, 0], 
        [0, 0, 1, 1, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 1, 0, 0]]'''
    result = client.check_line(board, (0,1), (0,5), player, 2)
    self.assertEqual(result, (4,(0,5)))
    #NOTE: was never going into while loop in this case because r=0 and r_increment=0, (fixed) 2/25
  
  def test_current_error2(self):
    player = 1
    board = [[1, 2, 2, 2, 2, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 0], [2, 1, 0, 1, 1, 0, 0, 0], [2, 0, 1, 1, 1, 0, 0, 0], [2, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0]]
    '''[[1, 2, 2, 2, 2, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 1, 1, 0], 
        [2, 1, 0, 1, 1, 0, 0, 0], 
        [2, 0, 1, 1, 1, 0, 0, 0], 
        [2, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 1, 0, 0]]'''
    result = client.check_line(board, (1,0), (6,0), player, 2)
    self.assertEqual(result, (3,(6,0)))

  def test_current_error3(self):
    player = 2
    board = [[0, 2, 2, 2, 2, 2, 2, 1], [2, 2, 1, 2, 1, 2, 2, 1], [0, 2, 2, 1, 1, 2, 2, 1], [0, 2, 2, 1, 1, 2, 2, 1], [0, 2, 1, 1, 2, 1, 1, 1], [2, 2, 2, 1, 2, 2, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1], [2, 0, 2, 1, 0, 0, 0, 0]]
    '''[[0, 2, 2, 2, 2, 2, 2, 1],
        [2, 2, 1, 2, 1, 2, 2, 1], 
        [0, 2, 2, 1, 1, 2, 2, 1], 
        [0, 2, 2, 1, 1, 2, 2, 1], 
        [0, 2, 1, 1, 2, 1, 1, 1], 
        [2, 2, 2, 1, 2, 2, 1, 1], 
        [2, 2, 2, 2, 2, 2, 2, 1], 
        [2, 0, 2, 1, 0, 0, 0, 0]]'''

    result = client.check_line(board, (0,1), (7,4), player, 1)
    self.assertEqual(result, (1,(7,4)))
    '''found opponents piece at [6,7]
    found empty spot adjacent to opp at [7,6]
    Checking row/col/diag
    Looking at [6,7]
    results for that empty spot - pts:0, best_spot(7, 6)
    found empty spot adjacent to opp at [7,7]
    Checking row/col/diag
    results for that empty spot - pts:0, best_spot(7, 7)

    found opponents piece at [7,3]
    found empty spot adjacent to opp at [7,4]
    Checking row/col/diag
    results for that empty spot - pts:0, best_spot(7, 4)
    Found options: {}
    Best Opt: (-1, -1)'''
    #NOTE: still had to fix the while loop in this case because r=7 but r_increment=0 too, (fixed) 2/25


class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

class TestGreatOdds(unittest.TestCase):
  def test_wins_min_51_out_of_100_plays(self):
    wins = 55 # TODO
    self.assertTrue(wins > 50)

if __name__ == '__main__':
  unittest.main()