from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats

from .tools.utils import int_round


class SamplingData(ABC):
    """ABC for sampling data. Sampling data is data ready to be sampled, with the `sample`
    method.
    """

    @abstractmethod
    def compute_samples(self, *args, **kwargs):
        pass

    @abstractmethod
    def sample(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def display_info(self, title: str):
        pass


class CategoricalSamplingData(SamplingData):
    """Categorical sampling data is data that is not considered as continuous, and can therefore
    be sampled with a simple `np.random.choice` call.
    """

    def __init__(self, values: List[Any]):
        self.values = values
        self.samples: List[Any] = []

    def compute_samples(self, size: int = 100, *args, **kwargs):
        samples = list(np.random.choice(self.values, size=size))
        self.samples.extend(samples)

    def sample(self, *args, **kwargs) -> Any:
        try:
            return self.samples.pop()
        except IndexError:
            self.compute_samples()
            return self.samples.pop()

    def display_info(self, title: str):
        print(f"{title} ({len(self.values)}): {set([str(value) for value in self.values][:5])}")


class UniqueCategoricalSamplingData(CategoricalSamplingData):
    """Unique categorical sampling data is a subset of categorical sampling data where the data
    is considered as unique and can therefore not be sampled with replacement.
    """

    def compute_samples(self, *args, **kwargs):
        pass

    def sample(self, size: int, *args, **kwargs) -> Any:  # type: ignore
        return list(np.random.choice(self.values, size=size, replace=False))

    def display_info(self, title: str):
        print(f"{title} ({len(self.values)}): {set([str(value) for value in self.values][:5])}")


class ContinuousSamplingData(SamplingData):
    """Continuous sampling data is data that is sampled through a probability density function."""

    def __init__(self, values: List[Any]):
        self.values = values
        self.min_value = min(values)
        self.max_value = max(values)
        self.samples: List[Any] = []

        if self.min_value != self.max_value:  # General case
            self.x = np.arange(0, self.max_value)
            dist = scipy.stats.gamma
            params = dist.fit(self.values)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]

            if arg:
                pdf = dist.pdf(self.x, *arg, loc=loc, scale=scale)
            else:
                pdf = dist.pdf(self.x, loc=loc, scale=scale)
            self.pdf = pdf
        else:  # Case where there is only one value
            self.x = None
            self.pdf = None

    def compute_samples(self, size: int = 100, *args, **kwargs):
        if self.pdf is not None:  # General case
            samples = list(np.random.choice(self.x, p=self.pdf / np.sum(self.pdf), size=size))
        else:  # Case where there is only one value
            samples = [self.values[0] for _ in range(size)]
        self.samples.extend(samples)

    def sample(self, *args, **kwargs) -> Any:
        try:
            sample = self.samples.pop()
        except IndexError:
            self.compute_samples()
            sample = self.samples.pop()

        return int(sample)

    def display_info(self, title: str):
        if self.pdf is not None:  # General case
            bins = 50

            fig, ax1 = plt.subplots()
            color1 = "tab:blue"
            ax1.hist(self.values, bins=bins, color=color1)
            ax1.set_ylabel("count", color=color1)
            ax1.tick_params(axis="y", labelcolor=color1)
            ax1.set_ylim(bottom=0)

            ax2 = ax1.twinx()
            color2 = "tab:red"
            ax2.plot(self.pdf, color=color2)
            ax2.set_ylabel("pdf", color=color2)
            ax2.tick_params(axis="y", labelcolor=color2)
            ax2.set_ylim(bottom=0)

            plt.title(title)
            plt.show()
        else:  # Case where there is only one value
            print(f"{title}: distribution with single value '{self.values[0]}'")


class DtSamplingData(SamplingData):
    """Datetime sampling data is a particular case of continuous sampling data where the data is
    made of datetimes. Datetimes are considered as made of two distinct continuous sampling data:
    one for the time of the day & the other one for the date.
    """

    def __init__(self, dts: List[datetime]):
        self.tz_info = dts[0].tzinfo  # Assume all the dates have the same timezone
        dates = [dt.date() for dt in dts]
        self.min_date = min(dates)
        days = [(date - self.min_date).days for date in dates]
        self.days_sampling_data = ContinuousSamplingData(days)

        minutes = [dt.time().hour * 60 + dt.time().minute for dt in dts]
        self.minutes_sampling_data = ContinuousSamplingData(minutes)

    def compute_samples(self, size: int = 100, *args, **kwargs):
        self.days_sampling_data.compute_samples(size=size)
        self.minutes_sampling_data.compute_samples(size=size)

    def sample_dt(self) -> datetime:
        day = self.days_sampling_data.sample()
        minute = self.minutes_sampling_data.sample()
        minute = int_round(minute, n=5)  # Round to 5 minutes

        min_dt = datetime(
            year=self.min_date.year,
            month=self.min_date.month,
            day=self.min_date.day,
            tzinfo=self.tz_info,
        )
        dt = min_dt + timedelta(days=day, minutes=minute)
        return dt

    def sample(self, *args, **kwargs) -> str:
        dt = self.sample_dt()
        return dt.isoformat()  # Output has format '2016-12-05T14:40:00+02:00'

    def display_info(self, title: str):
        self.days_sampling_data.display_info(title=f"{title} - days")
        self.minutes_sampling_data.display_info(title=f"{title} - minutes")


class DtDurationSamplingData(SamplingData):
    """Datetime duration sampling data is a particular case off continuous sampling where the
    data is made of duration between two datetimes. Durations are considered as made of two
    distinct continuous sampling data: one for the start date & the other one for the duration.
    """

    def __init__(self, dt_pairs: List[Tuple[datetime, datetime]]):
        start_dts = [dt_pair[0] for dt_pair in dt_pairs]
        self.start_dts_sampling_data = DtSamplingData(start_dts)

        second_durations = [(dt_pair[1] - dt_pair[0]).total_seconds() for dt_pair in dt_pairs]
        minute_durations = [round(duration / 60) for duration in second_durations]
        self.durations_sampling_data = ContinuousSamplingData(minute_durations)

    def compute_samples(self, size: int = 100, *args, **kwargs):
        self.start_dts_sampling_data.compute_samples(size=size)
        self.durations_sampling_data.compute_samples(size=size)

    def sample(self, *args, **kwargs) -> Tuple[str, str]:
        start_dt = self.start_dts_sampling_data.sample_dt()
        duration = -1
        while duration < 0:
            duration = self.durations_sampling_data.sample()
            duration = int_round(duration, n=5)  # Round to 5 minutes

        end_dt = start_dt + timedelta(minutes=duration)
        return start_dt.isoformat(), end_dt.isoformat()

    def display_info(self, title: str):
        self.start_dts_sampling_data.display_info(title=f"{title} - start")
        self.durations_sampling_data.display_info(title=f"{title} - duration")


def to_sampling_data(values: list, unique: bool = False) -> SamplingData:
    """Put the input data in the relevant SamplingData sub-class."""
    if all([isinstance(value, str) for value in values]):
        try:
            # Values has a format like '2016-11-21T14:45:00+02:00'
            dts = [datetime.fromisoformat(value) for value in values]
            return DtSamplingData(dts=dts)
        except ValueError:
            pass

    elif all([isinstance(value, tuple) for value in values]):
        try:
            # Values has a format like ('2016-11-21T14:45:00+02:00', '2016-11-21T15:45:00+02:00')
            dt_pairs = [
                (datetime.fromisoformat(start_dt), datetime.fromisoformat(end_dt))
                for start_dt, end_dt in values
            ]
            return DtDurationSamplingData(dt_pairs=dt_pairs)
        except ValueError:
            pass

    elif all(
        [
            (isinstance(value, dict) and "start" in value and "end" in value and len(value) == 2)
            for value in values
        ]
    ):
        try:
            # Values has a format like
            # {"start": '2016-11-21T14:45:00+02:00', "end": '2016-11-21T15:45:00+02:00'}
            dt_pairs = [
                (datetime.fromisoformat(value["start"]), datetime.fromisoformat(value["end"]))
                for value in values
            ]
            return DtDurationSamplingData(dt_pairs=dt_pairs)
        except ValueError:
            pass

    if not unique:
        return CategoricalSamplingData(values=values)
    else:
        return UniqueCategoricalSamplingData(values=values)