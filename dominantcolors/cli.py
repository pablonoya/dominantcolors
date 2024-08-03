import click

from .dominantcolors import color_extractor


@click.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option(
    "-c", "--target-contrast", default=3.0, show_default=True, help="Target contrast ratio"
)
@click.option("--bg-popup", default="#232A31", show_default=True, help="Background color of popup")
@click.option(
    "-a",
    "--alpha",
    default=208,
    type=click.IntRange(0, 255),
    show_default=True,
    help="Alpha value for blending with background color",
)
@click.option(
    "--bg-topbar", default="#303942", show_default=True, help="Background color of topbar"
)
def cli(image_path, target_contrast, bg_popup, alpha, bg_topbar):
    """Extract dominant colors from IMAGE_PATH"""

    color_extractor(image_path, target_contrast, bg_popup, alpha, bg_topbar)
