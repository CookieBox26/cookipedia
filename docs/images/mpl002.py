import matplotlib.pyplot as plt
from pathlib import Path


def main():
    out = Path(__file__).resolve().with_suffix('.png')

    x = [1, 2, 3, 4]
    y05 = [ 7.5, 10.5,  8.5, 13.5]  # 05 パーセンタイル
    y25 = [ 8.5, 12.0, 11.5, 15.5]  # 25 パーセンタイル
    y50 = [10.0, 14.0, 13.0, 18.0]  # 中央値
    y75 = [11.0, 16.5, 15.0, 21.5]  # 75 パーセンタイル
    y95 = [12.5, 18.5, 17.5, 23.0]  # 95 パーセンタイル

    yerr50 = [  # 50 パーセント区間の幅
        [y0 - y1 for y0, y1 in zip(y50, y25)],
        [y1 - y0 for y0, y1 in zip(y50, y75)],
    ]
    yerr90 = [  # 90 パーセント区間の幅
        [y0 - y1 for y0, y1 in zip(y50, y05)],
        [y1 - y0 for y0, y1 in zip(y50, y95)],
    ]

    context = {}
    context['font.family'] = 'Roboto'
    for key in ['font.weight', 'axes.labelweight']:
        context[key] = 'medium'
    context['font.size'] = 13
    colors = {'color': 'black', 'ecolor': 'black'}

    with plt.rc_context(context):
        fig, ax = plt.subplots(figsize=(3, 2))

        ebars90 = ax.errorbar(
            x, y50, yerr=yerr90, fmt='none',
            capsize=5, capthick=2, elinewidth=1.5, **colors,
        )
        for ebar in ebars90[2]:
            ebar.set_linestyle(':')  # 90 パーセント区間のエラーバーは点線にする
        ebars50 = ax.errorbar(
            x, y50, yerr=yerr50, fmt='o',
            capsize=4, capthick=2, elinewidth=2, **colors,
        )

        ax.set_xlabel('AAA')
        ax.set_ylabel('BBB')
        ax.set_xlim((0.5, 4.5))
        plt.grid(axis='both', linestyle='dotted')

        desc = {}
        desc['Median'] = ebars50[0]
        desc['50% interval'] = ebars50[2][0]
        desc['90% interval'] = ebars90[2][0]
        plt.legend(
            desc.values(), desc.keys(),
            loc='upper left', bbox_to_anchor=(1.05, 1),
        )

        fig.savefig(out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
