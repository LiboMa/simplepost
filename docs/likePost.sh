
# user liked post
curl -H "Content-type: application/json" -XPOST localhost:5000/api/likes/ -d "{\"user_id\":69, \"post_id\": 4}"

# Get Post
curl -XGET http://localhost:5000/api/posts/
