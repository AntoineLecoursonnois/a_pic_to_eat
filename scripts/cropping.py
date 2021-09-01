from patchify import patchify


def cropping_image(image, slice_dim=(256, 256, 3), step=256):
    '''
    Crope an image into smaller patches
    Params :
        image = the image you want to crope
        slice_dimension = Tuple of the dim you want (width, heigh, dim)
        step = The step of the cut (int)
    return :  List of array of the patches created
    '''
    # Generate the patches
    patch_images = patchify(image, slice_dim, step=step)

    # Instance the list of patches
    patch_list = []

    # Append them into the list
    for i in range(patch_images.shape[0]):
        for j in range(patch_images.shape[1]):
            for k in range(patch_images.shape[2]):
                single_patch = patch_images[i, j, k, :, :, :]
                patch_list.append(single_patch)

    # Return the list of patches
    return patch_list
