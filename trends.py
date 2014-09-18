"""Visualizing Twitter Sentiment Across America"""

from database import make_database, add_value, get_keys, get_values, get_value_from_key, get_items, get_len
from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


###################################
# Phase 1: The Feelings in Tweets #
###################################

# The tweet abstract data type, implemented as a list.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python list.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return [text, time, lat, lon]

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    return tweet[0]

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet[1]

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet[2], tweet[3])

# The tweet abstract data type, implemented as a function.

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> latitude(tweet_location_fn(t))
    38
    """
    "*** YOUR CODE HERE ***"
    # Please don't call make_tweet in your solution
    def make_tweet_fn_key_return(key):
        assert key == 'text' or key == 'time' or key == 'lat' or key == 'lon'
        if key == 'text':
            return text
        elif key == 'time':
            return time
        elif key == 'lat':
            return lat
        elif key == 'lon':
            return lon
        else:
            pass
    return make_tweet_fn_key_return

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))

def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    for i in range(len(text)):
        if text[i] not in ascii_letters:
            text = str.replace(text, text[i], ' ')
    return text.split()

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal sentiment value'
    "*** YOUR CODE HERE ***"
    return [value]

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    if s[0] is None:
        return False
    else:
        return True

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return s[0]

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    # You may change any of the lines below.
    #average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    #return average
    words_of_tweet = tweet_words(tweet)
    sent_list = []
    for word in words_of_tweet:
        if has_sentiment(get_word_sentiment(word)):
            sent_list.append(sentiment_value(get_word_sentiment(word)))
        else:
            pass
    if len(sent_list) == 0 or sum(sent_list) == 0:
        return make_sentiment(None)
    else:
        return make_sentiment(sum(sent_list)/len(sent_list))


#################################
# Phase 2: The Geometry of Maps #
#################################

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> round5 = lambda x: round(x, 5) # Rounds floats to 5 digits
    >>> list(map(round5, find_centroid(triangle)))
    [3.0, 2.0, 6.0]
    >>> list(map(round5, find_centroid([p1, p3, p2, p1])))
    [3.0, 2.0, 6.0]
    >>> list(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    [1.0, 2.0, 0.0]
    """
    "*** YOUR CODE HERE ***"
    cx_minus_coefficient = 0
    cy_minus_coefficient = 0
    double_area = 0
    for i in range(len(polygon)):
        if i <= (len(polygon) - 2):
            double_area += (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i]))
    area = double_area * (1/2)
    if area == 0:               #a zero area polygon
        cx = latitude(polygon[0])
        cy = longitude(polygon[0])
    else:
        for i in range(len(polygon)):
            if i <= (len(polygon) - 2):
                cx_minus_coefficient += (latitude(polygon[i]) + latitude(polygon[i + 1])) * (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i + 1])*longitude(polygon[i]))
        cx = (1/(6*area)) * cx_minus_coefficient
        for i in range(len(polygon)):
            if i <= (len(polygon) - 2):
                cy_minus_coefficient += (longitude(polygon[i]) + longitude(polygon[i + 1])) * (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i + 1])*longitude(polygon[i]))
        cy = (1/(6*area)) * cy_minus_coefficient
    return cx, cy, abs(area)


def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(get_value_from_key(us_states,'CA'))  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(get_value_from_key(us_states, 'HI'))  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    "*** YOUR CODE HERE ***"
    cx_num = 0
    cy_num = 0
    cx_cy_denom = 0
    for i in range(len(polygons)):
        cx_num += list(find_centroid(polygons[i]))[0] * list(find_centroid(polygons[i]))[2]
        cy_num += list(find_centroid(polygons[i]))[1] * list(find_centroid(polygons[i]))[2]
        cx_cy_denom += list(find_centroid(polygons[i]))[2]
    cx = cx_num/cx_cy_denom
    cy = cy_num/cx_cy_denom
    return make_position(cx, cy)


###################################
# Phase 3: The Mood of the Nation #
###################################

def closest_state_to_tweet(tweet):
    #takes in a tweet and returns the two-letter state postal code for the
    #closest state center to that tweet
    database = us_states
    new_dynamic_database = make_database()
    list_of_keys = get_keys(database)
    for i in range(get_len(database)):
        dist = geo_distance(tweet_location(tweet), find_state_center(get_value_from_key(database, list_of_keys[i])))
        new_dynamic_database = add_value(new_dynamic_database, list_of_keys[i], dist)
    distances_from_states = get_values(new_dynamic_database)
    closest_state = ""
    for i in range(get_len(new_dynamic_database)):
        if get_value_from_key(new_dynamic_database, get_keys(new_dynamic_database)[i]) == min(distances_from_states):
            closest_state = get_keys(new_dynamic_database)[i]
    return closest_state

def make_states_database_with_empty_lists():
    database = make_database()
    us_state_key_list = get_keys(us_states)
    for i in range(get_len(us_states)):
        database = add_value(database, us_state_key_list[i], [])
    return database

def group_tweets_by_state(tweets):
    """Return a database that aggregates tweets by their nearest state center.

    The keys of the returned database are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> get_len(two_tweets_by_state)
    2
    >>> california_tweets = get_value_from_key(two_tweets_by_state, 'CA')
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    tweets_by_state = make_states_database_with_empty_lists()
    "*** YOUR CODE HERE ***"
    for i in range(len(tweets)):
        state_of_tweet = closest_state_to_tweet(tweets[i])
        state_list = get_value_from_key(tweets_by_state, state_of_tweet)
        state_list.append(tweets[i])
        tweets_by_state = add_value(tweets_by_state, state_of_tweet, state_list)
    final_tweets_by_state_list = make_database()
    for i in range(get_len(tweets_by_state)):
        if get_values(tweets_by_state)[i] != []:
            final_tweets_by_state_list = add_value(final_tweets_by_state_list, get_keys(tweets_by_state)[i], get_values(tweets_by_state)[i])

    return final_tweets_by_state_list

def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a database from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    database entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0. 0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A database from state names to lists of tweets
    """
    averaged_state_sentiments = make_database() 
    "*** YOUR CODE HERE ***"
    for i in range(get_len(tweets_by_state)):
        list_of_tweets_by_state = get_value_from_key(tweets_by_state, get_keys(tweets_by_state)[i])
        list_of_all_sentiments = []
        for j in range(len(list_of_tweets_by_state)):
            if has_sentiment(analyze_tweet_sentiment(list_of_tweets_by_state[j])):
                list_of_all_sentiments.append(sentiment_value(analyze_tweet_sentiment(list_of_tweets_by_state[j])))
        if len(list_of_all_sentiments) > 0:
            average_sentiment_for_state = sum(list_of_all_sentiments)/len(get_value_from_key(tweets_by_state, get_keys(tweets_by_state)[i]))
            averaged_state_sentiments = add_value(averaged_state_sentiments, get_keys(tweets_by_state)[i], average_sentiment_for_state)


    return averaged_state_sentiments


##########################
# Command Line Interface #
##########################

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = make_database()
    for state, s in get_items(us_states):
        us_centers = add_value(us_centers, state, find_state_center(s))
    center = get_value_from_key(us_centers, center_state.upper()) 
    dist_from_center = lambda name: geo_distance(center, get_value_from_key(us_centers, name))
    for name in sorted(get_keys(us_centers), key=dist_from_center)[:int(n)]:
        draw_state(get_value_from_key(us_states, name))
        draw_name(name, get_value_from_key(us_centers, name))
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A database from state strings to sentiment values
    """
    for name, shapes in get_items(us_states):
        if name in get_keys(state_sentiments):
            sentiment = get_value_from_key(state_sentiments, name)
        else:
            sentiment = None
        draw_state(shapes, sentiment)
    for name, shapes in get_items(us_states):
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_query(term='my job', file_name='tweets2011.txt'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term, file_name)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', type=str)
    parser.add_argument('--tweets_file', '-t', type=str, default='tweets2011.txt')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    if args.draw_map_for_query:
        draw_map_for_query(args.draw_map_for_query, args.tweets_file)
        print(args.tweets_file)
        return
    for name, execute in args.__dict__.items():
        if name != 'text' and name != 'tweets_file' and execute:
            globals()[name](' '.join(args.text))
