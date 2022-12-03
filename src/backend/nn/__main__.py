import click


def update_progress_error(message: str):
    pass


def update_progress_done(message: str):
    pass


def update_progress(value: float):
    pass


def predict(umid: str, path: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('score=0.9')


def train(path: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('umid=m1')


@click.command()
@click.option('--command')
@click.option('--dataset')
def main(command, dataset):
    if command == 'predict':
        predict('m1', dataset)
    elif command == 'train':
        train(dataset)
    else:
        update_progress_error('unknown command')


if __name__ == '__main__':
    main()
