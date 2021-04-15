import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


__all__ = ['display_array3D', 'display_array2D']


def display_array3D(voxel_bools, voxel_colors='w', edge_color='k', width=6, height=6, nX=16, nY=16, nZ=16, show_axis=False):
    fig = plt.figure(figsize=(width,height)) # initialize figure dimensions
    ax = Axes3D(fig)
    nMax = max([nX,nY,nZ]) # get max dimension of the three
    ax.cla() # clear axes
    ax.voxels(voxel_bools, facecolors=voxel_colors, edgecolor=edge_color) # draw voxels with defined faces and edges colors
    if not show_axis:
        ax.set_axis_off() # turn off axis
    ax.auto_scale_xyz([0, nMax], [0, nMax], [0, nMax]) # scale based on max dimension
    plt.show()


def display_array2D(data, height, col='binary', edgecol='w'):
    """
    Display a 2D numpy array using matplotlib
    
    Parameters
    ----------
    data : 2D numpy array
    height : Height of the plot - Proportional length 
    col : Matplotlib color map for voxels - https://matplotlib.org/stable/gallery/color/colormap_reference.html
    edgecol : Matplotlib color palette for edges - https://matplotlib.org/stable/gallery/color/named_colors.html
    
    Returns
    -------
    Plot a 2D numpy array using matplotlib
    """
    plt.figure(figsize=(height * (data.shape[1] / data.shape[0]), height))
    plt.pcolor(data,cmap=col,edgecolors=edgecol, linewidths=height * 0.08)
    plt.tight_layout()
    plt.axis('off')
    plt.show()