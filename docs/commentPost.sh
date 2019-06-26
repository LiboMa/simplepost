
# user comment post
curl -H "Content-type: application/json" -XPOST localhost:5000/api/comments/4/ -d "{\"user_id\":69, \"text\": \"Ganz gut!\"}"

# Get Post
curl -XGET http://localhost:5000/api/posts/
