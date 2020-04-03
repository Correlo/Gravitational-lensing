#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 03/04/2020

How to use the code:

*** main.py ***
Code to deflect rays and obtain magnification maps using inverse ray shooting method.

params.ini is the file which contains the parameters of the lens that you want to obtain.

The fields to fill are:

- IMAGE:  Configure source plane using a .tiff image. If image is not a square, it will be cutted.
          Use [IMAGE] to identify the field. If [IMAGE] field is active, [MESH] and [SOURCE] will 
          be ignored.

          Parameters to configure:
  
          - path -> Path of the image
          - XL   -> Half of the image plane side in Einstein radius.
          - YL   -> Half of the source plane side in Einstein radius.

- MESH:   Configure source plane mesh (X) and image plane mesh(Y). A square mesh is
          assumed for both planes. Use [MESH] to identify the field.
 
          Parameters to configure:
  
          - nX -> Number of pixels along one axis in image plane (even number is recommended).
          - nY -> Number of pixels along one axis in source plane (even number is recommended).
          - XL -> Half of the image plane side in Einstein radius.
          - YL -> Half of the source plane side in Einstein radius.

- SOURCE: Configure source characteristics. Use [SOURCE] to identify the field.

          Parameters to configure:

          - rsx -> x position of the source center in Einstein radius.
          - rsy -> y position of the source center in Einstein radius.
          - rad -> Source radius in Einstein radius.

- LENS:   Configure lens characteristics. More than one lenses can be configure to be computed 
          using the same mesh and source. Use [LENS1], [LENS2], ... to identify the field of 
          each lens.

          Parameters to configure:

          - mode -> Type of lens. Modes available are PSL (Point Source Lens),
                    ChangRefsdal and SIS (Singular Isothermal Sphere).
          - mag  -> If mag == 1, magnification map will be calculated.
          - rp   -> Number of rays per pixel

          for PSL:

          - rlix -> x position of the lens center in Einstein radius.
          - rliy -> y position of the lens center in Einstein radius.
          - mli  -> Mass of the lens.

          The 'i' in parameter's name is the label of the i-lens. In params.ini, i = 1, 2, 3, ...
          Check the example params.ini to more details.

          for ChangRefsdal:

          - rlix -> x position of the lens center in Einstein radius.
          - rliy -> y position of the lens center in Einstein radius.
          - mli  -> Mass of the lens.
          - k    -> Convergence 0 <= k <= 1
          - g    -> Share       0 <= g <= 1

          The 'i' in parameter's name is the label of the i-lens. In params.ini, i = 1, 2, 3, ...
          Check the example params.ini to more details.

          for SIS:

          - rlx -> x position of the lens center in Einstein radius.
          - rly -> y position of the lens center in Einstein radius.
          - ThE -> Einstein radius

Modules Lib_lens.py and Core.py must be located in the same path as main.py.

*** Profile.py ***
Code to obtain profiles of the magnification map for different Gaussian sources.

Parameters to configure:

- LFile   -> Magnification map path. Expected format is .npy.
- p0      -> Tuple with the position of the first pixel of the profile, in pixel units
             (from 0 to nY - 1)
- p1      -> Tuple with the position of the last pixel of the profile, in pixel units 
             (from 0 to nY - 1)
- YL      -> Half of the source plane side in Einstein radius.
- rp      -> Number of rays per pixel.
- rad     -> List of source radii in Einstein radius. 
- Outname -> Name of the output file.
  

