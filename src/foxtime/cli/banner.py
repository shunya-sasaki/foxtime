"""User interface components for the Foxtime CLI application."""

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.output.color_depth import ColorDepth

from foxtime.utils import GitVersion
from foxtime.utils import WebColor


class Banner:
    """User interface components for the LynkScan CLI application."""

    @classmethod
    def _lerp(cls, a: int, b: int, t: float) -> int:
        return int(a + (b - a) * t)

    @classmethod
    def _gradient_text(
        cls,
        text: str,
        length: int,
        start_color: tuple[int, int, int],
        end_color: tuple[int, int, int],
    ) -> FormattedText:
        result: list[tuple[str, str]] = []
        for i, char in enumerate(text):
            t = i / max(1, length - 1)
            r = cls._lerp(start_color[0], end_color[0], t)
            g = cls._lerp(start_color[1], end_color[1], t)
            b = cls._lerp(start_color[2], end_color[2], t)
            color_code = f"#{r:02x}{g:02x}{b:02x}"
            result.append((f"fg:{color_code}", char))
        return FormattedText(result)

    @classmethod
    def print_banner(
        cls,
        start_color: tuple[int, int, int] = WebColor.ORANGE.value.rgb,
        end_color: tuple[int, int, int] = WebColor.BLUE.value.rgb,
    ):
        """Print the Foxtime banner with gradient colors."""
        banner_strs = [
            " ███████╗  ██████╗  ██╗  ██╗ ████████╗ ██╗ ███╗   ███╗ ███████╗",
            " ██╔════╝ ██╔═══██╗ ╚██╗██╔╝ ╚══██╔══╝ ██║ ████╗ ████║ ██╔════╝",
            " █████╗   ██║   ██║  ╚███╔╝     ██║    ██║ ██╔████╔██║ █████╗",
            " ██╔══╝   ██║   ██║  ██╔██╗     ██║    ██║ ██║╚██╔╝██║ ██╔══╝",
            " ██║      ╚██████╔╝ ██╔╝ ██╗    ██║    ██║ ██║ ╚═╝ ██║ ███████╗",
            " ╚═╝       ╚═════╝  ╚═╝  ╚═╝    ╚═╝    ╚═╝ ╚═╝     ╚═╝ ╚══════╝",
        ]
        n_max = max(len(s) for s in banner_strs)
        version = f"CLI Version {GitVersion.version()}"
        n_version = len(version)
        n_space = n_max - n_version
        print("")
        print(" Welcome to")
        for line in banner_strs:
            print_formatted_text(
                cls._gradient_text(
                    line,
                    n_max,
                    start_color=start_color,
                    end_color=end_color,
                ),
                color_depth=ColorDepth.DEPTH_24_BIT,
            )
        print(f"{' ' * n_space}{version}")

    @classmethod
    def print_simple_banner(cls):
        """Print a simple Foxtime banner."""
        banner_strs = [
            "Welcome to Foxtime!",
            " /\\_/\\",
            "( o.o ) Swift. Timeboxed.",
            " >   <",
        ]
        n_max = max(len(s) for s in banner_strs)
        version = f"CLI Version {GitVersion.version()}"
        n_version = len(version)
        n_space = n_max - n_version
        print("")
        for line in banner_strs:
            print(line)
        print(f"{version}")
