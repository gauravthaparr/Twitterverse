"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this 
          user is following (a list of str)
       
Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)
       
"""

# Write your Twitterverse functions here

def twitterverse_helper(data_file):
    ''' (file open for reading) -> list of lists 
     Return a list of lists of the data for each user.
    
    '''
    y = []
    for i in data_file.readlines():
        y.append(i.rstrip())    
    
    profile_of_users = []
    
    while y != []:
        info = []
        info.extend(y[0:4])
        bio1 = ''
        for b in y[4:y.index('ENDBIO')]:
            bio1 = bio1 + b + ' ' +'\n' # enters a new line after every submission
        bio1 = bio1[0:-1]
        info.append(bio1)            
        following = []
        for f in y[y.index('ENDBIO')+1:y.index('END')]:
            following.append(f)
        info.append(following)
        profile_of_users.append(info)
        z = y.index('END')
        del y[0:z+1]
        
    return profile_of_users
        
def process_data(data_file):
    '''(file open for reading)->dict of{str:dict of{str:object}}
    Return the data in the Twitterverse dictionary format. 
    
    '''    
    user_list = twitterverse_helper(data_file)
    twitterverse = {}
    for user in user_list:
        twitterverse[user[0]] = {}
        twitterverse[user[0]]['name'] = user[1]
        twitterverse[user[0]]['location'] = user[2]
        twitterverse[user[0]]['web'] = user[3]
        twitterverse[user[0]]['bio'] = user[4]
        twitterverse[user[0]]['following'] = user[5]
    return twitterverse   

def convert_list(query):
    """ (file open for reading) -> lst of str
    
    Return query converted into list format.
    """
    new_lst = []
    for line in query.readlines() :
        new_lst = new_lst + [ line.strip()]
    return new_lst

def searchq(lst) :
    """ (list of str) -> dict of {str :{str : object}}
    
    Precondition : 'FILTER' should be present in lst . 
    
    Return the query dictionary with search specification in it,converting lst to 
    dictionary.
    """
    
    x = {}
    z = {}
    x['username'] = lst[1]
    new_lst = []
    for i in range(2, lst.index('FILTER')) :
        new_lst.append(lst[i])   
    x['operations'] = new_lst
    z['search'] = x
    return z
    
def filterq(search,z) :
    """(dict of {str:{str : object}},list of str) -> dict of {str:{str:object}}
    
    Precondition : 'FILTER' and 'Present' in z .
    
    Return the query dictionary with filter specification in it, converting
    z into dictionary and adding it to search.
    """
    lst = {}
    a = search
    for x in range(z.index('FILTER'),z.index('PRESENT')):
        if 'name-includes' in z[x]:
            lst['name-includes']=z[x][z[x].index(' ')+1:]
        if 'following' in z[x] :
            lst['following'] = z[x][z[x].index(' ') + 1 : ]
        if 'follower' in z[x] :
            lst['follower'] = z[x][z[x].index(' ') + 1 : ]
        if 'location-includes' in z[x] :
            lst['location-includes'] = z[x][z[x].index(' ') + 1 : ]
    a['filter'] = lst
    return a 

def presentq(filter,a):
    """(dict of {str:{str : object}},list of str) -> dict of{str:{str : object}}
        
    Precondition : 'PRESENT' should be present in a .
        
    Return the query dictionary with filter specification in it by converting
    a into dictionary and adding it to filter.
    """
    lst = {}
    c = filter 
    for x in range( a.index('PRESENT'), len(a)) :
        if 'sort-by' in a[x] :
            name = a[x][ a[x].index(' ') + 1 : ]
            lst['sort-by'] = name
        if 'long' in a[x] :
            lst['format'] = 'long'
        if 'short' in a[x] :
                lst['format'] = 'short' 
    c['present'] = lst
    return c
    
def process_query(query) :
    """  (file open for reading) -> dict of {str: dict of {str: object}}
    
    Return Query Dictionary with data extracted from query.
    """
    conv_list = convert_list(query)
    search = searchq(conv_list)
    filterd = filterq(search,conv_list)
    new_lst = presentq(search,conv_list)
    
    return new_lst
    
def all_followers(twitterverse,user):
    """ (dict of {str: dict of {str: object}}, str) -> lst of str
    
    Return the list of followers of the user from twitterverse dictionary.
    
    >>> all_followers({'katieH': {'web':'www.tomkat.com','name':'Katie Holmes',\
    'following': [], 'location': '', 'bio': ''},\
    'tomCruise':{'web': 'http://www.tomcruise.com', 'name': 'Tom Cruise',\
    'following': ['katieH'], 'location': 'Los Angeles, CA', 'bio':''}},\
    'tomCruise')
    []
    
    >>> all_followers({'PerezHilton': {'name': 'Perez Hilton', 'location':\
    'Hollywood, California', 'bio': 'Perez Hilton is the creator and writer\
    of one of the most famous websites in the world. And he also loves music\
    - a lot!', 'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web':\
    'http://www.PerezH...'}, 'tomCruise': {'name': 'Tom Cruise', 'location':\
    'Los Angeles, CA', 'bio': 'Official TomCruise.com crew tweets. We love\
    you guys! Visit us at Facebook!', 'following': ['katieH', 'NicoleKidman']\
    , 'web': 'http://www.tomcruise.com'}},'tomCruise')
    ['PerezHilton']
    """
    new_lst=[]
    for i in twitterverse:
        for j in twitterverse[i]['following']:
            if j== user:
                new_lst=new_lst+[i]
    return new_lst

def get_search_results(twitterverse,search):
    """ (dict of {str: dict of {str: object}}, dict of {str : object})
    -> list of str
    
    Return the list of str after search specification extracted from search
    and data from twitterverse dictionary.
       
    >>> a = {'PerezHilton': {'location': 'Hollywood, California', 'name':\
    'Perez Hilton', 'following': ['tomCruise', 'katieH', 'NicoleKidman'],\
    'bio': 'Perez Hilton is the creator and writer of one of the most famous\
    website in the world. And he also loves music - a lot', 'web':\
    'http://www.PerezH...'}, 'tomCruise': {'location': 'Los Angeles, \
    CA', 'name': 'Tom Cruise', 'following': ['katieH', 'NicoleKidman'], \
    'bio': 'Official TomCruise.com crew tweets. We love you guys! Visit us at\
    Facebook', 'web': 'http://www.tomcruise.com'}}
    >>> b = {'operations': ['following'], 'username': 'tomCruise'}
    >>> sorted(get_search_results(a,b))
    ['NicoleKidman', 'katieH']

    
    >>> a = {'tomfan': {'location': 'Houston, Texas', 'name': 'Chris\
    Calderone', 'bio': 'Tom Cruise is the best actor in Hollywood',\
    'following': ['tomCruise'], 'web': ''}, 'tomCruise': {'location':\
    'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com\
    crew tweets. We love you guys! Visit us at Facebook', 'following':\
    ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com'},\
    'NicoleKidman': {'location': 'Oz', 'name': 'Nicole Kidman',\
    'bio': "At my house celebrating Halloween! I Know Haven't been\
    on like years So Sorry,Be safe And have fun tonigh", 'following':\
    [], 'web': ''}, 'PerezHilton': {'location': 'Hollywood, California',\
    'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer\
    of one of the most famous websites in the world. And he also loves music\
    - a lot', 'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web':\
    'http://www.PerezH...'}, 'katieH': {'location': '', 'name': 'Katie Holmes',\
    'bio': '', 'following': [], 'web': 'www.tomkat.com'}}
    >>> b = {'operations': ['followers', 'followers','followers'], \
    'username': 'tomCruise'}
    >>> get_search_results(a,b)
    []
    
    """
    lst=[]
    
    if search['operations'][0]=='followers':
        lst.extend(all_followers(twitterverse,search['username']))
    elif search['operations'][0]=='following':
        lst.extend(twitterverse[search['username']]['following'])
    
    for x in search['operations'][1:]:
        for f in lst:
            if x=='followers':
                lst[lst.index(f):lst.index(f)+1] =[all_followers(twitterverse,f)]
            
            elif x=='following':
                lst[lst.index(f):lst.index(f)+1]=[twitterverse[f]['following']]
                
        lst=helper_search(lst)
    return rmv_dup(lst) #removes the list after removing duplicates

def helper_search(lst):
    """ (list of list of int) -> list of int
    
    Return list of int after changing lst from a nested list into a new list
    with no nested lists.
    
    >>> helper_search([[1, 2, 3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> helper_search([[9],[3],[2,1]])
    [9, 3, 2, 1]
    """
    z = []
    for i in lst:
        for j in i:
            z.append(j)
    return z
                                 
def rmv_dup(lst):
    """ (list of int) -> list of int
    
    Return lst of int after removing duplicates from lst .
    
    >>> rmv_dup([3, 2, 2, 3])
    [3, 2]
    >>> rmv_dup([3, 2, 6, 4,5])
    [3, 2, 6, 4, 5]
    """
    output = []
    for x in lst:
        if x not in output:
            output.append(x)
    return output
    
def get_filter_results(twitterverse, lst, filterd) :
    """ (dict of {str: dict of {str: object}}, list of str, dict of {str : str})
    -> list of str
    
    Return list of str after filter specification taken from filterd,
    data taken from twitterverse dictionary is performed on lst.
    
    >>> a = {'tomfan': {'location': 'Houston, Texas', 'name': 'Chris\
    Calderone', 'bio': 'Tom Cruise is the best actor in Hollywood',\
    'following': ['tomCruise'], 'web': ''}, 'tomCruise': {'location':\
    'Los Angeles, CA', 'name': 'Tom Cruise', 'bio': 'Official TomCruise.com\
    crew tweets. We love you guys! Visit us at Facebook', 'following':\
    ['katieH', 'NicoleKidman'], 'web': 'http://www.tomcruise.com'},\
    'NicoleKidman': {'location': 'Oz', 'name': 'Nicole Kidman',\
    'bio': "At my house celebrating Halloween! I Know Haven't been\
    on like years So Sorry,Be safe And have fun tonigh", 'following':\
    [], 'web': ''}, 'PerezHilton': {'location': 'Hollywood, California',\
    'name': 'Perez Hilton', 'bio': 'Perez Hilton is the creator and writer\
    of one of the most famous websites in the world. And he also loves music\
    - a lot', 'following': ['tomCruise', 'katieH', 'NicoleKidman'], 'web':\
    'http://www.PerezH...'}, 'katieH': {'location': '', 'name': 'Katie Holmes',\
    'bio': '', 'following': [], 'web': 'www.tomkat.com'}}
    >>> b = {'name-includes' : 'r'}
    >>> get_filter_results(a, ['katieH', 'NicoleKidman', 'tomCruise'], b)
    ['tomCruise']
    
    >>> a = {'katieH': {'web':'www.tomkat.com','name':'Katie Holmes',\
    'following': [], 'location': '', 'bio': ''},\
    'tomCruise':{'web': 'http://www.tomcruise.com', 'name': 'Tom Cruise',\
    'following': ['katieH'], 'location': 'Los Angeles, CA', 'bio':''}}
    >>> b = {'following': 'katieH'}
    >>> get_filter_results(a, ['tomCruise'], b)
    ['tomCruise']
    
    """
    new_lst = lst[:]
    for b in filterd :
        if b == 'location-includes':
            for j in lst :
                location = twitterverse[j]['location']
                location1 = filterd[b]
                if location1 not in location :
                    new_lst.remove(j)
        elif b == 'name-includes' :
            for j  in lst :
                name = twitterverse[j]['name']
                name1 = filterd[b]
                if name1 not in name :
                    new_lst.remove(j)
        elif b == 'following' :
            for j in lst :
                following = twitterverse[j]['following']
                name = filterd[b]
                if name not in following :
                    new_lst.remove(j)
        elif b == 'follower' :
            for j in lst :
                name = filterd[b]
                following = twitterverse[name]['following']
                if j not in following :
                    new_lst.remove(j)
    return new_lst

def get_present_string(twitterverse, users, present):
    """ (dict of {str :{str : object}},list of str, dict of {str: object})->str.
    
    Return str according to present on users and relevent data taken from
    twitterverse.
    
    >>> a = {'gerrypower': {'location': 'Toronto, Ontario', 'name':\
    'Gerry Power', 'following': ['kenstruys', 'drscan', 'chanian',\
    'michaelcvet', 'JonasBrandon', 'karaswisher', 'gridcentric', 'adinscannell',\
    'viveklak', 'google', 'timtoronto'], 'web':\
    'http://gerrypower.wordpress.com/', 'bio': 'Passionate about Rails, Java,\
    Objective-C and the high performance teams that put it all together!'},\
    'SteveCase': {'location': 'Washington DC', 'name': 'Steve Case',\
    'following': ['mattcohler', 'davemcclure', 'paulg', 'bhorowitz'], 'web':\
    'http://www.revolution.com', 'bio': 'Co-founder of AOL; now Chairman of\
    Case Foundation and Revolution (Zipcar, LivingSocial, Exclusive Resorts,\
    Everyday Health, Revolution Money, Miraval, etc)'}}
    
    >>> b = {'format': 'long', 'sort-by': 'popularity'}
    >>> get_present_string(a, [], b)
    '----------\\n----------'
    
    >>> twitter =  {'katieH': {'web': 'www.tomkat.com', 'bio': '',\
    'following': '', 'name': 'Katie Holmes', 'location':''},\
    'tomCruise': {'web': 'http://www.tomcruise.com', 'bio': 'Official \
    TomCruise.com crew tweets. We love you guys! Visit us at Facebook!',\
    'following': ['katieH'], 'name': 'Tom Cruise', 'location':\
    'Los Angeles, CA'}}
    >>> usernames = ['tomCruise', 'katieH']
    >>> presentation = {'sort-by': 'username', 'format': 'short'}
    >>> get_present_string(twitter, usernames, presentation)
    "['katieH', 'tomCruise']"
    
    """

    lst = users[:]
    if lst == [] and present['format'] == 'long' :
        return '----------\n----------'
    elif lst == [] and present['format'] == 'short' : #if the format is short
        return []                                     # return empty list
    
    if present['sort-by'] == 'popularity':
        tweet_sort(twitterverse, lst, more_popular)
        for i in range(len(lst)):
            if len(lst) > 1 and lst[i] == lst[i - 1]:
                if username_first(twitterverse, lst[i], lst[i - 1]) == -1:
                    lst[i],lst[i - 1] = lst[i - 1],lst[i]
                    
    elif present['sort-by'] == 'username':
        tweet_sort(twitterverse, lst, username_first)
        
    elif present['sort-by'] == 'name':
        tweet_sort(twitterverse, lst, name_first)
        for i in range(len(lst)-1):
            if lst[i] == lst[i+1]:
                if username_first(twitterverse, lst[i], lst[i+1])==1:
                    lst[i],lst[i+1]=lst[i+1],lst[i]
                    
    if present['format'] == 'short':
        return str(lst)
    
    if present['format'] == 'long':
        st = '----------'
        for i in lst:
            st+= '\n' +i+'\nname: '+twitterverse[i]['name']+'\nlocation: '+\
            twitterverse[i]['location']+'\nwebsite: '+twitterverse[i]['web']+\
            '\nbio:\n'+twitterverse[i]['bio']+'\nfollowing: '+\
            str(twitterverse[i]['following'])+'\n----------'
        return st+'\n'
            
# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType
    
    Sort the results list using the comparison function cmp and the data in 
    twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current  
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       


if __name__ == '__main__':
    import doctest
    doctest.testmod()
