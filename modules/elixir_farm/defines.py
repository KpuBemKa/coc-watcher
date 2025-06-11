from modules.datas import Color
from modules.datas import Position


class Coords:
    ELIXIR_CART = Position(1590, 0, 10, 10)
    ELIXIR_ICONS = [
        Position(1675, 330),
        Position(1675, 545),
        Position(1675, 763),
        Position(1675, 980),
    ]
    COLLECT_BUTTON = Position(1880, 1210, 100, 60)
    BATTLE_ROWS = [
        Position(940, 245),
        Position(940, 265),
        Position(940, 685),
        Position(940, 900),
    ]

    ATTACK_BUTTON = Position(140, 1295, 100, 100)
    FIND_ATTACK_BUTTON = Position(1900, 950, 190, 90)
    BATTLE_WAIT = Position(1741, 879)
    UNIT_PLACEMENT = Position(537, 302, 50, 50)
    END_OKAY_BUTTON = Position(1519, 893)

class Colors:
    BATTLE_SEARCHING = Color(131, 119, 119)
    BATTLE_ROW_EXISTS = Color(229, 233, 235)
    BATTLE_ROW_IN_PROGRESS = Color(166, 158, 142)
    # ELIXIR_ICON = Color(218, 40, 148)
    ELIXIR_ICON = Color(248, 46, 169)
