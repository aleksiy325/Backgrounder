import hashtable


table = hashtable.hashtable(10)


links = ["https://reddit.com/r/futureporn" , "https://www.reddit.com/r/futureporn/top/?sort=top&t=all", "https://www.reddit.com/r/futureporn/top/?sort=top&t=all&count=25&after=t3_1wdbte" , "https://www.reddit.com/r/ImaginaryBestOf/top/?sort=top&t=all" , "https://www.reddit.com/r/ImaginaryBestOf/top/?sort=top&t=all&count=25&after=t3_3tk957" , "https://www.reddit.com/r/ImaginaryWinterscapes/top/?sort=top&t=all" , "https://www.reddit.com/user/Lol33ta/m/imaginarycharacters/top/?sort=top&t=all" , "https://www.reddit.com/user/Lol33ta/m/imaginarylandscapes/top/?sort=top&t=all"]

for link in links:
	print table.visited(link), link


print table.visited("https://reddit.com/r/futureporn") , "https://reddit.com/r/futureporn"

table.printtable()

table.grow()
print "-------------new table-----------------------"
table.printtable()