import Agents
from Model import Model
import matplotlib.pyplot as plt

def main():
    """initialise and run model"""
    test = Model(200, 0, 100)
    test.setup()
    test.iter_step(1)


if __name__ == "__main__":
    main()
