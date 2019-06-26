#!/usr/bin/env python

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from lib.PostWapers import metricsDecoretor

# from client_post import ClientSrv, GetPosts
from client_post import *

app = FlaskAPI(__name__)
TOKEN_USER_ID = 66

@app.route('/api/')
def example():
    return {'hello': 'world'}


@app.route('/api/posts/',methods=['GET'])
@metricsDecoretor
def getPosts():
    posts = GetPosts()
    print(posts)
    return posts

@app.route('/api/posts/<int:id>',methods=['GET'])
@metricsDecoretor
def getPost(id):
    post_id = str(id)
    post = GetPost(post_id)
    return post

@app.route('/api/posts/',methods=["POST"])
def createPost():
    """
    '{"user_id":3, "content":"this should be input from web frontend", "post_id": 10}'
    """
    user_id = request.data.get('user_id',)
    content = request.data.get('content',)
    # TODO will hanlded by redis increament key
    post_id = request.data.get('post_id',)
    print("user_id:{}, content:{}, post_id:{}".format(user_id, content, post_id))
    userPost = ClientSrv(user_id=user_id, post_id=post_id)
    _post = userPost.set_post(content)
    if _post:
        return {"status":"OK"}
    else:
        return {"status":"Error"}


@app.route('/api/likes/',methods=["POST"])
@metricsDecoretor
def userLikedPost():
    """
    "{"post_id": 5, "user_id": 1000}"
    """
    user_id = request.data.get('user_id',)
    post_id = request.data.get('post_id',)

    UserViewPost = ClientSrv(user_id=user_id, post_id=post_id)
    _post = UserViewPost.like_post(UserViewPost.post)
    print("DEBUG --> user_id:{}, post_id:{}, POST: {}".format(user_id, post_id, _post))
    if _post:
        return {"status":"OK"}
    else:
        return {"status":"Error"}


@app.route('/api/likes/',methods=["DELETE"])
@metricsDecoretor
def userUnLikedPost():
    """
    "{"post_id": 5, "user_id": 1000}"
    """
    user_id = request.data.get('user_id',)
    post_id = request.data.get('post_id',)

    UserViewPost = ClientSrv(user_id=user_id, post_id=post_id)
    _post = UserViewPost.unlike_post(UserViewPost.post)
    print("DEBUG Frtend--> user_id:{}, post_id:{}, POST: {}".format(user_id, post_id, _post))
    if _post:
        return {"status":"OK"}
    else:
        return {"status":"Error"}



@app.route('/api/comments/<int:id>/',methods=["POST", "DELETE"])
def userCommentPost(id):
    """
    {"user_id": 1000, "text":" some messages..."}
    """
    response = {"id": id, "status": "Error"}

    if request.method == "POST":
        user_id = request.data.get('user_id',)
        post_id = id
        text = str(request.data.get('text',))

        UserView = ClientSrv(user_id=user_id, post_id=post_id)
        _post = UserView.comment_post(UserView.post, text)

        print("DEBUG --> user_id:{}, post_id:{}, POST: {}".format(user_id, post_id, _post))
        response["text"] = text
        response["user_id"] = user_id
        response["status"] = "OK"
        return response

    if request.method == "DELETE":
        text = str(request.data.get('text',))
        response["text"] = text
        return {"id":id, "text": text}

    return response



if __name__ == "__main__":
    app.run(debug=True)
