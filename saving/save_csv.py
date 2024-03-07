import csv

def save_to_csv(posts, filename='posts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for post in posts:
            writer.writerow({'text': post['text']})
