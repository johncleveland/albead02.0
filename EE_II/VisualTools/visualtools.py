
from ipywidgets import interact
import matplotlib.pyplot as plt


def show_plane(ax, plane, cmap="gray", title=None):
    ax.imshow(plane, cmap=cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    
    if title:
        ax.set_title(title)

def slice_in_3D(ax, i,data):
    # From:
    # https://stackoverflow.com/questions/44881885/python-draw-3d-cube

    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

    Z = np.array([[0, 0, 0],
                  [1, 0, 0],
                  [1, 1, 0],
                  [0, 1, 0],
                  [0, 0, 1],
                  [1, 0, 1],
                  [1, 1, 1],
                  [0, 1, 1]])

    Z = Z * data.shape

    r = [-1,1]

    X, Y = np.meshgrid(r, r)
    # plot vertices
    ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])

    # list of sides' polygons of figure
    verts = [[Z[0], Z[1], Z[2], Z[3]],
             [Z[4], Z[5], Z[6], Z[7]], 
             [Z[0], Z[1], Z[5], Z[4]], 
             [Z[2], Z[3], Z[7], Z[6]], 
             [Z[1], Z[2], Z[6], Z[5]],
             [Z[4], Z[7], Z[3], Z[0]], 
             [Z[2], Z[3], Z[7], Z[6]]]

    # plot sides
    ax.add_collection3d(
        Poly3DCollection(verts, facecolors=(0, 1, 1, 0.25), linewidths=1,
                         edgecolors='darkblue')
    )

    verts = np.array([[[0, 0, 0],
                       [0, 0, 1],
                       [0, 1, 1],
                       [0, 1, 0]]])
    #verts = verts * (60, 256, 256)
    verts=verts*data.shape
    verts += [i, 0, 0]

    ax.add_collection3d(Poly3DCollection(verts, 
     facecolors='magenta', linewidths=1, edgecolors='black'))

    ax.set_xlabel('plane')
    ax.set_ylabel('col')
    ax.set_zlabel('row')

    # Auto-scale plot axes
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]] * 3)

    #plt.show()



def slice_explorer(data, cmap='gray'):
    N = len(data)
        
    @interact(plane=(0, N - 1))
    def display_slice(plane=34):
        fig, ax = plt.subplots(figsize=(20, 5))
        
        ax_3D = fig.add_subplot(133, projection='3d')
        
        show_plane(ax, data[plane], title="Plane {}".format(plane), cmap=cmap)
        slice_in_3D(ax_3D, plane,data)
        
        plt.show()

    return display_slice

def display(im3d, cmap="gray", step=2):
    _, axes = plt.subplots(nrows=5, ncols=6, figsize=(16, 14))
    
    vmin = im3d.min()
    vmax = im3d.max()
    
    for ax, image in zip(axes.flatten(), im3d[::step]):
        ax.imshow(image, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_xticks([])
        ax.set_yticks([])
