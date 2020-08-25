
import filters.functions as ff


DEFAULTS = {
    'rgb2gray': {
        'full_name': 'Grayscale',
        'fn': ff.rgb2gray,
        'description': 'transform colour-image to gray-image',
        'default_params': {
            'red':{
                'optional': False,
                'label': "Red",
                'description': "",
                'dtype': float,
                'default': 0.2989,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 1.0,
                'single_step': 0.05,
                'decimals': 4
            },
            'green':{
                'optional': False,
                'label': "Green",
                'description': "",
                'dtype': float,
                'default': 0.5870,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 1.0,
                'single_step': 0.05,
                'decimals': 4
            },
            'blue':{
                'optional': False,
                'label': "Blue",
                'description': "",
                'dtype': float,
                'default': 0.1140,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 1.0,
                'single_step': 0.05,
                'decimals': 4
            },
            'clip': {
                'full_name': 'clip',
                'wtype': 'checkbox',
                'dtype': bool, 
                'description': "Clip result to maximum for given dtype, else range will be stretched to dtype range", 
                'optional': False,
                'default': True,
                'value': True
            }
        }
    },
    'rescale': {
        'full_name': 'Rescale',
        'fn': ff.rescale,
        'description': 'Rescale (up/down) the image',
        'default_params': {
            'scale_x':{
                'optional': False,
                'label': 'scale_x',
                'description': "Scale factor for x-dimension",
                'dtype': float, 
                'wtype': 'double_spinbox',
                'default': 1.0,
                'minimum': 0.05,
                'maximum': 10.0,
                'single_step': 0.05
            },
            'scale_y':{
                'optional': False,
                'label': 'scale_y',
                'description': "Scale factor for y-dimension",
                'dtype': float, 
                'wtype': 'double_spinbox',
                'default': 1.0,
                'minimum': 0.05,
                'maximum': 10.0,
                'single_step': 0.05
            },
            'order':{
                'optional': True,
                'label': 'order',
                'description': "The order of the spline interpolation, default is 0 if image.dtype is bool and 1 otherwise. The order has to be in the range 0-5.",
                'dtype': int, 
                'wtype': 'spinbox',
                'default': 1,
                'minimum': 0,
                'maximum': 5,
                'single_step': 1
            },
            'mode':{
                'optional': True,
                'label': "Mode",
                'description': "Points outside the boundaries of the input are filled according to the given mode.",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'constant',
                'options': ['constant', 'edge', 'symmetric', 'reflect','wrap'],
                'options_description': [
                    "Pads with a constant value.",
                    "Pads with the edge values of array.",
                    "Pads with the reflection of the vector mirrored along the edge of the array.",
                    "Pads with the reflection of the vector mirrored on the first and last values of the vector along each axis.",
                    "Pads with the wrap of the vector along the axis. The first values are used to pad the end and the end values are used to pad the beginning."
                ]
            },
            'cval': {
                'optional': True,
                'label': "cval",
                'description': "Used in conjunction with mode ‘constant’, the value outside the image boundaries.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            'clip': {
                'optional': True,
                'label': 'clip',
                'description': "Whether to clip the output to the range of values of the input image. This is enabled by default, since higher order interpolation may produce values outside the given input range.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': True
            },
            'anti_aliasing': {
                'optional': True,
                'label': 'anti_aliasing',
                'description': "Whether to apply a Gaussian filter to smooth the image prior to down-scaling. It is crucial to filter when down-sampling the image to avoid aliasing artifacts. If input image data type is bool, no anti-aliasing is applied.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': False
            }
        }
    },
    'gaussianBlur': {
        'full_name': 'Gaussian Blur',
        'fn': ff.gaussianBlur,
        'description':  'filter whose impulse response is a Gaussian function',
        'default_params': {
            'sigma':{
                'optional': False,
                'label': "Sigma",
                'description': "Standard deviation for Gaussian kernel. The standard deviations of the Gaussian filter are given for each axis as a sequence, or as a single number, in which case it is equal for all axes.",
                'dtype': float,
                'default': 2.0,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 1000.0,
                'single_step': 0.5
            },
            'order':{
                'optional': True,
                'label': "Order",
                'description': "The order of the filter along each axis is given as a sequence of integers, or as a single number. An order of 0 corresponds to convolution with a Gaussian kernel. A positive order corresponds to convolution with that derivative of a Gaussian.",
                'dtype': int,
                'default': 0,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 5,
                'single_step': 1
            },
            'mode':{
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "truncate": {
                'optional': True,
                'label': "Truncate",
                'description': "Truncate the filter at this many standard deviations. Default is 4.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 4.0,
                'minimum': 0.5,
                'maximum': 10.0,
                'single_step': 0.5
            }
        }
    },
    'grey_dilation': {
        'full_name': 'Grey dilation',
        'fn': ff.grey_dilation,
        'description': "uses a structuring element for probing and expanding the shapes contained in the greyscale-image",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'default': 0.0,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 255.5,
                'single_step': 0.5
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'default': 0,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'grey_erosion': {
        'full_name': 'Grey erosion',
        'fn': ff.grey_erosion,
        'description': "uses a structuring element for probing and reducing the shapes contained in the greyscale-image",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'grey_opening': {
        'full_name': 'Grey opening',
        'fn': ff.grey_opening,
        'description': "succession of a greyscale erosion, and a greyscale dilation",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'grey_closing': {
        'full_name': 'Grey closing',
        'fn': ff.grey_closing,
        'description': "succession of a greyscale dilation and a greyscale erosion of a greyscale-image",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'default': 1,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'fixedThreshold': {
        'full_name': 'Fixed Threshold',
        'fn': ff.fixedThreshold,
        'description':  'Applies a fixed-level threshold to each pixel.',
        'default_params': {
            'thresh':{
                'optional': False,
                'label': 'thresh',
                'description': "Threshold value between 0-1",
                'dtype': float, 
                'wtype': 'double_spinbox',
                'default': 0.7,
                'minimum': 0.0,
                'maximum': 1.0,
                'single_step': 0.05
            },
            # 'maxval':{
            #     'optional': False,
            #     'label': 'maxval',
            #     'description': "Maximum value to use with THRESH_BINARAY(_INV), between 0-1",
            #     'dtype': float, 
            #     'wtype': 'double_spinbox',
            #     'default': 1.0  ,
            #     'minimum': 0.0,
            #     'maximum': 1.0,
            #     'single_step': 0.05
            # },
            'thresh_type':{
                'optional': False,
                'label': 'Thresholding type',
                'description': "",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'THRESH_BINARY',
                'options': ['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO', 'THRESH_TOZERO_INV'],
                'options_description': [
                    "Set each pixel above threshold to 1, 0 otherwise",
                    "Set each pixel below threshold to 1, 0 otherwise",
                    "Set each pixel above threshold to threshold.",
                    "Set each pixel below threshold to 0",
                    "Set each pixel above threshold to 0",
                ]
            },
            'thresh_algorithm':{
                'optional': True,
                'label': "Threshold algorithm",
                'description': "Use algorithm to find optimal threshold value",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'none',
                'options': ['none', 'otsu', 'triangle'],
                'options_description': [
                    "Manually choose value",
                    "Use Otsu algorithm to choose optimal threshold value",
                    "Use Triangle algorithm to choose optimal threshold value"
                ]
            }
        }
    },
    'adaptiveThreshold': {
        'full_name': 'Adaptive Threshold',
        'fn': ff.adaptiveThreshold,
        'description':  'Applies an adaptive threshold to each pixel.',
        'default_params': {
            # 'maxval':{
            #     'optional': False,
            #     'label': 'maxval',
            #     'description': "Maximum value to use with THRESH_BINARAY(_INV), between 0-1",
            #     'dtype': float, 
            #     'wtype': 'double_spinbox',
            #     'default': 1.0  ,
            #     'minimum': 0.0,
            #     'maximum': 1.0,
            #     'single_step': 0.05
            # },
            'adaptive_method':{
                'optional': False,
                'label': 'Adaptive method',
                'description': "Adaptive thresholding type to use",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'ADAPTIVE_THRESH_MEAN_C',
                'options': ['ADAPTIVE_THRESH_MEAN_C', 'ADAPTIVE_THRESH_GAUSSIAN_C'],
                'options_description': [
                    "The threshold value T(x,y) is a mean of the blocksize*blocksize neighborhood of (x,y) minus C",
                    "The threshold value T(x,y) is a weighted sum (cross-correlation with a Gaussian window) of the blocksize*blocksize neighborhood of (x,y) minus C . The default sigma (standard deviation) is used for the specified blocksize .",
                ]
            },
            'thresh_type':{
                'optional': False,
                'label': 'Thresholding type',
                'description': "",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'THRESH_BINARY',
                'options': ['THRESH_BINARY', 'THRESH_BINARY_INV'],
                'options_description': [
                    "Set each pixel above threshold to 1, 0 otherwise",
                    "Set each pixel below threshold to 1, 0 otherwise",
                ]
            },
            'block_size':{
                'optional': False,
                'label': 'block_size',
                'description': "Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.",
                'dtype': int, 
                'wtype': 'spinbox',
                'default': 5,
                'minimum': 3,
                'maximum': 2000,
                'single_step': 2
            },
            'subtract_cval':{
                'optional': False,
                'label': 'C',
                'description': "Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well.",
                'dtype': float, 
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 1.0,
                'single_step': 0.05
            },
        }
    },
    'binary_dilation': {
        'full_name': 'Binary dilation',
        'fn': ff.binary_dilation,
        'description': "uses a structuring element for probing and expanding the shapes contained in the binary-image",
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "iterations": {
                'optional': True,
                'label': "Iterations",
                'description': "The dilation is repeated iterations times (one, by default). If iterations is less than 1, the dilation is repeated until the result does not change anymore. Only an integer of iterations is accepted.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 20,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "border_value": {
                'optional': True,
                'label': "Border value",
                'description': "Value at the border in the output array.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1,
                'single_step': 1,
                'default': 0
            },
            "brute_force": {
                'optional': True,
                'label': "Brute force",
                'description': "Memory condition: if False, only the pixels whose value was changed in the last iteration are tracked as candidates to be updated (dilated) in the current iteration; if True all pixels are considered as candidates for dilation, regardless of what happened in the previous iteration.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': False
            },
        }
    },
    'binary_erosion': {
        'full_name': 'Binary erosion',
        'fn': ff.binary_erosion,
        'description': "uses a structuring element for probing and reducing the shapes contained in the binary-image",
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "iterations": {
                'optional': True,
                'label': "Iterations",
                'description': "The erosion is repeated iterations times (one, by default). If iterations is less than 1, the erosion is repeated until the result does not change anymore.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 20,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "border_value": {
                'optional': True,
                'label': "Border value",
                'description': "Value at the border in the output array.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1,
                'single_step': 1,
                'default': 0
            },
            "brute_force": {
                'optional': True,
                'label': "Brute force",
                'description': "Memory condition: if False, only the pixels whose value was changed in the last iteration are tracked as candidates to be updated (eroded) in the current iteration; if True all pixels are considered as candidates for erosion, regardless of what happened in the previous iteration.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': False
            }
        }
    },
    'binary_opening': {
        'full_name': 'Binary opening',
        'fn': ff.binary_opening,
        'description': "succession of a binary erosion, and a binary dilation",
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "iterations": {
                'optional': True,
                'label': "Iterations",
                'description': "The erosion step of the opening, then the dilation step are each repeated iterations times (one, by default). If iterations is less than 1, each operation is repeated until the result does not change anymore. Only an integer of iterations is accepted.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 20,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "border_value": {
                'optional': True,
                'label': "Border value",
                'description': "Value at the border in the output array.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1,
                'single_step': 1,
                'default': 0
            },
            "brute_force": {
                'optional': True,
                'label': "Brute force",
                'description': "Memory condition: if False, only the pixels whose value was changed in the last iteration are tracked as candidates to be updated in the current iteration; if true all pixels are considered as candidates for update, regardless of what happened in the previous iteration.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': False
            }
        }
    },
    
    'binary_closing': {
        'full_name': 'Binary closing',
        'fn': ff.binary_closing,
        'description': "succession of a greyscale dilation and a greyscale erosion of a binary-image",
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "iterations": {
                'optional': True,
                'label': "Iterations",
                'description': "The dilation step of the closing, then the erosion step are each repeated iterations times (one, by default). If iterations is less than 1, each operations is repeated until the result does not change anymore. Only an integer of iterations is accepted.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 20,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "border_value": {
                'optional': True,
                'label': "Border value",
                'description': "Value at the border in the output array.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1,
                'single_step': 1,
                'default': 0
            },
            "brute_force": {
                'optional': True,
                'label': "Brute force",
                'description': "Memory condition: if False, only the pixels whose value was changed in the last iteration are tracked as candidates to be updated in the current iteration; if true al pixels are considered as candidates for update, regardless of what happened in the previous iteration.",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': False
            },
        }
    },
    'binary_fill_holes': {
        'full_name': 'Binary fill holes',
        'fn': ff.binary_fill_holes,
        'description': 'fill holes in binary objects',
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            }
        }
    },
    
    'binary_propagation': {
        'full_name': 'Binary propagation',
        'fn': ff.binary_propagation,
        'default_params': {
            "structure_shape": {
                'optional': True,
                'label': "Structure shape",
                'description': "Shape of structure",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "structure_size_x": {
                'optional': True,
                'label': "Structure size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "structure_size_y": {
                'optional': True,
                'label': "Structure size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "origin_x": {
                'optional': True,
                'label': "Origin in x-direction",
                'description': "Placement of the filter in x-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "origin_y": {
                'optional': True,
                'label': "Origin in y-direction",
                'description': "Placement of the filter in y-direction, by default 0",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': -10000,
                'maximum': 10000,
                'single_step': 1,
                'default': 0
            },
            "border_value": {
                'optional': True,
                'label': "Border value",
                'description': "Value at the border in the output array.",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 0,
                'maximum': 1,
                'single_step': 1,
                'default': 0
            }
        }
    },
    'tophat': {
        'full_name': 'Top-hat',
        'fn': ff.tophat,
        'description': "extracts small elements and details from given images",
        'default_params': {
            "type": {
                'optional': False,
                'label': "Typ",
                'description': "type of top-hat",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'white',
                'options': ['white', 'black'],
                'options_description': [
                    'The white top-hat transform returns an image, containing those "objects" of an input image that are "smaller" than the structuring element (i.e., places where the structuring element does not fit in), and are brighter than their surroundings.',
                    'The black top-hat returns an image, containing the "objects" or "elements" that are "smaller" than the structuring element, and are darker than their surroundings'
                ]
            },
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'grabCut': {
        'full_name': 'GrabCut',
        'fn': ff.grabCut,
        'description': "Run GrabCut algorithm to extract foreground from background",
        'default_params': {
            'roi_left': {
                'optional': False,
                'description': "bounding rectangle left border",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 10,
                'minimum': 0,
                'maximum': 10000,
                'single_step': 1
            },
            'roi_right': {
                'optional': False,
                'description': "bounding rectangle right border",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 10,
                'minimum': 0,
                'maximum': 10000,
                'single_step': 1
            },
            'roi_top': {
                'optional': False,
                'description': "bounding rectangle top border",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 10,
                'minimum': 0,
                'maximum': 10000,
                'single_step': 1
            },
            'roi_bottom': {
                'optional': False,
                'description': "bounding rectangle bottom border",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 10,
                'minimum': 0,
                'maximum': 10000,
                'single_step': 1
            },
            'iterations': {
                'optional': False,
                'description': "Number of iterations",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 1,
                'minimum': 0,
                'maximum': 10,
                'single_step': 1
            },
            'return_type': {
                'optional': False,
                'label': "Return type",
                'description': "Defines what to return from the filter",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'fg',
                'options': ['fg', 'bg', 'binary_fg', 'binary_bg'],
                'options_description': [
                    'Foreground in RGB',
                    'Background in RGB',
                    'Foreground in binary',
                    'Background in binary'
                ]
            }
        }
    },
    'sobel_edge': {
        'full_name': 'Sobel Edge',
        'fn': ff.sobel_edge,
        'description': "Calculates an image derivative by convolving the image with a kernel",
        'default_params': {
            "dx": {
                'optional': False,
                'label': "x order",
                'description': "Order of the derivative x",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 1,
                'minimum': 0,
                'maximum': 5,
                'single_step': 1

            },
            "dy": {
                'optional': False,
                'label': "y order",
                'description': "Order of the derivative y",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 1,
                'minimum': 0,
                'maximum': 5,
                'single_step': 1

            },
            "ksize": {
                'optional': False,
                'label': "Kernel size",
                'description': "Aperture size used to compute the second-derivative filters",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 5,
                'minimum': 1,
                'maximum':7,
                'single_step': 2

            },
            "scale": {
                'optional': True,
                'label': "Scale factor",
                'description': "Scale factor for the computed Laplacian values",
                'dtype': float,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1,
                'default': 1.0
            },
            "delta": {
                'optional': True,
                'label': "Delta",
                'description': "Added to the results",
                'dtype': float,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1,
                'default': 0.0
            },
            "border_type": {
                'optional': True,
                'label': "Border Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'BORDER_REFLECT_101',
                'options': ['BORDER_REPLICATE', 'BORDER_REFLECT', 'BORDER_REFLECT_101', 'BORDER_TRANSPARENT'],
                'options_description': [
                    "aaaaaa|abcdefgh|hhhhhhh",
                    "fedcba|abcdefgh|hgfedcb",
                    "gfedcb|abcdefgh|gfedcba",
                    "uvwxyz|abcdefgh|ijklmno"
                ]
            },
            'stretch_range': {
                'optional': True,
                'label': "Stretch Range",
                'description': "If True, minimum and maximum values will be set to dtype minimum and maximum",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': True
            }
        }
    },
    'laplacian_edge': {
        'full_name': 'Laplacian Edge',
        'fn': ff.laplacian_edge,
        'description': "calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator",
        'default_params': {
            "ksize": {
                'optional': False,
                'label': "Kernel size",
                'description': "Aperture size used to compute the second-derivative filters",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 5,
                'minimum': 1,
                'maximum':7,
                'single_step': 2

            },
            "scale": {
                'optional': True,
                'label': "Scale factor",
                'description': "Scale factor for the computed Laplacian values",
                'dtype': float,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1,
                'default': 1.0
            },
            "delta": {
                'optional': True,
                'label': "Delta",
                'description': "Added to the results",
                'dtype': float,
                'wtype': 'double_spinbox',
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1,
                'default': 0.0
            },
            "border_type": {
                'optional': True,
                'label': "Border Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'BORDER_REFLECT_101',
                'options': ['BORDER_REPLICATE', 'BORDER_REFLECT', 'BORDER_REFLECT_101', 'BORDER_TRANSPARENT'],
                'options_description': [
                    "aaaaaa|abcdefgh|hhhhhhh",
                    "fedcba|abcdefgh|hgfedcb",
                    "gfedcb|abcdefgh|gfedcba",
                    "uvwxyz|abcdefgh|ijklmno"
                ]
            },
            'stretch_range': {
                'optional': True,
                'label': "Stretch Range",
                'description': "If True, minimum and maximum values will be set to dtype minimum and maximum",
                'dtype': bool,
                'wtype': 'checkbox',
                'default': True
            }
        }
    },
    'morphological_gradient': {
        'full_name': 'Morphological gradient',
        'fn': ff.morphological_gradient,
        'description': "difference between a dilation and an erosion of an greyscale-image",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'morphological_laplace': {
        'full_name': 'Morphological laplace',
        'fn': ff.morphological_laplace,
        'description': "arithmetic difference between the internal and the external gradient of an greyscale-image",
        'default_params': {
            "footprint_shape": {
                'optional': False,
                'label': "Footprint shape",
                'description': "Shape of footprint",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'rectangle',
                'options': ['rectangle', 'ellipse'],
                'options_description': [
                    '',
                    ''
                ]
            },
            "footprint_size_x": {
                'optional': False,
                'label': "Footprint size in x-direction",
                'description': "Length of the given shape in x-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "footprint_size_y": {
                'optional': False,
                'label': "Footprint size in y-direction",
                'description': "Length of the given shape in y-direction",
                'dtype': int,
                'wtype': 'spinbox',
                'minimum': 1,
                'maximum': 100,
                'single_step': 1,
                'default': 1
            },
            "mode": {
                'optional': True,
                'label': "Mode",
                'description': "The mode parameter determines how the input array is extended when the filter overlaps a border. By passing a sequence of modes with length equal to the number of dimensions of the input array, different modes can be specified along each axis. Default value is ‘reflect’. ",
                'dtype': str,
                'wtype': 'combobox',
                'default': 'reflect',
                'options': ['reflect', 'constant', 'nearest', 'mirror', 'wrap'],
                'options_description': [
                    "The input is extended by reflecting about the edge of the last pixel.",
                    "The input is extended by filling all values beyond the edge with the same constant value, defined by the cval parameter.",
                    "The input is extended by replicating the last pixel.",
                    "The input is extended by reflecting about the center of the last pixel.",
                    "The input is extended by wrapping around to the opposite edge."
                ]
            },
            "cval": {
                'optional': True,
                'label': "Cval",
                'description': "Value to fill past edges of input if mode is ‘constant’. Default is 0.0.",
                'dtype': float,
                'wtype': 'double_spinbox',
                'default': 0.0,
                'minimum': 0.0,
                'maximum': 255.0,
                'single_step': 0.1,
            },
            "origin": {
                'optional': True,
                'label': "Origin",
                'description': "The origin parameter controls the placement of the filter. Default is 0.",
                'dtype': int,
                'wtype': 'spinbox',
                'default': 0,
                'minimum': 0,
                'maximum': 1000000,
                'single_step': 1
            }
        }
    },
    'dummy': {
        'full_name': 'Dummy',
        'fn': ff.dummy,
        'description': 'Copy input (use in modifiers)',
        'default_params': {}
    },
    'invert': {
        'full_name': 'Invert',
        'fn': ff.invert,
        'description': 'Invert the image',
        'default_params': {}
    }
}
