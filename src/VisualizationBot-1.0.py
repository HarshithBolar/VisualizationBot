import praw
import datetime
from operator import itemgetter


from plotly.offline import plot
import plotly.graph_objs as go


def init():
    reddit = praw.Reddit('BOT-CONFIG', user_agent='VisualizationBot-1.0')
    return reddit


def commentsWithTime(redditor):
    comment_words = ""
    comment_preview = []
    comment_votes = []

    for comment in redditor.comments.new(limit=None):
        comment_words += comment.body.lower()
        comment_date = datetime.date.fromtimestamp(comment.created)
        comment_preview.append(str([str(comment_date), comment.body])) #" ".join(comment.body.split()[:3]) + " ...")
        comment_votes.append(comment.ups)


    data_comments = [go.Bar(
                x=comment_preview[::-1],
                y=comment_votes[::-1]
        )]

    plot(data_comments, filename='graphs/' + redditor.name + '_comments.html')
    return comment_words


def submissionsWithTime(redditor):
    submission_preview = []
    submission_votes = []

    for submission in redditor.submissions.new(limit=None):
        submission_date = datetime.date.fromtimestamp(submission.created)
        submission_preview.append(str([str(submission_date), submission.title]))
        submission_votes.append(submission.ups)

    data_submissions = [go.Bar(
        x=submission_preview[::-1],
        y=submission_votes[::-1],
    )]

    plot(data_submissions, filename='graphs/' + redditor.name + '_submissions.html')

def getVocabulary(commentText, redditor):
    commonWords = ['the', 'is', 'a', 'i', 'and', 'you', 'to', 'of', 'an', 'it', 'that', 'for', 'in', 'but', 'of', 'its', 'this', 'your', 'with', 'was', 'so',
                   'not', 'are', 'when', 'on', 'also', 'have', 'as', 'me', 'im', 'if', 'into', 'then', 'or', 'at', 'would', 'how', 'his', 'be', 'were', 'by',
                   'thats', 'those', 'because', 'isnt', 'cant', 'even', 'she', 'he', 'only', 'there', 'where', 'should', 'dont', 'had', 'which', 'all', 'they',
                   'like', 'what', 'our', 'will', 'from', 'want', 'been', 'us', 'their', 'much', 'out', 'has', 'who', 'them', 'than', 'any', 'could', 'why', 'just',
                   'my']

    commentText = [i for i in commentText.strip().split() if i.isalpha() and i not in commonWords and len(i)>3]
    dict = {}
    for word in set(commentText):
        dict[word] = 0
    for word in commentText:
        dict[word] += 1
    vocab = sorted(dict.items(), key=itemgetter(1))[::-1]
    words = []
    count = []
    for pair in vocab:
        if pair[1] > 4:
            words.append(pair[0])
            count.append(pair[1])

    data_vocab = [go.Bar(
        x=words[::-1],
        y=count[::-1],
    )]

    plot(data_vocab, filename='graphs/' + redditor.name + '_vocabulary.html')

def main():
    reddit = init()

    user = "krotonos"  # The user who needs to be analyzed
    redditor = reddit.redditor(user)

    commentText = commentsWithTime(redditor)  # Plot comments graph
    submissionsWithTime(redditor)            # Plot submission graph

    getVocabulary(commentText, redditor)



main()