import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Function to get index of the movie
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

#Function to get title of the movie
def get_index_from_title(title):
	for i in df.index:
		if df.title[i].lower() == title:
			return i
	return -1
	#return df[df.title == title]["index"].values[0]


#Read CSV File
df = pd.read_csv("movie_dataset.csv", engine='python',error_bad_lines=False)
#print df.columns

#Select Features
features = ['keywords','cast','genres','director','vote_average']

#Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return(row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]+" "+str(row["vote_average"]))
	except:
		print("Error:", row)

df["combined_features"] = df.apply(combine_features,axis=1)
#print "Combined Features:", df["combined_features"].head()


#Create count matrix from this new combined column
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

#Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)
mov = input("Enter a movie you like: ")
movie_user_likes = mov.lower()

#Get index of this movie from its title
movie_index = get_index_from_title(movie_user_likes)
if movie_index == -1:
	print("Sorry, movie not found.")
	exit()
#print(movie_index)

#Get a list of similar movies in descending order of similarity score
similar_movies =list(enumerate(cosine_sim[movie_index]))
#Accessing the row corresponding to given movie to find all similarity scores for that movie and enumerating over it.

sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

#Print titles of first 15 movies
print("-------------------------------------------------------------------------")
print("\nSimilar movies to",mov,"are :")
i=0
for element in sorted_similar_movies:
		print (get_title_from_index(element[0]))
		i=i+1
		if i>15:
			break