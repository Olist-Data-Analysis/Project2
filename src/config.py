from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / 'data'
MODEL_DIR = PROJECT_DIR / 'models'
SRC_DIR = PROJECT_DIR / 'src'
FONT_DIR = PROJECT_DIR / 'font'
RESULT_DIR = PROJECT_DIR / 'results'

state_neighbors = {
    "AC": ["AM", "RO"],
    "AL": ["PE", "SE", "BA"],
    "AP": ["PA"],
    "AM": ["AC", "RR", "PA", "RO", "MT"],
    "BA": ["MG", "ES", "GO", "TO", "PI", "PE", "AL", "SE"],
    "CE": ["PI", "PE", "PB", "RN"],
    "DF": ["GO", "MG"],
    "ES": ["BA", "MG", "RJ"],
    "GO": ["TO", "BA", "MG", "MT", "MS", "DF"],
    "MA": ["PA", "TO", "PI"],
    "MT": ["PA", "AM", "RO", "GO", "MS"],
    "MS": ["GO", "MT", "MG", "SP", "PR"],
    "MG": ["BA", "ES", "RJ", "SP", "GO", "DF", "MS"],
    "PA": ["AP", "MA", "TO", "MT", "AM", "RR"],
    "PB": ["CE", "PE", "RN"],
    "PR": ["SP", "MS", "SC"],
    "PE": ["CE", "PI", "BA", "AL", "PB"],
    "PI": ["MA", "TO", "BA", "PE", "CE"],
    "RJ": ["ES", "MG", "SP"],
    "RN": ["CE", "PB"],
    "RS": ["SC"],
    "RO": ["AC", "AM", "MT"],
    "RR": ["AM", "PA"],
    "SC": ["PR", "RS"],
    "SP": ["MG", "RJ", "PR", "MS"],
    "SE": ["BA", "AL"],
    "TO": ["MA", "PI", "BA", "GO", "PA", "MT"],
}

state_region_map = {
    # North Region
    "AC": "North",
    "AP": "North",
    "AM": "North",
    "PA": "North",
    "RO": "North",
    "RR": "North",
    "TO": "North",

    # Northeast Region
    "AL": "Northeast",
    "BA": "Northeast",
    "CE": "Northeast",
    "MA": "Northeast",
    "PB": "Northeast",
    "PE": "Northeast",
    "PI": "Northeast",
    "RN": "Northeast",
    "SE": "Northeast",

    # Central-West Region
    "DF": "Central-West",
    "GO": "Central-West",
    "MT": "Central-West",
    "MS": "Central-West",

    # Southeast Region
    "ES": "Southeast",
    "MG": "Southeast",
    "RJ": "Southeast",
    "SP": "Southeast",

    # South Region
    "PR": "South",
    "RS": "South",
    "SC": "South",
}