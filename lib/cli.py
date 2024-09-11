# lib/cli.py
from Movie import Movie
import prompts as p
from tabulate import tabulate

def run():
    start = input(p.start_prompt)
    #show random movie with no filters
    if start == '1':
        my_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id())
        my_movie.pretty_print()
        log = input(p.log_prompt)
        if log == 'y':
            username = input(p.username_prompt)
            rating = input(p.my_rating_prompt)
            my_movie.add_rating_to_table(username,rating)
        run()
    
    #return random movie with given filters
    elif start == '2':
        year = input(p.year_prompt)
        audience = input(p.audience_prompt)
        runtime = input(p.runtime_prompt)
        genre = input(p.genre_prompt)
        rating = input(p.rating_prompt)

        advanced_filter = input(p.advanced_filter_prompt)

        if advanced_filter == '1':
            title = input(p.title_prompt)
            description = input(p.description_prompt)
            stars = input(p.stars_prompt)
            advanced_filter_string = Movie.advanced_filter_movies(title,description,stars)
        else:
            advanced_filter_string = ""

        basic_filter_string = Movie.basic_filter_movies(year,audience,runtime,genre,rating)
        
        if len(advanced_filter_string) > 0 and len(basic_filter_string) > 0:
            random_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id(basic_filter_string + ' AND ' + advanced_filter_string))
        elif len(advanced_filter_string) > 0 and len(basic_filter_string) == 0:
            random_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id(advanced_filter_string))
        elif len(advanced_filter_string) == 0 and len(basic_filter_string) > 0:
            random_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id(basic_filter_string))
        else:
            random_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id())

        
        random_movie.pretty_print()

        log = input(p.log_prompt)
        if log == 'y':
            username = input(p.username_prompt)
            rating = input(p.my_rating_prompt)
            random_movie.add_rating_to_table(username,rating)

        run()
    
    #log a movie with given word or phrase in title
    elif start == '3':
        movie_title = input(p.log_title_prompt)
        filtered_movies = Movie.get_movies_from_title(movie_title)

        if len(filtered_movies) == 0:
            raise ValueError("There are no results that match. Please use a different key word")
        else:
            print(tabulate(filtered_movies, headers=["Id","Title"], tablefmt="grid"))

        select_movie = input(p.movie_selection_prompt)
        movie_selection = Movie.select_movie_id(movie_title,select_movie)

        movie_to_rate = Movie(id=movie_selection[0],title=movie_selection[1],year=movie_selection[2],certificate = movie_selection[3],\
        duration = movie_selection[4], genre = movie_selection[5], rating = movie_selection[6],description =movie_selection[7],\
        stars=movie_selection[8],votes=movie_selection[9], start_year=movie_selection[10],end_year=movie_selection[11],runtime = movie_selection[12])

        username = input(p.username_prompt)
        rating = input(p.my_rating_prompt)
        movie_to_rate.add_rating_to_table(username,rating)
        run()
    
    #show all rated movies for given username
    elif start =='4':
        username = input(p.username_prompt)
        my_movies = Movie.get_user_ratings(username)
        
        if len(my_movies) == 0:
            raise ValueError("Please enter an existing username or log a movie with a new username")
        else:
            print(tabulate(my_movies, headers=["Rating","Title"], tablefmt="grid"))

        run()
    else:
        exit()

if __name__ == '__main__':
    run()

#rename repo and python project
