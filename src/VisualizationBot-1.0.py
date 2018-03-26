import praw
import datetime
from operator import itemgetter

from plotly.offline import plot
import plotly.graph_objs as go

def init():
    reddit = praw.Reddit('BOT-CONFIG', user_agent='VisualizationBot-1.0')
    return reddit

def commentsWithVotes(redditor):
    commentList = []
    comment_preview = []
    comment_votes = []

    for comment in redditor.comments.new(limit=None):
        commentList.append(comment)
        comment_date = datetime.date.fromtimestamp(comment.created)
        comment_preview.append(str([str(comment_date), comment.body])) #" ".join(comment.body.split()[:3]) + " ...")
        comment_votes.append(comment.ups)

    data_comments = [go.Bar(
                x=comment_preview[::-1],
                y=comment_votes[::-1]
    )]

    plot(data_comments, filename='graphs/' + redditor.name + '_comments.html')
    return commentList

def submissionsWithVotes(redditor):
    submission_preview = []
    submissionList = []
    submission_votes = []
    votes_total = []
    total = 0

    for submission in redditor.submissions.new(limit=None):
        submissionList.append(submission)
        submission_date = datetime.date.fromtimestamp(submission.created)
        submission_preview.append(str([str(submission_date), submission.title]))
        total += submission.ups
        votes_total.append(total)
        submission_votes.append(submission.ups)

    data_submissions = [go.Bar(
        x=submission_preview[::-1],
        y=submission_votes[::-1],
    )]

    plot(data_submissions, filename='graphs/' + redditor.name + '_submissions.html')
    return submissionList

def getVocabulary(commentList, redditor):
    commonWords = ['the', 'is', 'a', 'i', 'and', 'you', 'to', 'of', 'an', 'it', 'that', 'for', 'in', 'but', 'of', 'its', 'this', 'your', 'with', 'was', 'so',
                   'not', 'are', 'when', 'on', 'also', 'have', 'as', 'me', 'im', 'if', 'into', 'then', 'or', 'at', 'would', 'how', 'his', 'be', 'were', 'by',
                   'thats', 'those', 'because', 'isnt', 'cant', 'even', 'she', 'he', 'only', 'there', 'where', 'should', 'dont', 'had', 'which', 'all', 'they',
                   'like', 'what', 'our', 'will', 'from', 'want', 'been', 'us', 'their', 'much', 'out', 'has', 'who', 'them', 'than', 'any', 'could', 'why', 'just',
                   'my', 'some']

    commentText = ""
    for comment in commentList:
        commentText += comment.body

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
    
def commentKarmaWithTime(commentList, redditor):
    totalKarma = 0
    commentList = commentList[::-1]
    comment_preview = []
    comment_votes = []

    for comment in commentList:
        comment_date = datetime.date.fromtimestamp(comment.created)
        comment_preview.append(str([str(comment_date), comment.body])) #" ".join(comment.body.split()[:3]) + " ...")
        totalKarma += comment.ups
        comment_votes.append(totalKarma)

    data_comments = [go.Bar(
                x=comment_preview,
                y=comment_votes
    )]

    plot(data_comments, filename='graphs/' + redditor.name + '_commentsWithTime.html')
    
def submissionKarmaWithTime(submissionList, redditor):
    totalKarma = 0
    submissionList = submissionList[::-1]
    submission_preview = []
    submission_votes = []

    for submission in submissionList:
        submission_date = datetime.date.fromtimestamp(submission.created)
        submission_preview.append(str([str(submission_date), submission.title])) #" ".join(comment.body.split()[:3]) + " ...")
        totalKarma += submission.ups
        submission_votes.append(totalKarma)

    data_comments = [go.Bar(
                x=submission_preview,
                y=submission_votes
    )]

    plot(data_comments, filename='graphs/' + redditor.name + '_submissionsWithTime.html')
    
def main():
    reddit = init()

    user = "divine_sense"  # The user who needs to be analyzed
    redditor = reddit.redditor(user)

    commentList = commentsWithVotes(redditor)  # Plot comments graph
    submissionList = submissionsWithVotes(redditor)            # Plot submission graph

    commentKarmaWithTime(commentList, redditor)
    submissionKarmaWithTime(submissionList, redditor)

    getVocabulary(commentList, redditor) # Plot vocabulary graph
    
main()
