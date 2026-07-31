import matplotlib.pyplot as plt
from pathlib import Path


def main():
    # 出力画像パスは好きにしてください
    out = Path(__file__).resolve().with_suffix('.png')

    # ダミーデータ
    data = [
        [7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.0, 12.0, 13.0],
        [9.0, 10.5, 12.0, 13.0, 14.0, 15.0, 16.0, 17.5, 19.0],
        [8.0, 10.0, 11.5, 12.0, 13.0, 14.0, 15.0, 16.5, 18.0],
        [12.0, 14.0, 15.5, 17.0, 18.0, 19.5, 21.5, 23.0, 25.0],
    ]

    context = {}
    context['font.family'] = 'Roboto'
    for key in ['font.weight', 'axes.labelweight']:
        context[key] = 'medium'
    context['font.size'] = 13

    line_style = {
        'color': 'black',
        'linewidth': 1.5,
    }

    with plt.rc_context(context):
        fig, ax = plt.subplots(figsize=(3, 2))

        boxes = ax.boxplot(
            data,
            tick_labels=['1', '2', '3', '4'],
            widths=0.5,
            patch_artist=True,
            boxprops={'facecolor': 'white', **line_style},
            medianprops={'color': 'black', 'linewidth': 2.5},
            whiskerprops=line_style,
            capprops=line_style,
            flierprops={
                'marker': 'o',
                'markerfacecolor': 'white',
                'markeredgecolor': 'black',
                'markersize': 4,
            },
        )

        ax.set_xlabel('AAA')
        ax.set_ylabel('BBB')
        ax.set_ylim((5, 27))
        ax.grid(axis='y', linestyle='dotted')

        # desc = {}
        # desc['Median'] = boxes['medians'][0]
        # desc['25–75% interval'] = boxes['boxes'][0]
        # desc['Whisker'] = boxes['whiskers'][0]
        # ax.legend(
        #     desc.values(),
        #     desc.keys(),
        #     loc='upper left',
        #     bbox_to_anchor=(1.05, 1),
        # )

        fig.savefig(out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
