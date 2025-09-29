"""Build the architecture diagram, both themes.

    python3 scripts/build-diagram.py

User and Web page are the two Octicons in the picture, in ink and outside the
boundary, bracketing the flow at either end. Cloudflare services take their
product icons in brand orange inside it, so the two sets are what make the
boundary readable before any label is.

Workers AI is an off-path card: the flow consults it to decide the next
action, rather than passing through it, so the generator draws it at
BRANCH_SCALE of the row height. Its connector is bidirectional because the
consultation is a round trip: the Worker sends page context and the model
returns the action to take.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path.home() / ".agents/skills/cloudflare-diagrams/assets"))

from cfdiagram import Diagram, Flow, Node  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/assets"


def build(theme):
    nodes = [
        Node("user", "person", "User", inside=False, external=True),
        Node("worker", "workers", "Workers", "stagehand-example"),
        Node("browser", "browser-run", "Browser Run"),
        Node("page", "globe", "Web page", inside=False, external=True),
    ]
    flows = [
        Flow(0, 1, "GET /"),
        Flow(1, 2, "drives Playwright", "over CDP"),
        Flow(2, 3, "navigates", ["observe, act,", "extract"]),
    ]
    d = Diagram(nodes, flows, theme,
                branch=(1, Node("ai", "workers-ai", "Workers AI"), "decides each action", True))
    d.render()
    return d


for theme in ("light", "dark"):
    d = build(theme)
    path = OUT / f"arch-diagram{'' if theme == 'light' else '-dark'}.svg"
    path.write_text(d.finish())
    print(f"  {path.name}: {d.W:.0f}x{d.H:.0f} aspect {d.W / d.H:.2f}")
