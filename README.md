# Unit tags

A [ProLeak](https://github.com/LegionTD2-Modding/ProLeak) plugin for Legion TD 2. Each fighter
you place gets the next free name from your list, shown above its health bar. A fighter keeps
its name through upgrades and waves; selling it frees the name for the next one.

## Settings

In the game, Mods > Unit tags > Settings:

| Setting | Default | Effect |
|---|---|---|
| Tag names | `Kidev, Alice, Bob` | The names, comma separated. Editing the list renames the fighters at once. |
| Reuse names | off | With more fighters than names, hand the names out again in order. |
| Tag color | `#33ff33` | Text color. |
| Tag size | 0.5 | Text size, 0.1 to 3. |
| Tag spacing | 5 | Gap above the health bar, -30 to 30 health bar pixels; below 0 moves the tag onto the bar. |

## Installing

In the game, Mods > Browse lists it: press Install. ProLeak installs the latest release and
offers each update in the Mods tab.

To install it by hand, copy this folder into `ProLeak/plugins/` in the game folder, so that
`plugin.yml` sits at `ProLeak/plugins/kidev.unit-tags/plugin.yml`.

## License

GNU Affero General Public License v3.0; see [LICENSE](LICENSE).
