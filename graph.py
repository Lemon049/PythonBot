import pandas as pd
import matplotlib.pyplot as plt


from PIL import Image





positions = [0.5, 3, 4, 5, 6, 7, 7.75, 8.75, 9.5]
Names = ['Link', 'Platform', "Edition", "Region", "Activation type", "Price", "Seller", "Rating", "Stars"]
Rows =

#filling array with needed columns(test if it work)
# !!!!!Разкоменьть если хочешь проерить как работает!!!!!!
# (Можешь поудалять append что бы посмотреть как он меняется от количества рядов)

# Rows.append(data.max_price_row)
# Rows.append(data.min_price_row)
# Rows.append(data.max_rating_row)
# Rows.append(data.max_stars_row)
# Rows.append(data.min_key_row)
# Rows.append(data.min_present_row)
# Rows.append(data.min_account_row)
# Rows.append(data.min_pc_row)
# Rows.append(data.min_xbox_row)

nrows = len(Rows)
ncols = len(Names)
fontsz = 8

fig = plt.figure(figsize=(19, 1.25*nrows), dpi=300)
ax = plt.subplot()

ax.set_xlim(0, ncols + 1)
ax.set_ylim(0, nrows)



#getting logos
ps = Image.open('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\ps.jpg')
pc = Image.open('C:\\Users\Yehor\\Documents\\GitHub\\PythonBot\\pc.jpg')
xbox = Image.open('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\xbox.jpg')
#resizing
base_width = 200
wpercent = (base_width / float(ps.size[0]))
hsize = int((float(ps.size[1]) * float(wpercent)))

ps = ps.resize((base_width, hsize), Image.Resampling.LANCZOS)
xbox = xbox.resize((base_width, hsize), Image.Resampling.LANCZOS)
pc = pc.resize((125, hsize), Image.Resampling.LANCZOS)

def show_logo(platform, i):
    start = 375
    i = i+0.25
    if platform == 'ps':
        ax.figure.figimage(ps, 6.65*300, 290*i+37*nrows)
    if platform == 'pc':
        ax.figure.figimage(pc, 6.75*300, 290*i+37*nrows)
    if platform == 'xbox':
        ax.figure.figimage(xbox, 6.65*300, 290*i+37*nrows)


#rows
for i in range(nrows):
    for j, column in enumerate(Names):
        if j == 1:
            show_logo(Rows[i]["Platform"], i)
            continue

        if j == 0:
            ha = 'left'
        else:
            ha = "center"

        ax.annotate(
            xy=(positions[j], i+0.5),
            text = Rows[i][Names[j]],
            ha=ha,
            va='center',
        )
#names
for index, c in enumerate(Names):
    if index == 0:
        ha="left"
    else:
        ha="center"
    ax.annotate(
        xy=(positions[index],nrows),
        text=Names[index],
        ha=ha,
        va='bottom',
        weight='bold',
        fontsize=14
    )

# Add dividing lines
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=3, color='black', marker='', zorder=4)
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=3, color='black', marker='', zorder=4)
ax.plot([0, 0], [ax.get_ylim()[0], ax.get_ylim()[1]], lw=3, color='black', marker='', zorder=4)
for x in range(1, nrows):
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='gray', ls=':', zorder=3 , marker='')


ax.fill_between(
    x=[0, 2.75],
    y1=ax.get_ylim()[0],
    y2=nrows,
    color='lightblue',
    alpha=1
)

ax.set_axis_off()
plt.show()

fig.savefig('Table.png')




