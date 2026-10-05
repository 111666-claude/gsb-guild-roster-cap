import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guild.roster import Roster  # noqa: E402


class RosterTest(unittest.TestCase):
    def test_first_apply_is_member(self):
        self.assertEqual(Roster(3).apply("e1", "a", False, 1), "member")

    def test_same_player_is_not_added_twice(self):
        r = Roster(3)
        r.apply("e1", "a", False, 1)
        self.assertEqual(r.apply("e2", "a", False, 2), "member")
        self.assertEqual(len(r.members), 1)

    def test_leave_removes_member(self):
        r = Roster(3)
        r.apply("e1", "a", False, 1)
        self.assertEqual(r.leave("e2", "a"), "left")
        self.assertEqual(len(r.members), 0)

    def test_leave_absent_player(self):
        self.assertEqual(Roster(3).leave("e1", "ghost"), "absent")


if __name__ == "__main__":
    unittest.main()
