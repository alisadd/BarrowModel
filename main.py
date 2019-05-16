import Agents
from Model import Model
import matplotlib.pyplot as plt
import pandas

def main():
    """
    Run model and make plot.
    """
    test = Model(200, 0, 100)
    test.setup()
    test.iter_step(1)
    means = test.get_data()
    means.plot()
    plt.show()



if __name__ == "__main__":
    main()
