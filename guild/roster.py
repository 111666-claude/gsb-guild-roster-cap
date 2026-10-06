"""公会名册：容量上限、VIP 覆盖层与候补补位。"""

from collections import deque


class Roster:
    """公会名册台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.members = []
        self.waiting = deque()
        self._member_set = set()
        self._waiting_set = set()
        self.seen = {}
        self.scanned = 0

    def apply(self, request_id, player, vip, at_ms):
        """申请入会，返回状态。"""
        if request_id in self.seen:
            return self.seen[request_id]
        if player in self._member_set:
            status = "member"
        elif player in self._waiting_set:
            status = "waiting"
        elif vip or len(self._member_set) < self.cap:
            self.members.append(player)
            self._member_set.add(player)
            status = "member"
        else:
            self.waiting.append(player)
            self._waiting_set.add(player)
            status = "waiting"
        self.seen[request_id] = status
        return status

    def leave(self, request_id, player):
        """退会，返回状态。"""
        if request_id in self.seen:
            return self.seen[request_id]
        if player in self._member_set:
            self._member_set.remove(player)
            self.members.remove(player)
            status = "left"
            self._promote()
        elif player in self._waiting_set:
            self._waiting_set.remove(player)
            self.waiting.remove(player)
            status = "left"
        else:
            status = "absent"
        self.seen[request_id] = status
        return status

    def _promote(self):
        """有空缺时按申请先后把候补补进名册。"""
        while self.waiting and len(self._member_set) < self.cap:
            player = self.waiting.popleft()
            self._waiting_set.remove(player)
            self.members.append(player)
            self._member_set.add(player)
