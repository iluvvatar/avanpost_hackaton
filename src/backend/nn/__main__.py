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


def retrain(umid: str, path: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('score=0.9')


@click.command()
@click.option('--command', required=True)
@click.option('--dataset', required=True)
@click.option('--umid')
def main(command, dataset, umid):
    if command == 'predict' and umid:
        predict(umid, dataset)
    elif command == 'train':
        train(dataset)
    elif command == 'retrain' and umid:
        retrain(umid, dataset)
    else:
        update_progress_error('unknown command')


if __name__ == '__main__':
    main()
