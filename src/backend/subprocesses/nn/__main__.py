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


def predict_single(umid: str, filename: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('class_name=snowboard')


def train(path: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('umid=m1;score=0.9')


def retrain(umid: str, path: str):
    for i in range(10):
        update_progress(0.1 * i)

    # TODO: pass results
    update_progress_done('umid=m2;score=0.9')


@click.command()
@click.option('--command', required=True)
@click.option('--dataset')
@click.option('--filename')
@click.option('--umid')
def main(command, dataset, umid):
    if command == 'predict' and umid and dataset:
        predict(umid, dataset)
    elif command == 'predict_single' and umid and filename:
        predict_single(umid, filename)
    elif command == 'train' and dataset:
        train(dataset)
    elif command == 'retrain' and dataset and umid:
        retrain(umid, dataset)
    else:
        update_progress_error('unknown command')


if __name__ == '__main__':
    main()
