# youtube-downloader
This is a library to search words on Youtube, download videos about these words and extract screenshots from the videos. You specify a word to search and the end result is a folder with images extracted from the first few videos about that word on Youtube. The packages that are necessary to install in order to run the functions are BeautifulSoup, OpenCV and pytube. 

The functionalities can be accessed by simply importing the function extract_images_from_word to a new script. This function takes in as argument the word to search. The optional inputs are
- image_delay, to decide how much time between the screenshots
- delete_video, to decide if the videos are deleted after being used
- num_urls, to decide how many videos to (try to) download
- max_images, to fix a maximum number of images to extract for each video
- name, to change the names of the files, which are of the form "name_##.jpg", the folder called name will contain the images
- max_duration, to decide the maximum length of the videos to download (in minutes)
- silent, to decide if messages about the saved images are printed, messages about the videos downloaded are always printed

The other functions in the library can be useful separately as well.
- extract_images_from_video: uses a .mp4 file to exract images
- download_video: takes the url of the video and downloads it
- get_urls: search for a specific word and returns a list of urls for the videos
- max_label: find the maximum label for files called "name_##.jpg" in a folder

I also wrote a blog post about this program for more details: 


