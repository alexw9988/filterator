
from math import ceil
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s]: [filter_functions] %(message)s')

import numba as nb
import numpy as np
import scipy.ndimage as ndimage
import scipy.misc as misc 
import cv2 as cv2
import skimage.transform
from skimage.util import img_as_ubyte, img_as_bool, img_as_float64


def invert(img, params):
    if img.dtype == np.uint8:
        return np.subtract(255,img)
    elif img.dtype == np.float64:
        return np.subtract(1.0, img)
    elif img.dtype == np.bool:
        return np.subtract(1, img)
    else:
        raise ValueError("Can't invert input dtype")

def dummy(img, params):
    return img 

def grabCut(img, params):
    if img.ndim != 3 or img.dtype != np.uint8: 
        raise ValueError("Grabcut only applicable to RGB uint8 images!")
    
    roi_left = params['roi_left']
    roi_right = params['roi_right']
    roi_top = params['roi_top']
    roi_bottom = params['roi_bottom']

    if roi_right <= roi_left:
        raise ValueError("roi_right must be larger than roi_left")

    if roi_bottom <= roi_top:
        raise ValueError("roi_bottom must be larger than roi_top")

    iterations = params['iterations'] 
    return_type = params['return_type']

    mode = cv2.GC_INIT_WITH_RECT
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    rect = (roi_left, roi_top, roi_right-roi_left, roi_bottom-roi_top)

    bgd_model = np.zeros((1,65),np.float64)
    fgd_model = np.zeros((1,65),np.float64)
    
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, iterations, mode=mode)

    if return_type == 'fg':
        mask = np.where(mask == cv2.GC_FGD)
        return img*mask[:,:,np.newaxis]

    elif return_type == 'bg':
        mask = np.where(mask == cv2.GC_BGD)
        return img*mask[:,:,np.newaxis]

    elif return_type == 'binary_bg':
        mask = np.where(mask == cv2.GC_FGD)
        return mask

    elif return_type == 'binary_fg':
        mask = np.where(mask == cv2.GC_BGD)
        return mask 
        
    else:
        raise ValueError("Invalid return_type {}".format(return_type))

def adaptiveThreshold(img, params):
    if img.ndim > 2:
        raise ValueError("Threshold only applicable to grayscale images!")

    maxval = 1
    adaptive_method = params['adaptive_method']
    thresh_type = params['thresh_type']
    block_size = params['block_size']
    subtract_cval = params['subtract_cval']

    adaptive_method = eval('cv2.{}'.format(adaptive_method))
    thresh_type = eval('cv2.{}'.format(thresh_type))
    
    retval = cv2.adaptiveThreshold(img_as_ubyte(img), maxval, adaptive_method, thresh_type, block_size, subtract_cval)
    return img_as_bool(retval) 

def fixedThreshold(img, params):
    if img.ndim > 2:
        raise ValueError("Threshold only applicable to grayscale images!")

    thresh = params['thresh']
    maxval = 1
    thresh_type = params['thresh_type']
    thresh_algorithm = params['thresh_algorithm']

    thresh_type = eval('cv2.{}'.format(thresh_type))
    
    if thresh_algorithm == 'none':
        pass
    elif thresh_algorithm == 'otsu':
        thresh_type += cv2.THRESH_OTSU
    elif thresh_algorithm == 'triangle':
        thresh_type += cv2.THRESH_TRIANGLE

    _, retval = cv2.threshold(img, thresh, maxval, thresh_type)
    if thresh_type in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV]:
        return img_as_bool(retval)
    elif thresh_type in [cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]:
        return img_as_float64(retval)
    else: 
        return retval

def rescale(img, params):
    scale_x = params['scale_x']
    scale_y = params['scale_y']
    order = params['order']
    mode = params['mode']
    cval = params['cval']
    clip = params['clip']
    anti_aliasing = params['anti_aliasing']

    scale = (scale_x, scale_y)
    preserve_range = True
    if img.ndim == 2:
        multichannel = False
    else:
        multichannel = True
    
    retval = skimage.transform.rescale(img, scale, order=order, mode=mode, cval=cval,
                            clip=clip, preserve_range=preserve_range, multichannel=multichannel,
                            anti_aliasing=anti_aliasing)

    if img.dtype == np.uint8:
        return img_as_ubyte(retval)
    elif img.dtype == np.float64:
        return img_as_float64(retval)
    elif img.dtype == np.bool:
        return img_as_bool(retval)
    else:
        return retval

def gaussianBlur(img, params):
    sigma = params['sigma']
    order = params['order']
    mode = params['mode']
    cval = params['cval']
    truncate = params['truncate']

    return ndimage.gaussian_filter(img,sigma, order = order, mode = mode, cval = cval, truncate = truncate)

def rgb2gray(img, params):
    weight_r = params['red']
    weight_g = params['green']
    weight_b = params['blue'] 
    clip = params['clip']

    retval = _rgb2gray(img, weight_r, weight_g, weight_b)
    if clip:
        retval = np.clip(retval, 0.0, 1.0)
    else: 
        minimum = np.amin(retval)
        maximum = np.amax(retval)
        retval = np.subtract(retval, minimum)
        retval = np.multiply(retval, 1/maximum, dtype=np.float64)

    return retval

@nb.njit(parallel=True)
def _rgb2gray(img, weight_r, weight_g, weight_b):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    weight_r = np.float64(weight_r)
    weight_g = np.float64(weight_g)
    weight_b = np.float64(weight_b)
    fac = np.float64(1/255)

    img_out = np.empty(r.shape,dtype=np.float64)
    for i in nb.prange(img.shape[0]):
        for j in range(img.shape[1]):
            img_out[i,j] = fac*(r[i,j]*weight_r + g[i,j]*weight_g + b[i,j]*weight_b)

    return img_out

def tophat(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    if params['type'] == 'black':
        return ndimage.black_tophat(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)
    elif params['type'] == 'white':
        return ndimage.white_tophat(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)

def binary_closing(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1
    
    iterations = params['iterations']
    origin = (params['origin_x'], params['origin_y'])
    border_value = params['border_value']
    brute_force = params['brute_force']
    
    return ndimage.binary_closing(img, structure=structure, iterations=iterations, output=None, origin=origin, mask=None, border_value=border_value, brute_force=brute_force).astype(img.dtype)


def binary_dilation(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1
    
    iterations = params['iterations']
    origin = (params['origin_x'], params['origin_y'])
    border_value = params['border_value']
    brute_force = params['brute_force']
    
    return ndimage.binary_dilation(img, structure=structure, iterations=iterations, output=None, origin=origin, mask=None, border_value=border_value, brute_force=brute_force).astype(img.dtype)


def binary_erosion(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1
    
    iterations = params['iterations']
    origin = (params['origin_x'], params['origin_y'])
    border_value = params['border_value']
    brute_force = params['brute_force']
    
    return ndimage.binary_erosion(img, structure=structure, iterations=iterations, output=None, origin=origin, mask=None, border_value=border_value, brute_force=brute_force).astype(img.dtype)


def binary_fill_holes(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1

    origin = (params['origin_x'], params['origin_y'])
    
    return ndimage.binary_fill_holes(img, structure=structure, output=None, origin=origin).astype(img.dtype)


def binary_opening(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1
    
    iterations = params['iterations']
    origin = (params['origin_x'], params['origin_y'])
    border_value = params['border_value']
    brute_force = params['brute_force']
    
    return ndimage.binary_opening(img, structure=structure, iterations=iterations, output=None, origin=origin, mask=None, border_value=border_value, brute_force=brute_force).astype(img.dtype)


def binary_propagation(img, params):
    if params['structure_shape'] == 'rectangle':
        structure = np.ones((params['structure_size_y'], params['structure_size_x']), dtype=bool)
    elif params['structure_shape'] == 'ellipse':
        a = params['structure_size_x'] / 2
        b = params['structure_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        structure = (x/a)**2 + (y/b)**2 < 1
    
    origin = (params['origin_x'], params['origin_y'])
    border_value = params['border_value']
    
    return ndimage.binary_propagation(img, structure=structure, output=None, origin=origin, mask=None, border_value=border_value).astype(img.dtype)


def grey_closing(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.grey_closing(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def grey_dilation(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.grey_dilation(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def grey_erosion(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.grey_erosion(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def grey_opening(img, params):  
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.grey_opening(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def morphological_gradient(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.morphological_gradient(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def morphological_laplace(img, params):
    if params['footprint_shape'] == 'rectangle':
        footprint = np.ones((params['footprint_size_y'], params['footprint_size_x']), dtype=int)
    elif params['footprint_shape'] == 'ellipse':
        a = params['footprint_size_x'] / 2
        b = params['footprint_size_y'] / 2
        x,y = np.mgrid[-ceil(a):ceil(a)+1, -ceil(b):ceil(b)+1]
        footprint = ((x/a)**2 + (y/b)**2 < 1)*1
   
    mode = params['mode']
    cval = params['cval']
    origin = params['origin']

    return ndimage.morphological_laplace(img, size=None, footprint=footprint, structure=None, mode=mode, cval=cval, origin=origin)


def sobel_edge(img, params):

    dx = params['dx']
    dy = params['dy']
    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']
    border_type = params['border_type']
    stretch_range = params['stretch_range']

    ddepth = -1 #cv2.CV_64F
    border_type = eval('cv2.{}'.format(border_type))

    retval = cv2.Sobel(img, ddepth, dx, dy, ksize=ksize, scale=scale, delta=delta, borderType=border_type)
    if stretch_range:
        minimum = np.amin(retval)
        maximum = np.amax(retval)
        interval = maximum-minimum

        retval = np.add(retval, -minimum)
        retval = np.multiply(retval, 1/interval)
    else:
        retval = np.add(retval, 127.0)
        retval = np.multiply(retval, 1/255.0)
    
    return retval 

def laplacian_edge(img, params):

    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']
    border_type = params['border_type']
    stretch_range = params['stretch_range']

    ddepth = cv2.CV_64F
    border_type = eval('cv2.{}'.format(border_type))

    retval = cv2.Laplacian(img,ddepth, ksize=ksize, scale=scale, delta=delta, borderType=border_type)
    if stretch_range:
        minimum = np.amin(retval)
        maximum = np.amax(retval)
        interval = maximum-minimum

        retval = np.add(retval, -minimum)
        retval = np.multiply(retval, 1/interval)
    else:
        retval = np.add(retval, 127.0)
        retval = np.multiply(retval, 1/255.0)
    
    return retval 


