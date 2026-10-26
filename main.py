"""Puts a name from a list above each fighter you place, and keeps it until the fighter is sold."""
from proleak import on, settings, timers, ui, world

from .names import Names, parse

NAMES = settings.add("tag_names", "Kidev, Alice, Bob", label="Tag names", subtitle="Comma separated")
LOOP = settings.add("tag_loop", False, label="Reuse names",
                    help="When there are more fighters than names, start the list again")
COLOR = settings.add("tag_color", "#33ff33", type="color", label="Tag color")
SIZE = settings.add("tag_size", 0.5, min=0.1, max=3, label="Tag size")
SPACING = settings.add("tag_spacing", 5, min=-30, max=30, label="Tag spacing",
                       subtitle="In health bar pixels",
                       help="The gap between the health bar and the tag. Below 0 moves the tag onto the bar.")

carriers = Names()


def on_load(ctx):
    timers.after(0, tag_existing)       # loaded mid-game (a reload): name the fighters already placed


def tag_existing():
    me = world.player()
    if me is None:
        return
    for unit in me.fighters():
        tag(unit)


@on("game.started")
def started(ev):
    global carriers
    carriers = Names()


@on("unit.built")
def built(ev):
    if ev.player is not None and ev.player.is_local:
        tag(ev.unit)


@on("unit.sold")
def sold(ev):
    carriers.release(ev.unit.id)


@NAMES.on_change
@LOOP.on_change
def names_changed(value):
    retag()


def retag():
    """Applies a changed name list or reuse option to the fighters already tagged."""
    me = world.player()
    if me is None:
        return
    wanted = carriers.retag([u.id for u in me.fighters()], parse(NAMES.value), LOOP.value)
    for unit, name in wanted.items():
        tags = ui.nameplates(unit=unit)
        if name is None:
            for nameplate in tags:
                nameplate.remove()
        elif tags:
            tags[0].set_text(name)
        else:
            plate(unit, name)


def tag(unit):
    if ui.nameplates(unit=unit):
        return
    name = carriers.take(unit.id, parse(NAMES.value), LOOP.value)
    if name is not None:
        plate(unit, name)


def plate(unit, name):
    # The tag follows the settings by itself, and an upgraded fighter keeps its unit id and its tag.
    ui.nameplate(unit, name, color=COLOR, size=SIZE, spacing=SPACING, name_suffix=True)
