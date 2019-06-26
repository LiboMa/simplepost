#!/usr/bin/env

import json
import time

from lib.Cache import Cache
from service_post import Post
from service_post import Comment
from service_post import Like

# const
r = Cache()
TOKEN_USER_ID = 66
LOGIN = True
POST_ID = 1


class ClientSrv:

    def __init__(self, user_id=TOKEN_USER_ID, post_id=POST_ID):
        # Post Client Constructor
        self.user_id = user_id
        self.post_id = post_id

        self._post_key = "post_id_{0}".format(self.post_id)
        self._post = r.get(self._post_key)

        self.post = None
        if self._post is not None:
            self.post = json.loads(self._post)
            print(self.post)
            self.post = Post(**self.post)

    def set_post(self, message):
        p = Post(self.post_id, self.user_id, message)
        self.post = p
        return self.post

    def get_post(self):
        return self.post

    def like_post(self, post):
        _post_key = "post_id_{0}".format(post.id)

        _post = r.get(_post_key)
        if not _post:
            print("post does not exist")
            return

        # create like action
        like = Like(5, self.user_id, post_id=post.id)
        # update post
        post.user_id = self.user_id

        if like.user_id not in post.likes:
            post.likes.append(like.user_id)
            _post_value = json.dumps(post.Json())
            r.set(_post_key, _post_value)
            return post

        print("DEBUG: POST alread like by user: ", self.user_id)
        return

    def unlike_post(self, post):
        _post_key = self._post_key
        post = r.get(_post_key)
        self.post = json.loads(post)

        # print(">>>>",self.post)
        self.post = Post(**self.post)
        # print(">>>>",type(self.post))
        # print(">>>>",self.post.likes)

        if self.user_id not in self.post.likes:
            print("DEBUG: POST alread unlike by user: ", self.user_id)
            return None

        print("User {} unliked post {} @ {}".format(self.user_id, self.post_id, int(time.time())))
        self.post.likes.remove(self.user_id)
        # remote from
        self.post.save()
        return self.post
        
        

    def comment_post(self, post, message):
        _post_key = "post_id_{0}".format(post.id)
        _post = r.get(_post_key)
        if not post:
            print("post does not exist")
            return

        if message:
            comment = Comment(5, user_id=self.user_id,
                              post_id=post.id, text=message)
        else:
            print("message required -> null")
            return
        post.user_id = self.user_id
        post.comments.append(comment.Json())

        _post_value = json.dumps(post.Json())
        r.set(_post_key, _post_value)
        return post


def GetPost(post_id):
    data = {}

    if post_id is None:
        print("ERROR: No post_id received post_id-> ", post_id)
    
    _post_key = "post_id_{}".format(post_id)
    print("DEBUG: trying to get post with key", _post_key)
    post = r.get(_post_key)
    data = {"post": post}
    print("get one post", data)
    return data


def GetPosts():
    start = time.time()
    _post_keys = "post_id_*"
    posts = r.getkeys(_post_keys)
    print("get all posts costs: {} s".format(time.time() - start))
    data = {}
    data["posts"] = posts
    return data


if __name__ == "__main__":

   # Test code here
    start = time.time()
    #user1post = ClientSrv(user_id=TOKEN_USER_ID, post_id=2)
    # user set post
    #user1post.set_post("This world is not changing")

    # user like post
    user66post = ClientSrv(user_id=TOKEN_USER_ID, post_id=4)
    user66post.like_post(user66post.post)
    post = user66post.get_post()

    # user unlike post
    user66post = ClientSrv(user_id=TOKEN_USER_ID, post_id=4)
    user66post.unlike_post(user66post.post)
    post = user66post.get_post()

    # user67post = ClientSrv(user_id=TOKEN_USER_ID+1, post_id=4)
    # user67post.like_post(user67post.post)
    # post = user67post.get_post()

    # # user comment post
    user68comment = ClientSrv(user_id=TOKEN_USER_ID+2, post_id=4)
    user68comment.comment_post(user68comment.post, "Yes, that absolutely right!")


    print(json.dumps(user68comment.post.Json(), indent=2))
