import click

from .dominantcolors import color_extractor


@click.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option(
    "-c", "--target-contrast", default=3.0, show_default=True, help="Target contrast ratio"
)
def cli(image_path, target_contrast):
    """Extract dominant colors from IMAGE_PATH"""
    color_extractor(image_path, target_contrast)
