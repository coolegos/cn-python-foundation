import expanddouban
from bs4 import BeautifulSoup
import csv
import time


class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link


# movie = Movie("肖申克的救赎", 9.6, "美国", "https://movie.douban.com/subject/1292052/", "剧情"
#               , "https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg")
# print(movie.name)
# print(movie.rate)
# print(movie.location)
# print(movie.category)
# print(movie.info_link)
# print(movie.cover_link)

def getMovieUrl(category, location):
    """
    return a string corresponding to the URL of douban movie lists given category and location.
    """
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
    return url + ',' + category + ',' + location


# print(getMovieUrl('剧情'))

# list-wp
# <a class="item" data-v-2c455d87="" data-v-3e982be2="" href="https://movie.douban.com/subject/24751811/" target="_blank">
#   <div class="cover-wp" data-id="24751811" data-v-2c455d87="">
#     <span class="pic" data-v-2c455d87="">
#       <img alt="剧院魅影：25周年纪念演出" data-v-2c455d87="" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2006533765.jpg" x="movie:cover_x" y="1200"/>
#     </span>
#   </div>
#   <p data-v-2c455d87="">
#     <span class="title" data-v-2c455d87="">
#       剧院魅影：25周年纪念演出
#     </span>
#     <span class="rate" data-v-2c455d87="">
#       9.7
#     </span>
#   </p>
# </a>
locations = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚',
             '爱尔兰', '瑞典', '巴西', '丹麦']


def getMovies(category):
    """
    return a list of Movie objects with the given category and location.
    """
    movie_list = []
    for location in locations:
        html = expanddouban.getHtml(getMovieUrl(category, location), True)
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.find(class_='list-wp').find_all('a')
        for item in list:
            name = item.find(class_='title').string
            rate = item.find(class_='rate').string
            info_link = item.get('href')
            cover_link = item.find(class_='cover-wp').find(class_='pic').contents[0].get('src')
            movie_list.append(Movie(name, rate, location, category, info_link, cover_link))
        time.sleep(2)  # sleep 2 seconds
    return movie_list


# movie_list = getMovies('剧情', '英国')
# movie_list = getMovies('科幻', '伊朗')
# for link in movie_list:
#     print(
#         link.name + ',' + link.rate + ',' + link.location + ',' + link.category + ',' +
#         link.info_link + ',' + link.cover_link)
#     print(link.find(class_='cover-wp').find(class_='pic').contents[0].get('src'))
#     print(link.find(class_='title').string + ',' + link.find(class_='rate').string)
#     print(link.find(class_='rate').string)
#     print(link.get('href'))


def writeMovie(writer, movie):
    """
    将单个movie 写入到csv 文件中
    :return:
    """
    writer.writerow([movie.name, movie.rate, movie.location, movie.category, movie.info_link, movie.cover_link])


def genLikeMoviesFile(category1, category2, category3):
    """
    生成3个喜欢电影的的csv 文件
    :return:
    """
    movie_list = []
    movie_list += getMovies(category1)
    movie_list += getMovies(category2)
    movie_list += getMovies(category3)

    with open('movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for movie in movie_list:
            writeMovie(writer, movie)


# 数量排名前三的地区有哪些？
# 分别占此类别电影总数的百分比为多少？

def calculateTheNumOfTopThree(category, movies):
    """
    计算数量排名前三
    :return:
    """
    category_movies = calculateMovies(category, movies)
    movie_dic = calculateMovieNumByLocation(category_movies)
    movie_list = sorted(movie_dic, key=movie_dic.get, reverse=True)
    # print(movie_list)
    movie_list = movie_list[:3]
    top_of_three = [movie_dic[movie] / len(category_movies) for movie in movie_list]

    return "'{}'类型数量排名前三的地区有：{}，{}，{}。分别占此类别电影总数的百分比为：{:.2%}，{:.2%}，{:.2%}\n".format(category, movie_list[0],
                                                                                     movie_list[1],
                                                                                     movie_list[2], top_of_three[0],
                                                                                     top_of_three[1],
                                                                                     top_of_three[2])


def calculateMovies(category, movies):
    """
    获取category 的电影列表
    :param category: 电影类型
    :param movies: 所有的电影列表
    :return: category 类型的电影列表
    """
    category_movies = [movie for movie in movies if category == movie[3]]
    return category_movies


def calculateMovieNumByLocation(movies):
    """
    根据location 计算电影的数量
    :param location: 代表一个地区
    :param movies: 某种特定类型的电影
    :return:
    """
    movie_dic = {}
    for movie in movies:
        if movie[2] in movie_dic:
            movie_dic[movie[2]] += 1
        else:
            movie_dic[movie[2]] = 1
    return movie_dic


def calculateMovieData(category1, category2, category3):
    """
    统计电影数据，统计你所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少？
    :return:
    """
    with open('movies.csv', 'r') as f:
        reader = csv.reader(f)
        movies = list(reader)

    with open('output.txt', 'w') as f:
        f.write(calculateTheNumOfTopThree(category1, movies))
        f.write(calculateTheNumOfTopThree(category2, movies))
        f.write(calculateTheNumOfTopThree(category3, movies))


def task(category1, category2, category3):
    genLikeMoviesFile(category1, category2, category3)
    calculateMovieData(category1, category2, category3)


task('喜剧', '动作', '犯罪')
