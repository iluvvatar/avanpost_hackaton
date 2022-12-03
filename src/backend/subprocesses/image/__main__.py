import click


from .collect import get_images_from_google, get_image, get_dataset


@click.command()
@click.option('--command', required=True)
@click.option('--path', required=True)
@click.option('--link', required=True)
@click.option('--class-name')
@click.option('--num-docs', default=10, type=int)
@click.option('--drawn-ratio', default=0.0, type=float)
def main(command, path, link, class_name, num_docs, drawn_ratio):
    if command == 'get_dataset_for_new_class' and class_name:
        get_images_from_google(path, class_name, num_docs, drawn_ratio)
    elif command == 'get_dataset' and link:
        get_dataset(path, link)
    elif command == 'get_image' and link:
        get_image(path, link)


if __name__ == '__main__':
    main()
