
#curl -H "Content-type: application/json" -XPOST localhost:5000/api/posts/ -d "{\"user_id\":1, \"content\":\"th s should be input from web frontend\", \"post_id\": 3}"

# Get Post
curl -XGET http://localhost:5000/api/posts/
