import random
import csv
import sqlite3
import re

conn = sqlite3.connect('imdb_movies.db')
cursor = conn.cursor()

def create_movies_table():

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
        
        #clean year and duration columns
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
            
            if len(row[3]) > 0:
                row.append(int(row[3].replace(" min","")))
            else:
                row.append(0)

    cursor.executemany("INSERT INTO movies (title,year,certificate,duration,genre,rating,description,stars,votes,start_year,end_year,runtime) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?);", tuple(to_db))
    conn.commit()

class Movie:
    def __init__(self,id,title,year,certificate,duration,genre,rating,description,stars,votes,start_year,end_year,runtime):
        self.id = id
        self.title = title
        self.year = year
        self.certificate = certificate
        self.duration = duration,
        self.genre = genre
        self.rating = rating
        self.description = description
        self.stars = stars
        self.votes = votes
        self.start_year = start_year
        self.end_year = end_year
        self.runtime = runtime
    
    def pretty_print(self):
        if self.start_year == self.end_year:
            year = self.start_year
        else:
            year = f"{self.start_year} - {self.end_year}"

        if self.runtime == 0:
            runtime = ""
        else:
            runtime = str(self.runtime) + " min"
        print(f"""
Title: {self.title}
Description: {self.description}
Rating: {self.rating}
{year}, {self.certificate}, {self.runtime} min
{self.genre}
        """)

    @classmethod
    def get_filtered_table_random_id(cls,filter=""):
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
            print(id_list)
            print(random_num)
            return id_list[random_num][0]

    @classmethod
    def get_filtered_random_movie(cls):
        random_num = Movie.get_filtered_table_random_id()

        sql = """
            SELECT *
            FROM movies
            WHERE id = ?
        """
        random_movie = cursor.execute(sql,[random_num]).fetchone()
        #fix below to do in loop
        #random_movie_obj = Movie(random_num,random_movie)
        random_movie_obj = Movie(id=random_num,title=random_movie[1],year=random_movie[2],certificate = random_movie[3], duration = random_movie[4], genre = random_movie[5], rating = random_movie[6],description =random_movie[7],stars=random_movie[8],votes=random_movie[9], start_year=random_movie[10],end_year=random_movie[11],runtime = random_movie[12])
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
            rating_filter = "(rating >= 8 AND rating < 9)"
        elif rating == '3':
            rating_filter = "(rating >= 7 AND rating < 8)"
        elif rating == '4':
            rating_filter = "(rating >= 6 AND rating < 7)"
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
        
        filter_string = filter[0]
        for f in filter[1::]:
            filter_string += (" AND " + f)
        
        print(filter_string)
        
        random_num = Movie.get_filtered_table_random_id(filter_string)

        return Movie.get_filtered_random_movie()


    @classmethod
    def advanced_filter_movies(self,title,description,stars):
        pass

def run():
    start_prompt = """
Select an option below:
1. Select a random movie
2. Give my preferences
3. Quit

>>"""

    year_prompt = """
Select a time period below:
1. Pre 1990
2. 1990-2000
3. 2000-2010
4. 2010-2020
5. Post 2020
6. No preference

>>"""

    audience_prompt = """
Select an audience:
1. Kids
2. Mature
3. Explicit
4. No preference

>>"""

    runtime_prompt = """
Select a runtime:
1. 60 min or less
2. 2 hrs or less
3. 2.5hrs or less
4. More than 2.5hrs
5. No preference

>>"""

    genre_prompt = """
Select a genre:
1. Comedy
2. Drama
3. Action
4. Romance
5. Thriller
6. Horror
7. Musical
8. No preference

>>"""

    rating_prompt = """
Select a rating on a scale of 10:
1. 9+
2. 8+
3. 7+
4. 6+
5. Below 6
6. No preference

>>"""

    start = input(start_prompt)

    if start == '1':
        Movie.get_filtered_random_movie().pretty_print()
        run()
    elif start == '2':
        year = input(year_prompt)
        audience = input(audience_prompt)
        runtime = input(runtime_prompt)
        genre = input(genre_prompt)
        rating = input(rating_prompt)

        Movie.basic_filter_movies(year,audience,runtime,genre,rating).pretty_print()
        run()

    else:
        exit()

if __name__ == '__main__':
    run()

#if time can create own table of user watched movies and favorites