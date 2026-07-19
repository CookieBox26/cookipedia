import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path


def main():
    out = Path(__file__).resolve().with_suffix('.png')

    x = [0, 1, 2, 3, 4]
    y = [3.5, 2.6, 1.8, 1.5, 1.4]

    context = {}
    context['font.family'] = 'Segoe UI'
    # for key in ['font.weight', 'axes.labelweight']:
    #     context[key] = 'semibold'
    context['font.size'] = 13
    with plt.rc_context(context):
        desc = {}
        fig, ax = plt.subplots(figsize=(3.5, 2))

        desc['Training loss'] = ax.plot(x, y)[0]

        ax.set_xlabel('Epoch')
        ax.set_ylabel('Training loss')
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(0.5))
        plt.grid(axis='both', linestyle='dotted')
        plt.legend(
            desc.values(), desc.keys(),
            loc='upper left', bbox_to_anchor=(1.05, 1),
        )
        fig.savefig(out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
