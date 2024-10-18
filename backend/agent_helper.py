examples = [
    {
        "input": "Select Oscar-winning movies",
        "query": '''
            SELECT netflix_title, movie_id, title_type, award
            FROM netflix_titles
            WHERE award LIKE '%Oscar%' AND title_type = 'Movie'
            '''
    },
    {
        "input": "Select movies that belong to multiple genres",
        "query": '''
            SELECT netflix_title, movie_id, title_type, genres
            FROM netflix_titles
            WHERE array_length(genres, 1) > 1 AND title_type = 'Movie'
            '''
    },
    {
        "input": "Select the top viewed movies from January to June",
        "query": '''
            SELECT netflix_title, movie_id, title_type, hours_viewed_jan_jun
            FROM netflix_titles
            WHERE title_type = 'Movie'
            ORDER BY hours_viewed_jan_jun DESC
            LIMIT 10
            '''
    },
    {
        "input": "Select movies released before the year 2000",
        "query": '''
            SELECT netflix_title, movie_id, title_type
            FROM netflix_titles
            WHERE EXTRACT(YEAR FROM release_date) < 2000 AND title_type = 'Movie'
            '''
    },
    {
        "input": "Select movies with a runtime greater than 2 hours",
        "query": '''
            SELECT netflix_title, movie_id, title_type, runtime
            FROM netflix_titles
            WHERE runtime > 7200 AND title_type = 'Movie'  -- Runtime in seconds (2 hours = 7200 seconds)
            '''
    },
    {
        "input": "Select movies available globally",
        "query": '''
            SELECT netflix_title, movie_id, title_type
            FROM netflix_titles
            WHERE available_globally = True AND title_type = 'Movie'
            '''
    },
    {
        "input": "Select movies projected on film",
        "query": '''
            SELECT netflix_title, movie_id, title_type, printed_formats
            FROM netflix_titles
            WHERE printed_formats && ARRAY['35mm Film', '8mm Film', '70mm Film', 'Super 35mm Film', 'Super 8mm Film', '16mm Film', 'IMAX 70mm Film']::varchar[] AND title_type = 'Movie'
            '''
    },
    {
        "input": "Select movies projected digitally",
        "query": '''
            SELECT netflix_title, movie_id, title_type, printed_formats
            FROM netflix_titles
            WHERE printed_formats && ARRAY['DCP', 'DCP (3D Version)', 'DCP 2K', 'DCP 4K']::varchar[] AND title_type = 'Movie'
            '''
    },
    {
        "input": "Identify titles with high worldwide gross but low ratings",
        "query": '''
            SELECT netflix_title, movie_id, title_type, aggregate_rating,
                   (COALESCE(worldwide_gross_amount, 0) - COALESCE(budget_amount, 0)) AS profit
            FROM netflix_titles
            WHERE aggregate_rating < 5.0  -- Low rating threshold
            AND (COALESCE(worldwide_gross_amount, 0) - COALESCE(budget_amount, 0)) > 1000000  -- High profit threshold
            ORDER BY profit DESC
            '''
    },
    {
        "input": "Calculate ROI for each title",
        "query": '''
            SELECT netflix_title, movie_id, title_type,
                   (COALESCE(worldwide_gross_amount, 0) - COALESCE(budget_amount, 0)) / NULLIF(budget_amount, 0) * 100 AS roi_percentage
            FROM netflix_titles
            WHERE budget_amount IS NOT NULL AND worldwide_gross_amount IS NOT NULL
            ORDER BY roi_percentage DESC
            '''
    },
    {
        "input": "Calculate cost per view for each title",
        "query": '''
            SELECT netflix_title, movie_id, title_type,
                   budget_amount / NULLIF(total_hours_viewed, 0) AS cost_per_view
            FROM netflix_titles
            WHERE budget_amount IS NOT NULL AND total_hours_viewed > 0
            ORDER BY cost_per_view ASC
            '''
    },
    {
        "input": "Rank U.S. movies by their audience engagement relative to their profit.",
        "query": '''
            SELECT netflix_title, movie_id, title_type, budget_amount, worldwide_gross_amount, total_hours_viewed,
                   ((worldwide_gross_amount - budget_amount) * total_hours_viewed) / NULLIF(budget_amount, 0) AS engagement_roi
            FROM netflix_titles
            WHERE budget_amount > 0
              AND worldwide_gross_amount > 0
              AND total_hours_viewed > 0
              AND 'United States' = ANY(countries_of_origin)
            ORDER BY engagement_roi DESC;
            '''
    },
    {
        "input": "Rank U.S. movies by profit-weighted audience engagement efficiency.",
        "query": '''
            SELECT netflix_title, movie_id, title_type, budget_amount, worldwide_gross_amount, total_hours_viewed,
                   (total_hours_viewed * (worldwide_gross_amount - budget_amount)) /
                   NULLIF((worldwide_gross_amount - budget_amount) + budget_amount, 0) AS profit_weighted_engagement_roi
            FROM netflix_titles
            WHERE budget_amount > 0
              AND worldwide_gross_amount > 0
              AND total_hours_viewed > 0
              AND 'United States' = ANY(countries_of_origin)
            ORDER BY profit_weighted_engagement_roi DESC;
            '''
    },    
    {
        "input": "Calculate budget to rating efficiency",
        "query": '''
            SELECT netflix_title, movie_id, title_type, budget_amount, aggregate_rating,
                   (aggregate_rating / NULLIF(budget_amount, 0)) AS budget_to_rating_efficiency
            FROM netflix_titles
            WHERE budget_amount IS NOT NULL
              AND budget_amount > 0
              AND aggregate_rating IS NOT NULL
            ORDER BY budget_to_rating_efficiency DESC;
            '''
    },
    {
        "input": "Find low-budget, critically acclaimed U.S. films with low viewership.",
        "query": '''
            WITH budget_ranges AS (
                SELECT movie_id, netflix_title, total_hours_viewed, budget_amount, aggregate_rating
                FROM netflix_titles
                WHERE aggregate_rating >= 8.0 AND budget_amount < 5000000 AND 'United States' = ANY(countries_of_origin)
            )
            SELECT netflix_title, total_hours_viewed, budget_amount
            FROM budget_ranges
            WHERE total_hours_viewed < (SELECT AVG(total_hours_viewed) FROM budget_ranges)
            ORDER BY total_hours_viewed ASC;
        '''
    },
    {
        "input": "Names of US origin directors who make profitable movies in action genre.",
        "query": '''
            SELECT DISTINCT n.name_id, n.name
            FROM netflix_names n
            JOIN names_movies nm ON n.name_id = nm.name_id
            JOIN netflix_titles t ON nm.movie_id = t.movie_id
            WHERE nm.role = 'Director'
            AND 'United States' = ANY(t.countries_of_origin)
            AND 'Action' = ANY(t.genres)
            AND (t.worldwide_gross_amount - t.budget_amount) > 0;
'''
    },
    {
        "input": "Rank U.S. movies by budget as a predictor of performance.",
        "query": '''
            WITH budget_ranges AS (
                SELECT movie_id, netflix_title, budget_amount, total_hours_viewed
                FROM netflix_titles
                WHERE 'United States' = ANY(countries_of_origin)
            )
            SELECT netflix_title, budget_amount, total_hours_viewed
            FROM budget_ranges
            ORDER BY budget_amount DESC;
        '''
    },    
    {
        "input": "Select profitable movies.",
        "query": '''
            SELECT
                movie_id,
                netflix_title,
                budget_amount,
                worldwide_gross_amount,
                (worldwide_gross_amount - budget_amount) AS profit
            FROM
                netflix_titles
            WHERE
                worldwide_gross_amount > budget_amount
                AND budget_amount IS NOT NULL
                AND worldwide_gross_amount IS NOT NULL
            ORDER BY
                profit DESC;
        '''
    },
    {
        "input": "List individual movie genres with the highest box office ROI, grouped by budget range and release decade for US movies. For each group, include up to 3 movie examples, and only consider genres with at least 3 occurrences.",
        "query": '''
            WITH budget_ranges AS (
                SELECT movie_id, netflix_title, budget_amount, worldwide_gross_amount, total_hours_viewed,
                       ((worldwide_gross_amount - budget_amount) * total_hours_viewed) / NULLIF(budget_amount, 0) AS engagement_roi,
                       genres,
                       (FLOOR(EXTRACT(YEAR FROM release_date) / 10) * 10) AS release_decade  -- Correct calculation for decade
                FROM netflix_titles
                WHERE budget_amount IS NOT NULL
                  AND worldwide_gross_amount IS NOT NULL
                  AND total_hours_viewed > 0
                  AND 'United States' = ANY(countries_of_origin)
            ),
            genre_roi AS (
                SELECT unnest(genres) AS genre,
                       CASE
                           WHEN budget_amount < 1000000 THEN 'Micro Budget'
                           WHEN budget_amount >= 1000000 AND budget_amount < 5000000 THEN 'Low Budget'
                           WHEN budget_amount >= 5000000 AND budget_amount < 30000000 THEN 'Mid-Budget'
                           WHEN budget_amount >= 30000000 AND budget_amount < 100000000 THEN 'High Budget'
                           ELSE 'Blockbuster Budget'
                       END AS budget_range,
                       release_decade,
                       COUNT(*) AS count,
                       AVG(engagement_roi) AS avg_roi
                FROM budget_ranges
                GROUP BY genre, budget_range, release_decade
                HAVING COUNT(*) >= 3
            ),
            genre_examples AS (
                SELECT br.movie_id, br.netflix_title, br.budget_amount, br.worldwide_gross_amount, br.total_hours_viewed,
                       br.engagement_roi, unnest(br.genres) AS genre,
                       CASE
                           WHEN br.budget_amount < 1000000 THEN 'Micro Budget'
                           WHEN br.budget_amount >= 1000000 AND br.budget_amount < 5000000 THEN 'Low Budget'
                           WHEN br.budget_amount >= 5000000 AND br.budget_amount < 30000000 THEN 'Mid-Budget'
                           WHEN br.budget_amount >= 30000000 AND br.budget_amount < 100000000 THEN 'High Budget'
                           ELSE 'Blockbuster Budget'
                       END AS budget_range,
                       br.release_decade,
                       ROW_NUMBER() OVER (PARTITION BY unnest(br.genres),
                                          CASE
                                              WHEN br.budget_amount < 1000000 THEN 'Micro Budget'
                                              WHEN br.budget_amount >= 1000000 AND br.budget_amount < 5000000 THEN 'Low Budget'
                                              WHEN br.budget_amount >= 5000000 AND br.budget_amount < 30000000 THEN 'Mid-Budget'
                                              WHEN br.budget_amount >= 30000000 AND br.budget_amount < 100000000 THEN 'High Budget'
                                              ELSE 'Blockbuster Budget'
                                          END,
                                          br.release_decade
                                          ORDER BY br.engagement_roi DESC) AS rn
                FROM budget_ranges br
            )
            SELECT gr.genre, gr.budget_range, gr.release_decade, gr.avg_roi, ARRAY_AGG(ge.netflix_title) AS movie_examples
            FROM genre_roi gr
            JOIN genre_examples ge ON gr.genre = ge.genre AND gr.budget_range = ge.budget_range AND gr.release_decade = ge.release_decade
            WHERE ge.rn <= 3
            GROUP BY gr.genre, gr.budget_range, gr.release_decade, gr.avg_roi
            ORDER BY gr.avg_roi DESC ;
        '''
    },
    {
        "input": "List the top movie genres based on average streaming performance (total hours viewed) in the United States, grouped by budget range and release decade. Only include genres with at least 25 movies in each group, and provide 3 example movies with the best streaming performance for each genre, budget range, and release decade.",
        "query": '''
            WITH budget_ranges AS (
                SELECT movie_id, netflix_title, genres, budget_amount, total_hours_viewed,
                       (total_hours_viewed) AS streaming_performance,
                       (FLOOR(EXTRACT(YEAR FROM release_date) / 10) * 10) AS release_decade
                FROM netflix_titles
                WHERE budget_amount IS NOT NULL
                  AND total_hours_viewed > 0
                  AND 'United States' = ANY(countries_of_origin)
                  AND title_type = 'Movie'
            ),
            genre_performance AS (
                SELECT unnest(genres) AS genre,
                       CASE
                           WHEN budget_amount < 1000000 THEN 'Micro Budget'
                           WHEN budget_amount >= 1000000 AND budget_amount < 5000000 THEN 'Low Budget'
                           WHEN budget_amount >= 5000000 AND budget_amount < 30000000 THEN 'Mid-Budget'
                           WHEN budget_amount >= 30000000 AND budget_amount < 100000000 THEN 'High Budget'
                           ELSE 'Blockbuster Budget'
                       END AS budget_range,
                       release_decade,
                       COUNT(*) AS count,
                       AVG(streaming_performance) AS avg_streaming_performance
                FROM budget_ranges
                GROUP BY genre, budget_range, release_decade
                HAVING COUNT(*) >= 25
            ),
            genre_examples AS (
                SELECT br.movie_id, br.netflix_title, br.budget_amount, br.total_hours_viewed,
                       br.streaming_performance, unnest(br.genres) AS genre,
                       CASE
                           WHEN br.budget_amount < 1000000 THEN 'Micro Budget'
                           WHEN br.budget_amount >= 1000000 AND br.budget_amount < 5000000 THEN 'Low Budget'
                           WHEN br.budget_amount >= 5000000 AND br.budget_amount < 30000000 THEN 'Mid-Budget'
                           WHEN br.budget_amount >= 30000000 AND br.budget_amount < 100000000 THEN 'High Budget'
                           ELSE 'Blockbuster Budget'
                       END AS budget_range,
                       br.release_decade,
                       ROW_NUMBER() OVER (PARTITION BY unnest(br.genres),
                                          CASE
                                              WHEN br.budget_amount < 1000000 THEN 'Micro Budget'
                                              WHEN br.budget_amount >= 1000000 AND br.budget_amount < 5000000 THEN 'Low Budget'
                                              WHEN br.budget_amount >= 5000000 AND br.budget_amount < 30000000 THEN 'Mid-Budget'
                                              WHEN br.budget_amount >= 30000000 AND br.budget_amount < 100000000 THEN 'High Budget'
                                              ELSE 'Blockbuster Budget'
                                          END,
                                          br.release_decade
                                          ORDER BY br.streaming_performance DESC) AS rn
                FROM budget_ranges br
            )
            SELECT gr.genre, gr.budget_range, gr.release_decade, ROUND(gr.avg_streaming_performance), ARRAY_AGG(ge.netflix_title) AS movie_examples
            FROM genre_performance gr
            JOIN genre_examples ge ON gr.genre = ge.genre AND gr.budget_range = ge.budget_range AND gr.release_decade = ge.release_decade
            WHERE ge.rn <= 3
            GROUP BY gr.genre, gr.budget_range, gr.release_decade, gr.avg_streaming_performance
            ORDER BY gr.avg_streaming_performance DESC;
        '''
    },    
]

system_prefix = """You are an agent designed to interact with a SQL database.

Clean the input when asked for a disctinct title type / title types. Valid title types: TV Short, Podcast Episode, TV Episode, Video, TV Series, Video Game, TV Mini Series, Movie, Podcast Series, TV Movie, TV Special, Short, Music Video.
Clean the input when asked for a disctinct genre / genres. Valid genres: Reality-TV, Comedy, Western, War, Romance, Biography, Documentary, News, Talk-Show, Musical, Thriller, Game-Show, Family, Music, Short, Crime, Drama, Mystery, Sci-Fi, Fantasy, Adventure, Action, Animation, Sport, Horror, Adult, History.
Clean the input when asked for a disctinct certificate / certificates. Valid certificates: 18+, TV-Y, 12, TV-Y7-FV, TV-G, TV-MA, TV-Y7, 13+, 16+, M/PG, PG, TV-PG, R, Unrated, M, X, TV-14, G, NC-17, PG-13.
Clean the input when asked about runtime. runtime should be in seconds.
Clean the input when asked for a place. choose the closest country/countries based on user query. User can ask about a country / region / city / state / language. Try to be precise when choosing. Valid countries: Uganda, Angola, Zambia, Belgium, Taiwan, Cyprus, Albania, Guadeloupe, Denmark, Kuwait, Jordan, Bhutan, Malaysia, Iceland, Turkey, North Korea, Pakistan, Panama, The Democratic Republic of Congo, Burkina Faso, Faroe Islands, Bangladesh, Algeria, Serbia, Libya, Philippines, Uruguay, Egypt, Ethiopia, Australia, Vatican, Liechtenstein, Malta, Somalia, Saudi Arabia, Serbia and Montenegro, United Arab Emirates, Slovenia, Ukraine, Latvia, Tunisia, Belarus, Estonia, Israel, United States, Andorra, Nigeria, Canada, Greece, Hong Kong, South Korea, Occupied Palestinian Territory, West Germany, Poland, Thailand, Montenegro, Tanzania, Kenya, Morocco, Romania, Luxembourg, Czech Republic, Chile, North Macedonia, Bahrain, Lithuania, Brazil, Indonesia, Bahamas, East Germany, China, Lebanon, Netherlands, Spain, Portugal, Colombia, Bosnia and Herzegovina, Yugoslavia, Russia, Mauritius, Cambodia, Isle of Man, Italy, Switzerland, Germany, Kazakhstan, Myanmar, France, Bermuda, Antarctica, Paraguay, Monaco, Ghana, Iran, Mauritania, Qatar, Chad, Peru, Iraq, New Zealand, Austria, Bulgaria, Guinea, United Kingdom, Ireland, Vietnam, Guatemala, Cayman Islands, Senegal, Argentina, India, Nepal, Soviet Union, Cameroon, Malawi, Niger, Zimbabwe, Japan, Lesotho, Dominican Republic, Hungary, Slovakia, South Africa, Venezuela, Croatia, Botswana, Puerto Rico, Czechoslovakia, Norway, Sweden, Laos, Ecuador, Mexico, Syria, Singapore, Finland, Georgia, Afghanistan.
Clean the input when asked for a disctinct aspect ratio / aspect ratios. Valid ratios: 2.47:1, 3.00:1, 1.19:1, 1.75:1, 1.9:1, 2.38:1, 2.85:1, 2.28:1, 2.39:1, 1.90:1, 16:94, 4:3, 1.16:1, 2.75:1, 2.35:1, 2.4:1, 2.66:1, 2:39:1, 1.91:1, 2.2:1, 17:9, 1.77:1, 2:00:1, 1.44:1, 2.40:1, 2.16:1, 2.1:1, 1.85:1, 1.37:1, 1.33:1, 2.20:1, 1.79:1, 2.58:1, 0.60:1, 2.10:1, 2:25:1, 2:55, 1.50:1, 1.96:1, 2.76:1, 1.60:1, 2:1, 2.25:1, 16:9, 21:9, 1.14:1, 2.41:1, 1.00:1, 1.88:1, 2.77:1, 2:39, 2.22:1, 1.89:1, 1.74:1, 2.11:1, 2.00:1, 1.56:1, 1.43:1, 17:94, 1.78:1, 2.30:1, 2.55:1, 7.17:1, 5.95:1, 1.55:1, 1:1, 1.48:1, 1.40:1, 1.92:1, 2.0:1, 14:9, 1.66:1, 9:16, 2.33:1.
Clean the input when asked for a disctinct sound mix / sound mixes. Valid sound mixes: IMAX 6-Track, D-Cinema 48kHz Dolby Surround 7.1, Ultra Stereo, Dolby Surround 5.1, Datasat, LC-Concept Digital Sound, D-Cinema 48kHz 5.1, DTS 70 mm, Dolby, D-Cinema 48kHz 7.1, D-Cinema 96kHz 7.1, CDS, Auro 11.1, Stereo, Sensurround, DTS-Stereo, Dolby Surround 7.1, Auro 9.1, 6-Track Stereo, 12-Track Digital Sound, DTS-ES, Dolby SR, Dolby Digital EX, SDDS, 4-Track Stereo, DTS:X, D-Cinema 96kHz Dolby Surround 7.1, Dolby Digital, 70 mm 6-Track, Mono, 3 Channel Stereo, IMAX 5.0, D-Cinema 96kHz 5.1, Dolby Atmos, Dolby Stereo, DTS.
Clean the input when asked for a disctinct coloration / colorations. Valid colorations: Color, Black and White.
Clean the input when asked for a distinct printed format / printed formats. Valid printed formats: DCP, 16mm Film, 35mm Film, DCP 4K, IMAX Digital, 8mm Film, Super 8mm Film, DCP (3D Version), 70mm Film, Super 35mm Film, DCP 2K, IMAX 70mm Film. DCP is Digital Cinema Package.
Clean the input when asked for a distnct award / awards. Valid award: BAFTA Film Award, BAFTA TV Award, Primetime Emmy, BAFTA Children''s Award, Oscar, Governor''s Award.

When querying fields with numerical values, always skip rows with NULL values.

Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
When matching any text / name fields, USE fuzzy matching with an appropriate threshold for robustness.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
On budgets: Micro Budget: Less than $1 million, Low Budget: $1 million - $5 million, Mid-Budget: $5 million - $30 million, High Budget: $30 million - $100 million, Blockbuster Budget: Over $100 million
If a query is returned empty. Don't hallucinate or search the web. Just say you don't have info on it.
When asking for qualititaive metrics like popularity you can use the web for reference.
don't search keywords column when asked about plot and related info.

Distinct roles that are avaialbe in names_movies table: Actor, Actress, Cinematographer, Composer, Director, Editor, Producer, Self, Writer


If you need to find a movie_id based on plot / plot detail / descriptor, you must ALWAYS first look up the plot using the "get_movie_ids" tool! Then you must use those found movie_id to filter the netflix_titles table.
If you need to find the appropriate proper noun on a camera model, sound mix, or processes, you must first look up the noun using the "get_technical_details" tool! Then you can filter the netflix_titles table.
If you need to find a name_id for an actor / director / writer based on bio / backstory / descriptor, you must ALWAYS first look up the plot using the "get_name_ids" tool! Then you must use those found name_id to filter the netflix_titles / names_movies / netflix_names tables.

When asking for info on cameras, search the web because you only have a list of cameras. And you don't have info on them.
When calculating numerical values, round them to the closest integer.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.


Here are some examples of user inputs and their corresponding SQL queries:"""


