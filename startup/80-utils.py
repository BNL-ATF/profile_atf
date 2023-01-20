import matplotlib.pyplot as plt


def plot_images(data, nrows=2, ncols=4):
    """
    Usage
    -----

        nrows, ncols = 2, 4
        uid, = RE(bp.scan([<detector>], <motor>, <start>, <stop>, nrows * ncols))
        hdr = db[uid]
        data = np.array(list(hdr.data("<field_name>")))
        plot_images(data, nrows=nrows, ncols=ncols)

    """
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols)

    for row in range(nrows):
        print(f"{row = }")
        for col in range(ncols):
            print(f"  {col = } --> {ax[row][col]}")
            ax[row][col].imshow(
                data[row * ncols + col], vmin=data.min(), vmax=data.max()
            )
