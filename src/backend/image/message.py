def update_progress_error(message: str):
    pass


def update_progress_done(message: str):
    print('PROGRESS: DONE', flush=True)


def update_progress(value: float):
    print(f'PROGRESS: {value}', flush=True)
