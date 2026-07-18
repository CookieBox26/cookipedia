import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path


def main():
    out = Path(__file__).stem + '.png'

    x = [0, 1, 2, 3, 4]
    y = [3.5, 2.6, 1.8, 1.5, 1.4]

    with plt.rc_context({
        'figure.figsize': (4, 3),
        'font.family': 'Yu Gothic UI',
        'font.size': 13,
    }):
        desc = {}
        fig, ax = plt.subplots()

        desc['Training loss'] = ax.plot(x, y)[0]

        ax.set_xlabel('Epoch')
        ax.set_ylabel('Training loss')
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(0.25))
        plt.grid(axis='both', linestyle='dotted')
        plt.legend(
            desc.values(), desc.keys(),
            loc='upper left', bbox_to_anchor=(1.05, 1),
        )
        fig.savefig(out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
