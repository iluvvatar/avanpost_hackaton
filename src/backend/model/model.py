from torch import nn


class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def load(self, version: str) -> "Model":
        pass

    def add_class(self, label: str, images_folder_path: str) -> None:
        pass

    def train(self) -> None:
        pass
