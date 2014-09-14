import json


def application (env, headcb):
	file = open(r'C:\users\hajaf10\desktop\votebattle\index.html')
	feed = open(r'C:\users\hajaf10\desktop\votebattle\feed.json')
	feed2 = json.load(feed)
	feed4 = ''
	for x in feed2:
		link = '/article/' + str(x['id'])
		title = '<h4 class="topTitle"><a href="' + link + '"class="topTitle">' + x['title'] + '</a></h4>'
		content = '<span class="topContent">' + x['content'] + '</span>'
		published = '<span class="topDate">' + x['published'] + '</span>'
		feed3 = '<div class="topic">' + '\n' + title + '\n' + content + '\n' + published + '\n</div>'
		feed4 += feed3
	output = file.read()%(feed4)
	output = output.encode('utf8')
	file.close()
	feed.close()
	header = [('Content-type', 'text/html;charset=utf-8'), ('Content-length', str(len(output)))]
	headcb('200 OK', header)
	return [output]


