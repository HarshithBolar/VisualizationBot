import praw
import datetime

from plotly.offline import plot
import plotly.graph_objs as go


def init():
    reddit = praw.Reddit('BOT-CONFIG', user_agent='VisualizationBot-1.0')
    return reddit


def commentsWithTime(redditor):
    comment_preview = []
    comment_votes = []

    for comment in redditor.comments.new(limit=None):
        comment_date = datetime.date.fromtimestamp(comment.created)
        comment_preview.append(str([str(comment_date), comment.body])) #" ".join(comment.body.split()[:3]) + " ...")
        comment_votes.append(comment.ups)


    data_comments = [go.Bar(
                x=comment_preview[::-1],
                y=comment_votes[::-1]
        )]

    plot(data_comments, filename='graphs/' + redditor.name + '_comments.html')


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


def main():
    reddit = init()

    user = "divine_sense"  # The user who needs to be analyzed
    redditor = reddit.redditor(user)

    commentsWithTime(redditor)
    submissionsWithTime(redditor)

main()