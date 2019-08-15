#!/usr/bin/python3

pids = {
    'SPEED': {'title': 'speed', 'min': 0, 'max': 200, 'warn': 135, 'alt_u': 'mph', 'titleunits': True},
    'RPM': {'title': 'rpm', 'min': 0, 'max': 6500, 'warn': 5900, 'alt_u': None, 'titleunits': False},
    'ENGINE_LOAD': {'title': 'load %', 'min': 0, 'max': 100, 'warn': 90, 'titleunits': False},
    'THROTTLE_POS': {'title': 'throttle %', 'min': 0, 'max': 100, 'warn': 90, 'titleunits': False},
    'COOLANT_TEMP': {'title': 'coolant temp', 'min': -40, 'max': 215, 'warn': 100, 'alt_u': 'degF', 'titleunits': True},
    'INTAKE_TEMP': {'title': 'intake temp', 'min': -40, 'max': 215, 'warn': 50, 'alt_u': 'degF', 'titleunits': True},
    'TIMING_ADVANCE': {'title': 'timing adv deg', 'min': -64, 'max': 64, 'titleunits': False},
    'INTAKE_PRESSURE': { 'title': 'map', 'min': 0, 'max': 765, 'titleunits': True},
    'MAF':  { 'title': 'maf', 'min': 0, 'max': 655, 'titleunits': True},
    'SHORT_FUEL_TRIM_1':  { 'title': 'stft1', 'min': -100, 'max': 99, 'titleunits': True},
    'LONG_FUEL_TRIM_1':  { 'title': 'ltft1', 'min': -100, 'max': 99, 'titleunits': True},
    'SHORT_FUEL_TRIM_2':  { 'title': 'stft2', 'min': -100, 'max': 99, 'titleunits': True},
    'LONG_FUEL_TRIM_2':  { 'title': 'ltft2', 'min': -100, 'max': 99, 'titleunits': True},
    }
