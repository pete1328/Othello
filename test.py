import unittest
import client

#2/22 NOTES ...
# both remote, p2 "always" wins (4 tries so far)
# against random (games so far)
#   p1 remote won
#   p2 remote lost
#   p2 remote won
#   p1 remote TIE
#   p1 remote won
#2/24 NOTES...
# both remote, p1 wins (4 tries so far)
# p1 remote lost, won, lost
# p2 remote lost, won, won
#2/25 NOTES...
# p2 remote won, TIE, TIE, lost, lost
# p1 remote won, lost, lost, won, lost
#^ after refactored
# p1 remote lost, won, lost

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
  def test_old_error1(self):
    player = 1
    board = [[0, 2, 2, 2, 2, 0, 1, 0], [1, 1, 2, 2, 1, 1, 0, 0], [1, 1, 2, 1, 2, 1, 1, 0], [0, 2, 1, 1, 1, 1, 1, 0], [1, 2, 1, 1, 1, 2, 1, 0], [1, 2, 1, 1, 1, 1, 2, 1], [0, 1, 1, 0, 0, 0, 1, 1], [1, 0, 1, 0, 0, 0, 0, 1]]
    '''
    [[0, 2, 2, 2, 2, 0, 1, 0],
     [1, 1, 2, 2, 1, 1, 0, 0], 
     [1, 1, 2, 1, 2, 1, 1, 0], 
     [0, 2, 1, 1, 1, 1, 1, 0], 
     [1, 2, 1, 1, 1, 2, 1, 0], 
     [1, 2, 1, 1, 1, 1, 2, 1], 
     [0, 1, 1, 0, 0, 0, 1, 1], 
     [1, 0, 1, 0, 0, 0, 0, 1]]
     ...sending [0, 0]'''
    self.assertEqual(client.get_move(player, board), [3,0])
    #NOTE: had to fix check_line while loop now that we add to opts instead of returning sub_opts list

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

if __name__ == '__main__':
  unittest.main()