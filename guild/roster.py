"""公会名册：容量上限、VIP 覆盖层与候补补位。"""


class Roster:
    """公会名册台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.members = []
        self.waiting = []
        self.seen = set()
        self.scanned = 0

    def apply(self, request_id, player, vip, at_ms):
        """申请入会，返回状态。"""
        self.seen.add(request_id)
        for name in self.members:
            self.scanned += 1
            if name == player:
                return "member"
        for name in self.waiting:
            self.scanned += 1
            if name == player:
                return "waiting"
        self.members.append(player)
        return "member"

    def leave(self, request_id, player):
        """退会，返回状态。"""
        self.seen.add(request_id)
        if player in self.members:
            self.members.remove(player)
            return "left"
        if player in self.waiting:
            self.waiting.remove(player)
            return "left"
        return "absent"
