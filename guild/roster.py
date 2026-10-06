"""公会名册：容量上限、VIP 覆盖层与候补补位。"""


class Roster:
    """公会名册台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.members = set()
        self.vips = set()
        self.waiting = {}
        self.seen = {}
        self.scanned = 0

    def _promote(self):
        """有空缺时按申请先后把候补第一名补进名册。"""
        if self.waiting and len(self.members) - len(self.vips) < self.cap:
            name = next(iter(self.waiting))
            del self.waiting[name]
            self.members.add(name)

    def apply(self, request_id, player, vip, at_ms):
        """申请入会，返回状态。"""
        if request_id in self.seen:
            return self.seen[request_id]
        self.scanned += 1
        if player in self.members:
            status = "member"
        elif player in self.waiting:
            status = "waiting"
        elif vip:
            self.members.add(player)
            self.vips.add(player)
            status = "member"
        elif len(self.members) - len(self.vips) < self.cap:
            self.members.add(player)
            status = "member"
        else:
            self.waiting[player] = None
            status = "waiting"
        self.seen[request_id] = status
        return status

    def leave(self, request_id, player):
        """退会，返回状态。"""
        if request_id in self.seen:
            return self.seen[request_id]
        self.scanned += 1
        if player in self.members:
            self.members.discard(player)
            self.vips.discard(player)
            self._promote()
            status = "left"
        elif player in self.waiting:
            del self.waiting[player]
            status = "left"
        else:
            status = "absent"
        self.seen[request_id] = status
        return status
