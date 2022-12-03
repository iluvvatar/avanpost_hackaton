import click
from .collect import get_images_from_google


def generate_dataset(path: str,
                     class_name: str,
                     num_docs: int,
                     drawn_ratio: float):
    get_images_from_google(path, class_name, num_docs, drawn_ratio)


@click.command()
@click.option('--path', required=True)
@click.option('--class-name', required=True)
@click.option('--num-docs', default=10, type=int)
@click.option('--drawn-ratio', default=0.0, type=float)
def main(path, class_name, num_docs, drawn_ratio):
    generate_dataset(path, class_name, num_docs, drawn_ratio)


if __name__ == '__main__':
    main()
