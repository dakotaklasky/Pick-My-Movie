import random
import csv
import sqlite3
import re
import prompts

conn = sqlite3.connect('imdb_movies.db')
cursor = conn.cursor()

class Movie:
    def __init__(self,id,title,year,certificate,duration,genre,rating,description,stars,votes,start_year,end_year,runtime):
        self.id = id
        self.title = title
        self.year = year
        self.certificate = certificate
        self.duration = duration
        self.genre = genre
        self.rating = rating
        self.description = description
        self.stars = stars
        self.votes = votes
        self.start_year = start_year
        self.end_year = end_year
        self.runtime = runtime

    @classmethod
    def create_movies_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            year TEXT,
            certificate TEXT,
            duration TEXT,
            genre TEXT,
            rating INTEGER,
            description TEXT,
            stars TEXT,
            votes INTEGER,
            start_year INTEGER,
            end_year INTEGER,
            runtime INTEGER
            )
        """
        cursor.execute(sql)
        with open('./lib/IMDB.csv','r') as fin:
            dr = csv.DictReader(fin)
            to_db = [[i['title'], i['year'],i['certificate'],i['duration'],i['genre'],i['rating'],i['description'],i['stars'],i['votes']] for i in dr]
            
            #clean year column
            for row in to_db:
                re_year = re.findall(r'\d+',row[1])
                if len(re_year) == 1:
                    row.append(int(re_year[0]))
                    row.append(int(re_year[0]))
                elif len(re_year) > 1:
                    row.append(int(re_year[0]))
                    row.append(int(re_year[1]))
                else:
                    row.append(0)
                    row.append(0)

                #clean duration column
                if len(row[3]) > 0:
                    row.append(int(row[3].replace(" min","")))
                else:
                    row.append(0)

                #clean description
                row[6] = row[6].replace('See full summary','')
                row[6] = row[6].replace('»','')

        cursor.executemany("INSERT INTO movies (title,year,certificate,duration,genre,rating,description,stars,votes,start_year,end_year,runtime) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?);", tuple(to_db))
        conn.commit()

    @classmethod
    def create_user_ratings_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS user_ratings (
        id INTEGER PRIMARY KEY,
        username TEXT,
        movie_id INTEGER,
        rating INTEGER)
        """
        cursor.execute(sql)
        conn.commit()
    
    def add_rating_to_table(self,new_username,new_rating):
        sql = f"""
        INSERT INTO user_ratings (username,movie_id,rating) 
        VALUES (?,?,?)
        """
        cursor.execute(sql,(new_username,self.id,new_rating))
        conn.commit()


    
    def pretty_print(self):
        if self.start_year == self.end_year:
            year = self.start_year
        else:
            year = f"{self.start_year} - {self.end_year}"

        if self.runtime == 0:
            runtime = ""
        else:
            runtime = ", " + str(self.runtime) + " min"

        if self.certificate == "":
            certificate = ""
        else:
            certificate = ", " + self.certificate

        print(f"""
Title: {self.title}
Description: {self.description}
Rating: {self.rating}
{year}{certificate}{runtime}
{self.genre}
        """)

    @classmethod
    def get_filtered_table_random_id(cls,filter=""):
        print(filter)
        if filter == "":
            sql_count = "SELECT COUNT(*) FROM movies"
            sql_query = "SELECT id FROM movies"
        else: 
            sql_count = f"SELECT COUNT(*) FROM movies WHERE {filter}"
            sql_query = f"SELECT id FROM movies WHERE {filter}"
        table_len = cursor.execute(sql_count).fetchone()[0]

        if table_len == 0:
            raise IndexError("There are no results with the given filters, please try again.")

        else:
            random_num = random.randint(0,table_len-1)
            id_list = cursor.execute(sql_query).fetchall()
            return id_list[random_num][0]

    @classmethod
    def get_filtered_random_movie(cls,random_num):

        sql = """
            SELECT *
            FROM movies
            WHERE id = ?
        """
        random_movie = cursor.execute(sql,[random_num]).fetchone()
        random_movie_obj = Movie(id=random_movie[0],title=random_movie[1],year=random_movie[2],certificate = random_movie[3],\
        duration = random_movie[4], genre = random_movie[5], rating = random_movie[6],description =random_movie[7],\
        stars=random_movie[8],votes=random_movie[9], start_year=random_movie[10],end_year=random_movie[11],runtime = random_movie[12])
        return random_movie_obj

  
    @classmethod
    def basic_filter_movies(self,year,certificate,runtime,genre,rating):

        #year filter
        if year == '1':
            year_filter = "(end_year <= 1990)"
        elif year =='2':
            year_filter = "((start_year > 1990 AND start_year <= 2000) OR (1990 >end_year AND end_year <= 2000))"
        elif year =='3':
            year_filter = "((start_year > 2000 AND start_year <= 2010) OR (end_year > 2000 AND end_year <= 2010))"
        elif year=='4':
            year_filter = "((start_year > 2010 AND start_year <= 2020) OR (end_year > 2010 AND end_year <= 2020))"
        elif year=='5':
            year_filter = "(end_year > 2020)"
        else:
            year_filter = ""
            
        #certificate filter
        if certificate == '1':
            certificate_filter = '(certificate = "TV-PG" OR certificate = "PG" OR certificate = "TV-Y7-FV" OR certificate = "TV-G" OR \
            certificate = "G" OR certificate = "12" OR certificate = "TV-Y" OR certificate = "TV-Y7" OR certificate = "E10+")'
        elif certificate == '2':
            certificate_filter = "(certificate = 'TV-14' OR certificate = 'PG-13')"
        elif certificate == '3':
            certificate_filter = '(certificate = "TV-MA" OR certificate = "NC-17" OR certificate = "R" OR certificate = "M" OR certificate ="MA-17")'
        else:
            certificate_filter = ""

        #runtime filter
        if runtime == '1':
            runtime_filter = "(runtime <= 60)"
        elif runtime == '2':
            runtime_filter = "(runtime > 60 AND runtime <= 120)"
        elif runtime == '3':
            runtime_filter = "(runtime > 120 AND runtime <= 150)"
        elif runtime == '4':
            runtime_filter = "(runtime > 150)"
        else:
            runtime_filter = ""

        #genre filter
        if genre == '1':
            genre_filter = "(genre LIKE '%Comedy%')"
        elif genre == '2':
            genre_filter = "(genre LIKE '%Drama%')"
        elif genre == '3':
            genre_filter = "(genre LIKE '%Action%')"
        elif genre == '4':
            genre_filter = "(genre LIKE '%Romance%')"
        elif genre == '5':
            genre_filter = "(genre LIKE '%Thriller%')"
        elif genre == '6':
            genre_filter = "(genre LIKE '%Horror%')"
        elif genre == '7':
            genre_filter = "(genre LIKE '%Musical%')"
        else:
            genre_filter = ""
        
        #rating filter
        if rating == '1':
            rating_filter = "(rating >= 9)"
        elif rating == '2':
            rating_filter = "(rating >= 8)"
        elif rating == '3':
            rating_filter = "(rating >= 7)"
        elif rating == '4':
            rating_filter = "(rating >= 6)"
        elif rating == '5':
            rating_filter = "(rating < 6)"
        else:
            rating_filter = ""

        filter = []
        if len(year_filter) > 0:
            filter.append(year_filter)
        if len(certificate_filter)> 0:
            filter.append(certificate_filter)
        if len(runtime_filter)> 0:
            filter.append(runtime_filter)
        if len(genre_filter)> 0:
            filter.append(genre_filter)
        if len(rating_filter)> 0:
            filter.append(rating_filter)
        
        if len(filter) > 0:
            filter_string = filter[0]
            for f in filter[1::]:
                filter_string += (" AND " + f)
        else:
            filter_string = ""

        return filter_string


    @classmethod
    def advanced_filter_movies(self,title,description,stars):
        #make not case sensitive
        filter = []
        if title != '0':
            filter.append(f"(LOWER(title) LIKE LOWER('%{title}%'))")
        if description != '0':
            filter.append(f"(LOWER(description) LIKE LOWER('%{description}%'))")
        if stars != '0':
            filter.append(f"(LOWER(stars) LIKE LOWER('%{stars}%'))")
        
        if len(filter) == 0:
            advanced_filter_string = ""
        else:
            advanced_filter_string = filter[0]
            if len(filter) > 1:
                for x in filter[1::]:
                    advanced_filter_string += ' AND ' + x
        
        return advanced_filter_string
    

    def add_log(self):

  
        username = input(username_prompt)
        rating = input(my_rating_prompt)
        self.add_rating_to_table(username,rating)

def run():

    start = input(start_prompt)

    if start == '1':
        my_movie = Movie.get_filtered_random_movie(Movie.get_filtered_table_random_id())
        my_movie.pretty_print()
        log = input(log_prompt)
        if log == 'y':
            my_movie.add_log()

        run()
    elif start == '2':
        year = input(year_prompt)
        audience = input(audience_prompt)
        runtime = input(runtime_prompt)
        genre = input(genre_prompt)
        rating = input(rating_prompt)

        advanced_filter = input(advanced_filter_prompt)

        if advanced_filter == '1':
            title = input(title_prompt)
            description = input(description_prompt)
            stars = input(stars_prompt)
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

        log = input(log_prompt)
        if log == 'y':
            random_movie.add_log()

        run()
    
    elif start == '3':
        #log movie
        movie_title = input(log_title_prompt)
        sql = f"""
        SELECT id, title
        FROM movies
        WHERE LOWER(title) LIKE LOWER('%{movie_title}%')
        """
        print(cursor.execute(sql).fetchall())

        select_movie = input(movie_selection_prompt)

        sql_movie_selection = f"""
        SELECT *
        FROM movies
        WHERE LOWER(title) LIKE LOWER('%{movie_title}%') AND id = {select_movie}
        """

        movie_selection = cursor.execute(sql_movie_selection).fetchone()
        print(movie_selection)

        movie_to_rate = Movie(id=movie_selection[0],title=movie_selection[1],year=movie_selection[2],certificate = movie_selection[3],\
        duration = movie_selection[4], genre = movie_selection[5], rating = movie_selection[6],description =movie_selection[7],\
        stars=movie_selection[8],votes=movie_selection[9], start_year=movie_selection[10],end_year=movie_selection[11],runtime = movie_selection[12])

        username = input(username_prompt)

        rating = input(my_rating_prompt)

        movie_to_rate.add_rating_to_table(username,rating)

        run()
    
    elif start =='4':
        #pull up list of movies
        username = input(username_prompt)
        #query user_ratings table for specific username and JOIN with movies table
        sql = f"""
        SELECT movies.title,user_ratings.rating
        FROM user_ratings
        INNER JOIN movies ON user_ratings.movie_id = movies.id
        WHERE username = '{username}'
        """

        my_movies = cursor.execute(sql).fetchall()

        
        if len(my_movies) == 0:
            raise ValueError("Please enter an existing username or log a movie with a new username")

        else:
            print(my_movies) # make pretty print

        run()

    else:
        exit()


if __name__ == '__main__':
    #run create tables if doesn't exist?
    run()
    

#what if wrong inputs are given??
#format my movies better and list from log movie
#refactor to have cli.py and Movie.py


