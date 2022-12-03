import click


def update_progress_error(message: str):
    pass


def update_progress_done(message: str):
    pass


def update_progress(value: float):
    pass


def generate_dataset(path: str,
                     class_name: str,
                     num_docs: int,
                     drawn_ratio: float):
    print(drawn_ratio)
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('done')


@click.command()
@click.option('--path', required=True)
@click.option('--class-name', required=True)
@click.option('--num-docs', default=500, type=int)
@click.option('--drawn-ratio', default=0.1, type=float)
def main(path, class_name, num_docs, drawn_ratio):
    generate_dataset(path, class_name, num_docs, drawn_ratio)


if __name__ == '__main__':
    main()
