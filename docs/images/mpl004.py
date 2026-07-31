import matplotlib.pyplot as plt
from pathlib import Path


def main():
    # 出力画像パスは好きにしてください
    out = Path(__file__).resolve().with_suffix('.png')

    # ダミーデータ
    x1 = [1.0, 1.5, 2.0, 2.5]
    y1 = [3.0, 4.5, 4.0, 5.5]

    x2 = [2.0, 2.5, 3.0, 3.5]
    y2 = [7.0, 6.5, 8.0, 7.5]

    x3 = [3.0, 3.5, 4.0, 4.5]
    y3 = [2.5, 3.5, 3.0, 4.0]

    context = {}
    context['font.family'] = 'Roboto'
    for key in ['font.weight', 'axes.labelweight']:
        context[key] = 'medium'
    context['font.size'] = 13

    with plt.rc_context(context):
        fig, ax = plt.subplots(figsize=(2.5, 2.5))

        points1 = ax.scatter(x1, y1, marker='o', s=40, color='tab:blue', zorder=3)
        points2 = ax.scatter(x2, y2, marker='s', s=40, color='tab:orange', zorder=3)
        points3 = ax.scatter(x3, y3, marker='^', s=50, color='tab:green', zorder=3)

        ax.set_xlabel('AAA')
        ax.set_ylabel('BBB')
        ax.set_xlim((0.5, 5.0))
        ax.set_ylim((1.5, 9.0))
        ax.set_axisbelow(True)
        ax.grid(axis='both', linestyle='dotted')

        desc = {}
        desc['Type A'] = points1
        desc['Type B'] = points2
        desc['Type C'] = points3
        ax.legend(
            desc.values(), desc.keys(), ncols=1,
            loc='upper center', bbox_to_anchor=(0.5, -0.25),
        )

        fig.savefig(out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
