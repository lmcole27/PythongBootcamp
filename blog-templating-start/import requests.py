import requests
from post import Blog

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

# class Blog:
#     def __init__(self, post_id, title, subtitle, body):
#         self.title = title
#         self.subtitle = subtitle
#         self.body = body

post_list = []

for post in posts:
    new_title = post["title"]
    new_blog = Blog(post["id"], post["title"], post["subtitle"], post["body"])
    post_list.append(new_blog)
print(post_list)
