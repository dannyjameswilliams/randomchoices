# randomchoices
An exploration of how random humans truly are.

You can find the [Google forms survey here](https://forms.gle/JvGfuUA2JNpdYm8G6), and the reddit post where most of the survey responses came from [here](https://www.reddit.com/r/SampleSize/comments/ja9gqd/academic_can_humans_truly_be_random_everyone/).

The blog post detailing the analysis and interpretation of the results can be found [here](https://dannyjameswilliams.co.uk/post/randomchoices), and there is a shorter infographic available [here](https://dannyjameswilliams.co.uk/post/randomchoices/infographic.png).

## Code

The code is written in Python 3, and plotly was used for the interactive html based plots. Other modules used were NumPy, SciPy, and pandas.

To reproduce the results, you need to clone this repository, and edit the follwing lines in `main.py`:
```
os.chdir("/home/fs19144/Documents/Personal_Projects/randomchoices/")
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/')
sys.path.append('/home/fs19144/Documents/Personal_Projects/randomchoices/code')
```
These must change to your own working directory, because as you can probably tell, these are my own working directories! After you have done that, you can run `main.py` from the terminal with
```
python3 main.py
```
if you are using `bash`. Otherwise if you are on Windows, you will need to run `main.py` through a Python launcher.
