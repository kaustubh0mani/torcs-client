import torch
from torch.utils.data.dataset import Dataset
import numpy as np
import pandas as pd


class DriverDataset(Dataset):
    """Dataset of the training data provided by the CI course"""

    def __init__(self, csv_file, normalize=False):
        """
        Args:
            csv_file (string): Path to the csv file containing training data.
        """
        df = pd.read_csv(csv_file)
        # Drop last row
        df.drop(df.tail(1).index, inplace=True)
        self.data = df.as_matrix()

        if normalize:
            self.normalize()

    def normalize(self):
        # Normalize data
        new_data = []
        for i, column in enumerate(self.data.transpose()):

            if i < 3:
                new_data.append(column)

            # Speed 0 --> 300 km/hour
            if i == 3:
                new_data.append([(speed / 300) for speed in column])

            # Distance from centre, already normalized
            if i == 4:
                new_data.append(column)

            # Angle to track -1/2 pi --> 1/2 pi radians
            if i == 5:
                new_data.append([((angle + (0.5 * np.pi)) / np.pi) for angle in column])

            # Track edges 0 --> 200 meters
            if i > 5:
                new_data.append([distance / 200 for distance in column])

        self.data = np.array(new_data).T

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.Tensor(self.data[idx, :3]), torch.Tensor(self.data[idx, 3:])
