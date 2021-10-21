# Syntheticity index for texts (in Russian only)

## Requirements
`pip install -r requirements.txt` (mostly depends on [Morpholog](https://github.com/constantin50/morpholog))

## Usage
`python syntheticity.py --file filename.txt`
(Argument not usable for now, will read `test.txt` from the project rootdir.)

## Technical details
Syntheticity index is the ratio of morphs in given language (or text) to the number of words in that language (or text).

![equation_index](https://latex.codecogs.com/gif.latex?S_i%20%3D%20%5Cfrac%7BM%7D%7BW%7D)

![equation_limits](https://latex.codecogs.com/gif.latex?S_i%20%5Cin%20%5B1%3B%20&plus;%5Cinfty%5D)

Languages can be divided into classes by syntheticity index: analytical (sometimes subdivided into isolating and analytical) (![equation_analytical](https://latex.codecogs.com/gif.latex?1%20%5Cleqslant%20S_i%20%5Cleqslant%202)), synthetic (![equation_synthetic](https://latex.codecogs.com/gif.latex?2%20%5Cleqslant%20S_i%20%5Cleqslant%203)), and polysynthetic (![equation_polysynthetic](https://latex.codecogs.com/gif.latex?S_i%20%3E%203))