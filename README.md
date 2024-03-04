# LipReading
Lip Reading using Image Processing and Deep Learning

# Steps to Get started :


Don't jump to any of the steps before doing *Step 1*.
Also please add issues on the things you are working on so we are aware of what is going on. If two people are working on the same issue one of you open it and then assign it to the other one. Or some way indicate two of you are working on it.
Make sure whatever you are doing isn't going nowhere.
And please don't waste much time on technicalities at this point. We just need a system in place. 

Possible tools and libraries : 

1. OpenCV and Dlib for Computer Visison and image processing 
2. pandas, numpy, scipy, scikit-learning for preprocessing and data handling.
3. Tensorflow, keras, pytorch etc. for DL model.



## Step 1: Understanding data 
 
 We need to understand the format in which the data is provided and make sense of how we can use it. Like for example we should be easily able to do things like at 10 sec in the video he say the word "x". We should also be able to get the frame of a particular time in the video. ( this small manipulations will be of great help through out the project in our video ) 
 
 
## Step 2: Preprocessing 

Once we have the data we should start by extracting the face and lips from the individual frames. And also see if the images should be fed to the model as it is ? or we should apply some kind of edge detection technique for this part probably follow a paper and we'll build up on it.


## Step 3: Preprocessing for model 

Figure out how will we feed the data to the model. For this you need to understand some basics things about neural networks and how they work in code so, after all the preprocessing you put it all together in a proper data structure with proper dimensions.
Here also figure out how are we going to split the data into training and testing.
The number of task here increases based on how well you understand the data in step one and how do you plan on working on it.

## Step 4: Model 

Pick the most simplest DL model that has worked in any of the paper and implement it. At this point use keras, get code from github doesn't matter we just want to see if the pipeliine works.


## Step 5: Output  

Present the output in such a way anyone can unstand. 


## Step 6: Accuracy measures

There are tons of model accuracy and relavancy measures, we need to atleast have some in place before hand. Take help of papers here too, but the basics one's llke accuracy on train data, accuracy on testing data, Model Loss, Confusion matrix etc. should be implemented.


 
