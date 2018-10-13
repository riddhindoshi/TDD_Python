"""
HW4: Movie Trivia

This homework deals with the following topics:
- Dictionaries
- Sets
- Databases using dictionaries (not too far from how they really work!)
- Test driven development (TDD)

In this HW, we will deal with representing movie data using dictionaries,
with the goal of answering some simple movie trivia questions. For example,
“what is the name of the movie that both Tom Hanks and Leonardo DiCaprio
acted in?”

We will use 2 dictionaries. The first corresponds to information about
an actor and all the movies that he/she has acted in.  The second
corresponds to information about the critics’ score and the audience
score from https://www.rottentomatoes.com/, about the movies.  

Given that information, we will then want to answer some typical movie
trivia questions.

"""

#Use these first 2 functions to create your 2 dictionaries
import csv
import operator


def create_actors_DB(actor_file):
    """
    Creates a dictionary keyed on actors from a text file.
    """
    
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = movies
    f.close()
    
    return movieInfo


def create_ratings_DB(ratings_file):
    """
    Makes a dictionary from the rotten tomatoes csv file.
    """
    
    scores_dict = {}
    with open(ratings_file, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
            
    return scores_dict


def insert_actor_info(actor, movies, actordb):
    '''
    This function updates/adds information to the dictionary of database. Return: None
    '''

    for actor_i in actordb:
        # if actor is already present in the dictionary, update the movies list associated with it
        if actor_i == actor:
            actordb[actor_i] += movies
            # required return as the job of the function is now done
            return

    # if actor not present, augment
    actordb[actor] = movies


def insert_rating(movie, ratings, ratingsdb):
    '''
    This function updates/adds information to the dictionary of ratings. Return: None
    '''

    for movie_i in ratingsdb:
        # if movie is already present in the dictionary, alter the ratings list associated with it
        if movie_i == movie:
            ratingsdb[movie_i] = ratings
            # required return as the job of the function is now done
            return
    # if movie not present, augment the movie with rating
    ratingsdb[movie] = ratings


def select_where_actor_is(actor_name, actordb):
    '''
    This function returns a list of all movies the actor_name passed as an input has acted in. Return: list of movies
    '''

    # if the actor_name isnt in database, return empty list
    if actor_name not in actordb.keys():
        return []
    return actordb[actor_name]


def select_where_movie_is(movie_name, actordb):
    '''
    This function returns a list of all the actors that have acted in a particular movie. Return: list of actors that
    have acted in particular movie
    '''

    # initiate the return list
    return_list_actor = []
    # loop through all actors
    for actor_i in actordb:
        # loop through the movies that belong to that actor
        for movie_i in actordb[actor_i]:
            if movie_i == movie_name:
                # add name to return list if they have acted in the movie
                return_list_actor += [actor_i]
    return return_list_actor


def select_where_rating_is(comparison, targeted_rating, is_critic, ratingsdb):
    '''
    This function function returns a list of movies that satisfy an inequality or equality,
    based on the comparison argument and the targeted rating argument.
    Return: list of movies satisfying the condition specified by input paramters of the function
    '''

    # initiate the dictionary to use the operator library
    ops = {'=': operator.eq,
           '>': operator.gt,
           '<': operator.lt}

    # initiate the return list
    return_list_movies = []

    # check the critics rating
    if is_critic:
        # check all the values in the critics list
        for movie_i in ratingsdb:
            # check if the condition satisfies target rating
            if ops[comparison](ratingsdb[movie_i][0], targeted_rating):
                # add movie to the return list if the condition satisfies
                return_list_movies += [movie_i]

    # check audience rating
    elif not is_critic:
        # check all the values in the audience list
        for movie_i in ratingsdb:
            # check if the condition satisfies target rating
            if ops[comparison](ratingsdb[movie_i][1], targeted_rating):
                # add movie to the return list if the condition satisfies
                return_list_movies += [movie_i]

    return return_list_movies


def get_co_actors(actor_name, actor_db):
    '''
    This function returns a list of all actors that the given actor has ever worked with in any movie.
    Return: List of actors who have worked with each other
    '''

    # initialize empty co_actors list
    co_actors = []
    # get all the movies the actor has worked on
    movies_actor_worked_on = select_where_actor_is(actor_name, actor_db)
    # if actor has not worked on any movie, he will have no co_actors, hence return empty
    if not movies_actor_worked_on:
        return co_actors

    for movie_i in movies_actor_worked_on:
        # make a list of all the actors worked on the movie the input actor has worked on
        co_actors += select_where_movie_is(movie_i, actor_db)
    #eliminate duplicate entries
    co_actors = list(set(co_actors))
    # input actor isn't the co_actor of itself, so strip him out
    co_actors.remove(actor_name)
    # return a sorted list
    co_actors.sort()
    return co_actors


def get_common_movie(actor1, actor2, actor_db):
    '''
    This function returns a list of movies where both actors were cast.
    Return: List of common movies of two actors taken as input
    '''
    # get list of movies for actor 1
    movies_actor1 = select_where_actor_is(actor1, actor_db)
    # get list of movies for actor 2
    movies_actor2 = select_where_actor_is(actor2, actor_db)
    # typecast returned lists to sets to find common movies
    # and then re-typecast to return the values of common movies as list
    return list(set(movies_actor1) & set(movies_actor2))


def good_movies(ratingsdb):
    '''
    This function returns the set of movies that both critics and the audience have rated
    above 85 (greater than or equal to 85).
    Return: set of movies satisfying above condition
    '''

    # get a list of good critics rating
    good_critics_movie = select_where_rating_is('>', '85', True, ratingsdb)
    good_critics_movie += select_where_rating_is('=', '85', True, ratingsdb)

    # get a list of good audience rating
    good_audience_movie = select_where_rating_is('>', '85', False, ratingsdb)
    good_audience_movie += select_where_rating_is('=', '85', False, ratingsdb)

    # return a set of ratings that are common to both the lists
    return set(good_critics_movie) & set(good_audience_movie)


def get_common_actors(movie1, movie2, actor_db):
    '''
    Given a pair of movies, this function returns a list of actors that acted in both movies.
    Return: list of actors that acted in both movies given as input
    '''

    # get actors acted in movie1
    actors_movie1 = select_where_movie_is(movie1, actor_db)
    # get actors acted in movie2
    actors_movie2 = select_where_movie_is(movie2, actor_db)
    # typecast returned lists to sets to find common actors
    # and then re-typecast to return the values of common actors as list
    return list(set(actors_movie1) & set(actors_movie2))


def print_ui_info():
    '''
    This function displays useful data with respect to what program does.
    Used majorly to reduce clutter in main function. Return: None
    '''
    print("This Database consists of two sections:")
    print("A. The Actors and the Movies they have acted in")
    print("B. The Movies and their Rating by Critics and Audience")
    print("\nThere are many things you can do with the Database from these options:")
    print("1. Press 1 to insert new actor information/ modify actor information")
    print("2. Press 2 to insert new rating information/ modify rating information")
    print("3. Press 3 to list all the movies the actor has acted in")
    print("4. Press 4 to list all the actors in the movie")
    print("5. Press 5 to compare ('<', '>', '=') the ratings of the movie to some target rating")
    print("\tFor eg. Tell me every movie that has an audience rating of exactly 65")
    print("6. Press 6 to get all the co-actors of a particular actor")
    print("7. Press 7 to find common movie between two actors")
    print("8. Press 8 to find out all the good movies(audience and critics rating equal to or above 85) in database")
    print("9. Press 9 to get common actors between two movies")


def get_capitalize_format(input_string):
    '''
    This function converts the given string input to an cleaner capitalize format
    For eg. meryl streep --> Meryl Streep
    For eg. added movie --> Added Movie
    Return: Formatted version of the string
    '''
    input_string = input_string.lower()
    input_list = input_string.split(' ')
    input_list1 = []
    for i in input_list:
        # capitalize individual members of list
        input_list1 += [i.capitalize()]
        # this is necessary to later join the list as a string
        input_list1.append(" ")
    # convert the list to string
    input_string = ''.join(input_list1)
    # strip trailing whitespaces and return
    return input_string.strip()


def main():
    # initiate the databases from the file, store it in dictionary
    actor_DB = create_actors_DB('moviedata.txt')
    ratings_DB = create_ratings_DB('movieratings.csv')
    print_ui_info()
    user_input = int(input("Enter the option you want to choose: "))

    # insert_actor_info
    if user_input == 1:
        actor_input = input("Enter the actor you want to add/modify to database.\t For eg. Firstname Lastname ")
        actor = get_capitalize_format(actor_input)
        movies_input = input("Enter the list of movies the actor has acted in.\t For eg. movie1, movie2, movie3 ")
        movies_list = list(movies_input.split(','))
        clean_list_movie = []
        for movie in movies_list:
            clean_list_movie += [get_capitalize_format(movie)]
        insert_actor_info(actor, clean_list_movie, actor_DB)
        print("Actor information successfully recorded/modified")

    # insert rating
    elif user_input == 2:
        movie_input = input("Enter the movie name you want to enter/modify ")
        movie = get_capitalize_format(movie_input)
        ratings = input("Enter the list of ratings for the movie.\t For eg. rating1, rating2 ")
        ratings_list = list(ratings.split(','))
        insert_rating(movie, ratings_list, ratings_DB)
        print("Ratings information successfully recorded/modified")

    # select_where_actor_is
    elif user_input == 3:
        actor_input = input("Enter the actor you want to look for.\t For eg. Firstname Lastname ")
        actor_input_string = get_capitalize_format(actor_input)
        ans_actor_list = select_where_actor_is(actor_input_string, actor_DB)
        if not ans_actor_list:
            print("Not Present")
        else:
            print(ans_actor_list)

    # select_where_movie_is
    elif user_input == 4:
        movie_input = input("Enter the movie for which you want to know the actors ")
        movie = get_capitalize_format(movie_input)
        actors_list = select_where_movie_is(movie, actor_DB)
        if not actors_list:
            print("Not Present")
        else:
            print(actors_list)

    # select_where_rating_is
    elif user_input == 5:
        comparison = input("Select how do you want to compare to target rating (</>/=) ")
        targeted_rating = input("Enter the target rating you want to compare to: ")
        is_critic = True
        critics_rating = input("Do you want to compare critics rating? Say Y or N."
                               "If N, it will compare to audience rating: ")
        if critics_rating == 'N':
            is_critic = False
        movie_list = select_where_rating_is(comparison, targeted_rating, is_critic, ratings_DB)
        if not movie_list:
            print("No such movies present")
        else:
            print(movie_list)

    # get_co_actors
    elif user_input == 6:
        actor_input = input("Enter the actor whose co-actors you would want to see.\t For eg. Firstname Lastname ")
        actor_input_string = get_capitalize_format(actor_input)
        ans_actor_list = get_co_actors(actor_input_string, actor_DB)
        if not ans_actor_list:
            print("Not Present")
        else:
            print(ans_actor_list)
        pass

    # get_common_movie
    elif user_input == 7:
        actor_input1 = input("Enter the actor1 whose common movie you would want to know.\t For eg. Firstname Lastname ")
        actor_input2 = input("Enter the actor2 whose common movie you would want to know.\t For eg. Firstname Lastname ")
        actor1 = get_capitalize_format(actor_input1)
        actor2 = get_capitalize_format(actor_input2)
        ans_movie_list = get_common_movie(actor1, actor2, actor_DB)
        if not ans_movie_list:
            print("No common movies")
        else:
            print(ans_movie_list)

    # good_movies
    elif user_input == 8:
        ans_good_movies = good_movies(ratings_DB)
        if not ans_good_movies:
            print("There are no good movies in database")
        else:
            print("The good movies are ", ans_good_movies)

    # get_common_actors
    elif user_input == 9:
        movie_input1 = input("Enter movie1 for which you want common actors: ")
        movie_input2 = input("Enter movie2 for which you want common actors: ")
        movie1 = get_capitalize_format(movie_input1)
        movie2 = get_capitalize_format(movie_input2)
        ans_actors_list = get_common_actors(movie1, movie2, actor_DB)
        if not ans_actors_list:
            print("There are no common actors")
        else:
            print("The common actors are ", ans_actors_list)


if __name__ == '__main__':
    main()
