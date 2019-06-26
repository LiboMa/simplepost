#!/usr/bin/env python

import time
import json
import random
import redis

from lib.Cache import Cache

r = Cache()

class Post:
    def __init__(self, id, user_id, content, comments=None, likes=None, createAt=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.comments = []
        self.likes = []

        # Get or create comments
        if not comments:
            self.comments = []
        else:
            self.comments = comments
        # Ger or create likes
        if not likes:
            self.likes = []
        else:
            self.likes = likes
        # Get or create timestamp
        if not createAt:
            self.createAt = int(time.time())
        else:
            self.createAt = createAt

        self.createAt = int(time.time())

        # init redis key
        _post_key = "post_id_{0}".format(id)
        _post_val = json.dumps(self.__dict__)
        r.set(_post_key, _post_val)

    def id(self):
        self.id += 1
        return self.id

    def user_id(self):
        return self.user_id

    def createAt(self):
        return self.creatAt

    def content(self):
        return self.content

    def comments(self):
        return self.comments
    def likes(self):
        return self.likes
    
    def save(self):
       # init redis key
        _post_key = "post_id_{0}".format(self.id)
        _post_val = json.dumps(self.__dict__)
        r.set(_post_key, _post_val)


    def Json(self):
        return self.__dict__

    def __repr__(self):
        return "<Post Model>: {0}".format(self.__dict__)

class Comment:
    def __init__(self, id, user_id, post_id, text="", createAt=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        if not createAt:
            self.createAt = int(time.time())
        else:
            self.createAt = createAt

        if text != "":
            print("User {} comment post {} with {} @ {}".format(self.user_id, self.post_id, self.text, self.createAt))

    def user_id(self):
        return self.user_id
    def text(self):
        return self.text
    def createAt(self):
        return self.createAt
    def Json(self):
        return self.__dict__

    def __repr__(self):
        return str(self.id)

class Like:
    def __init__(self, id, user_id, post_id=0, comment_id=0, createAt=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        if not createAt:
            self.createAt = int(time.time())
        else:
            self.createAt = createAt

        self.comment_id= comment_id

        if post_id != 0:
            print("User {} liked post {} @ {}".format(self.user_id, self.post_id, self.createAt))
        if comment_id != 0:
            print("User {} liked comment {} @ {}".format(self.user_id, self.comment, self.createAt))


    def user_id(self):
        return self.user_id
    def post_id(self):
        return self.post_id
    def comment_id(self):
        return self.comment_id

    def Json(self):
        return self.__dict__

    def __repr__(self):
        return str(self.id)

def generate_data(user_ids=10):
    data_list = []

    for i in range(1, user_ids):
        p = Post(i)
        p.name = "demo fine post"
        p.time = int(time.time())
        p.user_id= i
        p.content= "hello messages {0}".format(i)

        # get comment info from cache or db
        p.comments=[]
        # get likes info from cache or db
        p.likes=[]
        json_data=p.__dict__
        data_list.append(json_data)

    #print(data_list)
    return data_list


def postSerilizer(data_list):
    response = {}
    response["posts"] = data_list
    return response


#def UserLikedPost(user_id, post_id):
#    Users=[1,2,3]
#    p = Post(post_id)
#    likes = p.likes
#    likes.append(user_id)
#
def UserCommentPost(post, comment):

    post.user = comment.user_id
    post.comments.append(comment.Json())

    post_key = "post_id_{0}".format(post.id)
    post_value = str(post.Json())
    r.set(post_key, post_value )

    return post


if __name__ == '__main__':

    #posts = json.dumps(postSerilizer(generate_data(5)))
    #print(posts)
    post1 = Post(1, user_id=1, content="Wolrd is always changing")
    print(post1.__dict__)

    #like1 = Like(id=1, user_id=1, post_id=1)
    #c1 = Comment(id=1, user_id=99, post_id=1, text="This great!")
    #update_post = UserCommentPost(post1, c1)
    #print(update_post)

    #redis_update_post = r.get(update_post.id)
    #print("post in cache", redis_update_post)
    #c2 = Comment(id=2, user_id=2, post_id=1, text="let's make it come true!")
    #c3 = Comment(id=3, user_id=3, post_id=1, text="no so bad :_)")

    ##r.set("posts", posts)
    #val = r.get("posts")
    #print(val)

