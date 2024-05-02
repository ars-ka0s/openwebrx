from owrx.source.connector import ConnectorSource, ConnectorDeviceDescription
from owrx.command import Option, Flag
from owrx.form.input import Input, NumberInput, TextInput, CheckboxInput
from owrx.form.input.validator import RangeValidator, Range
from typing import List

# The following command line options are available:
#    --device     - TCI server address in host:port or ip:port format
#    --receiver   - Which receiver to use; 0 or 1
#    --port       - IQ data port number
#    --frequency  - Center frequency in Hz
#    --samplerate - Sample rate in Hz; 48000, 96000, 192000, 384000 are valid
#    --control    - Control port number
#    --startstop  - Start/stop the whole radio device alongside the IQ stream
#    --verbose    - Show additional details in the log

class EesdrSource(ConnectorSource):
    def getCommandMapper(self):
        return (
            super()
            .getCommandMapper()
            .setBase("eesdr-owrx-connector")
            .setMappings(
                {
                    "device": Option("--device"),
                    "receiver": Option("--receiver"),
                    "tuner_freq": Option("--frequency"),
                    "samp_rate": Option("--samplerate"),
                    "startstop": Flag("--startstop"),
                    "verbose": Flag("--verbose"),
                }
            )
        )

class EesdrDeviceDescription(ConnectorDeviceDescription):
    def getName(self):
        return "Expert Electronics TCI Protocol Devices (SunSDR2)"

    def getInputs(self) -> List[Input]:
        return super().getInputs() + [
            TextInput(
                "device",
                "TCI server address in host:port or ip:port format"
            ),
            NumberInput(
                "receiver",
                "Receiver Number",
                "Receiver number to use as data source (0 or 1)",
                validator=RangeValidator(0, 1)
            ),
            CheckboxInput(
                "startstop",
                "Start/stop the entire radio device in addition to the IQ stream"
            ),
            CheckboxInput(
                "verbose",
                "Show additional details in the log"
            ),
        ]

    def supportsPpm(self):
        return False

    def getDeviceOptionalKeys(self):
        return list(filter(lambda x : x not in ["rtltcp_compat", "iqswap", "rf_gain"], super().getDeviceOptionalKeys())) + ["device", "receiver", "startstop", "verbose"]

    def getProfileOptionalKeys(self):
        return list(filter(lambda x : x not in ["iqswap", "rf_gain"], super().getProfileOptionalKeys()))

    def getSampleRateRanges(self) -> List[Range]:
        return [
            Range(48000),
            Range(96000),
            Range(192000),
            Range(384000),
        ]
