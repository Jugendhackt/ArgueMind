
import json
import cgi
def application (env, headcb):
	if env ["REQUEST_METHOD"] == "GET":
		
		feed0 = open(r'C:\users\hajaf10\desktop\votebattle\feed.json')
		file = open(r'C:\users\hajaf10\desktop\votebattle\index.html')
		article = open(r'C:\users\hajaf10\desktop\votebattle\article.html')
		feed = json.load(feed0)
		article2 = article.read()
		comments = open(r'C:\users\hajaf10\desktop\votebattle\comments.json', 'r+')
		comments2 = json.load(comments)
		comments4 = []
		for y in comments2:
			if env ['PATH_INFO'][1:] == str(y["id"]):
				user = y["user"]
				content = y["content"]
				rating = y["rating"]
				comments3 = ('<div class="comment">' + '\n' + '<h4>' + user + '</h4>\n<span class="commentCon">' + content + '</span><br>\n<a onclick="up(' + str(y["rand"]) + ')">Up</a> | <a onclick="down(' + str(y["rand"]) + ')">Down</a>' + '  ' + str(rating) +"\n</div>")
				comments4.append(comments3)
				
		comments5 = '\n'.join(comments4)
		
		if env ["QUERY_STRING"] != '':
			form = cgi.parse_qs(env["QUERY_STRING"])
			vote = form ["type"]
			id = form ["id"]
			for z in comments2:
				if id == str(z["rand"]):
					if vote == 'up':
						z["rating"] += 1
					else:
						z["rating"] += -1
					break
		comments.seek(0)
		json.dump(comments2, comments)
		for x in feed:
			if env ['PATH_INFO'][1:] == str(x["id"]):
				title = x['title']
				date = x['published']
				content = x['content']
				article3 = article2%(title, date, content, comments5)
				break		
		else:
			article3 = 'not found'
		

		output = file.read()%(article3)
		output = output.encode('utf8')
		file.close()
		article.close()
		header = [('Content-type', 'text/html;charset=utf-8'), ('Content-length', str(len(output)))]
		headcb('200 OK', header)
		return [output]
	elif env ["REQUEST_METHOD"] == "POST":
		import uuid
		rating = 0
		comments = open(r'C:\users\hajaf10\desktop\votebattle\comments.json', 'r+')
		form = cgi.FieldStorage(fp = env ['wsgi.input'], environ = env)
		comments2 = json.load(comments)
		id = int(env ['PATH_INFO'][1:])
		user = form.getvalue('username')
		content = form.getvalue('content')
		rand = uuid.uuid4().int
		comment = {'user': user, 'content' : content, 'rand' : rand, 'rating' : rating, 'id' : id}
		comments2.append(comment)
		comments.seek(0)
		json.dump(comments2, comments)
		header = [('Location', 'http://100.109.223.49/article' + env ['PATH_INFO'])]
		headcb('303 See Other', header)
		return[]
	else:
		return[]
		