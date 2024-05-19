import matplotlib.pyplot as plt
from PIL import Image
import sorting


def create_plot_and_save(filepath):
    positions = [0.25, 1.5, 2.5, 3.75, 5, 6, 7, 7.75]
    Names = ['Platform', "Edition", "Region", "Activation type", "Price", "Seller", "Rating", "Stars"]

    # Assuming analyze_certain_amount_of_games returns a DataFrame
    Rows = sorting.analyze_certain_amount_of_games(8)

    nrows = len(Rows)
    ncols = len(Names)
    fontsz = 14

    fig = plt.figure(figsize=(18, 1.25 * nrows), dpi=300)
    ax = plt.subplot()

    ax.set_xlim(0, ncols + 1)
    ax.set_ylim(0, nrows)

    # Getting logos
    ps = Image.open('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\ps.png')
    pc = Image.open('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\pc.png')
    xbox = Image.open('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\xbox.png')

    # Resizing
    base_width = 200
    wpercent = (base_width / float(ps.size[0]))
    hsize = int((float(ps.size[1]) * float(wpercent)))

    ps = ps.resize((base_width, hsize), Image.LANCZOS)
    xbox = xbox.resize((base_width, hsize), Image.LANCZOS)
    pc = pc.resize((125, hsize), Image.LANCZOS)

    def show_logo(platform, i):
        start = 375
        i = i + 0.25
        if platform == 'ps':
            ax.figure.figimage(ps, 2.65 * 300, 290 * i + 37 * nrows)
        if platform == 'pc':
            ax.figure.figimage(pc, 2.75 * 300, 290 * i + 37 * nrows)
        if platform == 'xbox':
            ax.figure.figimage(xbox, 2.65 * 300, 290 * i + 37 * nrows)

    # Rows
    for i in range(nrows):
        for j, column in enumerate(Names):
            if j == 0:
                show_logo(Rows.iloc[i]["Platform"], i)  # Using iloc to access DataFrame by integer position
                continue

            ha = 'left' if j == 0 else "center"

            text_ = str(Rows.iloc[i][Names[j]]) + "€" if j == 4 else Rows.iloc[i][Names[j]]

            ax.annotate(
                xy=(positions[j], i + 0.5),
                text=text_,  # Using iloc to access DataFrame by integer position
                ha=ha,
                va='center',
                fontsize=fontsz
            )

    # Names
    for index, c in enumerate(Names):
        ha = "left" if index == 0 else "center"
        ax.annotate(
            xy=(positions[index], nrows),
            text=Names[index],
            ha=ha,
            va='bottom',
            weight='bold',
            fontsize=fontsz + 2
        )

    # Add dividing lines
    ax.plot([ax.get_xlim()[0] - 1, ax.get_xlim()[1] - 1], [nrows, nrows], lw=3, color='black', marker='', zorder=4)
    ax.plot([ax.get_xlim()[0] - 1, ax.get_xlim()[1] - 1], [0, 0], lw=3, color='black', marker='', zorder=4)
    ax.plot([0, 0], [ax.get_ylim()[0] - 1, ax.get_ylim()[1]], lw=3, color='black', marker='', zorder=4)
    ax.plot([ax.get_xlim()[1] - 1, ax.get_xlim()[1] - 1], [ax.get_ylim()[0], ax.get_ylim()[1]], lw=3, color='black',
            marker='', zorder=4)
    for x in range(1, nrows):
        ax.plot([ax.get_xlim()[0] - 1, ax.get_xlim()[1] - 1], [x, x], lw=1.15, color='gray', ls=':', zorder=3,
                marker='')

    # Highlight columns
    ax.fill_between(x=[4.75, 5.25], y1=ax.get_ylim()[0], y2=nrows, color='lightgreen', alpha=1)
    ax.fill_between(x=[7.5, ax.get_xlim()[1] - 1], y1=ax.get_ylim()[0], y2=nrows, color='Yellow', alpha=0.5)
    ax.fill_between(x=[0, 0.85], y1=ax.get_ylim()[0], y2=nrows, color='lightblue', alpha=1)

    ax.set_axis_off()
    fig.savefig(filepath)
    #plt.close(fig)


# Call the function to create the plot and save it
#create_plot_and_save('Table1.png')
