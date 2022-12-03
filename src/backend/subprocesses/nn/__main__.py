import click


from .operations import predict, predict_single, retrain


@click.command()
@click.option('--command', required=True)
@click.option('--dataset')
@click.option('--filename')
@click.option('--umid')
@click.option('--class-name')
def main(command, dataset, filename, umid, class_name):
    if command == 'predict' and umid and dataset:
        predict(umid, dataset)
    elif command == 'predict_single' and umid and filename:
        predict_single(umid, filename)
    elif command == 'retrain' and umid and class_name:
        retrain(umid, class_name)


if __name__ == '__main__':
    main()
