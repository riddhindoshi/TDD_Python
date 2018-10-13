import unittest
from movie_trivia import *


class TestMovieTrivia(unittest.TestCase):
    def setUp(self):
        self.ratings_DB = create_ratings_DB('movieratings.csv')
        self.actor_DB = create_actors_DB('moviedata.txt')

    def test_insert_actor_info(self):
        actor_DB1 = self.actor_DB.copy()
        actor_DB_result = self.actor_DB.copy()
        actor_DB_result['SRK'] = ['la', 'li', 'le']
        insert_actor_info('SRK', ['la', 'li', 'le'], actor_DB1)
        self.assertEqual(actor_DB_result, actor_DB1, "Adding new actor does not work")

        actor_DB_result1 = self.actor_DB.copy()
        actor_DB2 = self.actor_DB.copy()
        actor_DB_result1['Meryl Streep'] = ['Doubt', "Sophie's Choice", 'The Post', 'Added movie']
        insert_actor_info('Meryl Streep', ['Added movie'], actor_DB2)
        self.assertEqual(actor_DB_result1, actor_DB2, "he augmentation of movies does not work")

        actor_DB3 = self.actor_DB.copy()
        actor_DB_result2 = self.actor_DB.copy()
        actor_DB_result2['Tom Hanks'] = ['The Post', 'Catch Me If You Can', 'Cast Away', 'Added movie2']
        insert_actor_info('Tom Hanks', ['Added movie2'], actor_DB3)
        self.assertEqual(actor_DB_result2, actor_DB3, "The augmentation of movies does not work")

    def test_insert_rating(self):
        ratings_DB1 = self.ratings_DB.copy()
        ratings_DB_result = self.ratings_DB.copy()
        ratings_DB_result['Added movie'] = ['94', '83']
        insert_rating('Added movie', ['94', '83'], ratings_DB1)
        self.assertEqual(ratings_DB_result, ratings_DB1, "Adding new movie rating does not work")


        ratings_DB2 = self.ratings_DB.copy()
        ratings_DB_result1 = self.ratings_DB.copy()
        ratings_DB_result1['Doubt'] = ['97', '87']
        insert_rating('Doubt', ['97', '87'], ratings_DB2)
        self.assertEqual(ratings_DB_result1, ratings_DB2, "Altering existing rating does not work")

    def test_select_where_actor_is(self):
        result = ['Doubt', "Sophie's Choice", 'The Post']
        self.assertEqual(result, select_where_actor_is('Meryl Streep', self.actor_DB),
                         "Does not give the correct movies the actor has acted in")

        result1 = ['The Post', 'Catch Me If You Can', 'Cast Away']
        self.assertEqual(result1, select_where_actor_is('Tom Hanks', self.actor_DB),
                         "Does not give the correct movies the actor has acted in")

        self.assertEqual([], select_where_actor_is('Added actor', self.actor_DB),
                         "Does not give the correct answer for actor not present")

    def test_select_where_movie_is(self):
        self.assertEqual(['Meryl Streep'],select_where_movie_is('Sophie\'s Choice', self.actor_DB),
                         "The actors that have acted in the movie are incorrect")
        self.assertEqual(['Meryl Streep', 'Tom Hanks'], select_where_movie_is('The Post', self.actor_DB),
                         "Multiple actors not returned for a single movie")
        self.assertEqual(['Meryl Streep', 'Amy Adams'], select_where_movie_is('Doubt', self.actor_DB),
                         "Multiple actors not returned for a single movie")
        self.assertEqual([], select_where_movie_is('Added movie', self.actor_DB),
                         "Empty list not returned a single movie")

    def test_select_where_rating_is(self):
        # test critics rating
        self.assertEqual(['Doubt', 'Arrival', 'Jaws'], select_where_rating_is('>', '70', True, self.ratings_DB),
                         "Greater than rating does not work in critics")
        self.assertEqual(['Doubt'], select_where_rating_is('<', '80', True, self.ratings_DB),
                         "Greater than rating does not work in critics")
        self.assertEqual(['Jaws'], select_where_rating_is('=', '97', True, self.ratings_DB),
                         "Equal to rating does not work in critics")
        self.assertEqual([], select_where_rating_is('=', '70', True, self.ratings_DB),
                         "Equal to empty rating does not work in audience")

        # test audience ratings
        self.assertEqual(['Doubt'], select_where_rating_is('<', '80', False, self.ratings_DB),
                         "Less than rating does not work in audience")
        self.assertEqual(['Arrival'], select_where_rating_is('=', '82', False, self.ratings_DB),
                         "Equal to rating does not work in audience")
        self.assertEqual(['Doubt', 'Arrival', 'Jaws'], select_where_rating_is('>', '70', False, self.ratings_DB),
                         "Greater than rating does not work in audience")
        self.assertEqual(['Jaws'], select_where_rating_is('>', '85', False, self.ratings_DB),
                         "Greater than rating does not work in audience")
        self.assertEqual([], select_where_rating_is('=', '84', False, self.ratings_DB),
                         "Equal to empty rating does not work in audience")
        self.assertEqual([], select_where_rating_is('=', '40', False, self.ratings_DB),
                         "Equal to empty rating does not work in audience")

    def test_get_co_actors(self):
        self.assertEqual(['Amy Adams', 'Tom Hanks'], get_co_actors('Meryl Streep', self.actor_DB),
                         "Does not get correct co-actors")
        self.assertEqual(['Meryl Streep'], get_co_actors('Tom Hanks', self.actor_DB),
                         "Does not get correct co-actors")
        self.assertEqual(['Meryl Streep'], get_co_actors('Amy Adams', self.actor_DB,),
                         "Does not get correct co-actors")
        self.assertEqual([], get_co_actors('Added actor', self.actor_DB),
                         "Does not work when the input is invalid actor name")
        self.assertEqual([], get_co_actors('Added Actor1', self.actor_DB),
                         "Does not work when there are no co actors")

    def test_get_common_movie(self):
        self.assertEqual(['Doubt'], get_common_movie('Meryl Streep', 'Amy Adams', self.actor_DB),
                         "Does not get common movies correctly")
        self.assertEqual([], get_common_movie('Added Actor1', 'Meryl Streep', self.actor_DB),
                         "Does not get common movies correctly as empty list")
        self.assertEqual([], get_common_movie('Tom Hanks', 'Amy Adams', self.actor_DB),
                         "Does not get common movies correctly as empty list")
        self.assertEqual(['The Post'], get_common_movie('Meryl Streep', 'Tom Hanks', self.actor_DB),
                         "Does not get common movies correctly")
        self.assertEqual([], get_common_movie('Inexistent Actor', 'Invalid Input', self.actor_DB),
                         "Does not work for invalid inputs for common movies")
        self.assertEqual([], get_common_movie('Inexistent Actor', 'Meryl Streep', self.actor_DB),
                         "Does not work for 1 invalid input for common movies")
        self.assertEqual([], get_common_movie('Meryl Streep', 'Inexistent Actor',  self.actor_DB),
                         "Does not work for 1 invalid input for common movies")

    def test_good_movies(self):
        self.assertEqual({'Jaws'}, good_movies(self.ratings_DB),
                         "Getting good movies does not work as expected")
        # when DB changed
        # self.assertEqual({}, good_movies(self.ratings_DB))

    def test_get_common_actors(self):
        self.assertEqual(['Tom Hanks'], get_common_actors('The Post', 'Catch Me If You Can', self.actor_DB),
                         "Getting common actors does not work")
        self.assertEqual([], get_common_actors('Inexistent movie', 'Catch Me If You Can', self.actor_DB),
                         "Getting common actors does not work with error input")
        self.assertEqual([], get_common_actors('The Post', 'Inexistent movie', self.actor_DB),
                         "Getting common actors does not work with error input")
        self.assertEqual([], get_common_actors('Inexistent movie 1', 'Inexistent movie 2', self.actor_DB),
                         "Getting common actors does not work")
        self.assertEqual(['Amy Adams'], get_common_actors('Man of Steel', 'Doubt', self.actor_DB),
                         "Getting common actors does not work")
        self.assertEqual(['Amy Adams'], get_common_actors('Leap Year', 'Leap Year', self.actor_DB),
                         "Getting common actors does not work when movie repeats")

    def test_get_capitalize_format(self):
        self.assertEqual('Meryl Streep', get_capitalize_format('meryl streep'), "Capitalize format does not work")
        self.assertEqual('', get_capitalize_format(''), "Capitalize format does not work")
        self.assertEqual('This Movie', get_capitalize_format('this movie'), "Capitalize format does not work")


if __name__ == '__main__':
    unittest.main()
