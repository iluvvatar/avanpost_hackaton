import click
from .operations import predict, predict_single, retrain


@click.command()
@click.option('--command', required=True)
@click.option('--dataset')
@click.option('--filename')
@click.option('--umid')
def main(command, dataset, filename, umid):
    if command == 'predict' and umid and dataset:
        predict(umid, dataset)
    elif command == 'predict_single' and umid and filename:
        predict_single(umid, filename)
    elif command == 'retrain' and umid and dataset:
        retrain(umid, dataset)


if __name__ == '__main__':
    main()
